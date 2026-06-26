---
name: feishu-merged-msg
description: Fetch and parse Feishu merged/forwarded messages (合并转发消息). Activate when a Feishu message shows "Merged and Forwarded Message" with no readable content, or when you need to retrieve sub-messages from a merge_forward message type.
---

# Feishu Merged Message Fetcher

Feishu's merge_forward messages appear as "Merged and Forwarded Message" with no content in the bot API. Use the Feishu REST API to retrieve the actual sub-messages.

## When to Use

- Message body contains only `"Merged and Forwarded Message"`
- `msg_type` is `merge_forward`
- User asks about a forwarded/合并转发 message you can't read

## How It Works

The Feishu `GET /open-apis/im/v1/messages/{message_id}` endpoint returns the parent message plus all sub-messages in `data.items[]`. Sub-messages have `upper_message_id` pointing to the parent.

## Steps

1. Get the `message_id` of the merged message (from inbound context or replied message metadata).

2. Run the fetch script:
   ```bash
   bash <skill_dir>/scripts/fetch_merged_msg.sh <message_id> <app_id> <app_secret>
   ```
   - `app_id` / `app_secret`: from OpenClaw config at `.channels.feishu` in `openclaw.json`
   - If credentials are not readily available, extract them:
     ```bash
     python3 -c "import json; d=json.load(open('/root/.openclaw/openclaw.json')); c=d['channels']['feishu']; print(c.get('appId',''), c.get('appSecret',''))"
     ```

3. Parse the JSON response:
   - `data.items[0]` is the parent (merge_forward) message
   - `data.items[1:]` are the sub-messages in chronological order
   - Each sub-message has `body.content` with the actual text/post content
   - `mentions[]` maps `@_user_N` placeholders to real names
   - `sender.id` identifies who sent each sub-message

4. Summarize the conversation thread for the user.

## Notes

- The API requires `im:message:readonly` scope on the Feishu app.
- Images inside sub-messages show as `image_key` references; they cannot be directly displayed but can be described from context.
- Sub-messages may come from different chats (check `chat_id`); the original chat context may differ from the current group.
