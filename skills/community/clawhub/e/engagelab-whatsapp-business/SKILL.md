---
name: engagelab-whatsapp-business
description: >
  Call EngageLab WhatsApp Business REST APIs to send WhatsApp messages
  (template, text, image, video, audio, document, sticker), manage WABA
  message templates, and handle callback webhooks for delivery status and
  user responses. Use this skill whenever the user wants to send WhatsApp
  messages via EngageLab, create or manage WhatsApp templates, configure
  WhatsApp callbacks, or integrate with the EngageLab WhatsApp Business
  platform. Also trigger when the user mentions "engagelab whatsapp",
  "whatsapp business api", "whatsapp api", "send whatsapp message",
  "whatsapp template", "waba", "whatsapp notification", "whatsapp marketing",
  or asks to integrate WhatsApp messaging into their application. This skill
  covers authentication, all message types, template CRUD, and callback
  handling — use it even if the user only needs one of these capabilities.
---

# EngageLab WhatsApp Business API Skill

This skill enables interaction with the EngageLab WhatsApp Business REST API. As a Meta-authorized WhatsApp Business solution provider, EngageLab connects businesses with over 2 billion WhatsApp users for marketing, notifications, OTP verification, and customer service.

It covers three areas:

1. **Send Messages** — Deliver template, text, image, video, audio, document, and sticker messages
2. **Template Management** — Create, list, get, update, and delete WABA message templates
3. **Callbacks** — Receive message delivery status, user responses, and system notifications

## Resources

### scripts/

- **`whatsapp_client.py`** — Python client class (`EngageLabWhatsApp`) wrapping all API endpoints: `send_template()`, `send_text()`, `send_image()`, `send_video()`, `send_audio()`, `send_document()`, `send_sticker()`, and template CRUD (`list_templates()`, `get_template()`, `create_template()`, `update_template()`, `delete_template()`). Handles authentication, request construction, and typed error handling.

### references/

- **`error-codes.md`** — Complete error code tables for messaging and template APIs
- **`template-api.md`** — Full template CRUD specs with components object details (header, body, footer, buttons)
- **`callback-api.md`** — Webhook callback events: message status, message response, and system notifications

## Authentication

All EngageLab WhatsApp API calls use **HTTP Basic Authentication**.

- **Base URL**: `https://wa.api.engagelab.cc`
- **Header**: `Authorization: Basic <base64(dev_key:dev_secret)>`
- **Content-Type**: `application/json`

The user must provide their `dev_key` (DevKey) and `dev_secret` (DevSecret). Encode them as `base64("dev_key:dev_secret")` and set the `Authorization` header.

**Example** (using curl):

```bash
curl -X POST https://wa.api.engagelab.cc/v1/messages \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic $(echo -n 'YOUR_DEV_KEY:YOUR_DEV_SECRET' | base64)" \
  -d '{ ... }'
```

If the user hasn't provided credentials, ask them for their `dev_key` and `dev_secret` before generating API calls.

## Quick Reference — All Endpoints

| Operation | Method | Path |
|-----------|--------|------|
| Send message | `POST` | `/v1/messages` |
| List templates | `GET` | `/v1/templates` |
| Get template | `GET` | `/v1/templates/:templateId` |
| Create template | `POST` | `/v1/templates` |
| Update template | `PUT` | `/v1/templates/:templateId` |
| Delete template | `DELETE` | `/v1/templates/:templateName` |

## Sending Messages

**Endpoint**: `POST /v1/messages`

### Request Body (Template Message)

```json
{
  "from": "+8613800138000",
  "to": ["00447911123456"],
  "body": {
    "type": "template",
    "template": {
      "name": "code",
      "language": "en",
      "components": [
        {
          "type": "body",
          "parameters": [
            { "type": "text", "text": "12345" }
          ]
        }
      ]
    }
  },
  "request_id": "my-request-123",
  "custom_args": { "order_id": "ORD-456" }
}
```

### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `from` | `string` | No | Sending number with country code. Uses default sending number if omitted |
| `to` | `string[]` | Yes | Recipient WhatsApp phone numbers with country code |
| `body` | `object` | Yes | Message body — see message types below |
| `request_id` | `string` | No | Custom request ID, returned as-is in response and callbacks |
| `custom_args` | `object` | No | Custom data returned in message status callbacks |

### Message Types

The `body.type` field determines the message type. **Only template messages can be sent to users proactively.** Other types require the user to have replied within the last 24 hours.

| Type | Description | 24h Window Required |
|------|-------------|---------------------|
| `template` | Pre-approved template message | No |
| `text` | Plain text (max 4096 chars) | Yes |
| `image` | Image (JPEG/PNG, max 5MB) | Yes |
| `video` | Video (MP4/3GPP, max 16MB) | Yes |
| `audio` | Audio (AAC/MP4/AMR/MPEG/OGG, max 16MB) | Yes |
| `document` | File (any MIME type, max 100MB) | Yes |
| `sticker` | Sticker (WebP, static 100KB / animated 500KB) | Yes |

### Text Message

```json
{
  "to": ["8613800138000"],
  "body": {
    "type": "text",
    "text": { "body": "Hello, your order has shipped!" }
  }
}
```

### Image Message

```json
{
  "to": ["8613800138000"],
  "body": {
    "type": "image",
    "image": {
      "link": "https://example.com/photo.jpg",
      "caption": "Order confirmation"
    }
  }
}
```

### Video Message

```json
{
  "to": ["8613800138000"],
  "body": {
    "type": "video",
    "video": {
      "link": "https://example.com/demo.mp4",
      "caption": "Product demo"
    }
  }
}
```

### Audio Message

```json
{
  "to": ["8613800138000"],
  "body": {
    "type": "audio",
    "audio": { "link": "https://example.com/voice.mp3" }
  }
}
```

### Document Message

```json
{
  "to": ["8613800138000"],
  "body": {
    "type": "document",
    "document": {
      "link": "https://example.com/invoice.pdf",
      "caption": "Your invoice",
      "filename": "invoice_2024.pdf"
    }
  }
}
```

### Sticker Message

```json
{
  "to": ["8613800138000"],
  "body": {
    "type": "sticker",
    "sticker": { "link": "https://example.com/sticker.webp" }
  }
}
```

### Template Message Components

Template messages use pre-approved WABA templates with variable substitution via `components`:

```json
{
  "to": ["00447911123456"],
  "body": {
    "type": "template",
    "template": {
      "name": "order_update",
      "language": "en",
      "components": [
        {
          "type": "header",
          "parameters": [
            { "type": "image", "image": { "link": "https://example.com/product.jpg" } }
          ]
        },
        {
          "type": "body",
          "parameters": [
            { "type": "text", "text": "John" },
            { "type": "text", "text": "ORD-12345" },
            { "type": "currency", "currency": { "fallback_value": "$99.99", "code": "USD", "amount_1000": 99990 } }
          ]
        }
      ]
    }
  }
}
```

Parameter types: `text`, `currency`, `date_time`, `image`, `video`, `document`. Media types only appear in header components.

### Response

**Success**:

```json
{
  "message_id": "cbggf4if6o9ukqaalfug",
  "request_id": "my-request-123"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `message_id` | `string` | Unique EngageLab message ID |
| `request_id` | `string` | Your custom request ID (if provided) |

For error codes, read `references/error-codes.md`.

## Template Management

WhatsApp message templates must be created and approved before use. Templates support HEADER, BODY, FOOTER, and BUTTONS components with variables.

For full request/response details including components object specs, read `references/template-api.md`.

### Quick Summary

**List all** — `GET /v1/templates` with optional query params: `name`, `language_code`, `category`, `status`

**Get one** — `GET /v1/templates/:templateId`

**Create** — `POST /v1/templates`

```json
{
  "name": "order_confirmation",
  "language": "en",
  "category": "UTILITY",
  "components": [
    { "type": "BODY", "text": "Hi {{1}}, your order {{2}} has shipped." ,
      "example": { "body_text": [["John", "ORD-123"]] } }
  ]
}
```

**Update** — `PUT /v1/templates/:templateId` (same body as create)

**Delete** — `DELETE /v1/templates/:templateName` (deletes all languages for that name)

### Template Categories

| Category | Description |
|----------|-------------|
| `AUTHENTICATION` | Verification codes / OTP |
| `MARKETING` | Promotional content |
| `UTILITY` | Service notifications |

### Template Status Values

| Status | Description |
|--------|-------------|
| `APPROVED` | Available for sending |
| `PENDING` | Awaiting review |
| `REJECTED` | Review rejected |
| `DISABLED` | Banned |
| `IN_APPEAL` | Under appeal |
| `PAUSED` | Temporarily paused |

## Callbacks

Configure webhook URLs to receive message delivery status, user responses, and system notifications.

For full callback data structures and event types, read `references/callback-api.md`.

### Message Status Events

| Status | Description |
|--------|-------------|
| `plan` | Scheduled for sending |
| `target_valid` | Number verified as valid |
| `target_invalid` | Number is invalid |
| `sent` | Successfully sent to Meta |
| `delivered` | Delivered to user's device |
| `read` | User has read the message |
| `sent_failed` | Failed to send |
| `delivered_failed` | Sent but delivery failed |
| `delivered_timeout` | No delivery confirmation within 5 minutes |

### User Response Events

| Event | Description |
|-------|-------------|
| `received` | User sent a direct message |
| `reply` | User replied to your message |
| `order` | User placed an order |
| `deleted` | User deleted their message |

## Generating Code

When the user asks to send WhatsApp messages or manage templates, generate working code. Default to `curl` unless the user specifies a language. Supported patterns:

- **curl** — Shell commands with proper auth header
- **Python** — Using `requests` library (or the bundled `whatsapp_client.py`)
- **Node.js** — Using `fetch` or `axios`
- **Java** — Using `HttpClient`
- **Go** — Using `net/http`

Always include the authentication header and proper error handling. Use placeholder values like `YOUR_DEV_KEY` and `YOUR_DEV_SECRET` if the user hasn't provided credentials.

### Media Format Requirements

| Type | Formats | Max Size |
|------|---------|----------|
| Image | JPEG, PNG (no transparent background) | 5 MB |
| Video | MP4, 3GPP (H.264 video + AAC audio) | 16 MB |
| Audio | AAC, MP4, AMR, MPEG, OGG (opus codec) | 16 MB |
| Document | Any MIME type (PDF only for template headers) | 100 MB |
| Sticker | WebP | Static: 100 KB, Animated: 500 KB |
