---
name: bulk message delete
description:
  Use when user requests deleting multiple Discord messages or channel cleanup.
  Triggers on phrases like:
    - "delete [X] messages" 
    - "purge [X] messages"
    - "clean up [channel]"
    - "remove old messages"
    - "clear the chat"
    - "bulk delete in #[channel]"
  Always use when intent to delete Discord messages is clear, even without specifying skill name.
---

# Discord Bulk Message Purge Tool - Documentation

## Overview

A Python script for deleting messages from Discord channels without requiring npm/discord.js dependencies. Uses only Python standard library + requests.

**Location:** `discord-bulk-message-delete/scripts/discord-purge-tool.py` (in the subfolder of the skill!)

## Quick Start

### 1. Configure Bot Token

Create `token.json` in the workspace directory:

```json
{
  "token": "tokenhere"
}
```

OR set environment variable:

```powershell
$env:DISCORD_TOKEN = "YOUR_BOT_TOKEN_HERE"
```

### 2. ask for confirmation

 - run `python scripts/discord-purge-tool.py purge <amount> --channel-id <CHANNEL_ID>` to call dry-run mode
 - ask from the user if they really want to delete x amount of messages in the current channel

### 3. Run the Tool

From this skill's directory:

```powershell
# Delete last 5 messages
python scripts/discord-purge-tool.py --delete --channel-id <CHANNEL_ID>
OR
python scripts/discord-purge-tool.py -d --channel-id <CHANNEL_ID>

# Delete custom count
python scripts/discord-purge-tool.py purge 25 --delete --channel-id <CHANNEL_ID>
OR
python scripts/discord-purge-tool.py purge 25 -d --channel-id <CHANNEL_ID>

# Larger purge (handles batches automatically)
python scripts/discord-purge-tool.py purge 200 --delete --channel-id <CHANNEL_ID>
OR
python scripts/discord-purge-tool.py purge 200 -d --channel-id <CHANNEL_ID>
```

## Usage Examples

### Typical User Requests (I auto-detect intent):
- "delete 50 messages in #general"
- "purge the last 100 messages"
- "clean up #productivity"
- "remove old spam from chat"

- "clear the discord channel"
- "bulk delete last 25 messages in [channel]"

### Script Commands:
```PowerShell
# run in 'scout/dry-run' mode
python scripts/discord-purge-tool.py purge <count> --channel-id <CHANNEL_ID>
# Delete last X messages (default: 5)
python scripts/discord-purge-tool.py purge <count> -d --channel-id <CHANNEL_ID>
```

## Features

- ✅ **Standard library only** - No npm/discord.js required
- ✅ **Rate limiting** - Handles Discord's 100 messages per batch limit automatically  
- ✅ **Flexible arguments** - Works with multiple input formats
- ✅ **Dry-run mode** - check how many records are actually there, before deleting
- ✅ **Live mode** - Actual deletion when -d or --delete flags are added
- ✅ **Error handling** - Shows detailed error messages

## Rate Limiting

Discord enforces:
- Max 100 messages per bulk delete request (hard API limit)
- Waits automatically between batches for larger purges

The tool handles this transparently, so you don't need to worry about it.

## Permissions Required

Your Discord bot must have `MANAGE_MESSAGES` permission in target channels:

1. Go to your Discord server settings
2. find the role your bot uses
3. add "manage Messages" permission 

## Error Codes

- **403 Forbidden** - Bot lacks MANAGE_MESSAGES permission in channel
- **400 Bad Request** - Invalid channel ID or no messages found  
- **Other errors** - Displayed in output with details

## Configuration

### token.json

```json
{
  "token": "YOUR_BOT_TOKEN_HERE"
}
```

Or environment variable:

```powershell
$env:DISCORD_TOKEN = "YOUR_BOT_TOKEN_HERE"
```

## Command Reference

| Command | Description |
|---------|-------------|
| `python scripts/discord-purge-tool.py purge <count> --channel-id <id>` | dry-run last N messages |
| `python scripts/discord-purge-tool.py purge 10 -d --channel-id <id>` | Delete last 5 (default) |
| `python scripts/discord-purge-tool.py purge 10 --delete --channel-id <id>` | Delete last 10 |

## Troubleshooting

### "403 Forbidden" error

The bot doesn't have MANAGE_MESSAGES permission. Fix by:
1. Adding permissions via Discord settings
2. OR setting `DISCORD_TOKEN` env variable and running from this skill's directory

### "400 Bad Request" error  

Check that:
- Channel ID is correct
- Channel exists and has messages
- Token file is valid JSON with "token" key

## Notes

- Script path is relative: `scripts/discord-purge-tool.py`