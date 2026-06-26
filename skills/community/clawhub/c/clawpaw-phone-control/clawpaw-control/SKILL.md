---
name: clawpaw-control
description: Execute user instructions on the phone via ClawPaw MCP tools. Use when a user wants to do something on the phone — send a message, open an app, tap something, take a screenshot, etc.
---

# ClawPaw Phone Control

Execute user instructions on the phone step by step using the ClawPaw MCP tools.

The MCP tools are available directly — no curl, no API calls needed.

## Available MCP Tools

### UI / Interaction
- **`snapshot`** — Get the UI element tree (text, resource IDs, bounds, clickable state)
- **`tap`** — Tap by coordinates OR by text/resourceId/contentDesc
- **`long_press`** — Long press at x/y
- **`swipe`** — Swipe by direction shortcut (`up`/`down`/`left`/`right`) or explicit coordinates
- **`type_text`** — Type text into the focused field (supports Chinese, emoji)
- **`press_key`** — Press a key: `home`, `back`, `enter`, `delete`, `wakeup`, `volume_up`, `volume_down`, etc.
- **`screenshot`** — Take a screenshot (returns PNG image)

### Device Info
- **`battery`** — Battery level, charging state, temperature
- **`location`** — GPS coordinates
- **`network`** — WiFi / mobile data status
- **`storage`** — Storage usage
- **`screen_state`** — Screen on/off, locked

### Hardware

- **`flashlight`** — Get or set flashlight. Use `on=true` to turn on, `on=false` to turn off, omit to get state. **Never pass `action` — only `on: boolean`.**
- **`volume`** — Get or set volume (stream: media/ring/alarm/notification, level: 0-15)
- **`brightness`** — Get or set screen brightness (level: 0-255)
- **`vibrate`** — Vibrate device (duration ms)
- **`ringtone_mode`** — Get or set ringer mode (silent/vibrate/normal)
- **`media_control`** — Control playback (action: play/pause/toggle/next/previous/stop)

### Media
- **`camera_snap`** — Take a photo (back/front camera)
- **`audio_record`** — Record audio (action: capture/start/stop)
- **`audio_status`** — Check if recording is in progress
- **`sensors`** — Read accelerometer, gyroscope, light, etc.

## Prerequisites — Check Before Starting

### ADB connectivity
If ADB commands fail (tap has no effect, snapshot empty), confirm:
1. USB debugging enabled: Settings → Developer options → USB debugging
2. Device authorized: `shell` → `adb devices` → should show `device` (not `unauthorized`)
3. If unauthorized: disconnect/reconnect USB, accept the prompt on the phone

### ADB Keyboard (required for Chinese / emoji / non-ASCII input)
`type_text` with Chinese or emoji **requires ADBKeyboard** — standard IME cannot receive arbitrary Unicode via ADB.

**Setup:**
1. Install APK: `adb install ADBKeyboard.apk` (download from GitHub: senzhk/ADBKeyBoard)
2. Enable in settings: Language & Input → Virtual keyboard → Manage keyboards → ADB Keyboard ON
3. Set active: `shell` tool → `ime set com.android.adbkeyboard/.AdbIME`
4. Verify: `shell` → `ime list -s` should include `com.android.adbkeyboard/.AdbIME`

If `type_text` produces wrong output or does nothing, re-run step 3 to reactivate ADBKeyboard.

## Core Principles

### snapshot FIRST — screenshot is a fallback

**Always use `snapshot` before acting on the screen.** It returns real device-pixel bounds — use those for all taps and interactions.

| Goal | Tool |
|------|------|
| Read screen content / find elements | **`snapshot`** |
| Tap / type / interact with elements | **`snapshot`** to get coords, then act |
| Verify a visual result after an action | **`screenshot`** |
| snapshot returns no useful elements (image, video, game) | **`screenshot`** as fallback |

**Rules:**
- **NEVER guess coordinates from a screenshot** — screenshots may be scaled; bounds from `snapshot` are accurate
- Do not call `screenshot` unless: (a) user needs to see the screen visually, or (b) `snapshot` returned nothing useful
- `screenshot` is a fallback, not the default observation tool

### Tapping elements
1. Call `snapshot` — get element list with bounds
2. The `tap` tool can match by `text`, `resourceId`, or `contentDesc` — use that when possible
3. If using raw coordinates: compute center from bounds `[left,top][right,bottom]` → `x=(left+right)/2`, `y=(top+bottom)/2`

## Standard Execution Loop

For any user task:

1. **Wake screen** — `press_key wakeup`
2. **snapshot** — read the current screen state
3. **Navigate** — `press_key home` + tap, or `shell am start` if needed
4. **snapshot** — find element coordinates before acting
5. **Act** — tap, type, swipe
6. **snapshot** — verify result by reading updated UI state
7. **screenshot** — only if the user needs to see the screen visually, or snapshot gives no useful info
8. **Repeat** until done

## Common Patterns

### Send an SMS
```
1. shell (via adb): am start -a android.intent.action.SENDTO -d sms:<PHONE> --es sms_body <TEXT> --ez exit_on_sent true
2. snapshot → find send button by contentDesc="发送短信"
3. tap with contentDesc="发送短信"  ← tap tool supports this directly
```

### Open an app
```
tap with text="<app name>"   ← if visible on home screen
-- or --
press_key home, then tap the app icon
```

### Scroll
```
swipe with direction="up"   ← scroll down (swipe up)
swipe with direction="down" ← scroll up (swipe down)
```

### Type into a field
```
1. tap the input field (by text/resourceId)
2. type_text with the text to enter
```

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Screen is black / screenshot all dark | `press_key wakeup` first |
| Tap has no effect | Use `snapshot` → tap by `text` or `contentDesc` instead of coordinates |
| Element not found by text | Try `snapshot` to see all visible elements and their exact text |
| Chinese / emoji not typed correctly | ADBKeyboard not active — run `shell`: `ime set com.android.adbkeyboard/.AdbIME` |
| type_text does nothing | ADBKeyboard not installed — see Prerequisites section above |
| ADB commands silently fail | Check `adb devices` — device may be unauthorized; reconnect USB and accept prompt |
