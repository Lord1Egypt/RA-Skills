---
name: appium-android-adb
description: Base skill for Android automation over USB ADB. Ships ocr_bridge.py — the screenshot→RapidOCR→click/swipe→re-verify loop that 12306-android-adb, pdd-android-adb and hospital-android-adb all depend on. Primary backend is direct uiautomator2 + RapidOCR (battle-proven on real 12306 and hospital bookings); Appium via bridge_daemon.py is kept only as a fallback for fully native apps and is dead on Realme-class devices. ClawHub has no dependency resolver — install this alongside any skill that names it as a requirement.
---

# Android ADB Bridge (base skill)

Generic Android bridge for any app. Reads screens via OCR, executes taps/scrolling/typing.

## 📦 This is the base skill

**Other skills depend on this one.** It ships the shared parts:

| File | Role |
|------|------|
| `ocr_bridge.py` | The OCR loop — screenshot → RapidOCR → click/swipe → re-verify. **This is what dependents use.** |
| `requirements-adb.txt` | Pinned deps for the OCR-loop venv. Dependents install it as `$BASE/requirements-adb.txt`. |
| `bridge_daemon.py` | Appium backend (fallback only; see the failure mode below) |
| `start_bridge.sh` | Launches the Appium daemon (fallback only) |

Dependents: **`12306-android-adb`**, **`pdd-android-adb`**, **`hospital-android-adb`**. Each documents
`$PY $BASE/ocr_bridge.py <cmd>` where `BASE` is this skill's directory, so it works from any working
directory.

**ClawHub has no dependency resolver** — installing a dependent skill does *not* install this one.
Install it explicitly:

```bash
clawhub install appium-android-adb
```

`ocr_bridge.py` imports **no Appium** (only `uiautomator2` + `rapidocr-onnxruntime`), so dependents
pay nothing for the Appium backend they never use. Note the name under-sells the skill: the OCR loop
is the reason it exists and the reason others depend on it.

Two backends:

| Backend | Status | Best for | Limitations |
|---------|--------|----------|-------------|
| **uiautomator2 + RapidOCR** (`ocr_bridge.py`) | ✅ **Primary** (proven end-to-end on 12306 booking 2026-08-30) | UC WebView apps, scrolling, booking buttons, Chinese input | Needs rapidocr_onnxruntime in a venv |
| **Appium** (`bridge_daemon.py`) | ⚠️ Fallback | Native apps, structured dumps, `find`/`wait` | **Dead on many consumer devices**: Realme etc. block WRITE_SECURE_SETTINGS, so io.appium.settings and IME switching fail → session never starts |

## ⚠️ Appium Failure Mode (hit this in production)

On a Realme RMX3350 the Appium path was unusable:
- shell lacks `WRITE_SECURE_SETTINGS` → `io.appium.settings` commands fail
- `d.set_input_ime()` blocked → fastinput IME can't be activated → `send_keys` fails
- Result: Appium session creation error ("settings command problem"), bridge daemon useless

**Rule: try the OCR loop FIRST. Only fall back to Appium if the app is fully native and OCR is insufficient.**

## Quick Start (primary — OCR loop)

```bash
# One-time venv (Python 3.10+), shared with the three dependent skills.
# The pins live in requirements-adb.txt, in this skill's directory; adjust BASE
# if you installed the skill somewhere other than the default.
# Pinned deliberately — an unpinned `pip install` resolves "latest" at install
# time, so the code that actually runs is whatever PyPI happened to serve that
# day and can change under you (ClawHub review [T08]).
BASE=~/.openclaw/workspace/skills/appium-android-adb   # this skill
python3 -m venv ~/.openclaw/workspace/.venv-adb
~/.openclaw/workspace/.venv-adb/bin/pip install -r $BASE/requirements-adb.txt

# Every interaction is one command:
PY=~/.openclaw/workspace/.venv-adb/bin/python
$PY ocr_bridge.py dump                     # OCR whole screen: (text, l, t, r, b)
$PY ocr_bridge.py markers                  # page-state markers
$PY ocr_bridge.py tap-text 预订 --idx 0     # click OCR match, then re-OCR verify
$PY ocr_bridge.py tap 540 1987             # click exact coordinates
$PY ocr_bridge.py swipe up --scale 0.35    # normal list scroll
$PY ocr_bridge.py jump --n 3               # 3 rapid swipes (unstuck virtual list)
$PY ocr_bridge.py wait-text 提交订单        # poll until text appears
```

`uiautomator2` auto-installs its atx-agent on the phone at first `connect()` — no Appium needed.

The bare `$PY ocr_bridge.py …` form above works here because you're in this skill's directory.
**Dependent skills invoke it as `$PY $BASE/ocr_bridge.py …`** instead — `$BASE` being this skill's
path — so their commands run from any working directory. Use `$BASE` in anything you write that has
to work outside this directory.

## The Proven Loop

1. `shot()`: `adb exec-out screencap -p` (streamed over USB — **nothing is written to `/sdcard`**) → RapidOCR → `[(text, l, t, r, b)]`. The `screencap`+`pull` pair survives only as a fallback for old platform-tools, and deletes its device-side file.

   > Historical note: this step used to leave `s.png` in `/sdcard` forever, outside the private 0700
   > screenshot dir the Safety section promises. Fixed in 1.3.5 — see ClawHub review finding `[T09]`.
2. Decide: page-state via `markers()`, position via `deps()` (HH:MM at x<250)
3. Act: `d.click(cx, cy)` / `d.swipe_ext('up', scale=0.35)` / `d.swipe(x1,y1,x2,y2,duration=0.4)`
4. **Always re-OCR after every action and verify the screen actually changed** — this is what makes the loop robust against the virtual list's lies.

## Chinese Input (no IME needed)

IME switching is blocked on locked-down devices. The proven route:

```python
d.set_clipboard('苏州')          # uiautomator2 clipboard (works where fastinput fails)
d.long_click(400, 330, duration=1.2)   # long-press the input field
# → OCR: the 粘贴 (paste) menu item appears → tap it
```

`ocr_bridge.py type 苏州 --x 400 --y 330` sets clipboard and long-presses the field.

**Clear the field first** — pasting over existing text concatenates instead of
replacing (hit on the PDD search box). `ocr_bridge.py type` clears any focused
EditText by default (`--no-clear` to skip).

## FLAG_SECURE Pages (payment screens) — a11y Tree as the Eye

Payment pages (e.g. PDD 多多钱包, PayConfirmActivity) set FLAG_SECURE:
`screencap` returns black/0-byte files. **The accessibility tree still works** —
read and tap via it:

```bash
$PY ocr_bridge.py a11y                 # all text nodes + bounds + [SELECTED] flag
$PY ocr_bridge.py a11y-selected        # nodes with selected="true" (spec chips)
$PY ocr_bridge.py a11y-tap 直接免拼    # click text found in the a11y tree
```

Also the authoritative state check for selection chips when OCR is ambiguous:
`selected="true"` in the tree beats pixel guessing.

## Scrolling a UC WebView Virtual List

- Normal advance: `d.swipe_ext('up', scale=0.35)` (≈2 train cards per scroll on 12306)
- **List "skips" a section** (target train keeps getting jumped over): do `jump` — 3 rapid large swipes (`scale=0.5`, 1.2s apart), then micro-swipes back (`scale=0.15–0.25`, or `d.swipe(540, 1900, 540, 800, duration=0.4)`)
- Track position with departure-time markers: `deps()` = HH:MM texts at x<250 — you always know which time window is on screen, independent of the DOM

## Option B: bridge_daemon.py (Appium, fallback only)

```bash
# One-shot commands run with a short-lived session by default (safer):
python3 bridge_daemon.py dump
python3 bridge_daemon.py tap '{"text": "查询车票"}'
python3 bridge_daemon.py scroll '{"direction": "down"}'

# Persistent mode is opt-in — only if you need low-latency batches:
bash ~/.openclaw/workspace/skills/appium-android-adb/start_bridge.sh
# ...which runs: python3 bridge_daemon.py --daemon
```

A background daemon is NOT auto-started by single commands; one-shot mode
creates a session, executes, and quits. Screenshots and IPC files live in the
private 0700 dir `~/.cache/appium-bridge`. Cannot run simultaneously with
uiautomator2 (same AccessibilityService).

**Appium binds to loopback only.** Both launch paths pass `--address 127.0.0.1`,
because Appium exposes full control of the attached device — without it the
server binds broadly and anything else on the LAN could drive the phone. If you
start Appium yourself, do the same:

```bash
appium --address 127.0.0.1
```

## Commands (bridge_daemon.py)

All from `~/.openclaw/workspace/skills/appium-android-adb/`. All return JSON.

### dump — read the screen
```bash
python3 bridge_daemon.py dump
```
Returns:
```json
{
  "ok": true,
  "package": "com.MobileTicket",
  "activity": "com.alipay.mobile.nebulacore.ui.H5Activity",
  "title": "上海 <> 苏州",
  "alerts": [{"text": "温馨提示"}],
  "buttons": [
    {"text": "查询车票", "id": "", "bounds": "[99,970][981,1102]", "x": 540, "y": 1036},
    {"text": "预订", "id": "", "bounds": "[870,1988][1008,2075]", "x": 939, "y": 2031}
  ],
  "trains": [
    {"text": "G 7 0 0 4次列车...", "bounds": "[66,1793][291,1919]", "clickable": true, "x": 178, "y": 1856}
  ],
  "webview_contexts": ["NATIVE_APP"]
}
```

### tap — click element by text
```bash
python3 bridge_daemon.py tap '{"text": "查询车票"}'
python3 bridge_daemon.py tap '{"text": "预订", "index": 0}'
python3 bridge_daemon.py tap '{"id": "btn_submit"}'
```

### tap_bounds — click using bounds from dump
```bash
python3 bridge_daemon.py tap_bounds '{"bounds": "[870,1988][1008,2075]"}'
```
⚠️ Only works reliably if the element has **proper bounds** (h > 20px). Collapsed virtual list items (h=6px) will NOT respond.

### tap_coords — click at exact coordinates
```bash
python3 bridge_daemon.py tap_coords '{"x": 540, "y": 1200}'
```

### find — inspect element matches
```bash
python3 bridge_daemon.py find '{"text": "7004"}'
```

### scroll — swipe the screen
```bash
python3 bridge_daemon.py scroll '{"direction": "down"}'
python3 bridge_daemon.py scroll '{"direction": "down", "distance": "micro"}'
```
⚠️ **May not work on UC WebView** (used by 12306, Alipay apps). The WebView filters touch events. For UC WebView scrolling, use the OCR loop / `d.swipe_ext()` instead.

### screenshot — take phone screenshot
```bash
python3 bridge_daemon.py screenshot
# Returns {"ok": true, "path": "/tmp/screen.png"}
```

### type — input text
```bash
python3 bridge_daemon.py type '{"text": "上海"}'
```

### wait — poll until element appears
```bash
python3 bridge_daemon.py wait '{"text": "提交订单", "timeout": 30}'
```

## When to Use Which

| Situation | Recommended Tool |
|-----------|-----------------|
| UC WebView apps (12306, Alipay, many Chinese apps) — everything | **OCR loop** (`ocr_bridge.py`) |
| Screen state / text reading | `ocr_bridge.py dump` / `markers` / `deps` |
| Clicking anything visible | `ocr_bridge.py tap-text` / `tap` (u2 click) |
| Scrolling UC WebView lists | `ocr_bridge.py swipe` / `jump` / `micro` |
| Chinese text input | `d.set_clipboard` + long-press paste |
| Native apps with structured dumps / find / wait | bridge_daemon.py (Appium) — if the device allows it |

## ⚠️ UC WebView Virtual List — Critical Knowledge

Apps using UC WebView (12306, many Chinese apps) use **virtual lists** that collapse most items' accessibility bounds:

- **Visible items**: Have real bounds (h=60-130px), clickable via accessibility service
- **Off-screen items**: COLLAPSED to y≈407 (top) or y≈2255 (bottom), h=6px — DOM lies
- **The DOM is unreliable**: sometimes renders (usable), mostly collapsed. OCR is the dependable eye.

### What Works on UC WebView
1. `d.click(x, y)` from uiautomator2 — reliably delivers touches (unlike raw ADB)
2. Scrolling via `d.swipe_ext()` / `d.swipe()`
3. OCR + coordinate click (RapidOCR reads Chinese out of the box — no tesseract language packs)
4. `d.set_clipboard()` + long-press paste for Chinese input
5. `d.dump_hierarchy()` sometimes gives accurate data — use when it renders, never depend on it

### What Does NOT Work on UC WebView
1. Raw `adb shell input tap` — filtered by UC WebView (observed 2026-08-30)
2. Clicking collapsed text elements (train names, times, seat info) — h=6px bounds
3. `mobile: scrollGesture` via Appium — returns False
4. W3C Actions swipe — touch events filtered
5. JS injection (`execute_script`) — no WEBVIEW contexts exposed
6. `d.set_input_ime()` / fastinput on Realme — WRITE_SECURE_SETTINGS blocked

## 🛡️ Safety & Consent

- **Trigger boundary**: use this skill only when the user explicitly asks to
  control their phone (a specific booking/purchase/app task). Never touch the
  device speculatively or from background tasks.
- **Confirm before irreversible actions**: before submitting an order, a
  checkout step, or any tap that changes live app state, tell the user what
  will happen and wait for confirmation. Payment credentials (PIN,
  fingerprint) are ALWAYS entered by the user — scripts never request or
  store them.
- **Screen data**: screenshots/OCR captures can contain personal data. They
  are stored in a private 0700 dir (`~/.cache/ocr-bridge`, override
  `OCR_BRIDGE_DIR`) and shots older than 1 hour are purged automatically on
  every screenshot; `ocr_bridge.py clean` purges immediately. Note that
  `clean` only ages out that host-side dir — it cannot reach the device, so
  **nothing is written to `/sdcard` in the first place**: captures stream over
  USB via `adb exec-out`, and the older `screencap` + `pull` fallback deletes
  its own device file.
- **Appium exposure**: the server is bound to `127.0.0.1` on every launch path.
  It offers unrestricted control of the connected device, so never start it on
  `0.0.0.0`, and stop it when you're done.
- **No secret echoes**: typed/pasted content is never echoed in output or
  logs (only its length). One-shot bridge commands stop any Appium server
  they started themselves — no services left running.
- **Bridge IPC**: `bridge_daemon.py` keeps its command/response files in a
  private 0700 dir (`~/.cache/appium-bridge`) and rejects files not owned by
  the current user. Appium runs WITHOUT `--allow-insecure`/`--relaxed-security`.

## Troubleshooting

**Appium session creation error / "settings command problem"**: Device blocks WRITE_SECURE_SETTINGS (Realme etc.). Stop fighting it — use the OCR loop.
**uiautomator2 conflict**: "AccessibilityService already registered" means Appium is running. Kill Appium first (`pkill -f appium`).
**OCR finds nothing / misreads**: RapidOCR is noisy on small text — narrow search to a region (x/y bounds) and re-shoot; the screen may still be animating (sleep 2-3s after actions).
**Train number not found**: DOM text has spaces (`G 7 0 0 4`), but OCR text does not (`G7004`). Match with regex on OCR: `^[GDCK]\d+`.
**tesseract missing**: Don't install it — RapidOCR (rapidocr-onnxruntime) needs no language data and read Chinese reliably in production.
