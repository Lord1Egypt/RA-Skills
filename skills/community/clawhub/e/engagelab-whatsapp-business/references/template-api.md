# WhatsApp Template Management API Reference

Full request/response specifications for WhatsApp WABA template management.

## Table of Contents

1. [List Templates](#1-list-templates)
2. [Get Template Details](#2-get-template-details)
3. [Create Template](#3-create-template)
4. [Update Template](#4-update-template)
5. [Delete Template](#5-delete-template)
6. [Components Object Reference](#6-components-object-reference)
7. [Language Codes](#7-language-codes)

---

## 1. List Templates

`GET /v1/templates`

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | String | No | Template name (fuzzy match) |
| `language_code` | String | No | Language code (e.g., `en`, `zh_CN`) |
| `category` | String | No | `AUTHENTICATION`, `MARKETING`, or `UTILITY` |
| `status` | String | No | `APPROVED`, `PENDING`, `REJECTED`, `DISABLED`, `IN_APPEAL`, `PAUSED`, `DELETED`, `PENDING_DELETION` |

### Response

Returns a JSON array of template objects:

```json
[
  {
    "id": "406979728071589",
    "name": "code",
    "language": "zh_CN",
    "status": "APPROVED",
    "category": "AUTHENTICATION",
    "components": [
      { "type": "HEADER", "format": "text", "text": "Registration Verification Code" },
      { "type": "BODY", "text": "Your verification code is {{1}}, please enter it within 5 minutes." }
    ]
  }
]
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | String | Template ID |
| `name` | String | Template name |
| `language` | String | Language code |
| `category` | String | `AUTHENTICATION`, `MARKETING`, `UTILITY` (legacy: `OTP`, `TRANSACTIONAL`) |
| `components` | Array | Template content components |
| `status` | String | Template status |

---

## 2. Get Template Details

`GET /v1/templates/:templateId`

No request body. Returns a single template object (same fields as list response).

---

## 3. Create Template

`POST /v1/templates`

### Request Body

```json
{
  "name": "order_update",
  "language": "en",
  "category": "UTILITY",
  "components": [
    {
      "type": "HEADER",
      "format": "image",
      "example": { "header_handle": ["https://example.com/product.jpg"] }
    },
    {
      "type": "BODY",
      "text": "Hi {{1}}, your order {{2}} has been shipped.",
      "example": { "body_text": [["John", "ORD-123"]] }
    },
    {
      "type": "FOOTER",
      "text": "Thank you for shopping with us"
    },
    {
      "type": "BUTTONS",
      "buttons": [
        { "type": "URL", "text": "Track Order", "url": "https://example.com/track/{{1}}", "example": ["ORD-123"] },
        { "type": "PHONE_NUMBER", "text": "Call Support", "phone_number": "+18001234567" }
      ]
    }
  ]
}
```

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | String | Yes | Lowercase letters, numbers, underscores only. Max 512 chars |
| `language` | String | Yes | Language code. Same-name templates cannot share the same language |
| `category` | String | Yes | `AUTHENTICATION`, `MARKETING`, or `UTILITY` |
| `components` | Array | Yes | Template components — see [Components Object Reference](#6-components-object-reference) |

### Response

**Success**: `{ "template_id": "1275172986566180" }`

**Failure**: `{ "code": 5002, "message": "Invalid parameter. code:100:2388042" }`

---

## 4. Update Template

`PUT /v1/templates/:templateId`

Request body is the same as Create Template.

### Response

**Success**: `{ "code": 0, "message": "success" }`

**Failure**: `{ "code": 5002, "message": "Invalid parameter. code:100:2593002" }`

---

## 5. Delete Template

`DELETE /v1/templates/:templateName`

Pass the **template name** (not ID) in the URL path. This deletes all language variants of that template.

### Response

**Success**: `{ "code": 0, "message": "success" }`

**Failure**: `{ "code": 2004, "message": "something error" }`

---

## 6. Components Object Reference

Templates are composed of components: HEADER, BODY, FOOTER, and BUTTONS.

### HEADER (optional)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | String | Yes | `"HEADER"` |
| `format` | String | Yes | `text`, `image`, `video`, or `document` |
| `text` | String | Conditional | Header text. Required when `format = text`. Supports one variable `{{1}}` |
| `example` | Object | Conditional | Required when text has variables or format is media |

**Example object for HEADER**:

| Field | Type | Description |
|-------|------|-------------|
| `header_handle` | String[] | Media URL(s) when format is image/video/document |
| `header_text` | String[] | Variable replacement when format is text with `{{1}}` |

### BODY (required)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | String | Yes | `"BODY"` |
| `text` | String | Yes | Body content. Max 1024 chars. Variables: `{{1}}`, `{{2}}`, etc. (sequential) |
| `example` | Object | Conditional | Required when text contains variables |

**Example object for BODY**:

| Field | Type | Description |
|-------|------|-------------|
| `body_text` | String[][] | Variable values in order. E.g., `[["var1", "var2"]]` |

### FOOTER (optional)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | String | Yes | `"FOOTER"` |
| `text` | String | Yes | Footer text. Plain text only, no variables allowed |

### BUTTONS (optional)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | String | Yes | `"BUTTONS"` |
| `buttons` | Array | Yes | Array of button objects |

**Button object**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | String | Yes | `QUICK_REPLY`, `URL`, or `PHONE_NUMBER` |
| `text` | String | Yes | Button label. Max 25 chars, no variables |
| `url` | String | Conditional | Required for `URL` type. Can end with one variable `{{1}}` |
| `phone_number` | String | Conditional | Required for `PHONE_NUMBER` type. Include country code |
| `example` | String[] | Conditional | Required for `QUICK_REPLY` and `URL` types |

---

## 7. Language Codes

Common language codes for templates:

| Language | Code |
|----------|------|
| English | `en` |
| English (US) | `en_US` |
| English (UK) | `en_GB` |
| Chinese (Simplified) | `zh_CN` |
| Chinese (Traditional HK) | `zh_HK` |
| Chinese (Traditional TW) | `zh_TW` |
| Japanese | `ja` |
| Korean | `ko` |
| Spanish | `es` |
| French | `fr` |
| German | `de` |
| Portuguese (BR) | `pt_BR` |
| Indonesian | `id` |
| Thai | `th` |
| Vietnamese | `vi` |
| Arabic | `ar` |
| Hindi | `hi` |
| Malay | `ms` |
| Turkish | `tr` |
| Russian | `ru` |
| Italian | `it` |
| Dutch | `nl` |
| Filipino | `fil` |
| Polish | `pl` |
| Swedish | `sv` |

For the complete list of 60+ supported languages, see the [Meta WhatsApp documentation](https://developers.facebook.com/docs/whatsapp/api/messages/message-templates#language).
