# 17TRACK Skill for Claude Code

Track parcels and shipments via the [17TRACK](https://www.17track.net/) API directly from Claude Code. Local SQLite database, automatic status polling, webhook ingestion, and daily reports with auto-cleanup of delivered packages.

## Installation

```bash
clawhub install 17track
```

## Configuration

Get your API token from [17TRACK API](https://api.17track.net/) and add it to `~/.clawdbot/clawdbot.json`:

```json
{
  "skills": {
    "entries": {
      "17track": {
        "enabled": true,
        "apiKey": "YOUR_17TRACK_TOKEN"
      }
    }
  }
}
```

## What it does

Once installed, Claude Code can:

- **Add packages** — "track RR123456789CN, it's my new headphones"
- **Check status** — "where is my package?" / "any updates on my orders?"
- **Sync updates** — polls 17TRACK API for latest tracking events
- **Auto-cleanup** — delivered packages are automatically removed by daily reports
- **Webhook support** — optional real-time push updates from 17TRACK

## Features

- Zero external dependencies (Python 3 stdlib only)
- Local SQLite database for offline access
- Supports 1000+ carriers via 17TRACK
- Daily report script for scheduled automation (WhatsApp, email, etc.)
- Webhook server + payload ingestion

## License

MIT
