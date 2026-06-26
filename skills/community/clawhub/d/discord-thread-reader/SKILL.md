---
name: discord-context
description: Read Discord channel and thread message history directly via the Discord Bot API, bypassing OpenClaw's session-based message visibility. Use when you need to read messages from a Discord thread or channel that has no active OpenClaw session, fetch historical context from a conversation you weren't part of, or access thread content that was mentioned but not visible in the current session. Triggers on "read that thread", "what did they say in #channel", "fetch Discord messages", "get thread history", "I can't see that thread".
---

# Discord Context

## Problem

OpenClaw is session-based: agents only see messages from conversations where they have an active session. Discord threads that the agent wasn't mentioned in or hasn't interacted with are invisible — there's no built-in tool to read arbitrary channel/thread history.

Additionally, OpenClaw redacts the Discord bot token from `openclaw config get` and environment variables (by design), so agents cannot make direct Discord API calls using the configured token.

## Solution

Store the Discord bot token in a separate file accessible to the agent, then use `curl` to call the Discord API directly.

### Setup (one-time, run as the user)

```bash
# Store your bot token in a file outside the workspace (won't be git-committed)
echo 'YOUR_DISCORD_BOT_TOKEN' > ~/.openclaw/.discord-bot-token
chmod 600 ~/.openclaw/.discord-bot-token
```

Record the path in `TOOLS.md` so the agent knows where to find it across sessions.

### Reading Messages

```bash
# Load token
DISCORD_TOKEN=$(cat ~/.openclaw/.discord-bot-token)

# Read recent messages from a channel or thread (threads are channels in Discord)
curl -s -H "Authorization: Bot $DISCORD_TOKEN" \
  "https://discord.com/api/v10/channels/{channel_or_thread_id}/messages?limit=50" \
  | python3 -m json.tool

# Read messages before a specific message ID (pagination)
curl -s -H "Authorization: Bot $DISCORD_TOKEN" \
  "https://discord.com/api/v10/channels/{channel_id}/messages?limit=50&before={message_id}" \
  | python3 -m json.tool

# List active threads in a guild channel
curl -s -H "Authorization: Bot $DISCORD_TOKEN" \
  "https://discord.com/api/v10/channels/{parent_channel_id}/threads/active" \
  | python3 -m json.tool
```

### Finding Thread/Channel IDs

- Enable **Developer Mode** in Discord: User Settings → Advanced → Developer Mode
- Right-click any channel or thread → **Copy Channel ID**
- Thread IDs and channel IDs work the same way in the API

### Key Notes

- Discord returns messages newest-first by default
- Max `limit` is 100 per request; use `before`/`after` params to paginate
- The bot must be a member of the guild and have **View Channel** + **Read Message History** permissions
- Rate limits apply: 50 requests/second per route (respect `429` responses and `Retry-After` headers)

### Response Fields

Each message object contains:
- `content` — message text
- `author.username` / `author.global_name` — who sent it
- `timestamp` — when
- `id` — message ID (for pagination or reply references)
- `referenced_message` — the message being replied to (if a reply)

### Security Considerations

- The token file is `chmod 600` and outside the git-tracked workspace
- The bot token grants read/write access to all channels the bot is in — treat it like a password
- Prefer read-only API calls; do not use this for sending messages (use OpenClaw's native routing instead)
- If the token is rotated in Discord Developer Portal, update both `openclaw config` and the token file
