---
name: email-monitor
description: Monitor email inboxes for important messages and get alerts. Works with AgentMail, Gmail, and any IMAP inbox.
metadata:
  openclaw:
    emoji: "📧"
---

# Email Monitor Skill

Monitor your email inboxes and get alerts for important messages.

## Features

- **Multi-Inbox Support** – Monitor multiple email addresses
- **Keyword Alerts** – Get notified when specific keywords appear
- **Priority Detection** – Automatically prioritize important emails
- **Digest Mode** – Daily/weekly email summaries
- **Auto-Reply** – Optional automatic responses for urgent messages

## Usage

```bash
# Check inbox for new messages
email-monitor check

# Set up keyword alerts
email-monitor alert add "urgent" "invoice" "deadline"

# Generate daily digest
email-monitor digest --daily

# Monitor in background (cron)
email-monitor watch --interval 5m
```

## Installation

```bash
clawhub install email-monitor
```

## Configuration

Create `~/.email-monitor/config.json`:

```json
{
  "inboxes": [
    {
      "name": "work",
      "provider": "agentmail",
      "api_key": "your_key",
      "inbox_id": "you@agentmail.to"
    }
  ],
  "alerts": {
    "keywords": ["urgent", "invoice", "deadline"],
    "notify": ["telegram", "email"]
  },
  "digest": {
    "enabled": true,
    "time": "08:00",
    "timezone": "UTC"
  }
}
```

## Requirements

- Node.js >= 20
- AgentMail API key OR IMAP credentials
- OpenClaw (for notifications)

## License

MIT
