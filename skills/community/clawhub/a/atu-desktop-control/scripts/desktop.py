#!/usr/bin/env python3
"""Desktop Control - Screenshot, mouse, keyboard, window, clipboard automation.

All commands output JSON for agent parsing.
"""

__version__ = "1.0.0"

import argparse
import json
import os
import sys
import time
from datetime import datetime

# Default captures directory (relative to skill root, one level up from scripts/)
CAPTURES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "captures")


def json_output(data):
    """Print JSON and exit."""
    print(json.dumps(data, ensure_ascii=False))
    sys.exit(0)


def json_error(msg):
    """Print error JSON and exit with code 1."""
    print(json.dumps({"ok": False, "error": str(msg)}, ensure_ascii=False))
    sys.exit(1)


# ---------------------------------------------------------------------------
# Screenshot
# ---------------------------------------------------------------------------
def cmd_screenshot(args):
    try:
        import pyautogui
    except ImportError:
        json_error("pyautogui not installed. Run setup.ps1 (Windows) or setup.sh (Linux/Mac) first.")

    os.makedirs(CAPTURES_DIR, exist_ok=True)

    if args.output:
        path = args.output
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    else:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(CAPTURES_DIR, f"screenshot_{ts}.png")

    try:
        if args.region:
            left, top, width, height = args.region
            if width <= 0 or height <= 0:
                json_error("Region width and height must be positive integers.")
            img = pyautogui.screenshot(region=(left, top, width, height))
        else:
            img = pyautogui.screenshot()
        img.save(path)
        w, h = img.size
        json_output({"ok": True, "path": path, "width": w, "height": h})
    except Exception as e:
        json_error(f"Screenshot failed: {e}")


# ---------------------------------------------------------------------------
# Mouse
# ---------------------------------------------------------------------------
def cmd_mouse(args):
    try:
        import pyautogui
    except ImportError:
        json_error("pyautogui not installed. Run setup first.")

    sub = args.mouse_cmd

    if sub == "pos":
        x, y = pyautogui.position()
        json_output({"ok": True, "x": x, "y": y})

    elif sub == "move":
        dur = args.duration if args.duration else 0.0
        pyautogui.moveTo(args.x, args.y, duration=dur)
        json_output({"ok": True, "x": args.x, "y": args.y, "duration": dur})

    elif sub == "click":
        kwargs = {}
        if args.x is not None and args.y is not None:
            kwargs["x"] = args.x
            kwargs["y"] = args.y
        kwargs["button"] = args.button or "left"
        kwargs["clicks"] = args.clicks or 1
        pyautogui.click(**kwargs)
        json_output({"ok": True, **kwargs})

    elif sub == "drag":
        dur = args.duration if args.duration else 0.5
        pyautogui.moveTo(args.x1, args.y1)
        pyautogui.drag(args.x2 - args.x1, args.y2 - args.y1, duration=dur)
        json_output({"ok": True, "from": [args.x1, args.y1], "to": [args.x2, args.y2], "duration": dur})

    elif sub == "scroll":
        direction = args.direction or "vertical"
        if direction == "vertical":
            pyautogui.scroll(args.amount)
        else:
            pyautogui.hscroll(args.amount)
        json_output({"ok": True, "amount": args.amount, "direction": direction})

    else:
        json_error(f"Unknown mouse command: {sub}")


# ---------------------------------------------------------------------------
# Keyboard
# ---------------------------------------------------------------------------
def cmd_key(args):
    try:
        import pyautogui
    except ImportError:
        json_error("pyautogui not installed. Run setup first.")

    sub = args.key_cmd

    if sub == "type":
        interval = args.interval if args.interval else 0.0
        text = args.text
        # Use clipboard paste for non-ASCII text (CJK, emoji, etc.)
        if all(ord(c) < 128 for c in text):
            pyautogui.typewrite(text, interval=interval)
        else:
            _type_unicode(text, interval)
        json_output({"ok": True, "text": text, "interval": interval})

    elif sub == "press":
        times = args.times or 1
        for _ in range(times):
            pyautogui.press(args.key)
        json_output({"ok": True, "key": args.key, "times": times})

    elif sub == "hotkey":
        pyautogui.hotkey(*args.keys)
        json_output({"ok": True, "keys": args.keys})

    else:
        json_error(f"Unknown key command: {sub}")


def _type_unicode(text, interval=0.0):
    """Type unicode text using clipboard paste (pyautogui.typewrite only supports ASCII)."""
    try:
        import pyperclip
        import pyautogui
    except ImportError:
        json_error("pyperclip not installed. Run setup first.")

    old = pyperclip.paste()
    pyperclip.copy(text)
    time.sleep(0.05)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.1)
    pyperclip.copy(old)


# ---------------------------------------------------------------------------
# Window
# ---------------------------------------------------------------------------
def cmd_window(args):
    try:
        import pygetwindow as gw
    except ImportError:
        json_error("pygetwindow not installed. Run setup first.")

    sub = args.window_cmd

    if sub == "list":
        windows = []
        for w in gw.getAllWindows():
            if w.title.strip():
                windows.append({"title": w.title, "hwnd": w._hWnd})
        json_output({"ok": True, "windows": windows, "count": len(windows)})

    elif sub in ("activate", "minimize", "maximize", "info", "close", "resize", "move"):
        target = args.target
        win = _find_window(target)
        if not win:
            json_error(f"Window not found: {target}")

        if sub == "activate":
            try:
                win.activate()
            except Exception:
                try:
                    win.restore()
                    time.sleep(0.2)
                    win.activate()
                except Exception as e:
                    json_error(f"Failed to activate window '{target}': {e}")
            json_output({"ok": True, "action": "activate", "title": win.title})

        elif sub == "minimize":
            try:
                win.minimize()
            except Exception as e:
                json_error(f"Failed to minimize window '{target}': {e}")
            json_output({"ok": True, "action": "minimize", "title": win.title})

        elif sub == "maximize":
            try:
                win.maximize()
            except Exception as e:
                json_error(f"Failed to maximize window '{target}': {e}")
            json_output({"ok": True, "action": "maximize", "title": win.title})

        elif sub == "close":
            try:
                win.close()
            except Exception as e:
                json_error(f"Failed to close window '{target}': {e}")
            json_output({"ok": True, "action": "close", "title": win.title})

        elif sub == "resize":
            width = args.width
            height = args.height
            if width <= 0 or height <= 0:
                json_error("Width and height must be positive integers.")
            try:
                win.resizeTo(width, height)
            except Exception as e:
                json_error(f"Failed to resize window '{target}': {e}")
            json_output({"ok": True, "action": "resize", "title": win.title, "width": width, "height": height})

        elif sub == "move":
            x = args.x
            y = args.y
            try:
                win.moveTo(x, y)
            except Exception as e:
                json_error(f"Failed to move window '{target}': {e}")
            json_output({"ok": True, "action": "move", "title": win.title, "x": x, "y": y})

        elif sub == "info":
            json_output({
                "ok": True,
                "title": win.title,
                "hwnd": win._hWnd,
                "left": win.left,
                "top": win.top,
                "width": win.width,
                "height": win.height,
                "visible": win.visible,
                "isMinimized": win.isMinimized,
                "isMaximized": win.isMaximized,
                "isActive": win.isActive,
            })
    else:
        json_error(f"Unknown window command: {sub}")


def _find_window(target):
    """Find window by title (substring match) or hwnd (int)."""
    import pygetwindow as gw

    # Try hwnd first
    try:
        hwnd = int(target)
        for w in gw.getAllWindows():
            if w._hWnd == hwnd:
                return w
    except ValueError:
        pass

    # Title substring match (case-insensitive)
    target_lower = target.lower()
    for w in gw.getAllWindows():
        if target_lower in w.title.lower():
            return w
    return None


# ---------------------------------------------------------------------------
# Clipboard
# ---------------------------------------------------------------------------
def cmd_clipboard(args):
    try:
        import pyperclip
    except ImportError:
        json_error("pyperclip not installed. Run setup first.")

    if args.clip_cmd == "get":
        content = pyperclip.paste()
        json_output({"ok": True, "content": content, "length": len(content)})

    elif args.clip_cmd == "set":
        pyperclip.copy(args.text)
        json_output({"ok": True, "length": len(args.text)})

    else:
        json_error(f"Unknown clipboard command: {args.clip_cmd}")


# ---------------------------------------------------------------------------
# Screen
# ---------------------------------------------------------------------------
def cmd_screen(args):
    try:
        import pyautogui
    except ImportError:
        json_error("pyautogui not installed. Run setup first.")

    if args.screen_cmd == "size":
        w, h = pyautogui.size()
        json_output({"ok": True, "width": w, "height": h})

    elif args.screen_cmd == "pixel":
        try:
            from PIL import ImageGrab
            img = ImageGrab.grab(bbox=(args.x, args.y, args.x + 1, args.y + 1))
            r, g, b = img.getpixel((0, 0))
            json_output({"ok": True, "x": args.x, "y": args.y, "r": r, "g": g, "b": b, "hex": f"#{r:02x}{g:02x}{b:02x}"})
        except Exception as e:
            json_error(f"Failed to get pixel color: {e}")

    else:
        json_error(f"Unknown screen command: {args.screen_cmd}")


# ---------------------------------------------------------------------------
# Wait
# ---------------------------------------------------------------------------
def cmd_wait(args):
    seconds = args.seconds
    if seconds < 0:
        json_error("Wait seconds must be non-negative.")
    time.sleep(seconds)
    json_output({"ok": True, "waited": seconds})


# ---------------------------------------------------------------------------
# Argparse
# ---------------------------------------------------------------------------
def build_parser():
    parser = argparse.ArgumentParser(description="Desktop Control CLI - JSON output")
    parser.add_argument("--version", action="version", version=f"desktop-control {__version__}")
    parser.add_argument("--no-failsafe", action="store_true", help="Disable pyautogui failsafe (NOT recommended)")
    sub = parser.add_subparsers(dest="command", required=True)

    # -- screenshot --
    p_ss = sub.add_parser("screenshot", help="Take a screenshot")
    p_ss.add_argument("--output", "-o", help="Output file path")
    p_ss.add_argument("--region", nargs=4, type=int, metavar=("LEFT", "TOP", "WIDTH", "HEIGHT"), help="Region to capture")

    # -- mouse --
    p_mouse = sub.add_parser("mouse", help="Mouse control")
    mouse_sub = p_mouse.add_subparsers(dest="mouse_cmd", required=True)

    mouse_sub.add_parser("pos", help="Get current mouse position")

    p_move = mouse_sub.add_parser("move", help="Move mouse")
    p_move.add_argument("x", type=int)
    p_move.add_argument("y", type=int)
    p_move.add_argument("--duration", type=float, default=0.0)

    p_click = mouse_sub.add_parser("click", help="Click mouse")
    p_click.add_argument("x", type=int, nargs="?", default=None)
    p_click.add_argument("y", type=int, nargs="?", default=None)
    p_click.add_argument("--button", choices=["left", "right", "middle"], default="left")
    p_click.add_argument("--clicks", type=int, default=1)

    p_drag = mouse_sub.add_parser("drag", help="Drag mouse")
    p_drag.add_argument("x1", type=int)
    p_drag.add_argument("y1", type=int)
    p_drag.add_argument("x2", type=int)
    p_drag.add_argument("y2", type=int)
    p_drag.add_argument("--duration", type=float, default=0.5)

    p_scroll = mouse_sub.add_parser("scroll", help="Scroll mouse wheel")
    p_scroll.add_argument("amount", type=int, help="Positive=up, Negative=down")
    p_scroll.add_argument("--direction", choices=["vertical", "horizontal"], default="vertical")

    # -- key --
    p_key = sub.add_parser("key", help="Keyboard control")
    key_sub = p_key.add_subparsers(dest="key_cmd", required=True)

    p_type = key_sub.add_parser("type", help="Type text")
    p_type.add_argument("text", help="Text to type")
    p_type.add_argument("--interval", type=float, default=0.0)

    p_press = key_sub.add_parser("press", help="Press a key")
    p_press.add_argument("key", help="Key name (enter, tab, escape, f1, etc.)")
    p_press.add_argument("--times", type=int, default=1)

    p_hotkey = key_sub.add_parser("hotkey", help="Press key combination")
    p_hotkey.add_argument("keys", nargs="+", help="Keys to press together (e.g. ctrl c)")

    # -- window --
    p_win = sub.add_parser("window", help="Window management")
    win_sub = p_win.add_subparsers(dest="window_cmd", required=True)

    win_sub.add_parser("list", help="List all windows")

    for cmd_name in ("activate", "minimize", "maximize", "info", "close"):
        p = win_sub.add_parser(cmd_name, help=f"{cmd_name.capitalize()} a window")
        p.add_argument("target", help="Window title (substring) or hwnd")

    p_resize = win_sub.add_parser("resize", help="Resize a window")
    p_resize.add_argument("target", help="Window title (substring) or hwnd")
    p_resize.add_argument("width", type=int, help="New width in pixels")
    p_resize.add_argument("height", type=int, help="New height in pixels")

    p_move_win = win_sub.add_parser("move", help="Move a window")
    p_move_win.add_argument("target", help="Window title (substring) or hwnd")
    p_move_win.add_argument("x", type=int, help="New X position")
    p_move_win.add_argument("y", type=int, help="New Y position")

    # -- clipboard --
    p_clip = sub.add_parser("clipboard", help="Clipboard operations")
    clip_sub = p_clip.add_subparsers(dest="clip_cmd", required=True)

    clip_sub.add_parser("get", help="Get clipboard content")

    p_clip_set = clip_sub.add_parser("set", help="Set clipboard content")
    p_clip_set.add_argument("text", help="Text to copy to clipboard")

    # -- screen --
    p_screen = sub.add_parser("screen", help="Screen info")
    screen_sub = p_screen.add_subparsers(dest="screen_cmd", required=True)

    screen_sub.add_parser("size", help="Get screen resolution")

    p_pixel = screen_sub.add_parser("pixel", help="Get pixel color at coordinates")
    p_pixel.add_argument("x", type=int)
    p_pixel.add_argument("y", type=int)

    # -- wait --
    p_wait = sub.add_parser("wait", help="Wait for specified seconds")
    p_wait.add_argument("seconds", type=float, help="Seconds to wait")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # Configure failsafe (only import pyautogui if needed — wait doesn't need it)
    if args.command != "wait":
        try:
            import pyautogui
            pyautogui.FAILSAFE = not args.no_failsafe
        except ImportError:
            json_error("pyautogui not installed. Run setup.ps1 (Windows) or setup.sh (Linux/Mac) first.")

    dispatch = {
        "screenshot": cmd_screenshot,
        "mouse": cmd_mouse,
        "key": cmd_key,
        "window": cmd_window,
        "clipboard": cmd_clipboard,
        "screen": cmd_screen,
        "wait": cmd_wait,
    }

    fn = dispatch.get(args.command)
    if fn:
        try:
            fn(args)
        except SystemExit:
            raise
        except Exception as e:
            json_error(f"{args.command} failed: {e}")
    else:
        json_error(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
