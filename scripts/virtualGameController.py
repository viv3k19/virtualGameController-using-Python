import cv2 as cv
import datetime
import numpy as np
import HandTrackingModule as htm
import pyautogui as pg
import pydirectinput as pn
import win32api, win32con


wCam, hCam = 1280, 720
plocx, plocy = 0, 0
clocx, clocy = 0, 0

cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
tipIds = [4, 8, 12, 16, 20]
last_click = datetime.datetime.now()
detector = htm.HandDetector(maxHands=1, detectionCon=int(0.75))

while True:
    success, img = cap.read()
    img = cv.flip(img, 1)
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    lower_red = np.array([0, 139, 184])
    upper_red = np.array([179, 255, 255])
    mask_red = cv.inRange(hsv, lower_red, upper_red)

    contoursRed, _ = cv.findContours(mask_red, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for c in contoursRed:
        if cv.contourArea(c) <= 100:
            continue

        x, y, _, _ = cv.boundingRects(c)

        clocx = plocx + (x - plocx) / 6
        clocy = plocy + (y - plocy) / 6

        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(clocx - plocx), int(clocy - plocy), 0, 0)

        plocx, plocy = clocx, clocy
        cv.drawContours(img, contoursRed, -1, (0, 255, 0), 3)

    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        fingers = [0] * 5

        # THUMB
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers[0] = 1

        # INDEX FINGER
        if lmList[tipIds[1]][2] < lmList[tipIds[1] - 2][2]:
            fingers[1] = 1

        # MIDDLE FINGER
        if lmList[tipIds[2]][2] < lmList[tipIds[2] - 2][2]:
            fingers[2] = 1

        # RING FINGER
        if lmList[tipIds[3]][2] < lmList[tipIds[3] - 2][2]:
            fingers[3] = 1

        # LITTLE FINGER
        if lmList[tipIds[4]][2] < lmList[tipIds[4] - 2][2]:
            fingers[4] = 1

        if fingers == [0, 1, 0, 0, 0]:
            # Thumb and index finger raised, move forward
            pn.keyDown('w')
            pn.keyUp('a')
            pn.keyUp('d')
            pn.keyUp('s')
        elif fingers == [0, 0, 0, 0, 1]:
            # Little finger raised, move left
            pn.keyDown('a')
            pn.keyUp('d')
            pn.keyUp('w')
            pn.keyUp('s')
        elif fingers == [1, 0, 0, 0, 0]:
            # Ring finger raised, move right
            pn.keyDown('d')
            pn.keyUp('a')
            pn.keyUp('w')
            pn.keyUp('s')
        elif fingers == [0, 0, 0, 0, 0]:
            # No fingers raised, stop moving
            pn.keyUp('w')
            pn.keyUp('s')
            pn.keyUp('a')
            pn.keyUp('d')
        elif fingers == [1, 1, 1, 1, 1]:
            # All fingers raised, move backwards
            pn.keyDown('s')
            pn.keyUp('a')
            pn.keyUp('d')
            pn.keyUp('w')
        # SPACEBAR
        elif fingers == [0, 1, 1, 1, 1]:
            # Four fingers raised, press spacebar
            pn.press('space')

        # ENTER
        elif fingers == [0, 1, 1, 1, 0]:
            # Three fingers raised, press enter
            pn.press('enter')

            # ENTER
        elif fingers == [0, 1, 1, 0, 0]:
            # Three fingers raised, press enter
            pn.press('ctrl')

        elif fingers == [0, 1, 0, 0, 1]:
            # Three fingers raised, press enter
            pn.press('l')


        # Check for left mouse clicks
        now = datetime.datetime.now()
        delta = now - last_click
        if fingers == [0, 1, 1, 0, 0] and delta.total_seconds() >= 0.5:
            pg.click()
            last_click = now

    cv.imshow("Image", img)
    if cv.waitKey(1) == ord('q'):
        break

    # img = detector.findHands(img)
    # lmList = detector.findPosition(img)
    # if len(lmList) != 0:
    #     fingers = []
    #
    #     # THUMB
    #     if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
    #         fingers.append(1)
    #     else:
    #         fingers.append(0)
    #
    #     # INDEX FINGER + MIDDLE FINGER
    #     if lmList[tipIds[1]][2] < lmList[tipIds[1] - 2][2] and lmList[tipIds[2]][2] < lmList[tipIds[2] - 2][2]:
    #         fingers.append(1)
    #     else:
    #         fingers.append(0)
    #
    #     # RING FINGER + LITTLE FINGER
    #     if lmList[tipIds[3]][2] < lmList[tipIds[3] - 2][2] and lmList[tipIds[4]][2] < lmList[tipIds[4] - 2][2]:
    #         fingers.append(1)
    #     else:
    #         fingers.append(0)
    #
    #     if fingers == [1, 0, 0]:
    #         # Index finger raised
    #         pn.keyDown('a')
    #         pn.keyUp('w')
    #         pn.keyUp('s')
    #         pn.keyUp('d')
    #     elif fingers == [1, 1, 0]:
    #         # Index and middle fingers raised
    #         pn.keyUp('a')
    #         pn.keyUp('s')
    #         pn.keyDown('w')
    #         pn.keyUp('d')
    #     elif fingers == [1, 1, 1]:
    #     # Index, middle, and ring fingers raised
    #         pn.keyUp('a')
    #         pn.keyDown('s')
    #         pn.keyUp('w')
    #         pn.keyUp('d')
    #     elif fingers == [1, 1, 1, 1, 1]:
    #     # All fingers raised (fist)
    #         now = datetime.datetime.now()
    #         delta = now - last_click
    #         if delta.total_seconds() >= 0.5:
    #             pg.click()
    #             last_click = now
    # cv.imshow("Image", img)
    # if cv.waitKey(1) == ord('q'):
    #     break
cap.release()
cv.destroyAllWindows()