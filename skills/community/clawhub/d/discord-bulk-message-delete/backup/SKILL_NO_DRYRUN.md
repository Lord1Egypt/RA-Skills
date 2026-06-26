---

name: bulk message delete

description:

&nbsp; Use when user requests deleting multiple Discord messages or channel cleanup.

&nbsp; Triggers on phrases like:

&nbsp;   - "delete \[X] messages" 

&nbsp;   - "purge \[X] messages"

&nbsp;   - "clean up \[channel]"

&nbsp;   - "remove old messages"

&nbsp;   - "clear the chat"

&nbsp;   - "bulk delete in #\[channel]"

&nbsp; Always use when intent to delete Discord messages is clear, even without specifying skill name.

---



\# Discord Bulk Message Purge Tool - Documentation



\## Overview



A Python script for deleting messages from Discord channels without requiring npm/discord.js dependencies. Uses only Python standard library + requests.



\*\*Location:\*\* `discord-bulk-message-delete/scripts/discord-purge-tool.py` (in the subfolder of the skill!)



\## Quick Start



\### 1. Configure Bot Token



Create `token.json` in the workspace directory:



```json

{

&nbsp; "token": "tokenhere"

}

```



OR set environment variable:



```powershell

$env:DISCORD\_TOKEN = "YOUR\_BOT\_TOKEN\_HERE"

```



\### 2. ask for confirmation



&nbsp;- ask from the user if they really want to delete x amount of messages in the current channel 



\### 3. Run the Tool



From this skill's directory:



```powershell

\# Delete last 5 messages

python scripts/discord-purge-tool.py --channel-id <CHANNEL\_ID>



\# Delete custom count

python scripts/discord-purge-tool.py purge 25 --channel-id <CHANNEL\_ID>



\# Larger purge (handles batches automatically)

python scripts/discord-purge-tool.py purge 200 --channel-id <CHANNEL\_ID>

```



\## Usage Examples



\### Typical User Requests (I auto-detect intent):

\- "delete 50 messages in #general"

\- "purge the last 100 messages"

\- "clean up #productivity"

\- "remove old spam from chat"

\- "clear the discord channel"

\- "bulk delete last 25 messages in \[channel]"



\### Script Commands:

```powershell

\# Delete last X messages (default: 5)

python scripts/discord-purge-tool.py purge <count> --channel-id <CHANNEL\_ID>



\# Auto-detect channel from context if mentioned earlier

python scripts/discord-purge-tool.py purge 50

```



\## Features



\- ✅ \*\*Standard library only\*\* - No npm/discord.js required

\- ✅ \*\*Rate limiting\*\* - Handles Discord's 100 messages per batch limit automatically  

\- ✅ \*\*Flexible arguments\*\* - Works with multiple input formats

\- ✅ \*\*Live mode\*\* - Actual deletion when token configured

\- ✅ \*\*Error handling\*\* - Shows detailed error messages



\## Rate Limiting



Discord enforces:

\- Max 100 messages per bulk delete request (hard API limit)

\- Waits automatically between batches for larger purges



The tool handles this transparently, so you don't need to worry about it.



\## Permissions Required



Your Discord bot must have `MANAGE\_MESSAGES` permission in target channels:



1\. Go to your Discord server settings

2\. find the role your bot uses

3\. add "manage Messages" permission 



\## Error Codes



\- \*\*403 Forbidden\*\* - Bot lacks MANAGE\_MESSAGES permission in channel

\- \*\*400 Bad Request\*\* - Invalid channel ID or no messages found  

\- \*\*Other errors\*\* - Displayed in output with details



\## Configuration



\### token.json



```json

{

&nbsp; "token": "YOUR\_BOT\_TOKEN\_HERE"

}

```



Or environment variable:



```powershell

$env:DISCORD\_TOKEN = "YOUR\_BOT\_TOKEN\_HERE"

```



\## Command Reference



| Command | Description |

|---------|-------------|

| `python scripts/discord-purge-tool.py purge <count> --channel-id <id>` | Delete last N messages |

| `python scripts/discord-purge-tool.py 5 --channel-id <id>` | Delete last 5 (default) |



\## Troubleshooting



\### "403 Forbidden" error



The bot doesn't have MANAGE\_MESSAGES permission. Fix by:

1\. Adding permissions via Discord settings

2\. OR setting `DISCORD\_TOKEN` env variable and running from this skill's directory



\### "400 Bad Request" error  



Check that:

\- Channel ID is correct

\- Channel exists and has messages

\- Token file is valid JSON with "token" key



\## Notes



\- Script path is relative: `scripts/discord-purge-tool.py`

\- Works from this skill's directory or when `DISCORD\_TOKEN` env variable is set

