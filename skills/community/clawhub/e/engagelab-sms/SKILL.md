---
name: engagelab-sms
description: >
  Call EngageLab SMS REST APIs to send SMS messages and manage SMS templates and
  signatures (sender IDs). Use this skill whenever the user wants to send an SMS
  via EngageLab, create or manage SMS templates, configure sender ID signatures,
  or interact with any EngageLab SMS API endpoint. Also trigger when the user
  mentions "engagelab", "engagelab sms", "sms api", "send sms via api",
  "sms template management", "sender id", "sign config", or asks to integrate
  with the EngageLab messaging platform. This skill covers authentication,
  message sending, template CRUD, and signature CRUD — use it even if the user
  only needs one of these capabilities.
---

# EngageLab SMS API Skill

This skill enables you to interact with the EngageLab SMS REST API. It covers three areas:

1. **Send SMS** — Send notification or marketing SMS to one or more recipients
2. **Template Management** — Create, read, update, and delete SMS templates
3. **Signature (Sender ID) Management** — Create, read, update, and delete sender ID signatures

## Resources

### scripts/

- **`sms_client.py`** — Python client class (`EngageLabSMS`) wrapping all API endpoints: `send_sms()` (immediate and scheduled), template CRUD (`list_templates()`, `get_template()`, `create_template()`, `update_template()`, `delete_template()`), and signature CRUD (`list_signatures()`, `get_signature()`, `create_signature()`, `update_signature()`, `delete_signature()`). Handles authentication, request construction, and typed error handling. Use as a ready-to-run helper or import into the user's project.

### references/

- **`template-and-signature-api.md`** — Full request/response field specs for all template and signature endpoints
- **`error-codes.md`** — Complete error code tables for SMS sending and template/signature operations

## Authentication

All EngageLab SMS API calls use **HTTP Basic Authentication**.

- **Base URL**: `https://smsapi.engagelab.com`
- **Header**: `Authorization: Basic <base64(dev_key:dev_secret)>`
- **Content-Type**: `application/json`

The user must provide their `dev_key` and `dev_secret` (also called `apikey` and `apisecret`). Encode them as `base64("dev_key:dev_secret")` and set the `Authorization` header.

**Example** (using curl):

```bash
curl -X POST https://smsapi.engagelab.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic $(echo -n 'YOUR_DEV_KEY:YOUR_DEV_SECRET' | base64)" \
  -d '{ ... }'
```

If the user hasn't provided credentials, ask them for their `dev_key` and `dev_secret` before generating API calls.

## Quick Reference — All Endpoints

| Operation | Method | Path |
|-----------|--------|------|
| Send SMS | `POST` | `/v1/messages` |
| List templates | `GET` | `/v1/template-configs` |
| Get template | `GET` | `/v1/template-configs/:templateId` |
| Create template | `POST` | `/v1/template-configs` |
| Update template | `PUT` | `/v1/template-configs/:templateId` |
| Delete template | `DELETE` | `/v1/template-configs/:templateId` |
| List signatures | `GET` | `/v1/sign-configs` |
| Get signature | `GET` | `/v1/sign-configs/:signId` |
| Create signature | `POST` | `/v1/sign-configs` |
| Update signature | `PUT` | `/v1/sign-configs/:signId` |
| Delete signature | `DELETE` | `/v1/sign-configs/:signId` |

## Sending SMS

**Endpoint**: `POST /v1/messages`

### Request Body

```json
{
  "to": ["+6591234567"],
  "template": {
    "id": "TEMPLATE_ID",
    "params": {
      "var_name": "value"
    }
  },
  "plan_name": "Optional plan name",
  "schedule_time": 1700000000,
  "custom_args": {}
}
```

### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `to` | `string[]` | Yes | Target phone numbers (include country code) |
| `template.id` | `string` | Yes | ID of an approved SMS template |
| `template.params` | `object` | Yes | Key-value pairs matching template variables (e.g., `{{name}}` → `{"name": "Bob"}`) |
| `plan_name` | `string` | No | Plan name, defaults to `"-"` |
| `schedule_time` | `integer` | No | Unix timestamp for scheduled sends; omit for immediate |
| `custom_args` | `object` | No | Custom parameters for tracking |

### Template Variables

If the template contains `{{var}}` placeholders, populate them via `params`. For example, for template content `"Hi {{name}}, your code is {{code}}"`, pass:

```json
"params": { "name": "Alice", "code": "123456" }
```

Unpopulated variables are sent literally as `{{var}}`.

### Response

**Success (single target)**:

```json
{
  "plan_id": "1972488990548348928",
  "total_count": 1,
  "accepted_count": 1,
  "message_id": "1972488990804201472"
}
```

**Success (scheduled)**:

```json
{
  "plan_id": "1972492618659033088",
  "total_count": 1,
  "accepted_count": 1,
  "schedule_info": { "task_id": 1972492621368553472 }
}
```

**Error**: Contains `code` (non-zero) and `message` fields alongside `plan_id`.

For the full error code table, read `references/error-codes.md`.

## Template Management

Templates define the SMS content. Each template must pass review before it can be used for sending.

For full request/response details and field descriptions, read `references/template-and-signature-api.md`.

### Key Rules

- Template content **cannot** contain: `【`, `】`, `、`, `测试`, `test`, `[`, `]`
- After creation or update, templates enter **Pending Review** status (status=1) and cannot be used until **Approved** (status=2)
- Templates in Pending Review cannot be updated
- Templates tied to pending/running message plans cannot be updated or deleted
- Template types: `utility` (notification), `marketing` (marketing)

### CRUD Summary

**Create** — `POST /v1/template-configs`

```json
{
  "template_name": "Order Notification",
  "template_type": "utility",
  "template_content": "Your order {order_no} has shipped, arriving by {delivery_time}.",
  "country_codes": "CN,US",
  "add_signature": true,
  "sign_id": "SIGNATURE_ID",
  "sign_position": 2
}
```

**List all** — `GET /v1/template-configs` (returns array)

**Get one** — `GET /v1/template-configs/:templateId`

**Update** — `PUT /v1/template-configs/:templateId` (same body as create, all fields required)

**Delete** — `DELETE /v1/template-configs/:templateId`

## Signature (Sender ID) Management

Signatures identify the sender and are attached to templates. They also go through a review process.

For full request/response details and field descriptions, read `references/template-and-signature-api.md`.

### Key Rules

- Signature name: 2–60 characters, cannot contain `【`, `】`, `[`, `]`
- Names must be unique within the same business
- After creation or update, signatures enter **Pending Review** (status=1)
- Signatures in Pending Review cannot be updated
- Signatures tied to pending/running plans cannot be updated or deleted

### CRUD Summary

**Create** — `POST /v1/sign-configs`

```json
{ "sign_name": "MyCompany" }
```

**List all** — `GET /v1/sign-configs` (returns array)

**Get one** — `GET /v1/sign-configs/:signId`

**Update** — `PUT /v1/sign-configs/:signId` (same body as create)

**Delete** — `DELETE /v1/sign-configs/:signId`

## Generating Code

When the user asks to send SMS or manage templates/signatures, generate working code. Default to `curl` unless the user specifies a language. Supported patterns:

- **curl** — Shell commands with proper auth header
- **Python** — Using `requests` library
- **Node.js** — Using `fetch` or `axios`
- **Java** — Using `HttpClient`
- **Go** — Using `net/http`

Always include the authentication header and proper error handling. Use placeholder values like `YOUR_DEV_KEY` and `YOUR_DEV_SECRET` if the user hasn't provided credentials.

## Status Codes Reference

| Value | Template/Signature Status |
|-------|--------------------------|
| 1 | Pending Review |
| 2 | Approved |
| 3 | Rejected |

| Value | Signature Position |
|-------|-------------------|
| 0 | No Signature |
| 1 | Prefix |
| 2 | Suffix |

| Value | Template Type |
|-------|--------------|
| `utility` | Notification |
| `marketing` | Marketing |
