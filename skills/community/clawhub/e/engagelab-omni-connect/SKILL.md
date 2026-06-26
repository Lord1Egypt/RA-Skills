---
name: engagelab-omni-connect
description: EngageLab Omnichannel communications tool (SMS, WhatsApp, Email) with template management and messaging capabilities.
metadata:
  openclaw:
    requires:
      env:
        - ENGAGELAB_SMS_KEY
        - ENGAGELAB_SMS_SECRET
        - ENGAGELAB_WA_KEY
        - ENGAGELAB_WA_SECRET
        - ENGAGELAB_EMAIL_API_USER
        - ENGAGELAB_EMAIL_API_KEY
---

# EngageLab Omni-Connect

## Instructions  
You are a communication specialist. Choose the appropriate channel based on user needs:

1. **SMS**: Used for sending short, urgent verification codes or notifications. Call `POST /v1/sms/send`.  
2. **WhatsApp**: Used for sending rich media or interactive messages. Call `POST /v1/whatsapp/send`.  
3. **Email**: Used for sending long reports or formal notifications. Call `POST /v1/email/send`.

## Authentication  
All API requests must include an `Authorization` header.  

Format: `Basic ${Base64(dev_key:dev_secret)}`

- **SMS**: Use `ENGAGELAB_SMS_KEY` and `ENGAGELAB_SMS_SECRET`.  
- **WhatsApp**: Use `ENGAGELAB_WA_KEY` and `ENGAGELAB_WA_SECRET`.  
- **Email**: Use `ENGAGELAB_EMAIL_API_USER` and `ENGAGELAB_EMAIL_API_KEY`.

## API Definitions

### Send SMS
- Endpoint: `https://smsapi.engagelab.com/v1/messages`
- Method: POST
- Params: `to`, `from`,`template`

### Send WhatsApp
- Endpoint: `https://wa.api.engagelab.cc/v1/messages`
- Method: POST
- Params: `to`, `from`, `body`

### Send Email
- Endpoint: `https://email.api.engagelab.cc/v1/mail/send` or `https://emailapi-tr.engagelab.com`
- Method: POST
- Params: `to`, `from`, `body`


# EngageLab SMS Template Skill

## Product Summary
This skill enables the discovery of pre-configured SMS templates. It is an essential precursor to sending messages, as it provides the necessary `template_id` and the specific variable placeholders (e.g., `{order_no}`) required for the sending payload.

**Base URL**: `https://smsapi.engagelab.com`

## APIs

### 1. List Template Configs
Retrieve all template configurations under the current account.
- **Method**: `GET`
- **Path**: `/v1/template-configs`
- **Auth**: Required (Basic Auth)

### 2. Get Template Details
Retrieve detailed configuration for a specific template.
- **Method**: `GET`
- **Path**: `/v1/template-configs/{templateId}`
- **Auth**: Required (Basic Auth)

## Response Example
```json
{
  "template_id": "123456789",
  "template_name": "Order Notification",
  "template_content": "Your order {order_no} has shipped.",
  "status": 2,
  "sign_name": "Company Name"
}
```

## Workflow
1. **Identify Template**: Search the list for the template matching the desired use case (e.g., "Verification").
2. **Examine Content**: Check `template_content` to identify all variables inside curly braces `{}`.
3. **Verify Status**: Ensure `status` is approved (typically `2`) before attempting to send.


# EngageLab SMS Sender Skill

## Product Summary
EngageLab SMS allows developers to send transactional and marketing SMS via a simple REST API. All messages must be sent using pre-configured and approved templates.

**Endpoint**: `POST https://smsapi.engagelab.com/v1/messages`

## Usage Scenarios
- Sending verification codes (OTPs).
- Sending transactional notifications (order updates, alerts).
- Sending marketing messages.

## API Reference

### Headers
```http
Content-Type: application/json
Authorization: Basic ${base64(dev_key:dev_secret)}
```

### Request Body (JSON)
```json
{
    "to": [
        "923700056581"
    ],
    "template": {
        "id": "1233",
        "params": {
            "code": "039487"
        }
    }
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `to` | Array[String] | ✅ | Recipient phone numbers in E.164 format (e.g., `["+8618701235678"]`). |
| `template.id` | String | ✅ | The approved template ID. |
| `template.params` | Object | ❌ | Variables to substitute in the template (e.g., `{"code": "1234"}`). |

### Response (200 OK)
```json
{
  "plan_id": "1972...",
  "total_count": 1,
  "accepted_count": 1,
  "message_id": "1972..."
}
```

## Workflow
1. **Pull Template**: Use `engagelab-sms-template` to get the `template_id` and required `params`.
2. **Collect Data**: Get recipient numbers and variable values.
3. **Send**: Construct the JSON payload and POST to the endpoint.
4. **Verify**: Check `accepted_count` to ensure delivery acceptance.

## Common Gotchas
- **Format**: Always use E.164 format for `to` numbers.
- **Partial Success**: 200 OK can still mean some recipients failed. Compare `accepted_count` with `total_count`.
- **Variables**: If a variable is missing in `params`, the placeholder (e.g., `{{name}}`) is sent literally.

# EngageLab WhatsApp Template Skill

## Product Summary
This skill enables the management and discovery of pre-configured WhatsApp templates. It is an essential precursor to sending messages, as it provides the necessary template ID, name, language, category, components, and status. Templates must be approved before use.

**Base URL**: `https://wa.api.engagelab.cc/v1`

## APIs

### 1. List Templates
Retrieve all templates under the current WhatsApp Business Account.
- **Method**: `GET`
- **Path**: `/templates`
- **Auth**: Required (Basic Auth)
- **Params**: `name` (optional, fuzzy match), `language_code` (optional), `category` (optional: AUTHENTICATION, MARKETING, UTILITY), `status` (optional: APPROVED, PENDING, REJECTED, etc.)

### 2. Get Template Details
Retrieve detailed configuration for a specific template.
- **Method**: `GET`
- **Path**: `/templates/{template_id}`
- **Auth**: Required (Basic Auth)

### 3. Create Template
Add a new template for approval.
- **Method**: `POST`
- **Path**: `/templates`
- **Auth**: Required (Basic Auth)
- **Body**: JSON with `name`, `language`, `category`, `components` (array of HEADER, BODY, FOOTER, BUTTONS objects)

### 4. Update Template
Modify an existing template's components.
- **Method**: `PUT`
- **Path**: `/templates/{templateId}`
- **Auth**: Required (Basic Auth)
- **Body**: JSON with updated `components`

### 5. Delete Template
Remove a template (all language versions).
- **Method**: `DELETE`
- **Path**: `/templates/{template_name}`
- **Auth**: Required (Basic Auth)

## Response Example
```json
[
  {
    "id": "406979728071589",
    "name": "code",
    "language": "zh_CN",
    "status": "APPROVED",
    "category": "OTP",
    "components": [
      {
        "type": "HEADER",
        "format": "text",
        "text": "Registration Verification Code"
      },
      {
        "type": "BODY",
        "text": "Your verification code is {{1}}, please enter it within 5 minutes."
      }
    ]
  }
]
```

## Workflow
1. **Identify Template**: Use List Templates to find matching templates by name, language, category, or status.
2. **Examine Content**: Check `components` to identify placeholders (e.g., `{{1}}`) and required parameters.
3. **Verify Status**: Ensure `status` is "APPROVED" before using for sending.
4. **Create/Update if Needed**: Submit new or modified templates for Meta approval.
5. **Delete Unused**: Remove templates to manage limits.

# EngageLab WhatsApp Sender Skill

## Product Summary
EngageLab WhatsApp allows developers to send transactional and marketing messages via a simple REST API. Supports template, text, image, audio, video, document, and sticker messages. Proactive sends limited to approved templates.

**Endpoint**: `POST https://wa.api.engagelab.cc/v1/messages`

## Usage Scenarios
- Sending verification codes (OTPs) using templates.
- Delivering media-rich notifications (images, videos) in support or marketing.
- Interactive replies (text, stickers) within 24-hour window.

## API Reference

### Headers
```http
Content-Type: application/json
Authorization: Basic ${base64(dev_key:dev_secret)}
```

### Request Body (JSON)
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `from` | String | ❌ | Sender WhatsApp number (e.g., "+8613800138000"). Defaults to console setting. |
| `to` | Array[String] | ✅ | Recipient WhatsApp numbers (e.g., ["+447911123456"]). |
| `body` | Object | ✅ | Message content with `type` (template, text, image, etc.) and details. |
| `request_id` | String | ❌ | Custom tracking ID. |
| `custom_args` | Object | ❌ | Key-value pairs for callbacks. |

### Response (200 OK)
```json
{
  "message_id": "cbggf4if6o9ukqaalfug",
  "request_id": "your-sendno-string"
}
```

## Workflow
1. **Pull Template**: Use WhatsApp template skill for ID and components.
2. **Collect Data**: Get recipients, variables/media.
3. **Send**: Construct payload and POST to endpoint.
4. **Verify**: Check message_id for tracking.

## Common Gotchas
- Use approved templates for proactive sends.
- Include international codes in numbers.
- Media must meet format/size limits.
- Variables must match template placeholders.

# EngageLab Email Sender Skill

## Product Summary
EngageLab Email allows developers to send transactional and marketing emails via a REST API. Supports regular sends, templates, calendar invites, and MIME formats. Personalization via variables and Handlebars.

**Endpoint**: `POST https://email.api.engagelab.cc/v1/mail/send` (or Turkey: `https://emailapi-tr.engagelab.com`)

## Usage Scenarios
- Sending personalized transactional emails (confirmations, alerts).
- Bulk marketing campaigns with tracking.
- Calendar invitations for events.

## API Reference

### Headers
```http
Content-Type: application/json;charset=utf-8
Authorization: Basic ${base64(api_user:api_key)}
```

### Request Body (JSON)
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `from` | String | ✅ | Sender (e.g., "Team <support@engagelab.com>"). |
| `to` | Array[String] | ✅ | Recipients (max 100). |
| `subject` | String | ✅ | Email subject. |
| `body` | Object | ✅ | Content with `html`, `text`, etc. |
| `vars` | Object | ❌ | Variables for substitution. |

For templates: Use `/v1/mail/sendtemplate` with `template_invoke_name`.

### Response (200 OK)
```json
{
  "email_ids": ["1447054895514_15555555_32350_1350.sc-10_10_126_221-inbound0$111@qq.com"],
  "request_id": "<request_id>"
}
```

## Workflow
1. **Prepare Content**: Define subject, body, variables.
2. **Add Options**: Attachments, tracking, send_mode.
3. **Send**: POST to endpoint.
4. **Verify**: Check email_ids/task_id.

