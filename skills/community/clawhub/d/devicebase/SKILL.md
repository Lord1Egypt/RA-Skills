---
name: devicebase
description: "Devicebase CLI — cross-platform Go CLI for remote Android, HarmonyOS, and iOS device control via HTTP API. Supports tap, swipe, text input, app launching, screenshots, UI hierarchy inspection, and more."
---

# Devicebase CLI

A cross-platform Go CLI tool for remote device control. Supports **Android**, **HarmonyOS**, and **iOS** devices. Capabilities include tap, swipe, text input, app launching, screenshots, UI hierarchy inspection, and device information retrieval.

## When to Activate

- Building AI agents or automation scripts that interact with mobile devices
- Developing mobile app testing pipelines
- Creating remote device control workflows
- Implementing deviceFarm or mobile CI/CD integrations
- Any task requiring programmatic mobile device interaction

## Quick Reference

### Command Pattern

```
# Commands requiring device serial
devicebase -s <serial> <subcommand> [args]

# Global commands (no serial required)
devicebase list-devices [flags]
```

### All Commands

| Command | Args | Description |
|---------|------|-------------|
| `tap` | `<x>,<y>` | Single tap at coordinates |
| `double-tap` | `<x>,<y>` | Double tap at coordinates |
| `long-press` | `<x>,<y>` | Long press at coordinates |
| `swipe` | `<x1>,<y1>,<x2>,<y2>` | Swipe from start to end point |
| `back` | (none) | Press back button |
| `home` | (none) | Press home button |
| `launch-app` | `<app_name>` | Launch app by package name/bundle ID |
| `current-app` | (none) | Get foreground app identifier |
| `input` | `<text>` | Input text into focused field |
| `clear-text` | (none) | Clear text in focused field |
| `device-info` | (none) | Get device hardware and status info |
| `dump-hierarchy` | (none) | Get UI accessibility tree as JSON |
| `screenshot` | (none) | Capture screen (stdout or file) |
| `list-devices` | (none) | List all available devices |

---

## Environment Setup

Both environment variables are **required**. The CLI exits with code 1 if either is missing.

```bash
# Install Devicebase CLI on Linux/MacOS (if not already installed)
which devicebase || curl -fsSL https://downloads.devicebase.cn/cli/install.sh | bash
# Install Devicebase CLI on Windows (if not already installed)
powershell -c "irm https://downloads.devicebase.cn/cli/install.ps1 | iex"

# Export API key to environment variable on Linux/MacOS (recommended for repeated use)
export DEVICEBASE_API_KEY="your_api_key"
# Export API key to environment variable on Windows (recommended for repeated use)
$env:DEVICEBASE_API_KEY = "your_api_key"

# Or inline (for one-off commands)
DEVICEBASE_API_KEY=your_api_key \
  devicebase -s <serial> <command>
```

| Variable | Required | Description |
|----------|----------|-------------|
| `DEVICEBASE_API_KEY` | Yes | APK key for authentication. Sent as `Authorization: Bearer <your_api_key>` on every request. Get your API key from https://www.devicebase.cn/ |

---

## Global Flags

| Flag | Short | Required | Description |
|------|-------|----------|-------------|
| `--serial` | `-s` | **Yes** | Device serial number. Must be specified for every command. |
| `--help` | `-h` | No | Show help for any command or subcommand. |
| `--version` | | No | Show CLI version. |

Missing serial produces:
```
Error: required flag(s) "--serial" not set
```

---

## Device Listing

### list-devices

List all available devices with their serial numbers, states, and basic info.

```bash
devicebase list-devices

# Filter by keyword (brand/model/serial/name)
devicebase list-devices --keyword "iPhone"

# Filter by state (busy/free/offline)
devicebase list-devices --state free

# Combine filters
devicebase list-devices --keyword "Samsung" --state busy
```

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--keyword` | `-k` | (none) | Filter by brand, model, serial, or name |
| `--state` | | (none) | Filter by device state: `busy`, `free`, or `offline` |

**Common workflows:**
```bash
# Find an available device for testing
devicebase list-devices --state free

# Find a specific device by model
devicebase list-devices --keyword "Pixel"

# Check all iOS devices
devicebase list-devices --keyword "iPhone"
```

---

## Touch Interactions

All touch commands use pixel coordinates. Format: `x,y` (horizontal,vertical).

### tap

Single tap at coordinates.

```bash
devicebase -s <serial> tap 100,200
```

### double-tap

Double tap at coordinates.

```bash
devicebase -s <serial> double-tap 540,960
```

### long-press

Long press (touch and hold) at coordinates.

```bash
devicebase -s <serial> long-press 200,400
```

### swipe

Swipe from one point to another.

```bash
devicebase -s <serial> swipe 100,200,300,400
# Format: x1,y1,x2,y2 (start point to end point)
```

**Common workflows:**
```bash
# Tap center-bottom of a 1080x1920 screen
devicebase -s <serial> tap 540,1800

# Pull to refresh (swipe up)
devicebase -s <serial> swipe 540,1600,540,200

# Long press to trigger context menu
devicebase -s <serial> long-press 540,960
```

---

## Navigation

### back

Press the back button. Use to navigate back, dismiss dialogs, or close keyboards.

```bash
devicebase -s <serial> back
```

### home

Press the home button to return to the home screen.

```bash
devicebase -s <serial> home
```

**Workflow:**
```bash
# Navigate back twice
devicebase -s <serial> back
devicebase -s <serial> back

# Go home then launch an app
devicebase -s <serial> home
devicebase -s <serial> launch-app com.android.settings
```

---

## App Management

### launch-app

Launch an application by its package name (Android/HarmonyOS) or bundle ID (iOS).

```bash
# Android
devicebase -s <serial> launch-app com.android.settings

# iOS
devicebase -s <serial> launch-app com.apple.Maps

# HarmonyOS
devicebase -s <serial> launch-app com.huawei.systemmanager
```

Empty app name is rejected with exit code 1:
```
Error: app_name cannot be empty
```

### current-app

Get the identifier of the currently foreground app.

```bash
devicebase -s <serial> current-app
```

**Workflow:**
```bash
# Launch and verify
devicebase -s <serial> launch-app com.android.settings
sleep 1
devicebase -s <serial> current-app
# Output: com.android.settings

# Conditional action
CURRENT=$(devicebase -s <serial> current-app)
echo "Current app: $CURRENT"
```

---

## Text Input

### input

Type text into the currently focused text field. The device must have a text field focused (tap it first).

```bash
devicebase -s <serial> input "Hello World"
```

Quote text containing spaces or special characters:
```bash
devicebase -s <serial> input "user@example.com"
devicebase -s <serial> input "Password123!"
```

### clear-text

Clear all text in the focused text field.

```bash
devicebase -s <serial> clear-text
```

**Workflow:**
```bash
# Fill a search field
devicebase -s <serial> tap 540,100      # tap search box
devicebase -s <serial> input "android"  # type query
devicebase -s <serial> tap 540,200      # tap search button

# Correct a typo
devicebase -s <serial> input "hello"
devicebase -s <serial> clear-text
devicebase -s <serial> input "world"

# Login form
devicebase -s <serial> tap 540,400
devicebase -s <serial> input "myuser"
devicebase -s <serial> tap 540,600
devicebase -s <serial> input "mypassword"
devicebase -s <serial> tap 900,750
```

---

## Device Information

### device-info

Retrieve device information: status, hardware, connection state, OS version, screen resolution, battery, etc.

```bash
devicebase -s <serial> device-info
```

### dump-hierarchy

Dump the current UI accessibility tree as JSON. Returns nodes with attributes like `resource-id`, `text`, `class`, `bounds`, `clickable`, `enabled`.

```bash
devicebase -s <serial> dump-hierarchy
```

**Use cases:**
- Inspect UI layout to find element coordinates
- Verify UI state after interactions
- Build selectors for automation

### screenshot

Capture the device screen as an image.

```bash
# Save to file
devicebase -s <serial> screenshot -o screen.png

# Output to stdout (for piping)
devicebase -s <serial> screenshot > screen.png

# Output to stdout (for base64)
devicebase -s <serial> screenshot | base64
```

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--output` | `-o` | stdout | Output file path. |

**Workflow:**
```bash
# Capture state for analysis
devicebase -s <serial> screenshot -o /tmp/state.png

# Find a button's coordinates from hierarchy
devicebase -s <serial> dump-hierarchy | jq '.nodes[] | select(.text == "Submit") | .bounds'

# Full inspection pipeline
devicebase -s <serial> screenshot -o /tmp/screen.png
devicebase -s <serial> dump-hierarchy > /tmp/hierarchy.json
devicebase -s <serial> device-info > /tmp/device.json
```

---

## AI Agent Integration

### Sequential Actions

```bash
devicebase -s <serial> launch-app com.android.settings
sleep 2
devicebase -s <serial> tap 540,500
sleep 1
devicebase -s <serial> input "Wi-Fi"
```

### Conditional Execution

```bash
CURRENT=$(devicebase -s <serial> current-app)
if [ "$CURRENT" = "com.android.settings" ]; then
    devicebase -s <serial> back
else
    devicebase -s <serial> launch-app com.android.settings
fi
```

### Hierarchy-Driven Navigation

```bash
# Find and tap a button from the hierarchy
devicebase -s <serial> dump-hierarchy | jq -r '
  .nodes[]
  | select(.text == "Continue" and .enabled == true)
  | .bounds
' | while read -r bounds; do
  # Parse bounds [x,y][x,y] and tap center
  devicebase -s <serial> tap 540,960
done
```

### Multi-Device Orchestration

```bash
# Control multiple devices in parallel
devicebase -s device1_serial tap 100,200 &
devicebase -s device2_serial tap 300,400 &
devicebase -s device3_serial tap 500,600 &
wait
```

### Error-Aware Execution

```bash
if devicebase -s <serial> launch-app com.example.app; then
    echo "App launched successfully"
else
    echo "Failed to launch app"
    devicebase -s <serial> screenshot -o /tmp/error.png
    exit 1
fi
```

---

## Error Reference

### CLI Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `required flag(s) "--serial" not set` | Missing `-s` | Add `-s <serial>` |
| `invalid point format "x y", expected x,y` | Wrong separator | Use comma: `100,200` |
| `invalid bounds format "...", expected x1,y1,x2,y2` | Wrong format | Use 4 comma-separated ints |
| `app_name cannot be empty` | Empty string to `launch-app` | Provide valid package/bundle ID |
| `unknown command` | Typo in subcommand | Check command name |

### Environment Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `DEVICEBASE_BASE_URL environment variable is not set` | Missing base URL | Export `DEVICEBASE_BASE_URL` |
| `DEVICEBASE_API_KEY environment variable is not set` | Missing API key | Export `DEVICEBASE_API_KEY` |
| `API error (HTTP 401): ...` | Invalid/missing API key | Check `DEVICEBASE_API_KEY` |
| `API error (HTTP 404): ...` | Device not found | Verify serial number and device connection |
| `API error (HTTP 500): ...` | Server error | Check Devicebase server logs |
| `request failed: connection refused` | Server unreachable | Verify `DEVICEBASE_BASE_URL` and server is running |

---

## Critical Rules

1. **Always use `-s <serial>`** — every command requires the device serial.
2. **Set both environment variables** — `DEVICEBASE_BASE_URL` and `DEVICEBASE_API_KEY` before running.
3. **Use comma-separated coordinates** — `100,200`, NOT `100 200`.
4. **Quote text with spaces** — `input "Hello World"`.
5. **Screenshot defaults to stdout** — use `-o file` to save to a file.
6. **Exit code 1 on any error** — both bad input and API failures cause non-zero exit.
