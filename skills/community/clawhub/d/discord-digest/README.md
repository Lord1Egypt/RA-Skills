# 🎮 Discord Digest — OpenClaw Skill

Generate formatted digests from Discord servers. Reads messages from selected channels/threads via user token and creates concise summaries with direct links.

**No external dependencies** — uses only Python 3 stdlib.

![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)
![Python](https://img.shields.io/badge/Python-3.10+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 🔐 **User Token Auth** — no bot needed, works on any server you're a member of
- 🏠 **Multi-Server Support** — configure multiple servers with per-server channel selection
- 📋 **Interactive Setup** — scan servers → pick channels → save config
- ✅ **Token Validation** — auto-check before each run, notify on expiry
- 📝 **Formatted Output** — clean digest with post links, titles, summaries, and source links
- ⏰ **Cron Ready** — designed for daily automated digests via OpenClaw cron
- 📦 **Zero Dependencies** — Python 3 stdlib only (`urllib`, `json`)

## 📦 Installation

### Via ClawHub (recommended)

```bash
clawhub install discord-digest
```

### Manual

```bash
git clone https://github.com/NikolayBohdanov/discord-digest.git
cp -r discord-digest ~/.openclaw/workspace/skills/
```

## 🚀 Quick Start

### 1. Get Your Discord User Token

1. Open Discord in browser → Press `F12`
2. Go to **Network** tab → click any request to `discord.com/api`
3. Find **Authorization** header → copy the value

### 2. Save Token

```bash
python3 scripts/config_manager.py set-token "YOUR_TOKEN_HERE"
```

### 3. Browse Your Servers

```bash
python3 scripts/discord_api.py "YOUR_TOKEN" guilds
```

### 4. Browse Channels

```bash
python3 scripts/discord_api.py "YOUR_TOKEN" channels SERVER_ID
```

### 5. Add Server to Config

```bash
python3 scripts/config_manager.py add-server '{
  "id": "SERVER_ID",
  "name": "My Server",
  "channels": [
    {"id": "CHANNEL_ID", "name": "general", "type": "text"},
    {"id": "CHANNEL_ID", "name": "announcements", "type": "text"}
  ]
}'
```

### 6. Generate Digest

```bash
python3 scripts/run_digest.py --hours 24
```

## 📄 Output Format

```
**#SERVER_NAME DD.MM.YY**

**[→post](message_url) | 📝 channel-name**
**Post Title Here**
**Details:** Brief 1-sentence summary of the post content...
**Links:** [source 1](url) | [source 2](url)
```

## ⏰ Cron Setup (OpenClaw)

Add to your OpenClaw cron for daily automated digests:

```json
{
  "name": "Discord Digest",
  "schedule": {"kind": "cron", "expr": "0 21 * * *", "tz": "Europe/Kiev"},
  "payload": {
    "kind": "agentTurn",
    "message": "Run: cd ~/.openclaw/workspace/skills/discord-digest && python3 scripts/run_digest.py --hours 24. Send the output to Telegram.",
    "timeoutSeconds": 120
  },
  "sessionTarget": "isolated"
}
```

## 📁 Project Structure

```
discord-digest/
├── SKILL.md                 # OpenClaw skill manifest
├── README.md                # This file
├── LICENSE                  # MIT License
├── .gitignore
└── scripts/
    ├── discord_api.py       # Discord HTTP API client (user token)
    ├── digest_formatter.py  # Message → formatted digest
    ├── config_manager.py    # Token & server config management
    ├── run_digest.py        # Main entry point
    └── setup.sh             # Setup verification
```

## 🔧 Scripts Reference

| Script | Purpose | Usage |
|--------|---------|-------|
| `discord_api.py` | Discord API client | `python3 discord_api.py TOKEN validate\|guilds\|channels\|messages` |
| `digest_formatter.py` | Format messages | `python3 digest_formatter.py input.json "Server" server_id` |
| `config_manager.py` | Manage config | `python3 config_manager.py get\|set-token\|add-server\|list-servers` |
| `run_digest.py` | Generate digest | `python3 run_digest.py [--hours 24] [--server ID]` |

## ⚙️ Configuration

Config is stored at `~/.openclaw/workspace/config/discord-digest.json`:

```json
{
  "discord_token": "YOUR_TOKEN",
  "servers": [
    {
      "id": "829331298878750771",
      "name": "My Server",
      "channels": [
        {"id": "123456789", "name": "general", "type": "text"}
      ]
    }
  ],
  "digest_period_hours": 24
}
```

Override config directory with `DISCORD_DIGEST_CONFIG_DIR` env variable.

## ⚠️ Important Notes

- **User tokens** may violate Discord ToS — use at your own risk for personal use only
- Discord user tokens can expire — the skill validates before each run
- Rate limits are handled automatically (1 req/sec with retry on 429)
- No messages are sent or modified — **read-only access**

## 🤝 Contributing

PRs welcome! Please ensure:
- No hardcoded tokens or personal data
- Python 3.10+ compatibility
- No external dependencies

## 📝 License

MIT — see [LICENSE](LICENSE)
