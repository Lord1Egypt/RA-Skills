---
name: duoplus-agent
displayName: DuoPlus CloudPhone Agent
description: Control Android cloud phones via ADB broadcast commands - tap, swipe, type, screenshot, read UI elements. Requires DuoPlus CloudPhone service running on the device.
version: 1.0.9
license: MIT-0
metadata:
  clawdbot:
    emoji: "📱"
    requires:
      bins: ["adb", "cwebp"]
changelog: Restructure SKILL.md, add cwebp compression, use uiautomator for UI analysis
---
# DuoPlus CloudPhone Agent

Control and automate DuoPlus cloud phones using ADB broadcast commands.

For more information, visit [DuoPlus Official Website](https://www.duoplus.net/).

## Connecting Devices

### Wireless Connection
```bash
adb connect <IP>:<PORT>
adb devices -l
```

All subsequent commands use `-s <DEVICE_ID>` to target a specific device.

## Common Workflows

### Launching an App
```bash
scripts/send_command.sh <DEVICE_ID> '{"action_name":"OPEN_APP","params":{"package_name":"com.tencent.mm"}}'
```

### Analyzing the UI
Dump and pull the UI hierarchy to find element coordinates and attributes:
```bash
adb -s <DEVICE_ID> shell uiautomator dump /sdcard/view.xml && adb -s <DEVICE_ID> pull /sdcard/view.xml ./view.xml
```
Then grep for text or resource IDs to find `bounds="[x1,y1][x2,y2]"`.

### Interacting with Elements

All interactions are sent via the helper script as JSON commands:

- **Tap coordinate**: `scripts/send_command.sh <DEVICE_ID> '{"action_name":"CLICK_COORDINATE","params":{"x":500,"y":500}}'`
- **Tap element by text**: `scripts/send_command.sh <DEVICE_ID> '{"action_name":"CLICK_ELEMENT","params":{"text":"Login"}}'`
  - Optional params: `resource_id`, `class_name`, `content_desc`, `element_order` (0-based index)
- **Long press**: `scripts/send_command.sh <DEVICE_ID> '{"action_name":"LONG_COORDINATE","params":{"x":500,"y":500,"duration":1000}}'`
- **Double tap**: `scripts/send_command.sh <DEVICE_ID> '{"action_name":"DOUBLE_TAP_COORDINATE","params":{"x":500,"y":500}}'`
- **Type text**: `scripts/send_command.sh <DEVICE_ID> '{"action_name":"INPUT_CONTENT","params":{"content":"Hello","clear_first":true}}'`
  - Must tap the input field first to focus it
- **Keyboard key**: `scripts/send_command.sh <DEVICE_ID> '{"action_name":"KEYBOARD_OPERATION","params":{"key":"enter"}}'`
  - Supported keys: enter, delete, tab, escape, space
- **Swipe**: `scripts/send_command.sh <DEVICE_ID> '{"action_name":"SLIDE_PAGE","params":{"direction":"up","start_x":487,"start_y":753,"end_x":512,"end_y":289}}'`
  - `direction`: up/down/left/right (required). Coordinates are optional.
- **Home**: `scripts/send_command.sh <DEVICE_ID> '{"action_name":"GO_TO_HOME","params":{}}'`
- **Back**: `scripts/send_command.sh <DEVICE_ID> '{"action_name":"PAGE_BACK","params":{}}'`
- **Wait**: `scripts/send_command.sh <DEVICE_ID> '{"action_name":"WAIT_TIME","params":{"wait_time":3000}}'`
- **Wait for element**: `scripts/send_command.sh <DEVICE_ID> '{"action_name":"WAIT_FOR_SELECTOR","params":{"text":"Loading complete","timeout":10000}}'`
- **End task** (only when stuck): `scripts/send_command.sh <DEVICE_ID> '{"action_name":"END_TASK","params":{"success":false,"message":"reason"}}'`

All action commands are fire-and-forget — they do NOT return results. Take a screenshot after each action to verify.

### Visual Verification

Take a screenshot, compress with cwebp, and pull to local for analysis:
```bash
# Take screenshot on device
adb -s <DEVICE_ID> shell screencap -p /sdcard/screen.png

# Pull to local
adb -s <DEVICE_ID> pull /sdcard/screen.png ./screen.png

# Compress to WebP for smaller file size (optional, recommended for vision model)
cwebp -q 60 -resize 540 0 ./screen.png -o ./screen.webp
```

If `cwebp` is not available, use the PNG directly.

## How Commands Work (Internal)

Commands are sent as Base64-encoded JSON via ADB broadcast. The helper script `scripts/send_command.sh` handles this automatically:

```bash
# Usage: scripts/send_command.sh <DEVICE_ID> <ACTION_JSON>
scripts/send_command.sh 192.168.1.100:5555 '{"action_name":"CLICK_ELEMENT","params":{"text":"Login"}}'
```

The script builds the full payload (task_type, task_id, md5, etc.), Base64-encodes it, and sends via:
```bash
adb -s <DEVICE_ID> shell am broadcast -a com.duoplus.service.PROCESS_DATA --es message "<BASE64>"
```

## Typical Workflow

```
1. Analyze UI    → uiautomator dump to find elements, or screenshot for visual analysis
2. Execute action → send_command.sh with the appropriate action JSON
3. Wait 1-3s     → Let the action take effect
4. Verify        → Screenshot + cwebp compress, or uiautomator dump again
5. Repeat 2-4 until all requested steps are completed
```

## Tips
- **Coordinates**: The coordinate system is 0-1000 relative (top-left=0,0, bottom-right=1000,1000), NOT pixels.
- **Element matching**: Use CLICK_ELEMENT (by text) when possible; fall back to CLICK_COORDINATE when text matching fails.
- **Input**: Must tap the input field first (CLICK_COORDINATE or CLICK_ELEMENT) to focus, then INPUT_CONTENT.
- **Submit**: After typing, use KEYBOARD_OPERATION(key="enter") to submit.
- **Wait**: Use `sleep 1-3` between commands to allow the UI to update. Do NOT use shell sleep on the device.
- **Swipe coordinates**: Must use irregular integers, avoid round numbers (500, 800). Vary coordinates between consecutive swipes.
