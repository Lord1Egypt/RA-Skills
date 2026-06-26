---
name: discord-roster
description: "Query Discord guild members, list bots, get channel and role info via REST API. Use when: listing server members, checking who's a bot, viewing channel permissions, inspecting guild roles, or auditing a Discord server's roster."
metadata: { "openclaw": { "emoji": "📋", "requires": { "config": ["channels.discord.token"] } } }
allowed-tools: ["exec"]
---

# Discord Roster

Inspect Discord guilds: members, bots, channels, roles. Read-only queries via REST API.

## Setup

The script `scripts/discord-roster.sh` handles everything. It reads the bot token from `~/.openclaw/openclaw.json` and auto-detects proxy settings.

## Usage

```bash
bash skills/discord-roster/scripts/discord-roster.sh <command> [args...]
```

### Commands

**List guild members** (most common):

```bash
# All members
bash skills/discord-roster/scripts/discord-roster.sh members <guild_id>

# Bots only
bash skills/discord-roster/scripts/discord-roster.sh members <guild_id> --bots

# Humans only
bash skills/discord-roster/scripts/discord-roster.sh members <guild_id> --humans
```

**Get channel info**:

```bash
bash skills/discord-roster/scripts/discord-roster.sh channel <channel_id>
```

**List guild channels**:

```bash
bash skills/discord-roster/scripts/discord-roster.sh channels <guild_id>
```

**List guild roles**:

```bash
bash skills/discord-roster/scripts/discord-roster.sh roles <guild_id>
```

**Look up which guild a channel belongs to**:

```bash
bash skills/discord-roster/scripts/discord-roster.sh guild-of <channel_id>
```

## Output

All commands output clean, tab-separated text for easy parsing. Example for `members`:

```
TYPE    USERNAME        DISPLAY_NAME    ID                  JOINED_AT           ROLES
BOT     my-bot          —               1234567890123456789 2026-01-15T10:30    9876543210987654321
BOT     helper-bot      —               2345678901234567890 2026-01-15T10:31    —
HUMAN   johndoe         John            3456789012345678901 2026-01-15T10:25    —
```

## Proxy

The script checks for proxy in this order:
1. `channels.discord.proxy` in openclaw.json
2. `HTTPS_PROXY` / `https_proxy` env var
3. Direct connection (no proxy)

## Troubleshooting

- **403 Forbidden**: Bot lacks `SERVER MEMBERS INTENT` — enable in Discord Developer Portal > Bot > Privileged Gateway Intents.
- **Unknown Guild**: Bot isn't in that guild. Invite it first.
- **Connection timeout**: Check proxy settings. Discord requires external network access.
