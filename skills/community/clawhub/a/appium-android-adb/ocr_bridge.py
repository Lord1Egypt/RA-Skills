#!/usr/bin/env python3
"""OCR bridge for UC WebView apps — proven on a real 12306 booking (2026-08-30).

Direct uiautomator2 + RapidOCR interaction loop. Use this when:
- bridge_daemon.py (Appium) is blocked — e.g. device shell lacks
  WRITE_SECURE_SETTINGS (Realme etc.), so io.appium.settings / IME switching fail
- the app uses UC WebView and the accessibility tree is collapsed/unreliable

The loop that works (repeat as needed):
    screenshot → OCR → [(text, l, t, r, b)] → decide → click/swipe → re-OCR to verify

Dependencies (project venv, Python 3.10+):
    pip install uiautomator2 rapidocr-onnxruntime opencv-python onnxruntime

CLI (one command per step, safe for agent tool calls):
    ocr_bridge.py dump                     # OCR whole screen: (text l t r b)
    ocr_bridge.py markers                  # page-state markers (提交订单/立即支付/...)
    ocr_bridge.py deps                     # visible HH:MM departure times (x<250)
    ocr_bridge.py tap-text <text> [--idx N] [--x0/--x1/--y0/--y1 F]
    ocr_bridge.py tap <x> <y>              # d.click at coordinates
    ocr_bridge.py swipe up|down [--scale 0.35]   # swipe_ext scroll
    ocr_bridge.py micro up|down            # tiny scroll (scale 0.15)
    ocr_bridge.py jump [--n 3]             # rapid large swipes (skip stuck sections)
    ocr_bridge.py type <中文> [--x X --y Y]  # clear field + set_clipboard + long-press
    ocr_bridge.py wait-text <text> [--timeout 30]  # poll OCR until text appears
    ocr_bridge.py shot [tag]               # screenshot to ~/.cache/ocr-bridge/<tag>.png
    ocr_bridge.py a11y                     # read screen via a11y tree (FLAG_SECURE pages)
    ocr_bridge.py a11y-selected            # nodes with selected="true" (spec chips)
    ocr_bridge.py a11y-tap <text> [--idx N]  # click text found in the a11y tree
    ocr_bridge.py clean                    # delete screenshots older than 1h

Importable too:
    from ocr_bridge import (shot, markers, deps, tap_text, scroll, jump,
                            paste_text, a11y, a11y_tap)
"""

import os
import re
import subprocess
import sys
import time
from pathlib import Path

import uiautomator2 as u2
from rapidocr_onnxruntime import RapidOCR

_OCR = RapidOCR()


def _shot_dir() -> Path:
    """Private per-user screenshot dir (0700). Screenshots can contain
    sensitive screen content (orders, payments) — never use shared /tmp
    paths. Override with OCR_BRIDGE_DIR."""
    d = Path(os.environ.get("OCR_BRIDGE_DIR", str(Path.home() / ".cache" / "ocr-bridge")))
    d.mkdir(parents=True, exist_ok=True)
    os.chmod(d, 0o700)
    return d

# Page-state keywords observed on the 12306 order flow. Extend per app.
STATE_MARKERS = (
    "提交订单", "选择乘车人", "乘车人", "立即支付", "快速支付", "订单处理中",
    "预订", "静音车厢", "温馨提示", "确定", "确认", "下一步", "已选",
)


DEVICE_SHOT = "/sdcard/s.png"


def _grab_screenshot(dest):
    """Capture the screen into `dest`. Returns the file size in bytes.

    Preferred path is `adb exec-out`, which streams the PNG over USB without
    ever writing to the device's shared storage — so no screenshot debris
    (and no PII we can't reach with `clean`) accumulates in /sdcard. The old
    two-step `screencap` + `pull` survives as a fallback for platform-tools
    too old for `exec-out`, and removes its device-side file afterwards.
    """
    try:
        with open(dest, "wb") as fh:
            subprocess.run(["adb", "exec-out", "screencap", "-p"],
                           stdout=fh, timeout=15, check=False)
        if os.path.getsize(dest) > 0:
            return os.path.getsize(dest)
    except (OSError, subprocess.SubprocessError):
        pass
    subprocess.run(["adb", "shell", "screencap", "-p", DEVICE_SHOT], timeout=15)
    subprocess.run(["adb", "pull", DEVICE_SHOT, dest], timeout=15)
    subprocess.run(["adb", "shell", "rm", "-f", DEVICE_SHOT], timeout=15)
    return os.path.getsize(dest) if os.path.exists(dest) else 0


def _is_blank(path):
    """True if the capture is uniformly black — i.e. the screen is off.

    A dozing device still returns a perfectly valid PNG, so without this check
    callers get an empty OCR list and no clue why.
    """
    try:
        import cv2
        img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
        return img is not None and img.size > 0 and int(img.max()) == 0
    except Exception:
        return False        # a diagnostic must never break the capture path


def shot(tag=None, pull_path=None):
    """Screenshot the phone and OCR it.

    Screenshots land in a private 0700 dir (~/.cache/ocr-bridge) — they can
    contain sensitive screen content, so shots older than 1 hour are purged
    on every call (use `clean` to purge immediately). Nothing is written to
    the device. Returns list of (text, l, t, r, b).

    Raises RuntimeError when the capture comes back empty, which almost always
    means FLAG_SECURE — a focused password/verification field raising the IME's
    secure keyboard, or a protected page. Blur the field (tap an inert spot) or
    navigate away, then retry.
    """
    clean_shots(verbose=False)
    if pull_path is None:
        pull_path = str(_shot_dir() / (f"{tag}.png" if tag else "sc.png"))
    if _grab_screenshot(pull_path) == 0:
        raise RuntimeError(
            f"empty screenshot ({pull_path}) — the capture returned no data. "
            "FLAG_SECURE is the usual cause, and there are two common ones: "
            "(1) the device is LOCKED — a pattern/PIN/face keyguard is "
            "FLAG_SECURE, so ask the user to unlock the phone; or (2) a focused "
            "password field raised the IME's secure keyboard — blur it by "
            "tapping an inert spot, then shoot again. "
            "`ocr_bridge.py a11y` still reads these screens and will tell you "
            "which one it is."
        )
    if _is_blank(pull_path):
        raise RuntimeError(
            "screenshot is uniformly black — the device is asleep (screen off). "
            "Wake it first: `adb shell input keyevent KEYCODE_WAKEUP`, and keep it "
            "awake for the session with `adb shell svc power stayon true`."
        )
    res, _ = _OCR(pull_path)
    out = []
    if res:
        for box, text, score in res:
            xs = [p[0] for p in box]
            ys = [p[1] for p in box]
            out.append((text, int(min(xs)), int(min(ys)),
                        int(max(xs)), int(max(ys))))
    return out


def clean_shots(max_age_s=3600, verbose=True):
    """Delete screenshots older than max_age_s from the private shot dir."""
    d = _shot_dir()
    now = time.time()
    removed = 0
    for p in d.glob("*.png"):
        try:
            if now - p.stat().st_mtime > max_age_s:
                p.unlink()
                removed += 1
        except OSError:
            pass
    if verbose:
        print(f"removed {removed} old screenshots from {d}")
    return removed


def markers(t=None):
    """Page-state markers currently on screen (list of matched texts)."""
    t = t or shot()
    return [x[0] for x in t if any(k in x[0] for k in STATE_MARKERS)]


def deps(t=None):
    """Visible departure-time markers: HH:MM texts on the left edge (x<250)."""
    t = t or shot()
    return sorted(set(x[0] for x in t
                      if x[1] < 250 and re.match(r"^\d{2}:\d{2}$", x[0])))


def find_text(t, text, idx=0, x0=None, x1=None, y0=None, y1=None):
    """Nth OCR match of `text` (substring), optionally filtered by bounds."""
    matches = [x for x in t if text in x[0]
               and (x0 is None or x[1] >= x0) and (x1 is None or x[3] <= x1)
               and (y0 is None or x[2] >= y0) and (y1 is None or x[4] <= y1)]
    return matches[idx] if len(matches) > idx else None


def tap_text(text, idx=0, sleep=2.5, verify=True, **bounds):
    """Click the center of the Nth OCR match of `text`, then re-OCR to verify."""
    t = shot()
    m = find_text(t, text, idx, **bounds)
    if not m:
        print(f"NOT FOUND: {text!r} (matches: {[x[0] for x in t if text in x[0]][:5]})")
        return None
    cx, cy = (m[1] + m[3]) // 2, (m[2] + m[4]) // 2
    print(f"tap {text!r} -> ({cx},{cy})")
    u2.connect().click(cx, cy)
    time.sleep(sleep)
    return shot() if verify else m


def scroll(direction="up", scale=0.35, sleep=2.5):
    """Normal list scroll. Proven scale=0.35 for 12306 train list."""
    u2.connect().swipe_ext(direction, scale=scale)
    time.sleep(sleep)


def jump(n=3, scale=0.5):
    """N rapid large swipes — breaks the virtual list out of a stuck/skipped
    section (e.g. the list keeps jumping over a departure-time window)."""
    d = u2.connect()
    for _ in range(n):
        d.swipe_ext("up", scale=scale)
        time.sleep(1.2)
    time.sleep(3)


def paste_text(text, field_x=None, field_y=None, long=1.2, clear=True):
    """Chinese input without an IME: clear the field, set clipboard, long-press
    the input field, then (after OCR) tap the 粘贴 item. Realme blocks IME
    switching, so d.set_clipboard + long-press paste is the proven route.

    clear=True first clears any existing text (proven on PDD search box —
    pasting over old text concatenates instead of replacing)."""
    d = u2.connect()
    if clear:
        try:
            et = d.xpath("//android.widget.EditText")
            if et.exists:
                et.clear_text()
                time.sleep(0.5)
                print("field cleared")
        except Exception as e:
            print("clear skipped:", e)
    d.set_clipboard(text)
    time.sleep(0.5)
    if field_x is not None:
        d.long_click(field_x, field_y, duration=long)
        time.sleep(1.5)
    # Never echo the pasted content — it may include names/credentials
    print(f"clipboard set ({len(text)} chars); long-pressed field. Now tap 粘贴 via tap-text.")


def a11y(selected_only=False):
    """Read the screen via the accessibility tree (d.dump_hierarchy).

    Use on FLAG_SECURE pages (e.g. PDD payment) where screencap returns
    black/0-byte — the a11y tree is the only eye there. Also the
    authoritative state check for selection chips (selected="true").

    Returns list of (text, left, top, right, bottom, selected)."""
    d = u2.connect()
    xml = d.dump_hierarchy()
    out = []
    for m in re.finditer(r"<node[^>]*>", xml):
        tag = m.group(0)
        tm = re.search(r'text="([^"]*)"', tag)
        cm = re.search(r'content-desc="([^"]*)"', tag)
        bm = re.search(r'bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', tag)
        if not bm:
            continue
        text = (tm.group(1) if tm else "") or (cm.group(1) if cm else "")
        if not text.strip():
            continue
        sel = 'selected="true"' in tag
        if selected_only and not sel:
            continue
        l, t, r, b = map(int, bm.groups())
        out.append((text, l, t, r, b, sel))
    return out


def a11y_tap(text, idx=0, sleep=2.5):
    """Click the center of the Nth a11y-tree match of `text` (substring)."""
    items = [x for x in a11y() if text in x[0]]
    if not items:
        print(f"NOT FOUND in a11y: {text!r}")
        return None
    x = items[idx]
    cx, cy = (x[1] + x[3]) // 2, (x[2] + x[4]) // 2
    print(f"a11y-tap {text!r} -> ({cx},{cy})")
    u2.connect().click(cx, cy)
    time.sleep(sleep)
    return a11y()


def wait_text(text, timeout=30, interval=3):
    """Poll OCR until `text` appears on screen."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        t = shot()
        if any(text in x[0] for x in t):
            print(f"FOUND: {text!r}")
            return t
        print(f"waiting for {text!r}...")
        time.sleep(interval)
    print(f"TIMEOUT waiting for {text!r}")
    return None


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return

    cmd = args[0]
    rest = args[1:]

    def opt(name, default=None):
        if name in rest:
            i = rest.index(name)
            return rest[i + 1]
        return default

    if cmd == "dump":
        for x in shot():
            print(x)
    elif cmd == "markers":
        print(markers())
    elif cmd == "deps":
        print(deps())
    elif cmd == "tap-text":
        text = rest[0]
        tap_text(text, idx=int(opt("--idx", 0)),
                 x0=opt("--x0"), x1=opt("--x1"),
                 y0=opt("--y0"), y1=opt("--y1"))
        for x in shot():
            print(x)
    elif cmd == "tap":
        u2.connect().click(int(rest[0]), int(rest[1]))
        time.sleep(2.5)
        for x in shot():
            print(x)
    elif cmd == "swipe":
        direction = rest[0] if rest else "up"
        scroll(direction, scale=float(opt("--scale", 0.35)))
    elif cmd == "micro":
        direction = rest[0] if rest else "up"
        scroll(direction, scale=0.15)
    elif cmd == "jump":
        jump(n=int(opt("--n", 3)))
    elif cmd == "type":
        paste_text(rest[0],
                   field_x=int(opt("--x", -1)) if opt("--x") is not None else None,
                   field_y=int(opt("--y", -1)) if opt("--y") is not None else None,
                   clear=opt("--no-clear") is None)
    elif cmd == "wait-text":
        wait_text(rest[0], timeout=int(opt("--timeout", 30)))
    elif cmd == "a11y":
        for x in a11y():
            print((x[0], x[1], x[2], x[3], x[4]) + (" [SELECTED]" if x[5] else "",))
    elif cmd == "a11y-selected":
        for x in a11y(selected_only=True):
            print((x[0], x[1], x[2], x[3], x[4]))
    elif cmd == "a11y-tap":
        a11y_tap(rest[0], idx=int(opt("--idx", 0)))
    elif cmd == "clean":
        clean_shots()
    elif cmd == "shot":
        tag = rest[0] if rest else None
        shot(tag=tag)
        print("saved")
    else:
        print(f"unknown command: {cmd}\n")
        print(__doc__)


if __name__ == "__main__":
    main()
