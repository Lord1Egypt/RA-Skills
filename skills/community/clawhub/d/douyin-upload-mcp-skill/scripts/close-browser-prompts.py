#!/usr/bin/env python3
import ctypes
import os
import time


def click(display, x11, xtst, x, y):
    xtst.XTestFakeMotionEvent(display, -1, int(x), int(y), 0)
    x11.XFlush(display)
    time.sleep(0.08)
    xtst.XTestFakeButtonEvent(display, 1, True, 0)
    xtst.XTestFakeButtonEvent(display, 1, False, 0)
    x11.XFlush(display)
    time.sleep(0.18)


def key(display, x11, xtst, keysym):
    keycode = x11.XKeysymToKeycode(display, keysym)
    xtst.XTestFakeKeyEvent(display, keycode, True, 0)
    xtst.XTestFakeKeyEvent(display, keycode, False, 0)
    x11.XFlush(display)
    time.sleep(0.12)


def main():
    x11 = ctypes.cdll.LoadLibrary("libX11.so.6")
    xtst = ctypes.cdll.LoadLibrary("libXtst.so.6")
    x11.XOpenDisplay.argtypes = [ctypes.c_char_p]
    x11.XOpenDisplay.restype = ctypes.c_void_p
    x11.XFlush.argtypes = [ctypes.c_void_p]
    x11.XKeysymToKeycode.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
    x11.XKeysymToKeycode.restype = ctypes.c_uint
    xtst.XTestFakeMotionEvent.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_ulong]
    xtst.XTestFakeButtonEvent.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_bool, ctypes.c_ulong]
    xtst.XTestFakeKeyEvent.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_bool, ctypes.c_ulong]

    display = x11.XOpenDisplay(os.environ.get("DISPLAY", ":0").encode())
    if not display:
        print({"ok": False, "error": "open_display_failed"})
        return 1

    # Most Edge native prompts are browser chrome, not page DOM. They block
    # Puppeteer clicks. Coordinates are stable in this WSL desktop profile.
    # - location permission: click Block.
    # - leave-site confirmation: click Cancel to keep the publish editor.
    # - xdg-open external protocol: click Cancel.
    for _ in range(2):
        key(display, x11, xtst, 0xFF1B)  # Escape
    click(display, x11, xtst, 171, 225)  # location Block
    click(display, x11, xtst, 745, 239)  # Leave site? Cancel
    click(display, x11, xtst, 839, 291)  # xdg-open Cancel
    print({"ok": True, "closed_known_prompts": True})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
