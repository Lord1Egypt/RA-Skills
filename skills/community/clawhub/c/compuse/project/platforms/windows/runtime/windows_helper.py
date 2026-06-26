#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import ctypes
import json
import os
import shutil
import subprocess
import sys
import time
import winreg
from ctypes import wintypes
from io import BytesIO
from pathlib import Path
from typing import Any

import mss
import psutil
import pythoncom
import pyautogui
import win32api
import win32com.client
import win32con
import win32gui
import win32process
from PIL import Image

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
os.environ.setdefault("PYAUTOGUI_HIDE_SUPPORT_PROMPT", "1")

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

KEY_MAP = {
    **{chr(i): chr(i) for i in range(ord("a"), ord("z") + 1)},
    **{str(i): str(i) for i in range(10)},
    "cmd": "winleft",
    "command": "winleft",
    "meta": "winleft",
    "super": "winleft",
    "win": "winleft",
    "windows": "winleft",
    "ctrl": "ctrl",
    "control": "ctrl",
    "shift": "shift",
    "alt": "alt",
    "option": "alt",
    "opt": "alt",
    "escape": "esc",
    "esc": "esc",
    "enter": "enter",
    "return": "enter",
    "tab": "tab",
    "space": "space",
    "backspace": "backspace",
    "delete": "delete",
    "del": "delete",
    "insert": "insert",
    "up": "up",
    "down": "down",
    "left": "left",
    "right": "right",
    "home": "home",
    "end": "end",
    "pageup": "pageup",
    "pagedown": "pagedown",
    "capslock": "capslock",
    "printscreen": "printscreen",
    "prtsc": "printscreen",
    "apps": "apps",
    "menu": "apps",
    "f1": "f1",
    "f2": "f2",
    "f3": "f3",
    "f4": "f4",
    "f5": "f5",
    "f6": "f6",
    "f7": "f7",
    "f8": "f8",
    "f9": "f9",
    "f10": "f10",
    "f11": "f11",
    "f12": "f12",
    "-": "minus",
    "=": "equals",
    "[": "[",
    "]": "]",
    "\\": "\\",
    ";": ";",
    "'": "'",
    ",": ",",
    ".": ".",
    "/": "/",
    "`": "`",
}

MONITOR_DEFAULTTONEAREST = 2
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
SW_RESTORE = 9
CF_UNICODETEXT = 13
GMEM_MOVEABLE = 0x0002

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32


def normalize_key(name: str) -> str:
    key = name.strip().lower()
    if key not in KEY_MAP:
        raise ValueError(f"Unsupported key: {name}")
    return KEY_MAP[key]


def json_output(payload: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False))
    sys.stdout.write("\n")
    sys.stdout.flush()


def error_output(message: str, code: str = "runtime_error") -> None:
    json_output({"ok": False, "error": {"code": code, "message": message}})


def get_process_path(pid: int) -> str | None:
    if pid <= 0:
        return None
    try:
        return psutil.Process(pid).exe()
    except Exception:
        pass
    try:
        handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if not handle:
            return None
        try:
            size = wintypes.DWORD(32768)
            buf = ctypes.create_unicode_buffer(size.value)
            if kernel32.QueryFullProcessImageNameW(handle, 0, buf, ctypes.byref(size)):
                return buf.value
        finally:
            kernel32.CloseHandle(handle)
    except Exception:
        pass
    return None


def display_name_from_path(path: str | None, fallback: str) -> str:
    if path:
        stem = Path(path).stem
        if stem:
            return stem
    return fallback


def get_displays() -> list[dict[str, Any]]:
    displays: list[dict[str, Any]] = []
    with mss.mss() as sct:
        for idx, monitor in enumerate(sct.monitors[1:], start=1):
            origin_x = int(monitor["left"])
            origin_y = int(monitor["top"])
            width = int(monitor["width"])
            height = int(monitor["height"])
            is_primary = origin_x == 0 and origin_y == 0
            displays.append(
                {
                    "id": idx,
                    "displayId": idx,
                    "width": width,
                    "height": height,
                    "scaleFactor": 1,
                    "originX": origin_x,
                    "originY": origin_y,
                    "isPrimary": is_primary,
                    "name": f"Display {idx}",
                    "label": f"Display {idx}",
                }
            )
    if displays and not any(display["isPrimary"] for display in displays):
        displays[0]["isPrimary"] = True
    return displays


def choose_display(display_id: int | None) -> dict[str, Any]:
    displays = get_displays()
    if not displays:
        raise RuntimeError("No active displays found")
    if display_id is None:
        for display in displays:
            if display["isPrimary"]:
                return display
        return displays[0]
    for display in displays:
        if display["displayId"] == display_id or display["id"] == display_id:
            return display
    raise RuntimeError(f"Unknown display: {display_id}")


def capture_monitor(monitor: dict[str, int], resize: tuple[int, int] | None = None) -> dict[str, Any]:
    with mss.mss() as sct:
        raw = sct.grab(monitor)
        image = Image.frombytes("RGB", raw.size, raw.rgb)
    if resize:
        image = image.resize(resize, Image.Resampling.LANCZOS)
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=75, optimize=True)
    base64_data = base64.b64encode(buffer.getvalue()).decode("ascii")
    return {"base64": base64_data, "width": image.width, "height": image.height}


def capture_display(display_id: int | None, resize: tuple[int, int] | None = None) -> dict[str, Any]:
    display = choose_display(display_id)
    monitor = {
        "left": display["originX"],
        "top": display["originY"],
        "width": display["width"],
        "height": display["height"],
    }
    result = capture_monitor(monitor, resize)
    result.update(
        {
            "displayWidth": display["width"],
            "displayHeight": display["height"],
            "displayId": display["displayId"],
            "originX": display["originX"],
            "originY": display["originY"],
            "display": display,
        }
    )
    return result


def intersect(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> bool:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    return max(ax1, bx1) < min(ax2, bx2) and max(ay1, by1) < min(ay2, by2)


def enum_windows() -> list[dict[str, Any]]:
    windows: list[dict[str, Any]] = []

    def callback(hwnd: int, _lparam: int) -> bool:
        if not win32gui.IsWindowVisible(hwnd):
            return True
        if win32gui.IsIconic(hwnd):
            return True
        title = win32gui.GetWindowText(hwnd) or ""
        if not title.strip():
            return True
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top
        if width <= 1 or height <= 1:
            return True
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process_path = get_process_path(pid)
        windows.append(
            {
                "hwnd": hwnd,
                "title": title,
                "pid": pid,
                "processPath": process_path or "",
                "ownerName": display_name_from_path(process_path, f"pid-{pid}"),
                "bounds": {"x": left, "y": top, "width": width, "height": height},
            }
        )
        return True

    win32gui.EnumWindows(callback, 0)
    return windows


def process_identity(path: str | None, pid: int) -> str:
    if path:
        return os.path.normcase(path)
    return f"pid:{pid}"


def frontmost_app() -> dict[str, str] | None:
    hwnd = win32gui.GetForegroundWindow()
    if not hwnd:
        return None
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    path = get_process_path(pid)
    if not path:
        return None
    return {"bundleId": os.path.normcase(path), "displayName": display_name_from_path(path, f"pid-{pid}")}


def app_under_point(x: int, y: int) -> dict[str, str] | None:
    hwnd = user32.WindowFromPoint(wintypes.POINT(x, y))
    if hwnd:
        hwnd = win32gui.GetAncestor(hwnd, win32con.GA_ROOT)
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        path = get_process_path(pid)
        if path:
            return {"bundleId": os.path.normcase(path), "displayName": display_name_from_path(path, f"pid-{pid}")}
    return frontmost_app()


def find_window_displays(bundle_ids: list[str]) -> list[dict[str, Any]]:
    windows = enum_windows()
    displays = get_displays()
    result: list[dict[str, Any]] = []
    normalized_targets = [os.path.normcase(item) for item in bundle_ids]
    for bundle_id in normalized_targets:
        display_ids: set[int] = set()
        for window in windows:
            process_path = os.path.normcase(window["processPath"] or "")
            if not process_path:
                continue
            if process_path != bundle_id:
                continue
            bounds = window["bounds"]
            rect = (bounds["x"], bounds["y"], bounds["x"] + bounds["width"], bounds["y"] + bounds["height"])
            for display in displays:
                display_rect = (
                    display["originX"],
                    display["originY"],
                    display["originX"] + display["width"],
                    display["originY"] + display["height"],
                )
                if intersect(rect, display_rect):
                    display_ids.add(int(display["displayId"]))
        result.append({"bundleId": bundle_id, "displayIds": sorted(display_ids)})
    return result


def read_reg_value(root, subkey: str, value_name: str) -> str | None:
    try:
        with winreg.OpenKey(root, subkey) as key:
            value, _ = winreg.QueryValueEx(key, value_name)
            if isinstance(value, str) and value.strip():
                return value.strip()
    except OSError:
        return None
    return None


def extract_exe_from_command(command: str | None) -> str | None:
    if not command:
        return None
    command = command.strip()
    if not command:
        return None
    if command.startswith('"'):
        end = command.find('"', 1)
        if end > 1:
            return command[1:end]
    parts = command.split()
    return parts[0] if parts else None


def collect_registry_apps(root, subkey: str, out: dict[str, dict[str, Any]]) -> None:
    try:
        with winreg.OpenKey(root, subkey) as key:
            count, _, _ = winreg.QueryInfoKey(key)
            for i in range(count):
                child_name = winreg.EnumKey(key, i)
                child = f"{subkey}\\{child_name}"
                display_name = read_reg_value(root, child, "DisplayName")
                if not display_name:
                    continue
                install_location = read_reg_value(root, child, "InstallLocation")
                display_icon = read_reg_value(root, child, "DisplayIcon")
                app_path = extract_exe_from_command(display_icon)
                if not app_path and install_location:
                    candidate_dir = Path(install_location)
                    if candidate_dir.exists():
                        exe_candidates = sorted(candidate_dir.glob("*.exe"))
                        if exe_candidates:
                            app_path = str(exe_candidates[0])
                if not app_path:
                    continue
                identifier = os.path.normcase(app_path)
                out.setdefault(identifier, {"bundleId": identifier, "displayName": display_name, "path": app_path})
    except OSError:
        return


def collect_app_paths(root, subkey: str, out: dict[str, dict[str, Any]]) -> None:
    try:
        with winreg.OpenKey(root, subkey) as key:
            count, _, _ = winreg.QueryInfoKey(key)
            for i in range(count):
                child_name = winreg.EnumKey(key, i)
                child = f"{subkey}\\{child_name}"
                app_path = read_reg_value(root, child, "")
                if not app_path:
                    continue
                identifier = os.path.normcase(app_path)
                out.setdefault(identifier, {"bundleId": identifier, "displayName": Path(app_path).stem, "path": app_path})
    except OSError:
        return


def installed_apps() -> list[dict[str, Any]]:
    results: dict[str, dict[str, Any]] = {}
    uninstall_keys = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
    ]
    app_paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths"),
    ]
    for root, key in uninstall_keys:
        collect_registry_apps(root, key, results)
    for root, key in app_paths:
        collect_app_paths(root, key, results)
    return sorted(results.values(), key=lambda item: item["displayName"].lower())


def running_apps() -> list[dict[str, Any]]:
    results: dict[str, dict[str, Any]] = {}
    for proc in psutil.process_iter(["pid", "name", "exe"]):
        path = proc.info.get("exe")
        if not path:
            continue
        identifier = os.path.normcase(path)
        results.setdefault(
            identifier,
            {
                "bundleId": identifier,
                "displayName": display_name_from_path(path, proc.info.get("name") or f"pid-{proc.info['pid']}"),
            },
        )
    return sorted(results.values(), key=lambda item: item["displayName"].lower())


def open_app(bundle_id: str) -> None:
    target = bundle_id.strip()
    if not target:
        raise RuntimeError("Missing app identifier")
    if os.path.exists(target):
        os.startfile(target)
        return
    resolved = shutil.which(target)
    if resolved:
        subprocess.Popen([resolved])
        return
    subprocess.Popen(["cmd", "/c", "start", "", target], shell=False)


def read_clipboard() -> str:
    if not user32.OpenClipboard(None):
        return ""
    try:
        handle = user32.GetClipboardData(CF_UNICODETEXT)
        if not handle:
            return ""
        locked = kernel32.GlobalLock(handle)
        if not locked:
            return ""
        try:
            return ctypes.wstring_at(locked)
        finally:
            kernel32.GlobalUnlock(handle)
    finally:
        user32.CloseClipboard()


def write_clipboard(text: str) -> None:
    data = str(text)
    if not user32.OpenClipboard(None):
        raise RuntimeError("OpenClipboard failed")
    try:
        user32.EmptyClipboard()
        size = (len(data) + 1) * ctypes.sizeof(ctypes.c_wchar)
        handle = kernel32.GlobalAlloc(GMEM_MOVEABLE, size)
        if not handle:
            raise RuntimeError("GlobalAlloc failed")
        locked = kernel32.GlobalLock(handle)
        if not locked:
            kernel32.GlobalFree(handle)
            raise RuntimeError("GlobalLock failed")
        try:
            ctypes.memmove(locked, ctypes.create_unicode_buffer(data), size)
        finally:
            kernel32.GlobalUnlock(handle)
        if not user32.SetClipboardData(CF_UNICODETEXT, handle):
            kernel32.GlobalFree(handle)
            raise RuntimeError("SetClipboardData failed")
    finally:
        user32.CloseClipboard()


def check_permissions() -> dict[str, bool]:
    return {"accessibility": True, "screenRecording": True}


def click(x: int, y: int, button: str, count: int, modifiers: list[str] | None) -> None:
    pyautogui.moveTo(x, y)
    if modifiers:
        normalized = [normalize_key(m) for m in modifiers]
        for key in normalized:
            pyautogui.keyDown(key)
        try:
            pyautogui.click(x=x, y=y, button=button, clicks=count, interval=0.08)
        finally:
            for key in reversed(normalized):
                pyautogui.keyUp(key)
    else:
        pyautogui.click(x=x, y=y, button=button, clicks=count, interval=0.08)


def scroll(x: int, y: int, delta_x: int, delta_y: int) -> None:
    pyautogui.moveTo(x, y)
    if delta_y:
        pyautogui.scroll(int(delta_y), x=x, y=y)
    if delta_x:
        win32api.mouse_event(win32con.MOUSEEVENTF_HWHEEL, 0, 0, int(delta_x), 0)


def key_action(sequence: str, repeat: int = 1) -> None:
    parts = [normalize_key(part) for part in sequence.split("+") if part.strip()]
    for _ in range(max(1, repeat)):
        if len(parts) == 1:
            pyautogui.press(parts[0])
        else:
            pyautogui.hotkey(*parts, interval=0.02)
        time.sleep(0.01)


def hold_keys(keys: list[str], duration_ms: int) -> None:
    normalized = [normalize_key(k) for k in keys]
    for key in normalized:
        pyautogui.keyDown(key)
    try:
        time.sleep(max(duration_ms, 0) / 1000)
    finally:
        for key in reversed(normalized):
            pyautogui.keyUp(key)


def type_text(text: str) -> None:
    pyautogui.write(text, interval=0.008)


def restore_window(hwnd: int) -> None:
    try:
        win32gui.ShowWindow(hwnd, SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
    except Exception:
        pass


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    parser.add_argument("--payload", default="{}")
    args = parser.parse_args()
    payload = json.loads(args.payload)

    try:
        command = args.command
        if command == "check_permissions":
            json_output({"ok": True, "result": check_permissions()})
            return 0
        if command == "list_displays":
            json_output({"ok": True, "result": get_displays()})
            return 0
        if command == "get_display_size":
            json_output({"ok": True, "result": choose_display(payload.get("displayId"))})
            return 0
        if command == "screenshot":
            resize = None
            if payload.get("targetWidth") and payload.get("targetHeight"):
                resize = (int(payload["targetWidth"]), int(payload["targetHeight"]))
            result = capture_display(payload.get("displayId"), resize)
            json_output({"ok": True, "result": result})
            return 0
        if command == "resolve_prepare_capture":
            resize = None
            if payload.get("targetWidth") and payload.get("targetHeight"):
                resize = (int(payload["targetWidth"]), int(payload["targetHeight"]))
            result = capture_display(payload.get("preferredDisplayId"), resize)
            result["hidden"] = []
            result["resolvedDisplayId"] = result["displayId"]
            json_output({"ok": True, "result": result})
            return 0
        if command == "zoom":
            resize = None
            if payload.get("targetWidth") and payload.get("targetHeight"):
                resize = (int(payload["targetWidth"]), int(payload["targetHeight"]))
            region = {
                "left": int(payload["x"]),
                "top": int(payload["y"]),
                "width": int(payload["width"]),
                "height": int(payload["height"]),
            }
            json_output({"ok": True, "result": capture_monitor(region, resize)})
            return 0
        if command == "prepare_for_action":
            json_output({"ok": True, "result": []})
            return 0
        if command == "preview_hide_set":
            json_output({"ok": True, "result": []})
            return 0
        if command == "find_window_displays":
            json_output({"ok": True, "result": find_window_displays(list(payload.get("bundleIds") or []))})
            return 0
        if command == "key":
            key_action(str(payload["keySequence"]), int(payload.get("repeat") or 1))
            json_output({"ok": True, "result": True})
            return 0
        if command == "hold_key":
            hold_keys(list(payload.get("keyNames") or []), int(payload.get("durationMs") or 0))
            json_output({"ok": True, "result": True})
            return 0
        if command == "type":
            type_text(str(payload.get("text") or ""))
            json_output({"ok": True, "result": True})
            return 0
        if command == "click":
            click(int(payload["x"]), int(payload["y"]), str(payload.get("button") or "left"), int(payload.get("count") or 1), payload.get("modifiers"))
            json_output({"ok": True, "result": True})
            return 0
        if command == "drag":
            from_point = payload.get("from")
            if from_point:
                pyautogui.moveTo(int(from_point["x"]), int(from_point["y"]))
            pyautogui.dragTo(int(payload["to"]["x"]), int(payload["to"]["y"]), duration=0.2, button="left")
            json_output({"ok": True, "result": True})
            return 0
        if command == "move_mouse":
            pyautogui.moveTo(int(payload["x"]), int(payload["y"]))
            json_output({"ok": True, "result": True})
            return 0
        if command == "scroll":
            scroll(int(payload["x"]), int(payload["y"]), int(payload.get("deltaX") or 0), int(payload.get("deltaY") or 0))
            json_output({"ok": True, "result": True})
            return 0
        if command == "mouse_down":
            pyautogui.mouseDown(button="left")
            json_output({"ok": True, "result": True})
            return 0
        if command == "mouse_up":
            pyautogui.mouseUp(button="left")
            json_output({"ok": True, "result": True})
            return 0
        if command == "cursor_position":
            x, y = pyautogui.position()
            json_output({"ok": True, "result": {"x": int(x), "y": int(y)}})
            return 0
        if command == "frontmost_app":
            json_output({"ok": True, "result": frontmost_app()})
            return 0
        if command == "app_under_point":
            json_output({"ok": True, "result": app_under_point(int(payload["x"]), int(payload["y"]))})
            return 0
        if command == "list_installed_apps":
            json_output({"ok": True, "result": installed_apps()})
            return 0
        if command == "list_running_apps":
            json_output({"ok": True, "result": running_apps()})
            return 0
        if command == "open_app":
            open_app(str(payload["bundleId"]))
            json_output({"ok": True, "result": True})
            return 0
        if command == "read_clipboard":
            json_output({"ok": True, "result": read_clipboard()})
            return 0
        if command == "write_clipboard":
            write_clipboard(str(payload.get("text") or ""))
            json_output({"ok": True, "result": True})
            return 0
        error_output(f"Unknown command: {command}", code="bad_command")
        return 2
    except Exception as exc:
        error_output(str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
