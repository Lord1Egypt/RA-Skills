#!/usr/bin/env python3
"""ADB UI automation helper for Android apps.

Provides element finding and interaction via uiautomator dump + XML parsing.
For WebView content that ignores ADB touches, see book_12306.py (uses uiautomator2).

Usage:
    from adb_helper import ADB

    adb = ADB()  # or ADB("device_serial")
    root = adb.parse_ui()

    # Find elements
    search_btn = adb.find_first(resource_id="ticket_home_btn_search", root=root)
    trains = adb.find(class_contains="Button", text_contains="次列车", root=root)

    # Interact (works on native elements only; WebViews need uiautomator2)
    adb.tap_el(search_btn)
    adb.swipe(540, 1600, 540, 600, 100)  # fast drag for UC WebView scrolling

Note: UC WebView (used by 12306 and many Chinese apps) filters out ADB touch
events. Native Android elements and accessibility-based clicks (uiautomator2)
are required for WebView interaction.
"""

import re
import subprocess
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class UIElement:
    text: str = ""
    content_desc: str = ""
    resource_id: str = ""
    class_name: str = ""
    bounds: str = ""
    clickable: bool = False
    enabled: bool = False
    package: str = ""
    attrib: dict = field(default_factory=dict)

    @property
    def center(self) -> tuple:
        m = re.findall(r'\d+', self.bounds)
        if len(m) == 4:
            return ((int(m[0]) + int(m[2])) // 2, (int(m[1]) + int(m[3])) // 2)
        return (0, 0)

    @property
    def height(self) -> int:
        m = re.findall(r'\d+', self.bounds)
        return int(m[3]) - int(m[1]) if len(m) == 4 else 0

    @property
    def width(self) -> int:
        m = re.findall(r'\d+', self.bounds)
        return int(m[2]) - int(m[0]) if len(m) == 4 else 0


class ADB:
    """Android Debug Bridge helper for UI automation."""

    def __init__(self, device: Optional[str] = None):
        self._prefix = ["adb"] + (["-s", device] if device else [])

    def shell(self, cmd: str, timeout: int = 30) -> str:
        r = subprocess.run(self._prefix + ["shell", cmd],
                          capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()

    def dump_ui(self) -> str:
        self.shell("uiautomator dump /sdcard/ui_dump.xml")
        subprocess.run(self._prefix + ["pull", "/sdcard/ui_dump.xml", "/tmp/adb_ui.xml"],
                      capture_output=True, text=True, timeout=15)
        with open("/tmp/adb_ui.xml") as f:
            return f.read()

    def parse_ui(self, xml_str: Optional[str] = None) -> ET.Element:
        return ET.fromstring(xml_str or self.dump_ui())

    def find(self, root=None, *, text=None, text_contains=None,
             content_desc=None, content_desc_contains=None,
             resource_id=None, class_contains=None,
             clickable=None, enabled=None) -> list[UIElement]:
        """Find UI elements matching criteria. If root is None, dumps UI first."""
        if root is None:
            root = self.parse_ui()
        results = []

        def _search(node):
            for elem in node:
                a = elem.attrib
                t = a.get("text", "")
                cd = a.get("content-desc", "")
                rid = (a.get("resource-id", "") or "").split("/")[-1]
                cls = a.get("class", "")
                clk = a.get("clickable", "false") == "true"
                ena = a.get("enabled", "false") == "true"

                tests = []
                if text is not None: tests.append(t == text)
                if text_contains is not None: tests.append(text_contains in t)
                if content_desc is not None: tests.append(cd == content_desc)
                if content_desc_contains is not None: tests.append(content_desc_contains in cd)
                if resource_id is not None: tests.append(rid == resource_id)
                if class_contains is not None: tests.append(class_contains in cls)
                if clickable is not None: tests.append(clk == clickable)
                if enabled is not None: tests.append(ena == enabled)

                if all(tests):
                    results.append(UIElement(
                        text=t, content_desc=cd, resource_id=rid,
                        class_name=cls, bounds=a.get("bounds", ""),
                        clickable=clk, enabled=ena, package=a.get("package", ""),
                        attrib=dict(a),
                    ))
                _search(elem)

        _search(root)
        return results

    def find_first(self, **kwargs) -> Optional[UIElement]:
        r = self.find(**kwargs)
        return r[0] if r else None

    def tap(self, x: int, y: int):
        self.shell(f"input tap {x} {y}")

    def tap_el(self, el: UIElement):
        self.tap(*el.center)

    def tap_motion(self, x: int, y: int, press_ms: int = 150):
        """Tap using motionevent (works on some WebViews that reject input tap)."""
        self.shell(f"input motionevent DOWN {x} {y}")
        time.sleep(press_ms / 1000.0)
        self.shell(f"input motionevent UP {x} {y}")

    def swipe(self, x1: int, y1: int, x2: int, y2: int, ms: int = 500):
        self.shell(f"input swipe {x1} {y1} {x2} {y2} {ms}")

    def fast_drag(self, x1: int = 540, y1: int = 1600,
                  x2: int = 540, y2: int = 600, ms: int = 100):
        """Fast drag swipe (100ms) — works best for UC WebView scrolling."""
        self.swipe(x1, y1, x2, y2, ms)

    def press_back(self):
        self.shell("input keyevent 4")

    def launch_app(self, package: str):
        self.shell(f"monkey -p {package} -c android.intent.category.LAUNCHER 1")

    def screenshot(self, path: str = "/tmp/adb_screenshot.png"):
        self.shell("screencap -p /sdcard/adb_scr.png")
        subprocess.run(self._prefix + ["pull", "/sdcard/adb_scr.png", path],
                      capture_output=True, text=True, timeout=10)
        return path

    # ── Unicode text input ──────────────────────────────────────────

    def input_unicode(self, text: str) -> bool:
        """Input Unicode text (Chinese, etc.) using the best available method.

        Tries these strategies in order:
        1. Write to /sdcard/, use uiautomator2 ACTION_SET_TEXT (no IME needed)
        2. uiautomator2 send_keys (requires fastinput IME)
        3. Clipboard paste (may not work on all devices)
        4. ADBKeyboard broadcast (if installed)

        NOTE: For many 12306 flows, typing is NOT needed — the station picker
        and passenger selector use tap-on-suggestion. Only use this method
        when you truly need to type Chinese into a text field.
        """
        # Strategy 1: uiautomator2 ACTION_SET_TEXT on focused EditText
        if self._u2_set_text(text):
            return True

        # Strategy 2: uiautomator2 send_keys
        if self._u2_send_keys(text):
            return True

        # Strategy 3: clipboard + paste
        if self._clipboard_paste(text):
            return True

        # Strategy 4: ADBKeyboard broadcast
        if self._adbkeyboard_input(text):
            return True

        # Strategy 5: fallback — only works for ASCII
        escaped = text.replace(" ", "%s")
        try:
            result = self.shell(f"input text '{escaped}'")
            return len(result) == 0
        except Exception:
            return False

    def _u2_set_text(self, text: str) -> bool:
        """Use uiautomator2 ACTION_SET_TEXT — no IME switching needed."""
        try:
            import uiautomator2 as u2
            # Kill stale process first
            self.shell("am force-stop com.github.uiautomator 2>/dev/null")
            self.shell("am force-stop com.github.uiautomator.test 2>/dev/null")
            time.sleep(0.5)

            d = u2.connect()
            edit = d(className="android.widget.EditText", focused=True)
            if not edit.exists:
                edit = d(className="android.widget.EditText")
            if edit.exists:
                edit.set_text(text)
                return True
            return False
        except Exception:
            return False

    def _u2_send_keys(self, text: str) -> bool:
        """Use uiautomator2 send_keys (needs fastinput IME)."""
        try:
            import uiautomator2 as u2
            d = u2.connect()
            d.set_input_ime(True)
            d.send_keys(text)
            d.set_input_ime(False)
            return True
        except Exception:
            return False

    def _clipboard_paste(self, text: str) -> bool:
        """Write text to /sdcard/, attempt clipboard set + paste."""
        try:
            # Write Chinese text to file (base64 avoids encoding issues)
            import base64
            encoded = base64.b64encode(text.encode("utf-8")).decode()
            self.shell(f"echo '{encoded}' | base64 -d > /sdcard/_input.txt")
            # Some devices support cmd clipboard
            self.shell("cmd clipboard set \"$(cat /sdcard/_input.txt)\" 2>/dev/null")
            time.sleep(0.1)
            self.shell("input keyevent 279")  # KEYCODE_PASTE
            time.sleep(0.2)
            return True
        except Exception:
            return False

    def _adbkeyboard_input(self, text: str) -> bool:
        """Use ADBKeyboard IME broadcast (if installed)."""
        try:
            self.shell(f"am broadcast -a ADB_INPUT_TEXT --es msg '{text}' 2>/dev/null")
            return True
        except Exception:
            return False

    def current_package(self) -> str:
        out = self.shell("dumpsys window | grep mCurrentFocus")
        parts = out.strip().split()
        for p in parts:
            if "/" in p:
                return p.split("/")[0]
        return ""


# ─── Convenience ───────────────────────────────────────────────────────

def dump_tree(root: ET.Element, max_depth: int = 4) -> str:
    """Pretty-print accessibility tree for debugging."""
    lines = []

    def _dump(node, depth=0):
        if depth > max_depth:
            return
        for elem in node:
            a = elem.attrib
            cls = a.get('class', '').split('.')[-1]
            t = a.get('text', '')
            cd = a.get('content-desc', '')
            bounds = a.get('bounds', '')
            clk = a.get('clickable', '')
            marker = '✓' if clk == 'true' else ' '
            desc = t or cd or ''
            lines.append(f"{'  ' * depth}[{marker}] {cls} {bounds} {desc[:80]}")
            _dump(elem, depth + 1)

    _dump(root)
    return '\n'.join(lines)
