---
name: daily-briefing
description: Generate a consolidated daily briefing with weather, calendar events, tasks, news, and market data. Use when the user asks for a morning briefing, daily update, daily digest, agenda summary, "what's happening today", or "give me my briefing". Also useful for scheduled morning check-ins via cron.
---

# Daily Briefing

Generate a consolidated morning briefing from multiple data sources.

## Quick Start

```bash
python3 scripts/briefing.py              # full briefing
python3 scripts/briefing.py --weather    # weather only
python3 scripts/briefing.py --news       # news only
python3 scripts/briefing.py --crypto     # crypto prices only
python3 scripts/briefing.py --short      # compact one-liner version
```

## Sections

| Section | Source | Content |
|---------|--------|---------|
| 🌤️ Weather | wttr.in | Current conditions + 3-day forecast |
| 📰 News | Google News RSS | Top headlines by region/topic |
| 📈 Markets | Yahoo Finance | BTC, ETH, major indices, forex |
| 📋 Tasks | Local file | Pending tasks from tasks.json |
| 🎂 Events | Local file | Today's events from events.json |

## Configuration

Edit `~/.briefing/config.json`:

```json
{
  "location": "Dhaka, Bangladesh",
  "news_topics": ["technology", "business"],
  "news_region": "BD",
  "crypto": ["BTC-USD", "ETH-USD", "SOL-USD"],
  "stocks": ["SPY", "QQQ", "AAPL"],
  "forex": ["EURUSD=X", "GBPUSD=X"],
  "timezone": "Asia/Dhaka"
}
```

## Tasks File

Add tasks to `~/.briefing/tasks.json`:

```json
[
  {"task": "Submit project report", "due": "2026-03-31", "priority": "high"},
  {"task": "Call dentist", "due": "2026-04-01", "priority": "medium"}
]
```

## Cron Integration

Schedule daily briefing with OpenClaw cron:
```
Schedule: 0 8 * * * (8:00 AM daily)
Command: python3 scripts/briefing.py --short
```

## Output Modes

- **Default**: Full formatted briefing with all sections
- **--short**: Compact single-message version (good for chat delivery)
- **--json**: Machine-readable JSON output
- **--section**: Only specific section (weather/news/crypto/tasks)
