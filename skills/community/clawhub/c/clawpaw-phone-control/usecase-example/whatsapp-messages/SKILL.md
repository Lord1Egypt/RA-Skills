---
name: whatsapp-messages
description: Read unread WhatsApp messages and optionally reply. Use when user says "check my WhatsApp", "read my messages", "any new WhatsApp messages", etc.
disable-model-invocation: true
---

# WhatsApp Messages — Read & Reply

Read unread WhatsApp messages and optionally reply on behalf of the user. WhatsApp has no public API for personal accounts — this can only be done by operating the phone.

Use `snapshot` throughout. Avoid `screenshot` unless snapshot returns no useful elements.

## Package

`com.whatsapp`

## Step 1 — Launch WhatsApp

```
shell → monkey -p com.whatsapp -c android.intent.category.LAUNCHER 1
```

`snapshot` — confirm WhatsApp is open. Look for elements with `id` containing `com.whatsapp`. If not loaded yet, wait 2s and retry.

## Step 2 — Read chat list

`snapshot` the chat list. Key elements:

| Element | Resource ID | Content |
|---------|-------------|---------|
| Contact name | `conversations_row_contact_name` | Chat name |
| Last message | `single_msg_tv` | Message preview |
| Unread badge | `conversations_row_message_count` | desc contains "未读消息" or shows unread count |
| Date | `conversations_row_date` | Last message date |

**Identify unread chats:** Look for elements with id `conversations_row_message_count` — their desc will say something like "1条未读消息". The corresponding chat row (`contact_row_container`) is the parent.

Collect all unread chats. If none found, report "No unread messages" to the user and stop.

## Step 3 — Read messages in each unread chat

For each unread chat:

1. `tap` the chat row (use bounds center of the `contact_row_container`)
2. `snapshot` the conversation view

Key elements in chat view:

| Element | Resource ID | Content |
|---------|-------------|---------|
| Contact name | `conversation_contact_name` | Who you're chatting with |
| Message text | `message_text` | Each message bubble |
| Time | `date` | Message timestamp |
| Read status | `status` | desc "已读"/"已送达" — only on YOUR sent messages |
| Date divider | `conversation_row_date_divider` | Date separators like "2026年2月14日" |
| Unread divider | `unread_divider_tv` | "N条未读消息" — marks where unread starts |

**Distinguish sent vs received:**
- Sent messages (right side): have a sibling `status` ImageView with desc like "已读" or "已送达"
- Received messages (left side): no `status` element

**Read all visible messages** from the unread divider downward. If you need to see earlier messages, `swipe` down.

3. `press_key back` to return to chat list
4. Repeat for next unread chat

## Step 4 — Report to user

Summarize all unread messages:
```
WhatsApp — 2 unread chats:

1. **my Bro** (2 messages)
   - "你换模型了吗" (18:58)

2. **John** (1 message)
   - "Hey, are you free tonight?" (20:15)
```

Ask the user if they want to reply to any of them.

## Step 5 — Reply (if requested)

When the user wants to reply:

1. `tap` the chat to open it (from chat list, or navigate back if already inside)
2. `snapshot` — find the input field: `id="com.whatsapp:id/entry"` (placeholder text "发消息")
3. `tap` the input field (bounds center)
4. `type_text` with the reply message
5. `snapshot` — after typing, the voice note button changes to a send button. Find `id="com.whatsapp:id/send"` or the send icon
6. `tap` the send button
7. `snapshot` — verify the message appears in the chat with `status` showing "已送达" or similar

## Important Notes

1. **WhatsApp uses stable native Android resource IDs** — unlike WebView apps, you CAN reliably use `resourceId` for tapping. However, coordinates from bounds are still more reliable for tap actions.
2. **Language:** UI text may be in Chinese (e.g., "发消息", "已读", "未读消息") depending on device language settings. Match accordingly.
3. **Scrolling:** If chat list has many chats, `swipe up` to see more. In a conversation, `swipe down` to see older messages.
4. **Media messages:** Some messages may be images, videos, or voice notes. The `message_text` won't exist for these — look for `media_container` or content descriptions like "视频" / "图片" instead. Report them as "[Image]", "[Video]", "[Voice message]".
5. **Group chats:** In group chats, each message has `name_in_group_tv` showing the sender name.
6. **Privacy:** Always show the user what you're about to send before actually sending. Never auto-send without confirmation.
