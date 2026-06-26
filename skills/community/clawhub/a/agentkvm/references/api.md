# AgentKVM API Reference

Comprehensive reference for all CLI commands, key combos, and HTTP endpoints.

## Table of Contents

1. [CLI Commands](#cli-commands)
2. [Key Combo Syntax](#key-combo-syntax)
3. [Mouse Buttons](#mouse-buttons)
4. [HTTP API](#http-api)
5. [Device Profiles](#device-profiles)

---

## CLI Commands

### Global Options

Every command accepts these:

| Flag | Description | Example |
|------|-------------|---------|
| `--port <path>` | Serial port path | `--port /dev/ttyUSB0` |
| `--resolution <WxH>` | Capture resolution | `--resolution 1920x1080` |
| `--crop <x,y,w,h>` | Crop region | `--crop 738,55,447,970` |
| `--device-type <type>` | Device type | `--device-type iphone` |
| `--remote <url>` | Remote server URL | `--remote http://192.168.1.100:7070` |
| `--token <secret>` | Auth token | `--token my-secret` |
| `--json` | JSON output | |

### list

```bash
agentkvm list [--json]
```

List available serial ports. USB ports sorted first.

### status

```bash
agentkvm status [--json]
```

Returns: `{ serialPort, connected, chipVersion, targetConnected }`

### info

```bash
agentkvm info [--json]
```

Returns: `{ chipVersion, isConnected, numLock, capsLock, scrollLock }`

### screenshot

```bash
agentkvm screenshot [--json] [--device <id>] [--output <dir>] [--list-devices]
```

- Default output: current directory, timestamped PNG
- `--json` returns `{ path, fullResolution, crop?, imageSize? }`
- `--list-devices` lists video capture devices

### type

```bash
agentkvm type <text> [--delay <ms>]
```

- Types text character by character via HID keyboard
- `--delay` controls inter-keystroke delay (default: 50ms)
- Supports all printable ASCII, auto-applies Shift for uppercase and symbols

### key

```bash
agentkvm key <combo> [--hold <ms>]
```

- `--hold` controls how long keys are held before release (default: 50ms)
- See [Key Combo Syntax](#key-combo-syntax) below

### mouse move

```bash
agentkvm mouse move <x> <y>
```

### mouse click

```bash
agentkvm mouse click <x> <y> [--button <name>] [--double]
```

- `--button`: left (default), right, middle, back, forward
- `--double`: double-click

### mouse scroll

```bash
agentkvm mouse scroll <x> <y> --delta <n>
```

- `--delta` required: positive = scroll up, negative = scroll down
- Each step is one scroll notch

### mouse drag

```bash
agentkvm mouse drag <x1> <y1> <x2> <y2> [--button <name>] [--steps <n>]
```

- `--steps`: interpolation points for smooth movement (default: 20)

### device set / list / info / add / remove

```bash
agentkvm device set <type>          # Set active device type
agentkvm device list [--json]       # List all profiles
agentkvm device info [--json]       # Show current config
agentkvm device add <name> --mode <device|frame> [--description <text>]
agentkvm device remove <name>
```

### serve

```bash
agentkvm serve [--host <addr>] [--server-port <n>] [--token <secret>]
```

Starts persistent HTTP server. Default: `0.0.0.0:7070`.

---

## Key Combo Syntax

Format: `modifier+modifier+key` (case-insensitive, `+` separated)

### Modifiers

| Name | Aliases |
|------|---------|
| Control | `ctrl`, `control` |
| Shift | `shift` |
| Alt | `alt`, `option` |
| Meta | `meta`, `win`, `cmd`, `command`, `super` |

### Common Keys

| Category | Keys |
|----------|------|
| Letters | `a`–`z` |
| Numbers | `0`–`9` |
| Function | `f1`–`f24` |
| Navigation | `up`, `down`, `left`, `right`, `home`, `end`, `pageup`, `pagedown` |
| Editing | `enter`, `backspace`, `delete`, `tab`, `space`, `insert`, `escape` |
| Symbols | `minus`, `equal`, `bracketleft`, `bracketright`, `backslash`, `semicolon`, `quote`, `backquote`, `comma`, `period`, `slash` |
| System | `printscreen`, `scrolllock`, `pause`, `capslock`, `numlock` |
| Media | `volumemute`, `volumeup`, `volumedown`, `playpause`, `stop`, `prevtrack`, `nexttrack` |

### Examples

```
enter                   # Press Enter
ctrl+c                  # Copy / interrupt
ctrl+a                  # Select all
cmd+space               # Spotlight (macOS)
alt+f4                  # Close window (Windows)
ctrl+alt+del            # Security screen (Windows)
shift+ctrl+l            # Multi-modifier combo
cmd+shift+3             # Screenshot (macOS)
```

---

## Mouse Buttons

| Name | Description |
|------|-------------|
| `left` | Primary button (default) |
| `right` | Context menu |
| `middle` | Middle/wheel button |
| `back` | Browser back |
| `forward` | Browser forward |

---

## HTTP API

Base URL: `http://<host>:<port>` (default port 7070)

Authentication: `Authorization: Bearer <token>` header (if token configured)

All POST endpoints accept JSON body, all responses are JSON `{ success: bool, data?: ..., error?: string }`.

### GET /api/status

```json
{ "connected": true, "serialPort": "/dev/ttyUSB0" }
```

### GET /api/info

```json
{ "chipVersion": "...", "isConnected": true, "numLock": false, "capsLock": false, "scrollLock": false }
```

### GET /api/screenshot

Query: `?format=image` (raw PNG) or `?format=json` (base64)

JSON response:
```json
{ "image": "base64...", "width": 447, "height": 970 }
```

### POST /api/type

```json
{ "text": "hello world", "delay": 50 }
```

### POST /api/key

```json
{ "combo": "ctrl+c", "hold": 50 }
```

### POST /api/mouse/move

```json
{ "x": 223, "y": 485 }
```

### POST /api/mouse/click

```json
{ "x": 223, "y": 485, "button": "left", "double": false }
```

### POST /api/mouse/scroll

```json
{ "x": 300, "y": 500, "delta": -3 }
```

### POST /api/mouse/drag

```json
{ "x1": 100, "y1": 200, "x2": 400, "y2": 600, "button": "left", "steps": 20 }
```

---

## Device Profiles

### Built-in

| Type | Mode | Use Case |
|------|------|----------|
| `iphone` | device | iPhone via HDMI mirror |
| `android` | device | Android via HDMI mirror |
| `pc` | frame | Windows PC |
| `mac` | frame | macOS computer |
| `linux` | frame | Linux machine |

### Coordinate Mode Behavior

**device mode**: `normalized = pixel / cropSize` → HID 0–4096 spans the device screen only

**frame mode**: `normalized = (cropOffset + pixel) / fullResolution` → HID 0–4096 spans the full monitor

### Custom Profiles

```bash
agentkvm device add steamdeck --mode device --description "Steam Deck handheld"
agentkvm device set steamdeck
```

Custom profiles are stored in `~/.config/agentkvm/config.json` under `customProfiles`.
