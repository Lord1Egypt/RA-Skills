# Template & Signature API Reference

Detailed request/response specifications for template and signature management endpoints.

## Table of Contents

1. [Template Configuration APIs](#template-configuration-apis)
   - [List Templates](#1-list-templates)
   - [Get Template Details](#2-get-template-details)
   - [Create Template](#3-create-template)
   - [Update Template](#4-update-template)
   - [Delete Template](#5-delete-template)
2. [Signature Configuration APIs](#signature-configuration-apis)
   - [List Signatures](#1-list-signatures)
   - [Get Signature Details](#2-get-signature-details)
   - [Create Signature](#3-create-signature)
   - [Update Signature](#4-update-signature)
   - [Delete Signature](#5-delete-signature)

---

## Template Configuration APIs

### 1. List Templates

`GET /v1/template-configs`

No request parameters. Returns an array of all templates.

**Response fields**:

| Field | Type | Description |
|-------|------|-------------|
| template_id | string | Template ID |
| template_name | string | Template name |
| template_type | string | `utility` (notification) or `marketing` |
| template_content | string | Template content with variable placeholders |
| country_codes | string | Target country codes, comma-separated |
| status | int | 1=Pending Review, 2=Approved, 3=Rejected |
| sign_id | string | Attached signature ID (optional) |
| sign_name | string | Attached signature name (optional) |
| sign_position | int | 0=None, 1=Prefix, 2=Suffix (optional) |
| sign_status | int | Signature status (optional) |
| audit_remark | string | Review remarks |
| created_time | int64 | Unix timestamp |
| updated_time | int64 | Unix timestamp |

**Example response**:

```json
[
  {
    "template_id": "123456789",
    "template_name": "Order Notification Template",
    "template_type": "utility",
    "template_content": "Your order {order_no} has been shipped and is expected to arrive by {delivery_time}.",
    "country_codes": "CN,US",
    "status": 2,
    "sign_id": "987654321",
    "sign_name": "Company Name",
    "sign_position": 2,
    "sign_status": 2,
    "audit_remark": "",
    "created_time": 1699000000,
    "updated_time": 1699000000
  }
]
```

### 2. Get Template Details

`GET /v1/template-configs/:templateId`

| Path Param | Type | Required | Description |
|------------|------|----------|-------------|
| templateId | string | Yes | Template ID |

Response fields same as List Templates (single object, not array).

**Errors**: `400` if template ID is invalid or template does not exist.

### 3. Create Template

`POST /v1/template-configs`

**Request body**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| template_name | string | Yes | Up to 255 characters |
| template_type | string | Yes | `utility` or `marketing` |
| template_content | string | Yes | Cannot contain: `【`, `】`, `、`, `测试`, `test`, `[`, `]` |
| country_codes | string | Yes | Comma-separated country codes |
| add_signature | bool | No | Whether to attach a signature (default: false) |
| sign_id | string | Conditional | Required if add_signature is true |
| sign_position | int | Conditional | Required if add_signature is true. 1=Prefix, 2=Suffix |

**Example request**:

```json
{
  "template_name": "Order Notification Template",
  "template_type": "utility",
  "template_content": "Your order {order_no} has been shipped and is expected to arrive by {delivery_time}.",
  "country_codes": "CN,US",
  "add_signature": true,
  "sign_id": "987654321",
  "sign_position": 2
}
```

**Response**: `{ "template_id": "123456789" }`

**Errors**: `400` for parameter errors, non-existent signature, or unapproved signature.

**Rules**:
- Template starts in Pending Review (status=1) after creation
- If adding a signature, the signature must already be Approved

### 4. Update Template

`PUT /v1/template-configs/:templateId`

| Path Param | Type | Required | Description |
|------------|------|----------|-------------|
| templateId | string | Yes | Template ID |

Request body is the same as Create — all fields are required.

**Response**: `{ "code": 0, "message": "success" }`

**Rules**:
- Cannot update templates in Pending Review status
- Cannot update templates tied to pending/running message plans
- After update, status reverts to Pending Review (status=1)

### 5. Delete Template

`DELETE /v1/template-configs/:templateId`

| Path Param | Type | Required | Description |
|------------|------|----------|-------------|
| templateId | string | Yes | Template ID |

**Response**: `{ "code": 0, "message": "success" }`

**Rules**: Cannot delete templates tied to pending/running message plans.

---

## Signature Configuration APIs

### 1. List Signatures

`GET /v1/sign-configs`

No request parameters. Returns an array of all signatures.

**Response fields**:

| Field | Type | Description |
|-------|------|-------------|
| sign_id | string | Signature ID |
| sign_name | string | Signature name |
| status | int | 1=Pending Review, 2=Approved, 3=Rejected |
| related_template_count | int64 | Number of templates using this signature |
| audit_remark | string | Review remarks |
| created_time | int64 | Unix timestamp |
| updated_time | int64 | Unix timestamp |

**Example response**:

```json
[
  {
    "sign_id": "987654321",
    "sign_name": "Company Name",
    "status": 2,
    "related_template_count": 5,
    "audit_remark": "",
    "created_time": 1699000000,
    "updated_time": 1699000000
  }
]
```

### 2. Get Signature Details

`GET /v1/sign-configs/:signId`

| Path Param | Type | Required | Description |
|------------|------|----------|-------------|
| signId | string | Yes | Signature ID |

Response fields same as List Signatures (single object, not array).

**Errors**: `400` if signature ID is invalid, does not exist, or does not belong to current business.

### 3. Create Signature

`POST /v1/sign-configs`

**Request body**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| sign_name | string | Yes | 2–60 characters, cannot contain `【`, `】`, `[`, `]` |

**Example request**: `{ "sign_name": "Company Name" }`

**Response**: `{ "sign_id": "987654321" }`

**Rules**:
- Signature starts in Pending Review (status=1) after creation
- Names must be unique within the same business

### 4. Update Signature

`PUT /v1/sign-configs/:signId`

| Path Param | Type | Required | Description |
|------------|------|----------|-------------|
| signId | string | Yes | Signature ID |

Request body same as Create.

**Response**: `{ "code": 0, "message": "success" }`

**Rules**:
- Cannot update signatures in Pending Review status
- Cannot update signatures tied to pending/running message plans
- After update, status reverts to Pending Review (status=1)

### 5. Delete Signature

`DELETE /v1/sign-configs/:signId`

| Path Param | Type | Required | Description |
|------------|------|----------|-------------|
| signId | string | Yes | Signature ID |

**Response**: `{ "code": 0, "message": "success" }`

**Rules**: Cannot delete signatures tied to pending/running message plans.
