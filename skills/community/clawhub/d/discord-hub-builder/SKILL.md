---
name: discord-hub-builder
description: "Build a complete Discord AI command center server from scratch using the Discord REST API. Use when a user wants to set up a professional Discord server for AI agent management, including categories, channels, roles, permissions, and pinned workflow cards. Executes entirely via API — no manual Discord UI steps required. Requires a Discord bot token with Manage Channels, Manage Roles, and Send Messages permissions, plus the target guild/server ID."
---

# Discord Hub Builder

Builds a complete AI command center Discord server via API. No manual steps.

## What Gets Built

**Categories & Channels:**
- COMMAND CENTER → #daily-brief, #task-queue
- AGENT CHANNELS → #agent-openclaw, #agent-perplexity, #agent-manus
- RESEARCH & OUTPUTS → #financial-briefs, #content-drafts, #research-archive
- OPERATIONS → #agent-logs, #ops-notes, #personal

**Roles:** Agent (blue), Reviewer (green)

**Workflow Cards:** Pinned in each agent channel with TOOL / TRIGGER / INPUT / OUTPUT / FREQUENCY

## Prerequisites

Before running, confirm the user has:

1. **A Discord bot** — created at https://discord.com/developers/applications
2. **Bot permissions:** `Manage Channels`, `Manage Roles`, `Send Messages`, `Manage Messages` (for pinning)
3. **Bot invited to the server** — use OAuth2 URL with `bot` scope + above permissions
4. **Guild ID** — right-click server name → Copy Server ID (Developer Mode must be on)
5. **Bot token** — from the Bot tab in developer portal

If the user doesn't have these, walk through setup before running.

## Execution

### Dry run first (always)
```bash
python3 scripts/build_hub.py --token BOT_TOKEN --guild GUILD_ID --dry-run
```

Show the user the preview. Confirm before live run.

### Live run
```bash
python3 scripts/build_hub.py --token BOT_TOKEN --guild GUILD_ID
```

The script:
- Creates roles (skips if already exist by name)
- Creates all categories and channels
- Posts and pins workflow cards in agent channels
- Prints channel IDs on completion

## After Build

Tell the user:
1. Set channel-specific permissions manually for `#task-queue` (Owner-only send) and readonly channels — Discord's permission API requires role IDs which vary per server
2. To add more agent channels: copy an existing agent channel block in the script and re-run
3. Workflow cards can be edited by finding the pinned message in each agent channel

## Error Handling

If the script fails mid-run:
- Re-running is safe — roles skip if they exist by name
- Channels don't have dedup logic; re-run will create duplicates — delete extras manually or use the dry-run to check state first
- Rate limit errors (429): add `time.sleep(1)` between calls or wait and retry
