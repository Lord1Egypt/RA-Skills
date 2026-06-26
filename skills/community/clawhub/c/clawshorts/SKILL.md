---
name: clawshorts
description: Block YouTube Shorts on Fire TV. Use when asked to check, manage, or configure YouTube Shorts limiting on Buck's Fire TV devices. Triggers on requests like "check shorts quota", "reset shorts", "shorts status", "how much shorts watched today", "stop shorts limiter", "start shorts limiter".
metadata: { "openclaw": { "requires": { "bins": ["adb", "python3"] } } }
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
| `list` | List all configured devices with per-device config |
| `setup <IP> [NAME]` | First-time setup for a new device |
| `add <IP> [NAME]` | Add another Fire TV |
| `connect <IP>` | Connect ADB to device + auto-detect screen |
| `enable <IP>` / `disable <IP>` | Enable/disable a device |
| `config [show\|get\|set\|reset]` | View/set global or per-device config |
| `detect <IP>` | Re-detect screen resolution via ADB, update DB |

## Detection Logic

Detection requires **both** conditions to be true simultaneously:
1. Player width < **30%** of screen width (configurable per-device)
2. Aspect ratio < **1.3** (portrait — distinguishes Shorts from 16:9 landscape previews)

- Poll interval: 3 seconds via ADB
- Shorts: ~32% screen width, 9:16 portrait (ar ~0.56)
- Regular video: ~100% screen width, 16:9 landscape (ar ~1.78)
- Home/browse: no video active
- Only actual Shorts playback counts toward limit

## Configuration

All detection parameters are stored in SQLite with global defaults and per-device overrides.

**Global defaults** (`shorts config`):
| key | default | description |
|-----|---------|-------------|
| `shorts_width_threshold` | 0.30 | player width must be < this ratio of screen width |
| `shorts_max_aspect_ratio` | 1.3 | portrait if ar < this value |
| `shorts_fallback_height_ratio` | 0.4 | fallback: player height must exceed this ratio of screen height |
| `shorts_delta_cap` | 300 | max seconds accumulated per poll |
| `default_screen_width` | 1920 | fallback assumed screen width |
| `default_screen_height` | 1080 | fallback assumed screen height |

**Per-device overrides** — any of the above can be set per-device in the `devices` table. NULL = use global default.

**Config commands:**
```bash
shorts config                    # show all global defaults
shorts config get <key>         # get a specific value
shorts config set <key> <value> # set global default
shorts config set <IP> <col> <value>  # set per-device override
shorts config reset <IP>        # clear per-device overrides
shorts detect <IP>              # re-detect screen via ADB
```

## Data Locations

- Database: `~/.clawshorts/clawshorts.db` (SQLite)
  - `config` — global detection defaults
  - `devices` — per-device settings (IP, name, limit, screen size, thresholds)
  - `daily_usage` — daily watch time per device
- Daemon log: `~/.clawshorts/daemon.log`
- LaunchAgent: `~/Library/LaunchAgents/com.fink.clawshorts.plist`

## Requirements

- `adb` (Android platform tools)
- Python 3
- Fire TV with ADB debugging enabled
- `shorts` symlink at `/opt/homebrew/bin/shorts` (optional)

## ⚠️ Security Notes

**ADB has no built-in authentication.** Only enable ADB Debugging on a **trusted, password-protected home network**. Never on public WiFi. Anyone on the same network with ADB enabled can connect to your Fire TV.

**This tool only accepts private IP addresses** (10.x.x.x, 172.16–31.x.x, 192.168.x.x). Public IPs are rejected to prevent accidental targeting of unrelated hosts.
