---
name: engagelab-otp
description: >
  Call EngageLab OTP REST APIs to send one-time passwords (OTP), verify codes,
  send custom messages, and manage OTP templates across SMS, WhatsApp, Email,
  and Voice channels. Use this skill whenever the user wants to send an OTP or
  verification code via EngageLab, verify an OTP code, send custom messages
  through the OTP platform, manage OTP templates, configure callback webhooks,
  or integrate via SMPP. Also trigger when the user mentions "engagelab otp",
  "otp api", "send otp", "verify otp", "one-time password", "verification code",
  "engagelab verification", "otp template", "multi-channel otp", "whatsapp otp",
  "sms otp", "voice otp", "email otp", or asks to integrate with the EngageLab
  OTP platform. This skill covers OTP generation, delivery, verification,
  custom messaging, template management, callback configuration, and SMPP
  integration — use it even if the user only needs one of these capabilities.
---

# EngageLab OTP API Skill

This skill enables interaction with the EngageLab OTP REST API. The OTP service handles one-time password generation, multi-channel delivery (SMS, WhatsApp, Email, Voice), verification, and fraud monitoring.

It covers six areas:

1. **OTP Send** — Platform-generated OTP code delivery
2. **Custom OTP Send** — User-generated OTP code delivery
3. **OTP Verify** — Validate OTP codes
4. **Custom Messages Send** — Send custom template messages (notifications, marketing)
5. **Template Management** — Create, list, get, and delete OTP templates
6. **Callback & SMPP** — Webhook configuration and SMPP protocol integration

## Resources

### scripts/

- **`otp_client.py`** — Python client class (`EngageLabOTP`) wrapping all API endpoints: `send_otp()`, `send_custom_otp()`, `verify()`, `send_custom_message()`, and template CRUD. Handles authentication, request construction, and typed error handling. Use this as a ready-to-run helper or import it into the user's project.
- **`verify_callback.py`** — HMAC-SHA256 signature verifier for incoming OTP callback webhooks. Parses the `X-CALLBACK-ID` header and validates authenticity. Drop into any web framework (Flask, FastAPI, Django) to secure callback endpoints.

### references/

- **`error-codes.md`** — Complete error code tables for all OTP APIs
- **`template-api.md`** — Full template CRUD specs with all channel configurations
- **`callback-config.md`** — Webhook setup, security, and all event types
- **`smpp-guide.md`** — SMPP protocol connection, messaging, and delivery reports

## Authentication

All EngageLab OTP API calls use **HTTP Basic Authentication**.

- **Base URL**: `https://otp.api.engagelab.cc`
- **Header**: `Authorization: Basic <base64(dev_key:dev_secret)>`
- **Content-Type**: `application/json`

The user must provide their `dev_key` and `dev_secret`. Encode them as `base64("dev_key:dev_secret")` and set the `Authorization` header.

**Example** (using curl):

```bash
curl -X POST https://otp.api.engagelab.cc/v1/messages \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic $(echo -n 'YOUR_DEV_KEY:YOUR_DEV_SECRET' | base64)" \
  -d '{ ... }'
```

If the user hasn't provided credentials, ask them for their `dev_key` and `dev_secret` before generating API calls.

## Quick Reference — All Endpoints

| Operation | Method | Path |
|-----------|--------|------|
| Send OTP (platform-generated) | `POST` | `/v1/messages` |
| Send OTP (custom code) | `POST` | `/v1/codes` |
| Verify OTP | `POST` | `/v1/verifications` |
| Send custom message | `POST` | `/v1/custom-messages` |
| List templates | `GET` | `/v1/template-configs` |
| Get template details | `GET` | `/v1/template-configs/:templateId` |
| Create template | `POST` | `/v1/template-configs` |
| Delete template | `DELETE` | `/v1/template-configs/:templateId` |

## OTP Send (Platform-Generated Code)

Use this when you want **EngageLab to generate** the verification code and deliver it according to the template's channel strategy (SMS, WhatsApp, Email, Voice).

**Endpoint**: `POST /v1/messages`

### Request Body

```json
{
  "to": "+6591234567",
  "template": {
    "id": "test-template-1",
    "language": "default",
    "params": {
      "key1": "value1"
    }
  }
}
```

### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `to` | `string` | Yes | Phone number (with country code, e.g., `+6581234567`) or email address |
| `template.id` | `string` | Yes | Template ID |
| `template.language` | `string` | No | Language: `default`, `zh_CN`, `zh_HK`, `en`, `ja`, `th`, `es`. Defaults to `default` |
| `template.params` | `object` | No | Custom template variable values as key-value pairs |

### Notes on `params`

- Preset variables like `{{brand_name}}`, `{{ttl}}`, `{{pwa_url}}` are auto-filled from template settings — no need to pass them.
- For custom variables in the template (e.g., `Hi {{name}}, your code is {{code}}`), pass values via params: `{"name": "Bob"}`.
- If the template's `from_id` field is preset and you pass `{"from_id": "12345"}`, the preset value is overridden.

### Response

**Success**:

```json
{
  "message_id": "1725407449772531712",
  "send_channel": "sms"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `message_id` | `string` | Unique message ID, used for verification and tracking |
| `send_channel` | `string` | Current delivery channel: `whatsapp`, `sms`, `email`, or `voice` |

The `send_channel` indicates the initial channel — if fallback is configured (e.g., WhatsApp → SMS), the final delivery channel may differ.

For error codes, read `references/error-codes.md`.

## Custom OTP Send (User-Generated Code)

Use this when you want to **generate the verification code yourself** and have EngageLab deliver it. This API does not generate codes and does not require calling the Verify API afterward.

**Endpoint**: `POST /v1/codes`

### Request Body

```json
{
  "to": "+6591234567",
  "code": "398210",
  "template": {
    "id": "test-template-1",
    "language": "default",
    "params": {
      "key1": "value1"
    }
  }
}
```

### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `to` | `string` | Yes | Phone number or email address |
| `code` | `string` | Yes | Your custom verification code |
| `template.id` | `string` | Yes | Template ID |
| `template.language` | `string` | No | Language (same options as OTP Send). Defaults to `default` |
| `template.params` | `object` | No | Custom template variable values |

### Response

Same format as OTP Send — returns `message_id` and `send_channel`.

## OTP Verify

Validate a verification code that was sent via the OTP Send API (`/v1/messages`). Only applicable to platform-generated codes — not needed for Custom OTP Send.

**Endpoint**: `POST /v1/verifications`

### Request Body

```json
{
  "message_id": "1725407449772531712",
  "verify_code": "667090"
}
```

### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message_id` | `string` | Yes | The `message_id` returned by `/v1/messages` |
| `verify_code` | `string` | Yes | The code the user entered |

### Response

**Success**:

```json
{
  "message_id": "1725407449772531712",
  "verify_code": "667090",
  "verified": true
}
```

| Field | Type | Description |
|-------|------|-------------|
| `message_id` | `string` | Message ID |
| `verify_code` | `string` | The submitted code |
| `verified` | `boolean` | `true` = valid, `false` = invalid |

**Important**: Successfully verified codes cannot be verified again — subsequent attempts will fail. Expired codes return error `3003`.

## Custom Messages Send

Send custom template content (verification codes, notifications, or marketing messages) using templates created on the OTP platform.

**Endpoint**: `POST /v1/custom-messages`

### Request Body

```json
{
  "to": "+6591234567",
  "template": {
    "id": "test-template-1",
    "params": {
      "code": "123456",
      "var1": "value1"
    }
  }
}
```

### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `to` | `string` or `string[]` | Yes | Single recipient (string) or multiple (array). Phone number or email |
| `template.id` | `string` | Yes | Template ID |
| `template.params` | `object` | No | Template variable values |
| `template.params.code` | `string` | Conditional | Required if template type is verification code |

### Notes on `params`

- Preset variables (`{{brand_name}}`, `{{ttl}}`, `{{pwa_url}}`) are auto-replaced from template settings.
- For verification code templates, you **must** pass `{{code}}` or an error will occur.
- Custom variables need values via params, e.g., `{"name": "Bob"}` for `Hi {{name}}`.

### Response

Same format as OTP Send — returns `message_id` and `send_channel`.

### Use Case Examples

**Verification code**:
```json
{
  "to": "+6591234567",
  "template": { "id": "code-template", "params": { "code": "123456" } }
}
```

**Notification**:
```json
{
  "to": ["+6591234567"],
  "template": { "id": "notification-template", "params": { "order": "123456" } }
}
```

**Marketing**:
```json
{
  "to": ["+6591234567"],
  "template": { "id": "marketing-template", "params": { "name": "EngageLab", "promotion": "30%" } }
}
```

## Template Management

OTP templates define the message content, channel strategy, and verification code settings. Templates support multi-channel delivery with fallback (e.g., WhatsApp → SMS).

For full request/response details including all channel configurations (WhatsApp, SMS, Voice, Email, PWA), read `references/template-api.md`.

### Quick Summary

**Create** — `POST /v1/template-configs`

```json
{
  "template_id": "my-template",
  "description": "Login verification",
  "send_channel_strategy": "whatsapp|sms",
  "brand_name": "MyApp",
  "verify_code_config": {
    "verify_code_type": 1,
    "verify_code_len": 6,
    "verify_code_ttl": 5
  },
  "sms_config": {
    "template_type": 1,
    "template_default_config": {
      "contain_security": false,
      "contain_expire": false
    }
  }
}
```

**List all** — `GET /v1/template-configs` (returns array of templates without detailed content)

**Get details** — `GET /v1/template-configs/:templateId` (returns full template with channel configs)

**Delete** — `DELETE /v1/template-configs/:templateId`

### Template Status

| Value | Status |
|-------|--------|
| 1 | Pending Review |
| 2 | Approved |
| 3 | Rejected |

### Channel Strategy

Use `|` to define fallback chains. Examples:
- `"sms"` — SMS only
- `"whatsapp|sms"` — Try WhatsApp first, fall back to SMS
- `"whatsapp|sms|email"` — WhatsApp → SMS → Email

Supported channels: `whatsapp`, `sms`, `voice`, `email`

### Verification Code Config

| Field | Range | Description |
|-------|-------|-------------|
| `verify_code_type` | 1–7 | 1=Numeric, 2=Lowercase, 4=Uppercase. Combine: 3=Numeric+Lowercase |
| `verify_code_len` | 4–10 | Code length |
| `verify_code_ttl` | 1–10 | Validity in minutes. With WhatsApp: only 1, 5, or 10 |

## Callback Configuration

Configure webhook URLs to receive real-time delivery status, notification events, message responses, and system events.

For the full callback data structures, security mechanisms, and event types, read `references/callback-config.md`.

## SMPP Integration

For TCP-based SMPP protocol integration (used in carrier-level SMS delivery), read `references/smpp-guide.md`.

## Generating Code

When the user asks to send OTPs or manage templates, generate working code. Default to `curl` unless the user specifies a language. Supported patterns:

- **curl** — Shell commands with proper auth header
- **Python** — Using `requests` library
- **Node.js** — Using `fetch` or `axios`
- **Java** — Using `HttpClient`
- **Go** — Using `net/http`

Always include the authentication header and proper error handling. Use placeholder values like `YOUR_DEV_KEY` and `YOUR_DEV_SECRET` if the user hasn't provided credentials.

### Python Example — Send OTP and Verify

```python
import requests
import base64

DEV_KEY = "YOUR_DEV_KEY"
DEV_SECRET = "YOUR_DEV_SECRET"
BASE_URL = "https://otp.api.engagelab.cc"

auth_string = base64.b64encode(f"{DEV_KEY}:{DEV_SECRET}".encode()).decode()
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {auth_string}"
}

# Step 1: Send OTP
send_resp = requests.post(f"{BASE_URL}/v1/messages", headers=headers, json={
    "to": "+6591234567",
    "template": {"id": "my-template", "language": "default"}
})
result = send_resp.json()
message_id = result["message_id"]

# Step 2: Verify OTP (after user enters the code)
verify_resp = requests.post(f"{BASE_URL}/v1/verifications", headers=headers, json={
    "message_id": message_id,
    "verify_code": "123456"
})
verification = verify_resp.json()
print(f"Verified: {verification['verified']}")
```
