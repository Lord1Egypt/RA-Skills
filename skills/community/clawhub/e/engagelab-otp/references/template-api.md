# OTP Template API Reference

Detailed request/response specifications for OTP template management endpoints.

## Table of Contents

1. [Create Template](#1-create-template)
2. [Delete Template](#2-delete-template)
3. [List All Templates](#3-list-all-templates)
4. [Get Template Details](#4-get-template-details)

---

## 1. Create Template

`POST /v1/template-configs`

### Request Body

```json
{
  "template_id": "test-template-1",
  "description": "Test Template 1",
  "send_channel_strategy": "whatsapp|sms",
  "brand_name": "Brand Name",
  "verify_code_config": {
    "verify_code_type": 1,
    "verify_code_len": 6,
    "verify_code_ttl": 1
  },
  "whatsapp_config": {
    "template_type": 1,
    "template_default_config": {
      "contain_security": false,
      "contain_expire": false
    }
  },
  "sms_config": {
    "template_type": 2,
    "template_default_config": {
      "contain_security": false,
      "contain_expire": false
    },
    "template_custom_config": {
      "custom_sub_type": "authentication",
      "custom_content": "Your code is {{code}}",
      "custom_country_codes": "HK,PH"
    }
  },
  "voice_config": {
    "template_type": 1,
    "template_default_config": {
      "contain_security": false,
      "contain_expire": false
    }
  },
  "email_config": {
    "template_name": "Email Template Name",
    "template_custom_configs": [{
      "language": "default",
      "pre_from_name": "MyApp",
      "pre_from_mail": "noreply@myapp.com",
      "pre_subject": "Your verification code",
      "template_content": "Hi {{name}}, your verification code is {{code}}",
      "pre_param_map": {
        "name": "User"
      }
    }]
  },
  "pwa_config": {
    "pwa_platform": "xx",
    "pwa_code": "xx"
  }
}
```

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `template_id` | String | Yes | Custom template ID, unique within app. Max 128 chars |
| `description` | String | No | Template description, max 255 chars |
| `send_channel_strategy` | String | Yes | Channel strategy. Single: `whatsapp`, `sms`, `email`, `voice`. Use `\|` for fallback chains (e.g., `whatsapp\|sms`) |
| `brand_name` | String | No | Brand signature, 2–10 chars. Replaces `{{brand_name}}` in templates |
| `verify_code_config` | Object | Conditional | Required when template includes verification codes |
| `verify_code_config.verify_code_type` | Integer | Yes | Code type, range [1,7]. 1=Numeric, 2=Lowercase, 4=Uppercase. Combinable (3=Numeric+Lowercase) |
| `verify_code_config.verify_code_len` | Integer | Yes | Code length, range [4,10] |
| `verify_code_config.verify_code_ttl` | Integer | Yes | Validity in minutes, range [1,10]. With WhatsApp: only 1, 5, or 10 |

### WhatsApp Config

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `whatsapp_config.template_type` | Integer | Yes | Fixed value `1` (default template only) |
| `whatsapp_config.template_default_config.contain_security` | Boolean | Yes | Include security reminder |
| `whatsapp_config.template_default_config.contain_expire` | Boolean | Yes | Include expiration content |

### SMS Config

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sms_config.template_type` | Integer | Yes | 1=Default Template, 2=Custom Template |
| `sms_config.template_default_config` | Object | Conditional | Required for default template type (type=1) |
| `sms_config.template_default_config.contain_security` | Boolean | Yes | Include security reminder |
| `sms_config.template_default_config.contain_expire` | Boolean | Yes | Include expiration content |
| `sms_config.template_custom_config` | Object | Conditional | Required for custom template type (type=2) |
| `sms_config.template_custom_config.custom_sub_type` | String | Yes | `authentication` (verification code), `marketing`, or `utility` (notification) |
| `sms_config.template_custom_config.custom_content` | String | Yes | Template content. For `authentication` type, must include `{{code}}` |
| `sms_config.template_custom_config.custom_country_codes` | String | No | Target country codes (comma-separated), used during template review |

### Voice Config

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `voice_config.template_type` | Integer | Yes | Fixed value `1` (default template only) |
| `voice_config.template_default_config.contain_security` | Boolean | Yes | Include security reminder |
| `voice_config.template_default_config.contain_expire` | Boolean | Yes | Include expiration content |

### Email Config

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `email_config.template_name` | String | Yes | Email template name |
| `email_config.template_custom_configs` | Array | Conditional | Array of language-specific email configs |
| `.language` | String | Yes | Language: `default`, `zh_CN`, `zh_HK`, `en`, `ja`, `th`, `es` |
| `.pre_from_name` | String | No | Preset sender name |
| `.pre_from_mail` | String | Yes | Preset sender email |
| `.pre_subject` | String | Yes | Preset email subject |
| `.template_content` | String | Yes | Email content (supports HTML). Variables use `{{var}}` syntax |
| `.pre_param_map` | Object | No | Default values for template variables (key-value pairs, values must be strings) |

### PWA Config (Optional)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `pwa_config.pwa_platform` | String | No | PWA platform (contact technical support for values) |
| `pwa_config.pwa_code` | String | No | Code in the PWA platform |

### Response

**Success**:

```json
{
  "code": 0,
  "message": "success"
}
```

**Failure**:

```json
{
  "code": 3003,
  "message": "not contains any channel config"
}
```

---

## 2. Delete Template

`DELETE /v1/template-configs/:templateId`

The `{templateId}` in the URL is the custom template ID defined when creating the template.

No request body required.

### Response

**Success**:

```json
{
  "code": 0,
  "message": "success"
}
```

**Failure** (template not found):

```json
{
  "code": 4001,
  "message": "config not exist"
}
```

---

## 3. List All Templates

`GET /v1/template-configs`

No request parameters. Returns a brief list of all templates (excludes detailed channel content). Use the Get Template Details endpoint for full configuration.

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `template_id` | String | Custom template ID |
| `description` | String | Template description |
| `send_channel_strategy` | String | Channel strategy with `\|` fallback notation |
| `brand_name` | String | Brand name |
| `verify_code_config` | Object | Verification code settings (if applicable) |
| `whatsapp_config` | Object | WhatsApp config summary |
| `sms_config` | Object | SMS config summary (includes `template_parts` for billing) |
| `voice_config` | Object | Voice config summary |
| `email_config` | Object | Email config summary (template name only) |
| `pwa_config` | Object | PWA config (if applicable) |
| `created_time` | Integer | Creation timestamp (seconds) |
| `status` | Integer | 1=Pending Review, 2=Approved, 3=Rejected |
| `audit_remark` | String | Review remarks (e.g., rejection reason) |

### Example Response

```json
[{
  "template_id": "test-template-1",
  "description": "Test Template 1",
  "send_channel_strategy": "whatsapp|sms",
  "brand_name": "Brand Name",
  "verify_code_config": {
    "verify_code_type": 1,
    "verify_code_len": 6,
    "verify_code_ttl": 1
  },
  "sms_config": {
    "template_type": 2,
    "template_parts": 1
  },
  "created_time": 1234567890,
  "status": 2,
  "audit_remark": ""
}]
```

The `template_parts` field in `sms_config` indicates estimated billing parts — if the template content is long, billing = parts × unit price.

---

## 4. Get Template Details

`GET /v1/template-configs/:templateId`

Returns the full template configuration including detailed channel configs (custom template content, email HTML, etc.).

### Response

The response includes all fields from the List endpoint plus detailed channel configurations:

- `sms_config.template_custom_config` — Custom SMS content and sub-type
- `email_config.template_custom_configs` — Full email template configs per language
- All other channel configs with their detailed settings

### Example Response

```json
{
  "template_id": "test-template-1",
  "description": "Test Template 1",
  "send_channel_strategy": "whatsapp|sms",
  "brand_name": "Brand Name",
  "verify_code_config": {
    "verify_code_type": 1,
    "verify_code_len": 6,
    "verify_code_ttl": 1
  },
  "sms_config": {
    "template_type": 2,
    "template_parts": 1,
    "template_custom_config": {
      "custom_sub_type": "authentication",
      "custom_content": "Your code is {{code}}"
    }
  },
  "email_config": {
    "template_name": "Email Template Name",
    "template_custom_configs": [{
      "language": "default",
      "pre_from_name": "MyApp",
      "pre_from_mail": "noreply@myapp.com",
      "pre_subject": "Your verification code",
      "template_content": "Hi {{name}}, your code is {{code}}",
      "pre_param_map": {
        "name": "User"
      }
    }]
  },
  "created_time": 1234567890,
  "status": 2,
  "audit_remark": ""
}
```

**Failure** (template not found):

```json
{
  "code": 4001,
  "message": "config not exist"
}
```
