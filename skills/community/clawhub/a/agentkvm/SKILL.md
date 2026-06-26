---
name: agentkvm
description: Control physical devices (phones, PCs, Macs) through NanoKVM-USB hardware. Use this skill whenever the user asks you to interact with a physical screen, take screenshots of a connected device, click/type/scroll on a remote machine, automate a GUI workflow on real hardware, or implement a "computer use" loop that observes a screen and takes actions. Also trigger when you see AgentKVM in the project, references to NanoKVM-USB, or when the user says things like "click the button on my phone", "what's on the screen", "open Settings on the device", "type my password on the PC", or "automate this on the connected machine".
compatibility: Requires agentkvm CLI (npm install -g agentkvm), Node.js >= 18, ffmpeg, and NanoKVM-USB hardware connected via USB.
---

## Requirements

Before using AgentKVM, ensure the following are installed and available:

- **AgentKVM CLI** — `npm install -g agentkvm`
- **Node.js** >= 18
- **ffmpeg** — required for screenshot capture (`brew install ffmpeg` on macOS, `apt install ffmpeg` on Linux)
- **NanoKVM-USB** hardware connected to the host machine via USB
- **HDMI input** from the target device connected to the NanoKVM-USB

Run `agentkvm status` to verify everything is set up correctly. If the CLI is not found, install it first. If the device is not detected, check `agentkvm list` for available serial ports.

# AgentKVM — AI-Driven Device Control

AgentKVM lets you see and operate physical devices (iPhones, Android phones, PCs, Macs, Linux machines) connected via NanoKVM-USB hardware. You take screenshots to observe the screen, then send mouse clicks, keyboard input, and scrolls to interact — just like a human sitting in front of the device.

## Core Loop

Every interaction with a physical device follows the same pattern:

```
Screenshot → Analyze → Act → Verify
```

1. **Screenshot** — capture what's currently on screen
2. **Analyze** — look at the image to understand the UI state
3. **Act** — click, type, scroll, or drag based on what you see
4. **Verify** — take another screenshot to confirm the action worked

This loop is your fundamental building block. Chain multiple iterations to accomplish complex tasks.

## Quick Start

### Check connection

```bash
agentkvm --json status
```

If this fails, the device isn't connected. Check the serial port with `agentkvm list`.

### See the screen

```bash
agentkvm --json screenshot
```

Returns `{ "path": "/path/to/screenshot.png", ... }`. Read the image to see what's on screen.

### Interact

```bash
# Click at pixel coordinates (relative to the cropped image)
agentkvm mouse click 223 485

# Type text
agentkvm type "hello world"

# Press key combos
agentkvm key enter
agentkvm key ctrl+c
agentkvm key cmd+space

# Scroll (positive = up, negative = down)
agentkvm mouse scroll 300 500 --delta -3

# Drag from point A to point B
agentkvm mouse drag 100 200 400 600
```

### Remote operation

If AgentKVM is running on another machine, all commands work identically with `--remote`:

```bash
agentkvm --remote http://192.168.1.100:7070 --token my-secret screenshot --json
agentkvm --remote http://192.168.1.100:7070 --token my-secret mouse click 223 485
```

Or use the HTTP API directly — see `references/api.md`.

## How Coordinates Work

This is critical to get right. When you analyze a screenshot and identify a UI element at pixel `(x, y)`, those coordinates are **relative to the screenshot image itself** — top-left is `(0, 0)`. Pass these coordinates directly to `agentkvm mouse click x y`.

AgentKVM handles the translation to the actual hardware coordinates internally, based on the device type and crop settings. You don't need to do any math.

### Two coordinate modes

The device type determines how coordinates are translated:

**"device" mode** (iPhone, Android) — The cropped region IS the device's full screen. HID absolute coordinates 0–4096 map to the device's own display. Use this when the HDMI output shows the device screen within a larger capture frame.

**"frame" mode** (PC, Mac, Linux) — The cropped region is just a visual focus area; HID coordinates still map to the full monitor. Use this when you're controlling a computer where the capture resolution matches the target display.

The mode is selected automatically from the config. You rarely need to think about it.

## Implementing a Task

When asked to perform a GUI task (e.g., "open Safari and search for X"):

### Step 1: Observe first

Always start with a screenshot. Never assume what's on screen.

```bash
agentkvm --json screenshot
```

Read the returned image file. Describe what you see — this grounds your actions in reality.

### Step 2: Plan your actions

Break the task into individual interactions. For "open Safari and search for X":
1. Find the Safari icon → click it
2. Wait for Safari to load → screenshot to verify
3. Find the address bar → click it
4. Type the search query
5. Press Enter
6. Screenshot to verify results

### Step 3: Execute with verification

After each significant action, take a screenshot to verify it worked. Screens can be slow to update, so add brief waits between actions when needed (use `sleep` in your script).

Common pattern in a bash script:

```bash
# Click Safari icon at the observed position
agentkvm mouse click 223 950
sleep 1

# Verify it opened
agentkvm --json screenshot
# (read and analyze the screenshot)

# Click address bar
agentkvm mouse click 300 50
sleep 0.3

# Type search query
agentkvm type "weather today"
agentkvm key enter
sleep 2

# Verify search results loaded
agentkvm --json screenshot
```

### Step 4: Handle failures

If an action didn't produce the expected result:
- The element might have moved — take a fresh screenshot and re-locate it
- The screen might not have updated yet — wait and retry
- You might have clicked the wrong spot — re-analyze and adjust coordinates

## Config Reference

All settings live in `~/.config/agentkvm/config.json`. A typical setup:

```json
{
  "serialPort": "/dev/tty.usbserial-2140",
  "resolution": { "width": 1920, "height": 1080 },
  "videoDevice": "USB3 Video",
  "deviceType": "iphone",
  "crop": { "x": 738, "y": 55, "width": 447, "height": 970 }
}
```

Key fields:
- `serialPort` — path to the NanoKVM-USB serial device
- `resolution` — HDMI capture resolution
- `videoDevice` — video capture device name or index
- `deviceType` — determines coordinate mode (`iphone`/`android` = device, `pc`/`mac`/`linux` = frame)
- `crop` — sub-region of the capture frame to use as the working area

When config is set, you can run bare commands without flags: `agentkvm screenshot`, `agentkvm mouse click 100 200`, etc.

## Tips for Reliable Automation

**Prefer clicking on text labels** over icons — text is easier to locate precisely in screenshots.

**Use `--json` for programmatic access** — all commands support it and return structured data you can parse.

**Double-click when single-click doesn't respond** — some UI elements need `--double`.

**Scroll in small increments** — `--delta 1` or `--delta -1` is one scroll step. Use multiple steps with verification screenshots in between.

**Type slowly for unreliable connections** — increase `--delay` (default 50ms) if characters get dropped.

**Use key combos for navigation** — `cmd+space` (Spotlight), `alt+tab` (window switch), `ctrl+c` (cancel) are often faster than finding and clicking UI elements.

For the full CLI reference, key combo syntax, and HTTP API details, see `references/api.md`.
