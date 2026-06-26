# WhatsApp Callback API Reference

Callback data structures for message delivery status, user responses, and system notifications.

## Table of Contents

1. [Setup](#setup)
2. [Callback Structure](#callback-structure)
3. [Message Status Events](#message-status-events)
4. [Message Response Events](#message-response-events)
5. [Notification Events](#notification-events)

---

## Setup

Configure callback URLs in the [EngageLab console](https://www.engagelab.com) under callback settings. Your endpoint must:

- Accept `POST` requests with `Content-Type: application/json`
- Return HTTP 200 within 3 seconds
- Not require authentication (callback security mechanism is pending)

---

## Callback Structure

All callbacks use this outer structure:

```json
{
  "total": 1,
  "rows": [{ /* event object */ }]
}
```

### Common Fields in `rows` Objects

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message_id` | String | No | EngageLab message ID |
| `from` | String | No | Sender number |
| `to` | String | No | Recipient number |
| `server` | String | Yes | Fixed: `"whatsapp"` |
| `channel` | String | No | Fixed: `"whatsapp"` |
| `itime` | Integer | Yes | Callback timestamp |
| `custom_args` | Object | No | Custom data from original send request |
| `status` | Object | No | Message status details |
| `response` | Object | No | User response details |

---

## Message Status Events

Track the delivery lifecycle of each message.

### Status Values

| Status | Description |
|--------|-------------|
| `plan` | Message scheduled for sending |
| `target_valid` | Number verified as valid by EngageLab or Meta |
| `target_invalid` | Number deemed invalid |
| `sent` | Successfully submitted to Meta WhatsApp service |
| `delivered` | Meta confirms delivery to user's device |
| `read` | Meta confirms user read the message |
| `sent_failed` | Failed to send to Meta |
| `delivered_failed` | Sent to Meta but delivery failed |
| `delivered_timeout` | No delivery confirmation from Meta within 5 minutes |

### Status Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `message_status` | String | Status value from table above |
| `status_data` | Object | Detailed status data |
| `error_code` | Integer | Error code (on failure) |
| `error_detail` | Object | Error details with `message` field |
| `loss` | Object | Loss tracking info |

### Status Data Object

| Field | Type | Description |
|-------|------|-------------|
| `msg_time` | Integer | Message send timestamp |
| `channel_message_id` | String | Meta's WhatsApp message ID |
| `whatsapp_business_account_id` | String | WABA account ID |
| `timezone` | String | Organization timezone |
| `plan_user_total` | Integer | Total plan targets (only when status = `plan`) |
| `country_code` | String | Recipient's country code |
| `from_phone_id` | String | Sending number ID |
| `conversation` | Object | Session info: `id` and `origin.type` |
| `pricing` | Object | Price info: `pricing_model` and `category` |

### Conversation Origin Types

| Type | Description |
|------|-------------|
| `business_initiated` | Business sent first message (>24h since last user message) |
| `customer_initiated` | Business replied within 24h of user message |
| `referral_conversion` | Conversation from a free entry point |

### Loss Object

| Field | Type | Description |
|-------|------|-------------|
| `loss_step` | Integer | 1: Invalid target, 2: Send failed, 3: Delivery failed |
| `loss_source` | String | `engagelab` or `meta` |

### Example — Delivered Successfully

```json
{
  "total": 1,
  "rows": [{
    "message_id": "1666165485030094861",
    "from": "+8613800138000",
    "to": "+447911123456",
    "server": "whatsapp",
    "channel": "whatsapp",
    "itime": 1640707579,
    "custom_args": { "order_id": "ORD-123" },
    "status": {
      "message_status": "delivered",
      "status_data": {
        "msg_time": 1663432355,
        "channel_message_id": "wamid.123321abcdefed==",
        "whatsapp_business_account_id": "WABA123",
        "country_code": "GB",
        "from_phone_id": "111111",
        "conversation": { "id": "ebe2398cdaa37a0899ca5268b987b0c8", "origin": { "type": "business_initiated" } },
        "pricing": { "pricing_model": "CBP", "category": "business_initiated" }
      },
      "error_code": 0
    }
  }]
}
```

---

## Message Response Events

Callback events for user interactions (replies, direct messages, orders).

### Event Values

| Event | Description |
|-------|-------------|
| `received` | User sent a direct message |
| `reply` | User replied to your message |
| `order` | User placed an order |
| `deleted` | User deleted their message |

### Response Data Object

| Field | Type | Description |
|-------|------|-------------|
| `channel_message_id` | String | Meta's message ID |
| `whatsapp_business_account_id` | String | WABA account ID |
| `contact` | Object | Sender info: `profile.name` and `wa_id` (phone number) |
| `message` | Object | Message content with `type` field |
| `message_context` | Object | Reply context (for `reply` events) |

### Message Types in Responses

The `message.type` field can be: `text`, `image`, `audio`, `video`, `document`, `sticker`, `button`, `interactive`, `unknown`, `order`.

### Message Context (Reply Events)

| Field | Type | Description |
|-------|------|-------------|
| `origin_from_phone` | String | Sending number of referenced message |
| `origin_channel_message_id` | String | Meta ID of referenced message |
| `origin_from_phone_id` | String | Sending number ID of referenced message |
| `origin_message_id` | String | EngageLab message ID of referenced message |

### Example — User Text Reply

```json
{
  "total": 1,
  "rows": [{
    "message_id": "1666165485030094861",
    "from": "+8613800138000",
    "to": "+447911123456",
    "server": "whatsapp",
    "channel": "whatsapp",
    "itime": 1640707579,
    "response": {
      "event": "reply",
      "response_data": {
        "channel_message_id": "wamid.123321abcdefed==",
        "whatsapp_business_account_id": "123321",
        "contact": { "profile": { "name": "Bob" }, "wa_id": "8613800138000" },
        "message": { "type": "text", "text": { "body": "Thanks for the update!" } },
        "message_context": {
          "origin_from_phone": "447911123456",
          "origin_channel_message_id": "wamid.original123==",
          "origin_from_phone_id": "111111",
          "origin_message_id": "1666165485030094860"
        }
      }
    }
  }]
}
```

---

## Notification Events

System-level business alerts.

### Event Values

| Event | Description |
|-------|-------------|
| `insufficient_balance` | Account balance below threshold |
| `template_update` | Template status or quality changed |
| `phone_number_update` | Sending number limit tier changed |
| `whatsapp_business_update` | WABA account banned or violated |

### Notification Data Fields

| Field | Present When | Description |
|-------|--------------|-------------|
| `whatsapp_business_account_id` | Always | WABA account ID |
| `remain_balance` | `insufficient_balance` | Current balance (USD) |
| `balance_threshold` | `insufficient_balance` | Alert threshold (USD) |
| `template_id` | `template_update` | Template ID |
| `template_name` | `template_update` | Template name |
| `template_language` | `template_update` | Template language |
| `template_status` | `template_update` | `APPROVED`, `REJECTED`, `PENDING`, `DISABLED`, `FLAGGED`, `REINSTATED` |
| `template_status_reason` | `template_update` | Change reason (usually for rejections) |
| `phone_number_id` | `phone_number_update` | Sending number ID |
| `display_phone_number` | `phone_number_update` | Phone number display |
| `current_limit` | `phone_number_update` | Tier: `TIER_50`, `TIER_250`, `TIER_1K`, `TIER_10K`, `TIER_100K`, `TIER_UNLIMITED` |
| `waba_event` | `whatsapp_business_update` | `DISABLED_UPDATE` or `ACCOUNT_VIOLATION` |
| `ban_state` | `DISABLED_UPDATE` | `DISABLE` |
| `violation_type` | `ACCOUNT_VIOLATION` | `SPAM` or `SCAM` |

### Example — Insufficient Balance

```json
{
  "total": 1,
  "rows": [{
    "server": "whatsapp",
    "itime": 1640707579,
    "notification": {
      "event": "insufficient_balance",
      "notification_data": {
        "whatsapp_business_account_id": "WABA123",
        "remain_balance": 5.1234,
        "balance_threshold": 10
      }
    }
  }]
}
```
