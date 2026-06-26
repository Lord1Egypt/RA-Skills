#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import os
import shutil
import subprocess
import sys
import time
from io import BytesIO
from pathlib import Path
from tkinter import Tk
from typing import Any

import mss
import psutil
import pyautogui
from PIL import Image
from Xlib import X, display as xdisplay
from Xlib.error import XError

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
os.environ.setdefault("PYAUTOGUI_HIDE_SUPPORT_PROMPT", "1")

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

KEY_MAP = {
    **{chr(i): chr(i) for i in range(ord("a"), ord("z") + 1)},
    **{str(i): str(i) for i in range(10)},
    "cmd": "winleft",
    "command": "winleft",
    "meta": "winleft",
    "super": "winleft",
    "win": "winleft",
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


def require_x11() -> xdisplay.Display:
    if not os.environ.get("DISPLAY"):
        raise RuntimeError("DISPLAY is not set. Linux computer-use currently requires an X11 desktop session.")
    try:
        return xdisplay.Display()
    except Exception as exc:
        raise RuntimeError(f"Unable to open X display: {exc}") from exc


def atom(disp: xdisplay.Display, name: str):
    return disp.intern_atom(name, only_if_exists=True)


def get_displays() -> list[dict[str, Any]]:
    displays: list[dict[str, Any]] = []
    with mss.mss() as sct:
        for idx, monitor in enumerate(sct.monitors[1:], start=1):
            displays.append(
                {
                    "id": idx,
                    "displayId": idx,
                    "width": int(monitor["width"]),
                    "height": int(monitor["height"]),
                    "scaleFactor": 1,
                    "originX": int(monitor["left"]),
                    "originY": int(monitor["top"]),
                    "isPrimary": idx == 1,
                    "name": f"Display {idx}",
                    "label": f"Display {idx}",
                }
            )
    return displays


def choose_display(display_id: int | None) -> dict[str, Any]:
    displays = get_displays()
    if not displays:
        raise RuntimeError("No active displays found")
    if display_id is None:
        return displays[0]
    for display in displays:
        if display["displayId"] == display_id or display["id"] == display_id:
            return display
    raise RuntimeError(f"Unknown display: {display_id}")


def capture_monitor(region: dict[str, int], resize: tuple[int, int] | None = None) -> dict[str, Any]:
    with mss.mss() as sct:
        raw = sct.grab(region)
        image = Image.frombytes("RGB", raw.size, raw.rgb)
    if resize:
        image = image.resize(resize, Image.Resampling.LANCZOS)
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=75, optimize=True)
    return {
        "base64": base64.b64encode(buffer.getvalue()).decode("ascii"),
        "width": image.width,
        "height": image.height,
    }


def capture_display(display_id: int | None, resize: tuple[int, int] | None = None) -> dict[str, Any]:
    display = choose_display(display_id)
    region = {
        "left": display["originX"],
        "top": display["originY"],
        "width": display["width"],
        "height": display["height"],
    }
    result = capture_monitor(region, resize)
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


def window_name(win) -> str:
    for prop in ["_NET_WM_NAME", "WM_NAME"]:
        try:
            value = win.get_full_property(atom(win.display, prop), X.AnyPropertyType)
            if value and getattr(value, "value", None):
                raw = value.value
                if isinstance(raw, bytes):
                    return raw.decode("utf-8", errors="ignore")
                if isinstance(raw, str):
                    return raw
                if hasattr(raw, "tolist"):
                    data = bytes(raw.tolist())
                    return data.decode("utf-8", errors="ignore")
        except XError:
            continue
        except Exception:
            continue
    return ""


def get_window_pid(win) -> int | None:
    try:
        value = win.get_full_property(atom(win.display, "_NET_WM_PID"), X.AnyPropertyType)
        if value and getattr(value, "value", None):
            return int(value.value[0])
    except Exception:
        return None
    return None


def get_process_path(pid: int | None) -> str | None:
    if not pid:
        return None
    try:
        return psutil.Process(pid).exe()
    except Exception:
        return None


def display_name_from_path(path: str | None, fallback: str) -> str:
    if path:
        stem = Path(path).stem
        if stem:
            return stem
    return fallback


def list_windows() -> list[dict[str, Any]]:
    disp = require_x11()
    root = disp.screen().root
    client_list = root.get_full_property(atom(disp, "_NET_CLIENT_LIST"), X.AnyPropertyType)
    windows: list[dict[str, Any]] = []
    if not client_list:
        return windows
    for window_id in client_list.value:
        try:
            win = disp.create_resource_object("window", int(window_id))
            geom = win.get_geometry()
            abs_pos = win.translate_coords(root, 0, 0)
            width = int(geom.width)
            height = int(geom.height)
            if width <= 1 or height <= 1:
                continue
            pid = get_window_pid(win)
            process_path = get_process_path(pid)
            title = window_name(win)
            windows.append(
                {
                    "windowId": int(window_id),
                    "pid": pid or 0,
                    "processPath": process_path or "",
                    "displayName": display_name_from_path(process_path, title or f"pid-{pid or 0}"),
                    "title": title,
                    "bounds": {"x": int(abs_pos.x), "y": int(abs_pos.y), "width": width, "height": height},
                }
            )
        except Exception:
            continue
    return windows


def frontmost_window() -> dict[str, Any] | None:
    disp = require_x11()
    root = disp.screen().root
    active = root.get_full_property(atom(disp, "_NET_ACTIVE_WINDOW"), X.AnyPropertyType)
    if not active or not active.value or int(active.value[0]) == 0:
        return None
    win = disp.create_resource_object("window", int(active.value[0]))
    pid = get_window_pid(win)
    process_path = get_process_path(pid)
    return {
        "bundleId": process_path or (window_name(win) or f"pid-{pid or 0}"),
        "displayName": display_name_from_path(process_path, window_name(win) or f"pid-{pid or 0}"),
    }


def point_in_bounds(x: int, y: int, bounds: dict[str, int]) -> bool:
    return bounds["x"] <= x < bounds["x"] + bounds["width"] and bounds["y"] <= y < bounds["y"] + bounds["height"]


def app_under_point(x: int, y: int) -> dict[str, str] | None:
    windows = list_windows()
    for window in reversed(windows):
        if point_in_bounds(x, y, window["bounds"]):
            bundle_id = window["processPath"] or window["title"] or f"pid-{window['pid']}"
            return {"bundleId": bundle_id, "displayName": window["displayName"]}
    return frontmost_window()


def intersects(a: dict[str, int], b: dict[str, int]) -> bool:
    return max(a["x"], b["x"]) < min(a["x"] + a["width"], b["x"] + b["width"]) and max(a["y"], b["y"]) < min(a["y"] + a["height"], b["y"] + b["height"])


def find_window_displays(bundle_ids: list[str]) -> list[dict[str, Any]]:
    windows = list_windows()
    displays = get_displays()
    result: list[dict[str, Any]] = []
    for bundle_id in bundle_ids:
        display_ids: set[int] = set()
        for window in windows:
            if (window["processPath"] or "") != bundle_id:
                continue
            for display in displays:
                display_bounds = {
                    "x": display["originX"],
                    "y": display["originY"],
                    "width": display["width"],
                    "height": display["height"],
                }
                if intersects(window["bounds"], display_bounds):
                    display_ids.add(int(display["displayId"]))
        result.append({"bundleId": bundle_id, "displayIds": sorted(display_ids)})
    return result


def list_installed_apps() -> list[dict[str, Any]]:
    results: dict[str, dict[str, Any]] = {}
    desktop_files = []
    for root in [Path("/usr/share/applications"), Path.home() / ".local/share/applications"]:
        if root.exists():
            desktop_files.extend(root.rglob("*.desktop"))
    for desktop_file in desktop_files:
        try:
            text = desktop_file.read_text(errors="ignore")
        except Exception:
            continue
        name = ""
        exec_path = ""
        for line in text.splitlines():
            if line.startswith("Name=") and not name:
                name = line.split("=", 1)[1].strip()
            if line.startswith("Exec=") and not exec_path:
                exec_value = line.split("=", 1)[1].strip().split()[0]
                exec_path = exec_value.replace("%u", "").replace("%U", "")
        if not exec_path:
            continue
        if not exec_path.startswith("/"):
            resolved = shutil.which(exec_path)
            exec_path = resolved or exec_path
        bundle_id = exec_path
        results.setdefault(bundle_id, {"bundleId": bundle_id, "displayName": name or Path(exec_path).stem, "path": exec_path})
    return sorted(results.values(), key=lambda item: item["displayName"].lower())


def list_running_apps() -> list[dict[str, Any]]:
    results: dict[str, dict[str, Any]] = {}
    for proc in psutil.process_iter(["pid", "name", "exe"]):
        exe = proc.info.get("exe")
        if not exe:
            continue
        results.setdefault(exe, {"bundleId": exe, "displayName": display_name_from_path(exe, proc.info.get("name") or exe)})
    return sorted(results.values(), key=lambda item: item["displayName"].lower())


def open_app(bundle_id: str) -> None:
    target = bundle_id.strip()
    if not target:
        raise RuntimeError("Missing app identifier")
    if target.endswith(".desktop") and os.path.exists(target):
        subprocess.Popen(["gtk-launch", Path(target).stem])
        return
    if os.path.exists(target):
        subprocess.Popen([target])
        return
    subprocess.Popen([target])


def read_clipboard() -> str:
    root = Tk()
    root.withdraw()
    try:
        return root.clipboard_get()
    finally:
        root.destroy()


def write_clipboard(text: str) -> None:
    root = Tk()
    root.withdraw()
    try:
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()
    finally:
        root.destroy()


def check_permissions() -> dict[str, bool]:
    has_display = bool(os.environ.get("DISPLAY"))
    return {"accessibility": has_display, "screenRecording": has_display}


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
        pyautogui.hscroll(int(delta_x), x=x, y=y)


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
            json_output({"ok": True, "result": capture_display(payload.get("displayId"), resize)})
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
            region = {"left": int(payload["x"]), "top": int(payload["y"]), "width": int(payload["width"]), "height": int(payload["height"])}
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
            json_output({"ok": True, "result": frontmost_window()})
            return 0
        if command == "app_under_point":
            json_output({"ok": True, "result": app_under_point(int(payload["x"]), int(payload["y"]))})
            return 0
        if command == "list_installed_apps":
            json_output({"ok": True, "result": list_installed_apps()})
            return 0
        if command == "list_running_apps":
            json_output({"ok": True, "result": list_running_apps()})
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
