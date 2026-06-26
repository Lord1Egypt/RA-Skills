---
name: feishu-message
description: |
  Fetch Feishu message content by message_id, with optional thread context.
  Activate when: needing to read the content of a specific Feishu message by its message_id,
  needing thread context around a message, or encountering "[Interactive Card]" placeholder text.
  Handles all msg_types: text, post, interactive (fallback only), image, merge_forward.
---

# Feishu Message Fetcher

Fetch any Feishu message content by `message_id` using the IM API, with optional thread context.

## Known Limitation

**Interactive cards** (`msg_type: interactive`): The Feishu GET message API (`/im/v1/messages/{id}`) only returns **fallback/degraded text** in `body.content`, not the full card JSON. This is a Feishu platform limitation — there is no API to retrieve the rendered card structure after sending.

**Workaround**: Use `--thread` to fetch the entire thread context. The interactive card is usually a reply to a text/post message that contains the actual content. Reading the thread gives you the full picture.

## Usage

```bash
# Fetch a single message
python3 scripts/fetch_message.py <message_id>

# Fetch with thread context (root message + all replies in thread)
python3 scripts/fetch_message.py <message_id> --thread

# Raw API response
python3 scripts/fetch_message.py <message_id> --raw
```

## Auth

Automatic — reads `appId`/`appSecret` from `~/.openclaw/openclaw.json`. Alternatively set `FEISHU_APP_ID` + `FEISHU_APP_SECRET` env vars, or pass `--token <tenant_access_token>`.

## Output

JSON with: `message_id`, `msg_type`, `sender_id`, `sender_type`, `chat_id`, `create_time`, `root_id`, `parent_id`, `content` (parsed).

With `--thread`: adds `thread` array (all messages in the same thread, sorted chronologically) and `thread_count`.

## Typical Workflow

When you encounter `[Interactive Card]` in a replied-to message:

1. Get the message_id from inbound metadata (`has_reply_context`, parent message info)
2. Run `fetch_message.py <parent_message_id> --thread`
3. The thread context will contain the text/post messages with actual content
4. Use that content to fulfill the user's request
