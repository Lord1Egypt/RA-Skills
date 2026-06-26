---
name: Control USB Relay
slug: control-usb-relay
version: 1.0.2
description: Control USB relay modules with on/off switching, state tracking, and automation support.
metadata: {"clawdbot":{"emoji":"🔌","requires":{"bins":["python3"]},"os":["linux"]}}
---

## When to Use

User wants to control a USB relay module to switch devices on/off or automate based on sensor input.

## Core Rules

1. **Verify Hardware First** — Confirm relay is at `/dev/ttyUSB1` and user is in `dialout` group.

2. **Always Initialize** — Call `relay.connect()` before any control. Wait 500ms for connection.

3. **Use Correct Protocol** — ON: `A0 01 01 A2`, OFF: `A0 01 00 A1`. Different modules may use different protocols.

4. **State May Drift** — `get_status()` tracks last command. May differ if manual override occurred.

5. **Disconnect on Exit** — Always call `relay.disconnect()` to release serial port.

## Data Storage

No persistent storage. Relay state tracked in memory during session only.

## External Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/dev/ttyUSB1` | Serial control |

## Quick Reference

| Topic | File |
|-------|------|
| Setup & examples | `setup.md` |
| Troubleshooting | `setup.md` |

## Security Notes

- Physical device control — confirm with user before switching
- Some relays need external 5V/12V power supply
