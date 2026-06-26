---
name: device-heartbeat
description: "Monitor remote device online status via heartbeat pings to healthchecks.io. Use when user asks to check if a device is online or offline, user reports device unreachable or no response from remote OpenClaw, user wants to set up device monitoring or heartbeat, user asks about network connectivity of their devices, or user says ping my device or is my Mac online."
---

# Device Heartbeat Monitor

Monitor device online status using heartbeat pings to healthchecks.io (free tier).

## Architecture

```
Device → every N min → curl GET → healthchecks.io → missed? → alert user
User asks "device online?" → agent reads state file or queries API → answer
```

## Security Warning

Never share the full ping URL (`https://hc-ping.com/UUID`) in any chat message. Messaging platforms (Feishu, Slack, etc.) auto-fetch URLs for link previews, which creates false heartbeat pings. Only pass the UUID portion separately.

## Quick Commands

Check local status (no API key needed):
```bash
bash scripts/status.sh
```

View recent logs:
```bash
tail -20 ~/.openclaw/logs/heartbeat.log
```

Read state file directly:
```bash
cat ~/.openclaw/logs/heartbeat-state.json
```

## Setup

### 1. Create a Check on healthchecks.io

Register at https://healthchecks.io, create a Check. Set Period = 3 min, Grace = 5 min. See `references/healthchecks-setup.md` for details.

### 2. Install heartbeat service

```bash
bash scripts/setup.sh "https://hc-ping.com/UUID" 180
```

- Arg 1: Full ping URL
- Arg 2: Interval in seconds (default 180 = 3 min)
- Installs as macOS LaunchAgent (auto-start on boot, auto-restart on crash)
- Low priority background process, minimal CPU/battery

### 3. Verify

```bash
bash scripts/status.sh
```

## Remote Status Check (from another device)

```bash
bash scripts/check.sh "READONLY_API_KEY" "CHECK_UUID"
```

Response fields: `status` (up/down/grace), `last_ping` (timestamp).

## Multi-Device Setup

Create a separate Check per device on healthchecks.io. Each device gets its own UUID. Run `setup.sh` on each device with its unique URL.

## Uninstall

```bash
bash scripts/uninstall.sh
```

## Features

- **Log rotation**: Auto-truncates at 500 lines
- **State file**: `~/.openclaw/logs/heartbeat-state.json` for quick local queries
- **Recovery detection**: Logs "RECOVERED after N failures" on reconnect
- **Fail counter**: Tracks consecutive failures in state file

## Troubleshooting

- **Service not running**: `bash scripts/setup.sh "URL" 180` to reinstall
- **Ping failing**: Check network; verify URL with `curl -v "URL"`
- **Logs**: `~/.openclaw/logs/heartbeat.log` and `heartbeat-error.log`
- **False pings from chat platforms**: Regenerate UUID, never share full URL in chat
