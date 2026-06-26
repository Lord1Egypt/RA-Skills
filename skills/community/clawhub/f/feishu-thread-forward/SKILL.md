---
name: feishu-thread-forward
description: |
  Forward Feishu thread/topic to a user, group, or topic via REST API.
  Activate when: forwarding a thread/topic to another chat, sharing a topic post to a different group,
  or any scenario involving Feishu thread-level forwarding (转发话题).
  The built-in feishu message tool does NOT support thread forwarding — this skill fills that gap.
---

# Feishu Thread Forward

Forward a Feishu thread (话题) to a user, group, or another topic using the Feishu Open API.

## When to Use

- User asks to forward/share a thread or topic to another group or user
- You need to cross-post a topic post from one group to another
- The built-in `message` tool cannot do thread-level forwarding

## API

```
POST https://open.feishu.cn/open-apis/im/v1/threads/{thread_id}/forward?receive_id_type={type}
```

### Parameters

| Param | Location | Required | Description |
|-------|----------|----------|-------------|
| `thread_id` | path | yes | Thread ID to forward (format: `omt_xxxxx`) |
| `receive_id_type` | query | yes | Target ID type: `open_id`, `chat_id`, `user_id`, `union_id`, `email`, `thread_id` |
| `receive_id` | body | yes | Target ID matching the `receive_id_type` |
| `uuid` | query | no | Idempotency key (max 50 chars, dedup within 1 hour) |

### Headers

```
Authorization: Bearer {tenant_access_token}
Content-Type: application/json
```

## How to Get `thread_id`

A message in a topic group has a `thread_id` field. Retrieve it via:

```
GET https://open.feishu.cn/open-apis/im/v1/messages/{message_id}
```

The response `data.items[0].thread_id` contains the thread ID (e.g., `omt_1accc5a75c0f9b93`).

## Script

Use `scripts/forward_thread.py` for the complete implementation.

```bash
python3 skills/feishu-thread-forward/scripts/forward_thread.py \
  --thread-id omt_xxxxx \
  --receive-id oc_xxxxx \
  --receive-id-type chat_id
```

## Typical Flow

1. **Get `thread_id`** — from the message's metadata, or by calling GET message API
2. **Call forward API** — `POST /im/v1/threads/{thread_id}/forward`
3. **Result** — a `merge_forward` type message appears in the target chat as a clickable topic card

## Forward vs Merge Forward vs Message Forward

| Method | API | Result |
|--------|-----|--------|
| **Thread forward** (this skill) | `POST /threads/{thread_id}/forward` | Topic card (clickable, shows thread context) ✅ |
| Merge forward | `POST /messages/merge_forward` | "群聊会话记录" bundle (expandable message list) |
| Message forward | `POST /messages/{message_id}/forward` | Single message copied to target (loses thread context) |

**Thread forward** is what users see when they click "转发话题" in Feishu client.

## Prerequisites

- Bot must be in the source group (and can see the thread)
- Bot must be in the target group (or target user must be in bot's availability scope)
- Bot needs `im:message` or `im:message:send_as_bot` permission

## Credentials

Read from `/root/.openclaw/openclaw.json` → `channels.feishu.appId` / `channels.feishu.appSecret` to obtain `tenant_access_token`.

## Error Codes

| Code | Meaning |
|------|---------|
| 230002 | Bot not in target group |
| 230013 | Target user not in bot's availability scope |
| 230064 | Invalid thread_id |
| 230066 | Thread is in a secret group (no forwarding) |
| 230070 | Thread's group has anti-leak mode enabled |
| 230073 | Thread invisible to bot (joined after thread creation + history hidden) |
