---
name: clawshorts
description: Block YouTube Shorts on Fire TV. Use when asked to check, manage, or configure YouTube Shorts limiting on Buck's Fire TV devices. Triggers on requests like "check shorts quota", "reset shorts", "shorts status", "how much shorts watched today", "stop shorts limiter", "start shorts limiter".
---

# ClawShorts

YouTube Shorts limiter for Fire TV. Monitors watch time per device and auto-blocks when daily limit is reached.

## Invocation

**Primary entry point:**
```bash
~/.openclaw/workspace/skills/clawshorts/scripts/clawshorts.sh <command>
```

## Commands

| Command | When to use |
|---------|-------------|
| `status` | Check today's usage, remaining quota, daemon health |
| `reset [IP]` | Reset today's counter (all devices or specific IP) |
| `start` | Start the daemon if not running |
| `stop` | Stop the daemon |
| `history [days]` | Show watch history (default 30 days) |
| `logs [N]` | Show last N daemon log lines (default 50) |
| `list` | List all configured devices |
| `setup <IP> [NAME]` | First-time setup for a new device |
| `add <IP> [NAME]` | Add another Fire TV |
| `connect <IP>` | Connect ADB to device |
| `enable <IP>` / `disable <IP>` | Enable/disable a device |

## Detection Logic

- Poll interval: 3 seconds via ADB
- Shorts: ~45% screen width (portrait aspect)
- Regular video: ~100% screen width
- Home/browse: no video active
- Only actual Shorts playback counts toward limit

## Data Locations

- Device config + history: `~/.clawshorts/clawshorts.db` (SQLite)
- Daemon log: `~/.clawshorts/daemon.log`
- LaunchAgent: `~/Library/LaunchAgents/com.fink.clawshorts.plist`

## Requirements

- `adb` (Android platform tools)
- Python 3
- Fire TV with ADB debugging enabled
- `shorts` symlink at `/opt/homebrew/bin/shorts`
