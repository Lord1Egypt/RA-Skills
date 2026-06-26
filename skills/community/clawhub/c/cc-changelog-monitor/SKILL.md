---
name: cc-changelog-monitor
description: Monitor Claude Code releases and get Telegram alerts when new versions ship. Zero AI credits — pure bash monitoring.
---

# cc-changelog-monitor

Monitors `@anthropic-ai/claude-code` on npm and sends Telegram alerts when a new version is detected, including a diff summary of what changed between versions.

**Zero AI credits used during monitoring** — pure bash + curl + jq.

## Quick Start

### 1. Setup (one-time)

```bash
bash ~/clawd/skills/cc-changelog-monitor/scripts/setup.sh
```

This will:
- Auto-detect your Telegram bot token from OpenClaw config
- Ask for your Telegram chat ID (defaults to your personal ID)
- Initialize the version tracker at the current Claude Code version
- Make scripts executable

### 2. Manual run

```bash
bash ~/clawd/skills/cc-changelog-monitor/scripts/monitor.sh
```

Output when no new version:
```
✓ Claude Code is at v2.1.69 — no change.
```

Output when new version detected:
```
🔔 New version detected: v2.1.69 → v2.1.70
📦 Downloading @anthropic-ai/claude-code@2.1.70...
✅ Telegram alert sent!
✅ Saved v2.1.70 as current version.
```

### 3. Add to OpenClaw Cron

See `cron-payload.md` for the exact payload to set up automatic monitoring every 2 hours.

## How It Works

1. **Polls npm registry** — `curl https://registry.npmjs.org/@anthropic-ai/claude-code/latest`
2. **Compares** with `~/.cc-changelog-version` (stored version)
3. **If new version**: downloads the tarball, extracts it, diffs against previous
4. **Sends Telegram alert** with version info + diff summary
5. **Saves new version** to disk

## Config

Credentials stored in `~/.cc-changelog-config`:

```bash
TELEGRAM_BOT_TOKEN="your-bot-token"
TELEGRAM_CHAT_ID="your-chat-id"
```

## Files Created by Monitor

- `~/.cc-changelog-version` — tracks the last seen version
- `~/.cc-changelog-config` — Telegram credentials
- `~/clawd/projects/cc-changelog/{version}/` — extracted npm packages for diffing

## Force Test Alert

```bash
# Reset version to trigger an alert
echo "0.0.0" > ~/.cc-changelog-version
bash ~/clawd/skills/cc-changelog-monitor/scripts/monitor.sh
```

## Skill Invocation (from OpenClaw chat)

You can ask OpenClaw to run the monitor manually:

> "Check if there's a new Claude Code version"

OpenClaw will run `monitor.sh` and report the result.
