---
name: autothread
version: 1.2.2
description: >
  Add `/topic` to the start of any message and the agent creates a
  topic/thread from it with an auto-generated title. Telegram and
  Nicegram: a forum topic is created via the Bot API and the original
  message is quoted inside it (media is forwarded). Discord: a public
  thread is created from the message and the quote is posted inside.
  Signal has no native topics or threads, so its adapter instead posts
  a titled digest message to the group (or as a DM to a phone number) —
  no topic object is created there. All credentials are read from the
  local OpenClaw config; nothing is sent anywhere except the target
  platform's own API. Each platform adapter is a separate script that
  implements only its own platform; scripts/ shared helpers handle
  title fallback and JSON output. The repo also ships an offline test
  suite with a localhost mock API server (not part of the runtime).
metadata:
  openclaw:
    emoji: "🧵"
    homepage: https://github.com/abyssbugg/autothread
    requires:
      bins:
        - curl
        - jq
        - signal-cli
        - python3
allowed-tools:
  - Bash(scripts/autothread-telegram.sh)
  - Bash(scripts/autothread-discord.sh)
  - Bash(scripts/autothread-signal.sh)
  - Bash(scripts/autothread-nicegram.sh)
  - Bash(curl)
  - Bash(jq)
  - Bash(signal-cli)
  - Bash(python3)
  - Read(~/.openclaw/openclaw.json)
---

# AutoThread

Add `/topic` to the start of any message in a supported group → a new topic or thread is created from it. The title is figured out from your message automatically — no need to think of one yourself.

## Supported platforms

| Platform | Mechanism | Script |
|----------|-----------|--------|
| Telegram | Forum topic (Bot API `createForumTopic`) | `scripts/autothread-telegram.sh` |
| Nicegram | Same as Telegram (Nicegram chats are Telegram chats) | `scripts/autothread-nicegram.sh` |
| Discord | Thread from message (`POST /channels/{id}/messages/{mid}/threads`) | `scripts/autothread-discord.sh` |
| Signal | Pseudo-topic digest (no native topics — see limitations) | `scripts/autothread-signal.sh` |

## Handling /topic

When a message starts with `/topic`, detect the platform from the message context, generate a concise 3-7 word title summarising the message, then run the matching adapter script with arguments filled from the message context:

**Telegram / Nicegram:**
```
bash scripts/autothread-telegram.sh <chat_id> <message_id> "<sender name>" "<title>" "<text after /topic>"
```
(Nicegram: use `bash scripts/autothread-nicegram.sh` identically. Pass an empty string for the text arg if there's no text, e.g. media-only.)

**Discord:**
```
bash scripts/autothread-discord.sh <channel_id> <message_id> "<sender name>" "<title>" "<text after /topic>"
```

**Signal:**
```
bash scripts/autothread-signal.sh <group_id> <message_timestamp> "<sender name>" "<title>" "<text after /topic>"
```

Each script returns JSON: `{"topic_id": ..., "title": "...", "link": "..."}`.

After the script succeeds:

1. Reply to the original message with: `Topic created → [<title>](<link>)` (omit the link part on Signal, where `link` is null).
2. Then send a response to the actual message content in the NEW topic (use the message tool with `threadId` from the returned `topic_id`). Respond naturally as you would to any message.
3. After both replies are sent, respond with NO_REPLY.

## Prerequisites

**Telegram / Nicegram:**
- The group must be configured in OpenClaw (`channels.telegram.groups.<CHAT_ID>`).
- The group must have **forum/topics** enabled.
- The bot must be an admin with the **Manage Topics** permission.
- Bot token in the config (`.channels.telegram.botToken`; Nicegram optionally `.channels.nicegram.botToken`).

**Discord:**
- The channel must be configured in OpenClaw (`channels.discord...`).
- The bot needs **Create Public Threads** and **Send Messages in Threads** permissions.
- Bot token in the config (`.channels.discord.token`).

**Signal:**
- `signal-cli` installed with a registered account (`.channels.signal.account` in the config).

## Limitations

- **Telegram attribution:** quoted messages appear as sent by the bot (Telegram API limitation); sender name is included as attribution text below the quote.
- **Telegram media:** forwarded media shows a "Forwarded from" header.
- **Telegram title length:** topic names capped at 128 characters.
- **Discord:** threads can only be created from messages in guild text channels; thread names capped at 100 characters.
- **Signal:** no native topics/threads — the adapter posts a titled digest message instead and returns the sent timestamp as `topic_id` with `link: null`.

## Optional configuration (Telegram)

**Skip the @bot mention** — by default, the bot only responds when mentioned; keep that default in busy or public groups. Only set `requireMention: false` in a group you control where accidental activation is harmless, because any `/topic` message will then trigger a repost of content and sender name — never disable it where sensitive content is discussed:

```json
"channels.telegram.groups.<CHAT_ID>": { "requireMention": false }
```

**Telegram autocomplete** — add under `channels.telegram`:

```json
{
  "customCommands": [
    { "command": "topic", "description": "Create a new topic from a message" }
  ]
}
```
