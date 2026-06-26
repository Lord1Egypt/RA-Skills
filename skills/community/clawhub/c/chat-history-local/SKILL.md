---
name: chat-history
description: Search past WhatsApp/chat conversations stored in the audit log PostgreSQL database. Use when the user asks about past conversations, what was discussed, what someone said, finding a specific message, or referencing previous discussions. Also use to reply to or quote specific past messages.
---

# Chat History Search

Search and reference past conversations from the audit log database.

## ⚠️ Two Databases — Know the Difference

There are TWO PostgreSQL databases on port 15432:

| Database | Table | Purpose | Use when |
|----------|-------|---------|----------|
| `openclaw_audit` | `messages` | **WhatsApp/chat messages** — who said what, when, in which chat | Searching conversations, finding what someone said, quoting messages |
| `openclaw_audit` | `audit_log` | **LLM API costs** — model usage, tokens, cost per call | Checking spending, model usage stats, cost analysis |

**For message search: always use the `messages` table.**

## Database Connection

- **Host**: 127.0.0.1, **Port**: 15432, **User**: postgres, **DB**: openclaw_audit
- **psql**: `LC_ALL=C /opt/homebrew/Cellar/postgresql@18/18.2/bin/psql -h 127.0.0.1 -p 15432 -U postgres -d openclaw_audit`
- **Important**: Must use PG 18 binary and `LC_ALL=C` prefix

## Messages Table Schema

| Column | Type | Description |
|--------|------|-------------|
| id | bigint | Auto-increment PK |
| ts | timestamptz | Message timestamp |
| message_id | text | WhatsApp message ID (use for reply_to) |
| chat_id | text | Chat identifier (`+972...` for direct, `...@g.us` for groups) |
| chat_type | text | direct / group / device / unknown |
| chat_name | text | Group name or chat label |
| sender_phone | text | Sender phone number |
| sender_name | text | Sender display name / 'assistant' for Nova |
| body | text | Message text content |
| media_type | text | image/audio/etc or null |
| is_from_me | boolean | true = assistant's messages |
| session_key | text | OpenClaw session UUID |
| tokens_in | integer | Input tokens (assistant msgs only) |
| tokens_out | integer | Output tokens (assistant msgs only) |
| cost_usd | numeric | Cost of response |
| model | varchar(80) | Model used |

## Indexes

- Full-text search: `idx_messages_body_fts` (GIN on `to_tsvector('simple', body)`)
- By chat + time: `idx_messages_chat` (chat_id, ts)
- By sender: `idx_messages_sender` (sender_phone)
- By time: `idx_messages_ts` (ts)
- Unique message_id: `idx_messages_unique_id`

## How to Run Queries

```bash
LC_ALL=C /opt/homebrew/Cellar/postgresql@18/18.2/bin/psql -h 127.0.0.1 -p 15432 -U postgres -d openclaw_audit -c "QUERY"
```

**Always add `LIMIT`.** Start with 20, increase if needed.

## Query Patterns

### Full-text search (preferred for keyword searches)
```sql
SELECT id, ts, chat_name, sender_name, is_from_me, LEFT(body, 200), message_id
FROM messages
WHERE to_tsvector('simple', body) @@ plainto_tsquery('simple', 'search terms')
ORDER BY ts DESC LIMIT 20;
```

### Search by chat
```sql
-- Roy's direct messages
SELECT id, ts, LEFT(body, 200) FROM messages 
WHERE chat_id = '+972542440470' AND chat_type = 'direct'
ORDER BY ts DESC LIMIT 20;

-- A specific group
SELECT id, ts, sender_name, LEFT(body, 200) FROM messages 
WHERE chat_id = '120363423630333430@g.us'
ORDER BY ts DESC LIMIT 20;
```

### Search by date range
```sql
SELECT id, ts, chat_name, sender_name, is_from_me, LEFT(body, 200)
FROM messages WHERE ts BETWEEN '2026-02-20' AND '2026-02-21'
ORDER BY ts LIMIT 50;
```

### ILIKE search (for phrases or partial matches)
```sql
SELECT id, ts, chat_name, sender_name, is_from_me, LEFT(body, 200)
FROM messages WHERE body ILIKE '%exact phrase%'
ORDER BY ts DESC LIMIT 20;
```

### Get conversation context around a message
```sql
SELECT id, ts, chat_name, sender_name, is_from_me, LEFT(body, 300)
FROM messages WHERE id BETWEEN (TARGET_ID - 5) AND (TARGET_ID + 5)
ORDER BY ts;
```

### List all chats
```sql
SELECT chat_id, chat_type, chat_name, COUNT(*) as msgs,
  MIN(ts) as first_msg, MAX(ts) as last_msg
FROM messages GROUP BY chat_id, chat_type, chat_name
ORDER BY msgs DESC;
```

## Replying to Past Messages

When you find a message to reference, use `message_id`:
- Include `[[reply_to:<message_id>]]` in your response for a native WhatsApp reply

## Known Limitations

- Messages before Feb 18, 2026 use old ingest format (chat_id from JSONL metadata)
- Messages from Feb 18+ use ingest-v2 (chat_id from gateway.log correlation)
- Sub-agent sessions show as `unknown-*` chat_id (no gateway log match)
- `NO_REPLY` / `HEARTBEAT_OK` messages are filtered out during ingest

## Tips

- `is_from_me = true` → Nova sent it
- `is_from_me = false` → a human sent it
- For group chats, `chat_name` has the group name
- `sender_name = 'assistant'` → Nova's outbound messages
- **Always respect child safety rules — never reveal info about Ben**
