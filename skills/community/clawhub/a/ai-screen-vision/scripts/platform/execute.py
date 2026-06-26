#!/usr/bin/env python3
"""
Unified action executor for screen-vision skill.
Translates AI action commands into platform-specific mouse/keyboard operations.

Usage: execute.py --action click --x 100 --y 200
       execute.py --action type --text "hello"
       execute.py --action key --text "Return"
       execute.py --action scroll --direction down --amount 300
       execute.py --action drag --x1 100 --y1 200 --x2 300 --y2 400
"""

import argparse
import subprocess
import sys
import platform
import time


def get_os():
    system = platform.system().lower()
    if system == "linux":
        return "linux"
    elif system == "darwin":
        return "macos"
    elif system in ("windows", "mingw", "msys", "cygwin"):
        return "windows"
    return "unknown"


def get_display():
    import os
    display = os.environ.get("SV_DISPLAY", os.environ.get("DISPLAY", ":1"))
    return display


def run_cmd(cmd, display=None):
    """Run command with optional DISPLAY env."""
    import os
    env = os.environ.copy()
    if display and get_os() == "linux":
        env["DISPLAY"] = display
    result = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=10)
    if result.returncode != 0:
        print(f"WARN: {cmd} -> {result.stderr.strip()}", file=sys.stderr)
    return result.returncode


def click(x, y, button="left", count=1):
    """Click at coordinates."""
    os_name = get_os()
    display = get_display()
    
    if os_name == "linux":
        btn_map = {"left": "1", "middle": "2", "right": "3"}
        btn = btn_map.get(button, "1")
        if count == 2:
            return run_cmd(["xdotool", "mousemove", str(x), str(y), "click", "--repeat", "2", btn], display)
        return run_cmd(["xdotool", "mousemove", str(x), str(y), "click", btn], display)
    
    elif os_name == "macos":
        if count == 2:
            return run_cmd(["cliclick", f"dc:{x},{y}"])
        elif button == "right":
            return run_cmd(["cliclick", f"rc:{x},{y}"])
        return run_cmd(["cliclick", f"c:{x},{y}"])
    
    elif os_name == "windows":
        import pyautogui
        if count == 2:
            pyautogui.doubleClick(x, y)
        elif button == "right":
            pyautogui.rightClick(x, y)
        else:
            pyautogui.click(x, y)
        return 0


def type_text(text, delay=50):
    """Type text."""
    os_name = get_os()
    display = get_display()
    
    if os_name == "linux":
        return run_cmd(["xdotool", "type", "--delay", str(delay), text], display)
    elif os_name == "macos":
        return run_cmd(["cliclick", f"t:{text}"])
    elif os_name == "windows":
        import pyautogui
        pyautogui.typewrite(text, interval=delay/1000)
        return 0


def press_key(key):
    """Press a key."""
    os_name = get_os()
    display = get_display()
    
    # Normalize key names
    key_map = {
        "enter": "Return", "return": "Return",
        "tab": "Tab", "escape": "Escape", "esc": "Escape",
        "backspace": "BackSpace", "delete": "Delete",
        "up": "Up", "down": "Down", "left": "Left", "right": "Right",
        "space": "space",
    }
    mapped_key = key_map.get(key.lower(), key)
    
    if os_name == "linux":
        return run_cmd(["xdotool", "key", mapped_key], display)
    elif os_name == "macos":
        return run_cmd(["cliclick", f"kp:{mapped_key.lower()}"])
    elif os_name == "windows":
        import pyautogui
        pyautogui.press(key.lower())
        return 0


def scroll(direction="down", amount=300):
    """Scroll."""
    os_name = get_os()
    display = get_display()
    
    if os_name == "linux":
        btn = "5" if direction == "down" else "4"
        clicks = max(1, amount // 100)
        for _ in range(clicks):
            run_cmd(["xdotool", "click", btn], display)
            time.sleep(0.05)
        return 0
    
    elif os_name == "macos":
        scroll_amount = -amount if direction == "down" else amount
        return run_cmd(["cliclick", f"scroll:0,{scroll_amount}"])
    
    elif os_name == "windows":
        import pyautogui
        scroll_amount = -amount if direction == "down" else amount
        pyautogui.scroll(scroll_amount)
        return 0


def drag(x1, y1, x2, y2, duration=0.5):
    """Drag from one point to another."""
    os_name = get_os()
    display = get_display()
    
    if os_name == "linux":
        run_cmd(["xdotool", "mousemove", str(x1), str(y1), "mousedown", "1"], display)
        time.sleep(0.1)
        run_cmd(["xdotool", "mousemove", str(x2), str(y2)], display)
        time.sleep(0.1)
        return run_cmd(["xdotool", "mouseup", "1"], display)
    
    elif os_name == "macos":
        return run_cmd(["cliclick", f"dd:{x1},{y1}", "dm:{x2},{y2}", f"du:{x2},{y2}"])
    
    elif os_name == "windows":
        import pyautogui
        pyautogui.moveTo(x1, y1)
        pyautogui.dragTo(x2, y2, duration=duration)
        return 0


def wait(seconds=1.0):
    """Wait for screen to update."""
    time.sleep(seconds)
    return 0


def main():
    parser = argparse.ArgumentParser(description="Screen-Vision Action Executor")
    parser.add_argument("--action", required=True,
                       choices=["click", "type", "key", "scroll", "drag", "wait"])
    parser.add_argument("--x", type=int, default=0)
    parser.add_argument("--y", type=int, default=0)
    parser.add_argument("--x1", type=int, default=0)
    parser.add_argument("--y1", type=int, default=0)
    parser.add_argument("--x2", type=int, default=0)
    parser.add_argument("--y2", type=int, default=0)
    parser.add_argument("--text", default="")
    parser.add_argument("--button", default="left", choices=["left", "right", "middle"])
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--direction", default="down", choices=["up", "down"])
    parser.add_argument("--amount", type=int, default=300)
    parser.add_argument("--delay", type=int, default=50)
    parser.add_argument("--duration", type=float, default=0.5)
    
    args = parser.parse_args()
    
    result = 0
    if args.action == "click":
        result = click(args.x, args.y, args.button, args.count)
    elif args.action == "type":
        result = type_text(args.text, args.delay)
    elif args.action == "key":
        result = press_key(args.text)
    elif args.action == "scroll":
        result = scroll(args.direction, args.amount)
    elif args.action == "drag":
        result = drag(args.x1, args.y1, args.x2, args.y2, args.duration)
    elif args.action == "wait":
        result = wait(args.duration)
    
    sys.exit(result)


if __name__ == "__main__":
    main()
