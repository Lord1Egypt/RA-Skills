#!/usr/bin/env python3
"""
Persistent Appium session daemon for 12306 bridge.

Runs as a background process holding one Appium session.
Accepts JSON commands on stdin, returns JSON responses on stdout.
Keeps the session alive between commands — no per-call session overhead.

Start:   python3 bridge_daemon.py &
Stop:    echo '{"action":"quit"}' > /tmp/bridge_cmd

Or use the bridge_daemon.sh wrapper to send commands.
"""

import json
import os
import sys
import time
import warnings
import xml.etree.ElementTree as ET
from pathlib import Path

warnings.filterwarnings("ignore", message=".*urllib3 v2.*OpenSSL.*")
os.environ["PYTHONWARNINGS"] = "ignore"

APPIUM_URL = "http://127.0.0.1:4723"
PACKAGE = os.environ.get("BRIDGE_PACKAGE", "com.MobileTicket")
CMD_FILE = Path("/tmp/bridge_cmd")
RESP_FILE = Path("/tmp/bridge_resp")
LOCK_FILE = Path("/tmp/bridge.lock")

_driver = None


def _ensure_appium():
    import subprocess, urllib.request
    try:
        r = urllib.request.urlopen(f"{APPIUM_URL}/status", timeout=2)
        if r.status == 200:
            return
    except Exception:
        pass
    # Auto-detect Android SDK path (Linux vs macOS)
    android_home = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
    if not android_home:
        for candidate in [
            os.path.expanduser("~/android-sdk"),
            os.path.expanduser("~/Library/Android/sdk"),
            "/usr/lib/android-sdk",
        ]:
            if os.path.isdir(candidate):
                android_home = candidate
                break
    if not android_home:
        android_home = os.path.expanduser("~/android-sdk")  # Linux default

    subprocess.Popen(
        ["appium", "--allow-insecure", "all", "--relaxed-security",
         "--log", "/tmp/appium.log"],
        env={**os.environ, "ANDROID_HOME": android_home,
             "ANDROID_SDK_ROOT": android_home},
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    time.sleep(4)


def _get_driver():
    global _driver
    from appium import webdriver
    from appium.options.android import UiAutomator2Options
    from selenium.common.exceptions import WebDriverException

    if _driver is not None:
        try:
            _driver.get_window_size()
            return _driver
        except WebDriverException:
            _driver = None
        except Exception:
            _driver = None

    # Cold start 12306 if needed
    import subprocess
    r = subprocess.run(["adb", "shell", "pidof", PACKAGE], capture_output=True, text=True, timeout=15)
    if not r.stdout.strip():
        subprocess.run(
            ["adb", "shell", "monkey", "-p", PACKAGE, "-c", "android.intent.category.LAUNCHER", "1"],
            capture_output=True, timeout=10)
        time.sleep(2)

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.app_package = PACKAGE
    options.no_reset = True
    options.auto_launch = False
    options.automation_name = "UiAutomator2"
    options.new_command_timeout = 600
    options.ignore_hidden_api_policy_error = True
    options.skip_server_installation = True
    options.skip_device_initialization = True

    _driver = webdriver.Remote(APPIUM_URL, options=options)
    time.sleep(2)

    if PACKAGE not in (_driver.current_package or ""):
        _driver.activate_app(PACKAGE)
        time.sleep(1)

    return _driver


def cmd_dump(_args):
    driver = _get_driver()
    result = {"package": driver.current_package, "activity": driver.current_activity,
              "alerts": [], "buttons": [], "trains": [], "book_buttons": [],
              "webview_contexts": []}

    try:
        source = driver.page_source
        root = ET.fromstring(source)
    except Exception as e:
        return {"ok": False, "error": str(e)[:200]}

    btn_count = 0
    train_count = 0
    for elem in root.iter():
        a = elem.attrib
        text = (a.get("text", "") or "").strip()
        cd = (a.get("content-desc", "") or "").strip()
        rid = (a.get("resource-id", "") or "").split("/")[-1]
        cls = a.get("class", "") or ""
        bounds = a.get("bounds", "") or ""
        clickable = a.get("clickable", "") == "true"

        if any(kw in text for kw in ["提示", "温馨提示", "确定要", "放弃支付"]):
            if clickable:
                result["alerts"].append({"text": text[:200]})

        if ("title" in rid.lower() or "h5_title" in rid) and text:
            result["title"] = text

        if text == "预订" and clickable:
            entry = {"text": "预订", "bounds": bounds, "x": 0, "y": 0}
            m = __import__('re').findall(r'\d+', bounds)
            if len(m) >= 4:
                entry["x"] = (int(m[0]) + int(m[2])) // 2
                entry["y"] = (int(m[1]) + int(m[3])) // 2
            result["book_buttons"].append(entry)

        if "次列车" in text and "经停" not in text and len(text) > 10:
            if train_count < 40:
                entry = {"text": text[:300], "bounds": bounds, "clickable": clickable}
                # Add center coordinates for direct tap_coords use
                m = __import__('re').findall(r'\d+', bounds)
                if len(m) >= 4:
                    entry["x"] = (int(m[0]) + int(m[2])) // 2
                    entry["y"] = (int(m[1]) + int(m[3])) // 2
                result["trains"].append(entry)
            train_count += 1

        if clickable and (text or cd or rid):
            if btn_count < 100:
                entry = {"text": (text or cd or rid)[:200], "id": rid, "bounds": bounds}
                m = __import__('re').findall(r'\d+', bounds)
                if len(m) >= 4:
                    entry["x"] = (int(m[0]) + int(m[2])) // 2
                    entry["y"] = (int(m[1]) + int(m[3])) // 2
                result["buttons"].append(entry)
            btn_count += 1

    return {"ok": True, **result}


def cmd_tap(args):
    driver = _get_driver()
    text = args.get("text", "")
    eid = args.get("id", args.get("element_id", ""))
    idx = args.get("index", 0)
    el = None

    if eid:
        try:
            el = driver.find_element("id", eid)
        except Exception:
            pass

    if not el and text:
        escaped = text.replace('"', '\\"')
        # Strategy 1: exact text match on clickable elements
        try:
            matches = driver.find_elements(
                "xpath", f'//*[@clickable="true" and contains(@text, "{escaped}")]')
            if matches:
                el = matches[min(idx, len(matches) - 1)]
        except Exception:
            pass

    if not el and text:
        escaped = text.replace('"', '\\"')
        # Strategy 2: any element containing the text (even non-clickable parent)
        try:
            matches = driver.find_elements("xpath", f'//*[contains(@text, "{escaped}")]')
            if matches:
                el = matches[min(idx, len(matches) - 1)]
                # If the matched element isn't clickable, try its parent
                if el.get_attribute("clickable") != "true":
                    try:
                        parent = el.find_element("xpath", "..")
                        if parent.get_attribute("clickable") == "true":
                            el = parent
                    except Exception:
                        pass
        except Exception:
            pass

    if not el and text:
        # Strategy 3: try content-desc
        escaped = text.replace('"', '\\"')
        try:
            matches = driver.find_elements(
                "xpath", f'//*[contains(@content-desc, "{escaped}")]')
            if matches:
                el = matches[min(idx, len(matches) - 1)]
        except Exception:
            pass

    if not el:
        return {"ok": False, "error": f"not found: '{text}'"}

    bounds = ""
    try:
        bounds = el.get_attribute("bounds") or ""
    except Exception:
        pass
    el.click()
    time.sleep(1)
    return {"ok": True, "tapped": text, "bounds": bounds, "activity": driver.current_activity}


def cmd_tap_bounds(args):
    """Tap the center of a bounds rectangle like '[x1,y1][x2,y2]'."""
    driver = _get_driver()
    bounds = args.get("bounds", "")
    if not bounds:
        return {"ok": False, "error": "missing bounds"}

    import re
    nums = re.findall(r'\d+', bounds)
    if len(nums) < 4:
        return {"ok": False, "error": f"invalid bounds format: {bounds}"}

    x = (int(nums[0]) + int(nums[2])) // 2
    y = (int(nums[1]) + int(nums[3])) // 2
    try:
        driver.execute_script("mobile: clickGesture", {"x": x, "y": y})
    except Exception:
        # Fallback: tap via ADB if gesture click fails
        import subprocess
        subprocess.run(["adb", "shell", "input", "tap", str(x), str(y)],
                       capture_output=True, timeout=5)
    time.sleep(0.5)
    return {"ok": True, "tapped": f"({x},{y})", "bounds": bounds}


def cmd_tap_coords(args):
    """Tap at exact coordinates."""
    driver = _get_driver()
    x = args.get("x", 0)
    y = args.get("y", 0)
    if not x and not y:
        return {"ok": False, "error": "missing x,y coordinates"}
    try:
        driver.execute_script("mobile: clickGesture", {"x": x, "y": y})
    except Exception:
        import subprocess
        subprocess.run(["adb", "shell", "input", "tap", str(x), str(y)],
                       capture_output=True, timeout=5)
    time.sleep(0.5)
    return {"ok": True, "tapped": f"({x},{y})"}


def cmd_find(args):
    """Find elements by text and return their details (text, bounds, clickable) for inspection."""
    driver = _get_driver()
    text = args.get("text", "")
    if not text:
        return {"ok": False, "error": "missing text"}

    escaped = text.replace('"', '\\"')
    results = []
    try:
        matches = driver.find_elements("xpath", f'//*[contains(@text, "{escaped}")]')
        for el in matches[:20]:
            try:
                t = (el.get_attribute("text") or "")[:200]
                b = el.get_attribute("bounds") or ""
                clk = el.get_attribute("clickable") or ""
                rid = (el.get_attribute("resource-id") or "").split("/")[-1]
                results.append({"text": t, "bounds": b, "clickable": clk == "true", "id": rid})
            except Exception:
                pass
    except Exception as e:
        return {"ok": False, "error": str(e)[:200]}

    # Annotate collapsed bounds
    for r in results:
        m = __import__('re').findall(r'\d+', r.get("bounds", ""))
        if len(m) >= 4:
            h = int(m[3]) - int(m[1])
            r["height_px"] = h
            r["collapsed"] = h <= 6

    return {"ok": True, "matches": results}


def cmd_scroll(args):
    driver = _get_driver()
    direction = args.get("direction", "down")
    dist = args.get("distance", "normal")

    if dist == "micro":
        pct = 0.15
    elif dist == "short":
        pct = 0.4
    elif dist == "long":
        pct = 0.85
    else:
        pct = 0.6

    # UC WebView only responds to elementId-based scrollGesture.
    # Find the WebView and scroll it directly.
    # Let exceptions propagate so the daemon can recreate the driver on crash.
    wv = driver.find_element("xpath", "//android.webkit.WebView")

    # Snapshot the page source before scroll to verify it actually moved
    try:
        before = driver.page_source
        before_hash = hash(before)
    except Exception:
        before_hash = None

    driver.execute_script("mobile: scrollGesture", {
        "elementId": wv.id,
        "direction": direction,
        "percent": pct,
        "speed": 3000,
    })
    time.sleep(0.8)

    # Verify the scroll actually changed the page
    if before_hash is not None:
        try:
            after = driver.page_source
            if hash(after) == before_hash:
                # Content didn't change — UIAutomator2 is probably dead.
                # Raise so the daemon recreates the session and retries.
                raise RuntimeError("scroll did not change page content — session may be stale")
        except RuntimeError:
            raise
        except Exception:
            pass  # Can't verify, assume ok

    return {"ok": True, "direction": direction, "distance": dist,
            "scrolled": True, "method": "elementId"}


def cmd_js_scroll(args):
    """Scroll the WebView content using JavaScript injection.

    This is the ONLY reliable way to scroll UC WebView (used by 12306 and many
    Chinese apps). Touch-based gestures (swipe, scrollGesture, ADB input) are
    all filtered out by UC WebView.

    Args:
        direction: "down" (scroll toward later content) or "up"
        distance: "micro"|"short"|"normal"|"long" — pixels to scroll
    """
    driver = _get_driver()
    direction = args.get("direction", "down")
    dist = args.get("distance", "normal")

    dist_px = {"micro": 200, "short": 500, "normal": 1200, "long": 2500}.get(dist, 1200)
    if direction == "up":
        dist_px = -dist_px

    saved = driver.context or "NATIVE_APP"
    scrolled = False

    # Try each WebView context
    for ctx in (driver.contexts or []):
        if "WEBVIEW" not in str(ctx).upper() and "CHROMIUM" not in str(ctx).upper():
            continue
        try:
            driver.switch_to.context(ctx)
            # Scroll by injecting JS. Try multiple selectors for the scrollable container.
            js = (
                f"(function(){{"
                f"var d=document.documentElement||document.body;"
                f"var s=d.querySelector('.train-list, .list, [class*=scroll], [class*=list], .content, #app, body');"
                f"if(!s)s=d;"
                f"s.scrollTop=(s.scrollTop||0)+{dist_px};"
                f"d.scrollTop=(d.scrollTop||0)+{dist_px};"
                f"return s.scrollTop||d.scrollTop;"
                f"}})()"
            )
            driver.execute_script(js)
            scrolled = True
            break
        except Exception:
            continue
        finally:
            try:
                driver.switch_to.context(saved)
            except Exception:
                pass

    if not scrolled:
        # Fallback: try JS in native context via mobile: command
        try:
            driver.execute_script("mobile: executeScript", {
                "script": (
                    f"(function(){{"
                    f"var el=document.documentElement||document.body;"
                    f"el.scrollTop=(el.scrollTop||0)+{dist_px};"
                    f"return el.scrollTop;"
                    f"}})()"
                )
            })
            scrolled = True
        except Exception:
            pass

    time.sleep(0.5)
    return {"ok": scrolled, "direction": direction, "distance": dist,
            "scrolled": scrolled, "method": "js"}


def cmd_screenshot(_args):
    """Take a screenshot of the phone and save to /tmp/screen.png.
    Returns the file path so the caller can read it for visual verification
    or OCR-based position detection."""
    import subprocess
    path = "/tmp/screen.png"
    subprocess.run(["adb", "shell", "screencap", "-p", "/sdcard/scr.png"],
                   capture_output=True, timeout=10)
    subprocess.run(["adb", "pull", "/sdcard/scr.png", path],
                   capture_output=True, timeout=10)
    return {"ok": True, "path": path}


def cmd_type(args):
    driver = _get_driver()
    text = args.get("text", "")
    if not text:
        return {"ok": False, "error": "no text"}
    try:
        el = driver.find_element("xpath", '//android.widget.EditText')
        el.click()
        time.sleep(0.2)
        el.send_keys(text)
        return {"ok": True, "typed": text}
    except Exception as e:
        return {"ok": False, "error": str(e)[:200]}


def cmd_ocr_tap(args):
    """Take screenshot, OCR for a target text, tap at its position.

    Args:
        text: Text to find via OCR (e.g. "08:00" or "G7004")
        tap_offset_x: Optional x-offset from text center (default: 0)
        tap_offset_y: Optional y-offset from text center (default: +30, below the text)
        side: "left" to restrict search to left half of screen (x<300 for departure times)
    """
    import subprocess, re, pytesseract
    from PIL import Image

    target = args.get("text", "")
    if not target:
        return {"ok": False, "error": "missing text parameter"}

    off_x = args.get("tap_offset_x", 0)
    off_y = args.get("tap_offset_y", 30)
    side = args.get("side", "")

    # Take screenshot
    subprocess.run(["adb", "shell", "screencap", "-p", "/sdcard/ocr_scr.png"],
                   capture_output=True, timeout=10)
    subprocess.run(["adb", "pull", "/sdcard/ocr_scr.png", "/tmp/ocr_scr.png"],
                   capture_output=True, timeout=10)

    img = Image.open("/tmp/ocr_scr.png")
    data = pytesseract.image_to_data(img, lang="chi_sim+eng",
                                     output_type=pytesseract.Output.DICT,
                                     config="--psm 6 --oem 3")

    for i in range(len(data["text"])):
        text = data["text"][i].strip()
        if not text:
            continue
        try:
            conf = int(data["conf"][i])
        except (ValueError, TypeError):
            conf = 0

        if target in text and conf > 40:
            x = data["left"][i]
            y = data["top"][i]
            w = data["width"][i]
            h = data["height"][i]

            # Optional side filter
            if side == "left" and x > 300:
                continue
            if side == "right" and x < 300:
                continue

            tap_x = x + w // 2 + off_x
            tap_y = y + h // 2 + off_y

            subprocess.run(["adb", "shell", "input", "tap", str(tap_x), str(tap_y)],
                           capture_output=True, timeout=5)

            return {"ok": True, "found": text, "position": {"x": x, "y": y},
                    "tapped": {"x": tap_x, "y": tap_y}, "confidence": conf}

    return {"ok": False, "error": f"text '{target}' not found in screenshot"}


def cmd_find_book_button(args):
    """Find '预订' buttons and return their positions relative to a target train.

    Uses uiautomator2 (not Appium) to avoid stale sessions. Run this when the
    train list is visible and the target train's text is present in the DOM.

    Args:
        near_y: Optional y-coordinate to filter buttons near this position
    """
    import subprocess, json, re

    near_y = args.get("near_y", 0)
    # Use adb to call uiautomator2's dump and parse
    try:
        import uiautomator2 as u2
        d = u2.connect()
        buttons = d(text="预订")
        results = []
        for btn in buttons:
            info = btn.info
            b = info.get("bounds", {})
            top = b.get("top", 0)
            bottom = b.get("bottom", 0)
            left = b.get("left", 0)
            right = b.get("right", 0)
            cx = (left + right) // 2
            cy = (top + bottom) // 2
            entry = {"bounds": f"[{left},{top}][{right},{bottom}]",
                     "center": {"x": cx, "y": cy}, "clickable": info.get("clickable")}
            if near_y and abs(top - near_y) < 300:
                entry["near_target"] = True
            results.append(entry)
        return {"ok": True, "book_buttons": results, "count": len(results)}
    except Exception as e:
        return {"ok": False, "error": str(e)[:300], "hint": "Appium may be running (kill it first)"}


def cmd_wait(args):
    """Wait for a specific text/element to appear on screen (polling)."""
    timeout = args.get("timeout", 30)
    text = args.get("text", "")
    driver = _get_driver()
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            if text:
                matches = driver.find_elements("xpath", f'//*[contains(@text, "{text}")]')
                if matches:
                    return {"ok": True, "found": text, "after": f"{timeout - (deadline - time.time()):.1f}s"}
            time.sleep(1)
        except Exception:
            time.sleep(1)
    return {"ok": False, "error": f"timeout waiting for '{text}'"}


ACTIONS = {
    "dump": cmd_dump, "tap": cmd_tap, "tap_bounds": cmd_tap_bounds,
    "tap_coords": cmd_tap_coords, "find": cmd_find,
    "scroll": cmd_scroll, "js_scroll": cmd_js_scroll,
    "screenshot": cmd_screenshot,
    "type": cmd_type, "wait": cmd_wait,
    "ocr_tap": cmd_ocr_tap,
    "find_book_button": cmd_find_book_button,
}


def run_daemon():
    """Main loop: watch CMD_FILE for commands, write responses to RESP_FILE."""
    global _driver
    LOCK_FILE.write_text(str(os.getpid()))

    # Clean up on exit
    import atexit, signal
    def cleanup():
        try:
            _driver.quit()
        except Exception:
            pass
        LOCK_FILE.unlink(missing_ok=True)
        CMD_FILE.unlink(missing_ok=True)
        RESP_FILE.unlink(missing_ok=True)
    atexit.register(cleanup)
    for sig in (signal.SIGTERM, signal.SIGINT):
        try:
            signal.signal(sig, lambda s, f: sys.exit(0))
        except Exception:
            pass

    _ensure_appium()
    _get_driver()  # Pre-warm

    while True:
        if CMD_FILE.exists():
            try:
                raw = CMD_FILE.read_text().strip()
                CMD_FILE.unlink()
                if not raw:
                    continue
                cmd = json.loads(raw)
                action = cmd.get("action", "dump")
                args = cmd.get("args", {})
            except (json.JSONDecodeError, ValueError):
                RESP_FILE.write_text(json.dumps({"ok": False, "error": "invalid json"}))
                continue

            if action == "quit":
                try:
                    _driver.quit()
                except Exception:
                    pass
                RESP_FILE.write_text(json.dumps({"ok": True, "message": "daemon stopped"}))
                break

            handler = ACTIONS.get(action, lambda a: {"ok": False, "error": f"unknown: {action}"})
            try:
                result = handler(args)
            except Exception as e:
                # Session maybe died — recreate and retry once
                try:
                    _driver = None
                    result = handler(args)
                except Exception as e2:
                    result = {"ok": False, "error": str(e2)[:300]}

            RESP_FILE.write_text(json.dumps(result, ensure_ascii=False, default=str))

        time.sleep(0.1)


# ─── CLI wrapper (for backwards compatibility) ──────────────────────────

def run_one_shot():
    """Single command mode — send to daemon, wait for response."""
    if len(sys.argv) < 2:
        print(json.dumps({"ok": False, "error": "usage: bridge_daemon.py <action> [json_args]"}))
        sys.exit(1)

    action = sys.argv[1]
    args = {}
    if len(sys.argv) > 2:
        try:
            args = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            print(json.dumps({"ok": False, "error": "invalid json args"}))
            sys.exit(1)

    # Send command to daemon
    cmd = json.dumps({"action": action, "args": args})
    CMD_FILE.write_text(cmd)

    # Wait for response
    deadline = time.time() + 60
    while time.time() < deadline:
        if RESP_FILE.exists():
            resp = RESP_FILE.read_text().strip()
            RESP_FILE.unlink()
            print(resp)
            return
        time.sleep(0.1)

    print(json.dumps({"ok": False, "error": "daemon timeout"}))


def _daemon_alive():
    """Check if the daemon process from LOCK_FILE is actually running."""
    if not LOCK_FILE.exists():
        return False
    try:
        pid = int(LOCK_FILE.read_text().strip())
        os.kill(pid, 0)  # Signal 0 = just check if process exists
        return True
    except (ValueError, OSError, ProcessLookupError):
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--daemon":
        run_daemon()
    else:
        # Auto-start daemon if not running, then send command
        if not _daemon_alive():
            import subprocess
            LOCK_FILE.unlink(missing_ok=True)
            proc = subprocess.Popen(
                [sys.executable, __file__, "--daemon"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            # Daemon writes its own PID to LOCK_FILE on startup
            time.sleep(4)  # Wait for daemon to start + pre-warm session

        run_one_shot()
