---
name: dokidoki
description: Control interactive BLE devices (scan/connect/playback/timeline) from terminal.
metadata: {"clawdbot":{"emoji":"🎮","requires":{"bins":["doki"]},"install":[{"id":"npm","kind":"npm","package":"@tryjoy/dokidoki","global":true,"bins":["doki"],"label":"Install dokidoki (npm)"}],"label":"dokidoki"}}

---

# DokiDoki CLI

Use `doki` to control interactive BLE devices from the terminal.

## Quick Start

- `doki scan` - Scan for BLE devices (auto-starts daemon)
- `doki connect DK-META2` - Connect to device (auto-starts daemon)

## Common Tasks

### Daemon Management
- `doki start` - Start background daemon
- `doki stop` - Stop background daemon
- `doki status` - Check daemon and connection status

### Device Connection
- `doki scan` - Scan for BLE devices
- `doki connect [name]` - Connect to device (default: DK-META2)
- `doki disconnect` - Disconnect from device

### Timeline Playback
- `doki player play [audio] <timeline.json>` - Play timeline with optional audio sync
- `doki player pause` - Pause playback (stops device)
- `doki player resume` - Resume playback

### Direct Device Control
- `doki action linear 50` - Set linear to 50%
- `doki action rotary -30` - Set rotary to -30 (reverse)
- `doki action vibration 80` - Set vibration to 80%
- `doki action pause` - Immediately stop all device actions

## Timeline Format

Timeline files are JSON files defining device actions at specific timestamps:

```json
{
  "duration": 180.5,
  "actions": [
    {"timestamp": 0.0, "type": "VIBRATION", "value": 50},
    {"timestamp": 5.5, "type": "LINEAR", "value": 30},
    {"timestamp": 10.0, "type": "ROTARY", "value": -50}
  ]
}
```

### Action Types

| Type | Value Range | Description |
|------|-------------|-------------|
| `LINEAR` | 0-100 | Linear/stroke motion intensity |
| `ROTARY` | -100 to 100 | Rotation speed (negative=reverse) |
| `VIBRATION` | 0-100 | Vibration intensity |

## Notes

- Requires Node.js 18+ and Bluetooth Low Energy (BLE) support
- Supported audio formats: MP3, AAC/M4A, WAV, FLAC, OGG, AIFF
- Audio playback requires `ffplay` (Linux/Windows) or `afplay` (macOS)
- Logs are written to `/tmp/dokidoki.log`
