---
name: clank-daily-summary
description: Generate a daily summary of your agent's activities. Perfect for tracking progress and sharing updates.
metadata:
  openclaw:
    emoji: "📊"
---

# Clank Daily Summary

Generate a comprehensive daily summary of your agent's activities.

## Features

- **Activity Tracking** – Count commits, emails, messages
- **Progress Report** – What was accomplished today
- **Blockers Identified** – What's holding you back
- **Next Steps** – What to do tomorrow
- **Telegram Integration** – Send summary to your chat

## Usage

```bash
# Generate daily summary
clank-summary

# Generate and send to Telegram
clank-summary --send

# Generate for specific date
clank-summary --date 2026-03-28
```

## Installation

```bash
clawhub install clank-daily-summary
```

## Requirements

- OpenClaw with cron support
- Git (for commit tracking)
- Telegram bot (optional, for sending)

## License

MIT
