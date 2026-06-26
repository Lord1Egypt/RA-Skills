---
name: adb-phone-control
description: Use when the user asks to control, operate, or automate an Android phone via ADB — tapping, swiping, typing, launching apps, or any UI interaction on a connected device
metadata:
  requires:
    bins:
      - adb
      - python3
---

# ADB Phone Control

Control Android devices through ADB with a structured observe-locate-act-verify loop.

## Requirements

- **adb** — Android Debug Bridge, must be in PATH
- **python3** — Required for `app_explorer.py`
- **ADB_OUTPUT_DIR** (optional env var) — Directory for saving screenshots and UI dumps; defaults to current working directory

### Permissions Used

This skill executes the following on the connected Android device:
- `adb shell input` — tap, swipe, text input
- `adb shell uiautomator dump` — UI hierarchy extraction
- `adb shell screencap` — screen capture
- `adb shell am broadcast` — ADBKeyboard IME input (for CJK text)
- `adb shell service call clipboard` — clipboard-based text input fallback

## Prerequisites

Before any operation, verify device connection:

```bash
adb devices
```

If no device found, instruct the user to:
1. Connect via USB and enable USB Debugging
2. Or connect wirelessly: `adb connect <ip>:5555`

## Core Principle

**NEVER guess coordinates from screenshots. ALWAYS use UI hierarchy as the primary locator.**

Screenshots are for human-readable context and visual verification. UI dumps give exact pixel bounds.

## Operation Loop

Every interaction follows this cycle:

```
┌─────────────────────────────────────────┐
│  1. OBSERVE  — dump UI + screenshot     │
│  2. LOCATE   — find element by text/id  │
│  3. ACT      — tap / swipe / type       │
│  4. VERIFY   — screenshot + dump again  │
│  5. REPEAT   — next action or done      │
└─────────────────────────────────────────┘
```

**Do NOT skip the VERIFY step.** UI transitions may take time; always confirm before proceeding.

## Helper Functions

Source the helper script before starting any operation session:

```bash
source "$(dirname "${BASH_SOURCE[0]:-$0}")/adb-helpers.sh" 2>/dev/null || source ./adb-helpers.sh
```

### Available Functions

| Function | Usage | Description |
|----------|-------|-------------|
| `adb_dump` | `adb_dump` | Dump UI hierarchy to `/tmp/ui_dump.xml` |
| `adb_screenshot` | `adb_screenshot` | Capture screen to `/tmp/adb_screen.png` |
| `adb_observe` | `adb_observe` | Dump UI + screenshot in one call |
| `adb_tap_text "Submit"` | Find element by text, tap center | |
| `adb_tap_id "btn_send"` | Find element by resource-id, tap center | |
| `adb_tap_xy 540 1200` | Tap exact coordinates | |
| `adb_swipe x1 y1 x2 y2 [ms]` | Swipe between points (default 300ms) | |
| `adb_input_text "hello"` | Type text (supports spaces and CJK) | |
| `adb_key <keycode>` | Send keyevent (BACK, HOME, ENTER, etc.) | |
| `adb_hide_keyboard` | Press BACK to dismiss keyboard | |
| `adb_scroll_down` | Swipe up to scroll content down | |
| `adb_scroll_up` | Swipe down to scroll content up | |
| `adb_long_press x y [ms]` | Long press at coordinates (default 1000ms) | |
| `adb_wait [seconds]` | Sleep before next action (default 1s) | |
| `adb_screen_size` | Get device screen resolution | |
| `adb_launch_app <package>` | Launch app by package name | |
| `adb_find_package <keyword>` | Search installed packages by keyword | |
| `adb_bounds_center "bounds_string"` | Parse "[x1,y1][x2,y2]" → center x y | |

### Element Lookup Details

`adb_tap_text` and `adb_tap_id` work by:
1. Running `adb_dump` to get fresh UI hierarchy
2. Parsing the XML for matching `text=` or `resource-id=` attributes
3. Extracting the `bounds="[x1,y1][x2,y2]"` attribute
4. Computing center point: `((x1+x2)/2, (y1+y2)/2)`
5. Executing `adb shell input tap <cx> <cy>`

If multiple matches are found, the function taps the **first** match and prints a warning.
If no match is found, the function prints an error — fall back to `adb_screenshot` + Read tool for visual inspection.

## Standard Operating Procedure

### Phase 1: Setup

```bash
# Source helpers
source "$(dirname "${BASH_SOURCE[0]:-$0}")/adb-helpers.sh" 2>/dev/null || source ./adb-helpers.sh

# Verify connection
adb devices

# Get screen resolution (important for swipe calculations)
adb_screen_size
```

### Phase 2: Navigate & Operate

For each interaction step:

```bash
# 1. Observe current state
adb_observe
# Then read /tmp/adb_screen.png with the Read tool to see the screen

# 2. Locate and act (prefer text/id over raw coordinates)
adb_tap_text "Create"
# or: adb_tap_id "iv_send"
# or as last resort: adb_tap_xy 540 2009

# 3. Wait for transition
adb_wait 2

# 4. Verify result
adb_screenshot
# Then read /tmp/adb_screen.png to confirm the action worked
```

### Phase 3: Text Input

```bash
# Tap the input field first
adb_tap_text "Search..."
adb_wait 1

# Type text
adb_input_text "Hello World"

# Hide keyboard before tapping other elements
adb_hide_keyboard
adb_wait 1

# Now safe to tap other buttons
adb_tap_text "Send"
```

## Critical Rules

### 1. UI Dump First, Screenshot Second

- `uiautomator dump` gives exact bounds, element states (enabled/focused/clickable), text content, and resource IDs
- Screenshots only for: visual verification, understanding layout context, or when UI dump fails (e.g., animations, WebView content)
- When UI dump returns elements with `NAF="true"`, the element has No Accessible Framework info — use screenshot + coordinates as fallback

### 2. Keyboard Awareness

- **Always hide keyboard before tapping non-input elements.** The keyboard shifts the layout, making UI dump bounds stale.
- After typing, call `adb_hide_keyboard` then `adb_dump` before tapping anything else.
- If `uiautomator dump` returns `ERROR: could not get idle state`, the keyboard animation may still be running — wait 1s and retry.

### 3. Wait Strategy

- After tap: wait **1s** before next dump/screenshot
- After launching app: wait **2-3s**
- After page navigation: wait **2s**
- After typing: wait **0.5s**
- If UI hasn't changed after action: wait longer, up to **5s**, then re-check
- **Never blindly chain actions without verification**

### 4. Chinese / CJK Text Input

`adb shell input text` does not support CJK characters natively. The helper `adb_input_text` handles this by:
- Using `adb shell am broadcast` with ADBKeyboard if available
- Falling back to clipboard-based input: copy to clipboard via `adb shell service call clipboard`, then paste

If ADB Keyboard IME is installed (`com.android.adbkeyboard`), enable it:
```bash
adb shell ime set com.android.adbkeyboard/.AdbIME
```

### 5. Coordinate System

- All coordinates are in **physical pixels** matching the device resolution
- `adb shell wm size` returns the canonical resolution (e.g., 1080x2340)
- Screenshot pixel dimensions may differ from device resolution — **never** estimate coordinates from screenshot pixel positions
- Always derive coordinates from `uiautomator dump` bounds

### 6. Handling Failures

If an action doesn't produce the expected result:
1. Re-dump UI hierarchy — the element may have moved or state changed
2. Take a screenshot — visual context may reveal popups, loading states, or errors
3. Check if the element is `enabled="true"` and `clickable="true"` before tapping
4. If element is not found by text, try partial match or search by resource-id
5. If the app is in a WebView, UI dump may not capture web elements — use screenshot + coordinate estimation as fallback

### 7. App Launch

Prefer `adb_find_package` + `adb_launch_app` over monkey command:
```bash
# Find the app
adb_find_package "wechat"
# Launch it
adb_launch_app "com.tencent.mm"
```

## Limitations

- `uiautomator dump` doesn't work during animations — wait for idle state
- WebView/Flutter/game content may not appear in UI hierarchy — use screenshot-based approach
- Some custom views may have empty text and no resource-id — use bounds + screenshot cross-reference
- Maximum ~100 actions per task is a reasonable limit to avoid infinite loops
