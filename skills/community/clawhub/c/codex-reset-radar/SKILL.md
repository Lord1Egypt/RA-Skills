---
name: codex-reset-radar
description: >
  Monitor Codex usage reset windows via codex-reset-radar.pages.dev.
  Polls current.json, detects window open/close, prediction level changes, and probability jumps.
  Pushes alerts via OpenClaw cron only when state changes, using the default agent chat channel.
  LLM only processes script-generated JSON diffs — minimal token burn.
user-invocable: true
allowed-tools: Bash(python3:*), Read
metadata:
  version: "1.0.4"
  author: ljd
  tags: [codex, monitoring, radar, quota, cron]
---

# Codex Reset Radar — Usage Reset Window Monitor

Monitors the [Codex Reset Radar](https://codex-reset-radar.pages.dev/) `current.json` endpoint to detect Codex usage quota reset windows ("speed windows"), pushing alerts via OpenClaw cron to the default agent chat channel.

## How It Works

```
Cron triggers
     │
     ▼
① Data collection: python3 scripts/codex-radar-check.py
   → fetch current.json + compare against local cache
     │
     ▼
② JSON diff: outputs has_changes + events[] or has_changes: false
   → no changes → agent replies NO_REPLY (silent)
     │
     ▼
③ LLM formatting: reads JSON diff only
   → formats into a friendly chat message
     │
     ▼
④ Chat push: announce → user session (default chat channel)
```

### Detection Script

`scripts/codex-radar-check.py` — stdlib only, zero dependencies:

- Fetches `https://codex-reset-radar.pages.dev/current.json`
- Compares against `cache/codex-radar-last.json` from previous run
- Creates baseline on first run

**Change types detected:**

| Event | Trigger | Output type |
|-------|---------|-------------|
| Window opened | `window_open` false→true | `window_opened` |
| Window closed | `window_open` true→false | `window_closed` |
| Status change | `status` field changed | `status_change` |
| New window | `last_window.id` changed | `new_window` |
| Prediction change | `prediction.level` changed | `prediction_change` |
| Probability jump | `prediction.probability_24h` crosses 0.1 threshold | `prediction_probability_change` |

### Output JSON Examples

No changes:
```json
{"has_changes": false}
```

Changes detected:
```json
{
  "has_changes": true,
  "events": [
    {"type": "window_opened", "detail": "Codex usage reset window opened", "opened_at": "2026-05-24T08:21:33+08:00", "scope": "Codex users"}
  ],
  "current_status": {
    "window_open": true,
    "status": "open",
    "last_window_id": "codex-speed-window-2026-05-24-codex",
    "prediction_level": "low",
    "probability_24h": 0.06
  }
}
```

## Installation

```bash
clawhub install codex-reset-radar
```

## Cron Setup

Create an OpenClaw cron job (recommended: hourly 8 AM–11 PM, silent overnight).
The delivery target will automatically use your default agent chat channel:

```json
{
  "name": "Codex Reset Radar Monitor",
  "schedule": {"kind": "cron", "expr": "0 8-23 * * *", "tz": "Asia/Shanghai"},
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "timeoutSeconds": 60,
    "lightContext": true,
    "message": "Codex Reset Radar monitor.\n1. cd ~/.openclaw/workspace && python3 skills/codex-reset-radar/scripts/codex-radar-check.py\n2. If has_changes: false, reply NO_REPLY\n3. If changes detected, format and push to default chat channel"
  }
}
```

> 💡 The cron job will push alerts to whatever chat channel your OpenClaw agent uses by default (Feishu, Discord, Telegram, etc.). No channel-specific config needed.

**Recommended schedules:**
- `0 8-23 * * *` — hourly during waking hours, silent 0-7
- `*/10 * * * *` — every 10 minutes (urgent monitoring)

## Design Principles

- **LLM only sees JSON diffs** — no raw RSS/HTML semantic analysis, minimal token usage
- **Zero-cost silence** — `has_changes: false` → agent replies `NO_REPLY` → nothing pushed to chat
- **Stdlib only** — uses `json`, `urllib`, `datetime`, `os`; zero external dependencies
- **Fault-tolerant** — network errors output `{"has_changes": false, "error": "..."}`, never false-trigger or crash
- **Channel-agnostic** — works with any chat channel (Feishu, Discord, Telegram, etc.) via OpenClaw's delivery system
