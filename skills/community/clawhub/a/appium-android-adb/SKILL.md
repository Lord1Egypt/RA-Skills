---
name: appium-android-adb
description: Read and control any Android app via Appium or uiautomator2. Provides a persistent bridge daemon (bridge_daemon.py) with dump/tap/scroll/type/wait commands AND direct uiautomator2 Python library support. For UC WebView (Alipay Nebula) apps like 12306, prefer uiautomator2 for scrolling and booking action clicks.
---

# Appium Android Bridge

Generic Android bridge for any app. Reads screens as structured JSON, executes taps/scrolling/typing. Supports two backends:

| Backend | Best for | Limitations |
|---------|----------|-------------|
| **Appium** (bridge_daemon.py) | Native apps, structured dumps, `find`/`wait` | UC WebView virtual list taps fail on collapsed elements |
| **uiautomator2** (Python lib) | WebView content, scrolling, booking buttons | Conflicts with Appium (same session can't share AccessibilityService) |

## Quick Start

### Option A: bridge_daemon.py (Appium-based)

```bash
# Once per session (~28s):
bash ~/.openclaw/workspace/skills/appium-android-adb/start_bridge.sh

# Then all interactions (~1-2s each):
python3 bridge_daemon.py dump
python3 bridge_daemon.py tap '{"text": "查询车票"}'
python3 bridge_daemon.py scroll '{"direction": "down"}'
```

### Option B: uiautomator2 (direct Python)

```bash
pip3 install uiautomator2  # already installed
python3 -c "
import uiautomator2 as u2
d = u2.connect()
d.app_start('com.MobileTicket')
"
```

Use for WebView scroll + booking button clicks. **Cannot run simultaneously with Appium.**

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
⚠️ **May not work on UC WebView** (used by 12306, Alipay apps). The WebView filters touch events. For UC WebView scrolling, use uiautomator2's `d.swipe_ext()` instead.

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
| Native Android views (date tabs, search buttons, bottom nav) | Either — both work |
| App dump / text search / element inspection | bridge_daemon.py `dump` + `find` |
| UC WebView content (train list, booking pages) | **uiautomator2** |
| Clicking "预订" / "提交订单" / action buttons | uiautomator2 `d.text('预订').click()` |
| Scrolling UC WebView lists | uiautomator2 `d.swipe_ext('up', scale=0.3)` |
| OCR + coordinate tap | ADB `input tap` (works on visible content) |
| WebView text content (crashes UIAutomator2) | bridge_daemon.py `dump` (via Appium) |

## ⚠️ UC WebView Virtual List — Critical Knowledge

Apps using UC WebView (12306, many Chinese apps) use **virtual lists** that collapse most items' accessibility bounds:

- **Visible items**: Have real bounds (h=60-130px), clickable via accessibility service
- **Off-screen items**: COLLAPSED to y=407 (top) or y=2255 (bottom), h=6px
- **Action buttons**: "预订" buttons ALWAYS have proper bounds (h=87px) even in virtual lists

### What Works on UC WebView
1. Clicking action buttons like "预订", "提交订单", "查询车票" — they have persistent proper bounds
2. Scrolling via `d.swipe_ext()` in uiautomator2
3. OCR + coordinate-based ADB tap (with good image preprocessing)
4. Element `click()` via uiautomator2 when the element has h > 20px

### What Does NOT Work on UC WebView
1. Clicking collapsed text elements (train names, times, seat info) — h=6px bounds
2. ADB `input tap` on WebView content — silently filtered by UC WebView
3. `mobile: scrollGesture` via Appium — returns False
4. W3C Actions swipe — touch events filtered
5. JS injection (`execute_script`) — no WEBVIEW contexts exposed

## Troubleshooting

**Daemon died**: Run `start_bridge.sh` again.
**uiautomator2 conflict**: "AccessibilityService already registered" means Appium is running. Kill Appium first.
**Appium session error / ANDROID_HOME**: Ensure `export ANDROID_HOME=/usr/lib/android-sdk` before starting Appium.
**G7004 text not found**: Search with spaces: `G 7 0 0 4`, not `G7004`.
**"预订" not found**: The list may not have loaded yet. Wait and re-dump.
**OCR not reading Chinese**: Use `lang='chi_sim+eng'` with `--psm 6` config.
