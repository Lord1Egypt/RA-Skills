# Claw Use — Device Control for AI Agents

Give your AI agent eyes, hands, and a voice on real devices.

Claw Use is a **protocol + skill** for AI agents to control physical devices over HTTP. The `cu` CLI provides a unified interface — the same commands work across any device that implements the Claw Use API.

## Supported Devices

| Platform | Implementation | Status |
|----------|---------------|--------|
| Android | [claw-use-android](https://github.com/4ier/claw-use-android) | ✅ Available |
| iOS | claw-use-ios | 🔮 Planned |
| Desktop | claw-use-desktop | 🔮 Planned |

## Prerequisites

- `cu` CLI installed (ships with claw-use-android, or install standalone)
- At least one device running a Claw Use implementation
- Device and agent on the same network (or connected via Tailscale)

## Setup

```bash
# Add a device with a friendly name
cu add redmi 192.168.0.105 <token>
cu add pixel 100.80.1.10 <token>

# List devices
cu devices
# ▸ redmi  192.168.0.105  online v1.2.0
#   pixel  100.80.1.10    offline

# Switch default
cu use pixel

# Target a specific device
cu -d redmi screenshot
```

## Core API (all platforms)

Every Claw Use implementation exposes the same HTTP endpoints:

### Perception — read the device
```bash
cu screen              # UI tree (semantic: element text, bounds, state)
cu screen -c           # compact mode (interactive elements only)
cu screenshot          # visual capture (JPEG, configurable quality)
cu notifications       # system notifications
cu status              # device health dashboard
```

### Action — control the device
```bash
cu tap <x> <y>         # tap coordinates
cu click <text>        # tap by visible text (semantic click)
cu type "text"         # type text (CJK supported)
cu swipe up|down|left|right
cu scroll up|down|left|right
cu back / cu home      # system navigation
cu launch <app>        # open an application
cu open <url>          # open URL
cu intent '<json>'     # platform-specific intent (Android)
```

### Audio
```bash
cu tts "hello"         # speak through device speaker
cu say "你好"          # alias
```

### Device State
```bash
cu wake                # wake screen
cu lock / cu unlock    # lock/unlock (PIN required for unlock)
```

## Workflow Patterns

### Navigate and interact
```bash
cu launch org.telegram.messenger
cu screen -c                        # see what's on screen
cu click "Search"
cu type "John"
cu click "John, last seen recently"
cu type "Hey!"
cu click "Send"
```

### Visual + semantic dual-channel
```bash
cu screen -c                         # semantic: what elements exist
cu screenshot 50 720 /tmp/look.jpg   # visual: what it actually looks like
```

### Multi-device orchestration
```bash
cu -d phone1 launch com.whatsapp
cu -d phone2 screenshot
cu -d tablet open "https://example.com"
```

## For Agent Developers

Claw Use is designed as a **protocol**, not just an app. To add support for a new platform:

1. Implement the [Claw Use HTTP API spec](https://github.com/4ier/claw-use-android#api-details)
2. Expose endpoints on a configurable port (default: 7333)
3. Support token auth via `X-Bridge-Token` header
4. Return JSON responses matching the documented schemas

The `cu` CLI and this skill work automatically with any compliant implementation.

## Tips

- **`cu screen -c`** is the primary perception tool — compact mode filters noise
- **`cu click`** by text is more reliable than `cu tap` when text is visible
- **`cu screenshot`** when you need visual context the UI tree can't capture
- Auto-unlock is transparent: locked devices auto-unlock before any command
- Combine with Tailscale for remote access from anywhere
