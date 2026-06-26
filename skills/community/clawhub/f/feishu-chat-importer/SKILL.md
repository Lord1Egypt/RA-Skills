---
name: feishu-chat-importer
description: "Convert Feishu chat history exports into OpenClaw episodic memory format. Parses feishu_chat_YYYYMMDD.json files, normalizes messages, and writes daily episodic summaries to memory/episodic/. Trigger phrases: import feishu chat, convert feishu history, feishu memory import."
metadata: {"clawdbot":{"emoji":"📥","requires":{"bins":["python3"]},"env":[],"os":["win32","linux","darwin"],"homepage":"https://clawhub.com"}}
---

# Feishu Chat History Importer

Import Feishu chat history exports into OpenClaw episodic memory. Converts feishu JSON exports into daily episodic summaries that the Dreaming system can process and display in Imported Insights and Memory Palace views.

## Quick Start

```bash
# Dry run — preview what would be imported
python3 skills/feishu-chat-importer/scripts/batch.py --dir memory/Chat-history --dry-run

# Import all Feishu chats
python3 skills/feishu-chat-importer/scripts/batch.py --dir memory/Chat-history

# Import only chats since a date
python3 skills/feishu-chat-importer/scripts/batch.py --dir memory/Chat-history --since 2026-03-01

# Verbose — show every message
python3 skills/feishu-chat-importer/scripts/batch.py --dir memory/Chat-history --dry-run --verbose
```

## How It Works

1. **Read** `feishu_chat_YYYYMMDD.json` files from the source directory
2. **Group** messages by date (from `create_time` / millisecond timestamp)
3. **Normalize** each message to `{role, content, timestamp}`
   - `sender.sender_type = "user"` → role = `user`
   - `sender.sender_type = "app"` → role = `assistant` (Feishu bot = AI)
4. **Write** daily episodic summaries to `memory/episodic/YYYY-MM-DD.md`
5. **Dreaming** processes episodic files → appears in Imported Insights + Memory Palace

## Output Format

Writes to `memory/episodic/YYYY-MM-DD.md`:

```markdown
## Feishu Chat: <chat_id> (2026-03-19)
- Messages: <count>
- Participants: user_id, app_id

### user (首长):
message content here...

### assistant (飞书机器人):
message content here...
```

## Key Concepts

- **Daily grouping**: All messages from the same YYYYMMDD file land in the same episodic file
- **Deduplication**: Chat IDs tracked — re-running never creates duplicates
- **Role mapping**: User messages → `user`, App/bot messages → `assistant`
- **Content extraction**: Handles `text` and `post` msg_type automatically
- **OPENCLAW_WORKSPACE**: Set this env var to point imports to the right agent workspace

## Source Format

Expects Feishu export files named `feishu_chat_YYYYMMDD.json` with this structure:

```json
[
  {
    "message_id": "om_xxx",
    "chat_id": "oc_xxx",
    "create_time": "1773899372102",
    "msg_type": "text|post",
    "sender": {
      "id": "ou_xxx",
      "sender_type": "user|app"
    },
    "body": {
      "content": "{\"text\":\"message text\"}"  // text type
      // or
      "content": "{\"title\":\"\",\"content\":[[{\"tag\":\"text\",\"text\":\"...\"}]]}"  // post type
    }
  }
]
```
