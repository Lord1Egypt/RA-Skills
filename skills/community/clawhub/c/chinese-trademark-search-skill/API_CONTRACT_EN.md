# Proprietary Platform API Contract

This document describes the open contract for the "proprietary trademark SaaS platform API," not the upstream trademark data provider interface contract.

All requests are sent by the Skill to the platform API, which then handles binding, points, modules, auditing, and upstream data access internally.

## General Conventions

### Base URL

```text
{CHINA_TM_PLATFORM_BASE_URL}
```

### Authorization Header

```http
Authorization: Bearer {CHINA_TM_USER_TOKEN}
```

### Content-Type

```http
Content-Type: application/json
```

### Idempotency Header (Billing Reliability)

Clients may send an `X-OC-Request-Id` header (8-64 characters, charset `[A-Za-z0-9_-]`) as an idempotency key; reusing the same ID on network retries will not cause double charges. The CLI handles this automatically.

```http
X-OC-Request-Id: req_a1B2c3D4e5F6
```

### Automatic Refund on Failure

- Failed searches (upstream errors) are automatically refunded; the API returns 500 `SERVER_ERROR` with `refundedPoints` in the body
- Failed detail lookups (upstream errors) are automatically refunded; the API returns 502 `UPSTREAM_ERROR`
- Failed export job creation is automatically refunded

> **A refund releases the idempotency key.** The platform de-duplicates on `X-OC-Request-Id` permanently. If the key survived a refund, a client retrying with the same ID would hit de-duplication and receive the result without being charged (and because the detail key is bound to the tmid, that trademark would be free forever). So on a successful refund the platform renames the corresponding `usage_events.request_id` to release it: **a retry after a refund is charged normally**, while a retry without a refund is still protected from double charging by the original key.

### Insufficient Points (HTTP 402)

When points are insufficient, the API returns HTTP 402 with this body:

```json
{
  "success": false,
  "error": {
    "code": "POINTS_NOT_ENOUGH",
    "message": "点数不足，请先充值",
    "rechargeUrl": "https://tm.zhengquai.com/billing"
  }
}
```

---

## 1. GET /v1/openclaw/capabilities

Retrieve the current user's binding status, points balance, metering hints, and available capabilities.

### Request Example

```http
GET /v1/openclaw/capabilities HTTP/1.1
Authorization: Bearer tmu_demo_user_token
```

### Response Example

```json
{
  "success": true,
  "user": {
    "userId": "usr_20260310_001",
    "organizationId": "org_20260310_001",
    "organizationName": "Chongqing Huayuan Intellectual Property Services Co., Ltd.",
    "bound": true
  },
  "wallet": {
    "totalPoints": 86,
    "giftedPoints": 18,
    "paidPoints": 68
  },
  "metering": {
    "search": { "estimatedPoints": 1, "label": "Search costs an estimated 1 point" },
    "detail": { "estimatedPoints": 2, "label": "Detail lookup costs an estimated 2 points" },
    "exportTiers": [
      { "min": 1, "max": 10, "points": 1 },
      { "min": 11, "max": 50, "points": 3 },
      { "min": 51, "max": 100, "points": 5 },
      { "min": 101, "max": null, "points": 10 }
    ]
  },
  "billing": {
    "pointsPerYuan": 5,
    "rechargeUrl": "https://tm.zhengquai.com/billing"
  },
  "featureEntitlements": [
    { "code": "renew_monitor", "name": "Renewal Monitoring", "enabled": true },
    { "code": "notifications", "name": "Notifications", "enabled": true },
    { "code": "miniapp", "name": "WeChat Mini Program", "enabled": false }
  ]
}
```

---

## 2. POST /v1/openclaw/trademarks/search

Execute a trademark search. Each search costs 1 point and always returns the first page of up to 50 results.

**Pagination is not currently supported**: passing `page` greater than 1 returns a `PAGINATION_NOT_SUPPORTED` error and no points are charged.

### Request Example

```json
{
  "query": "Chongqing Huayuan Technology Co., Ltd.",
  "page": 1,
  "pageSize": 50,
  "channel": "clawhub"
}
```

### Response Example

```json
{
  "success": true,
  "queryId": "qry_20260310_0008",
  "query": "Chongqing Huayuan Technology Co., Ltd.",
  "page": 1,
  "pageSize": 50,
  "total": 3,
  "estimatedPoints": 1,
  "chargedPoints": 1,
  "remainingPoints": 85,
  "results": [
    {
      "tmid": "tm_20260310_0001",
      "markName": "华源智造",
      "applicationNo": "2024101234567",
      "registrationNo": "78123456",
      "applicantName": "Chongqing Huayuan Technology Co., Ltd.",
      "classNo": 9,
      "className": "Scientific Instruments",
      "status": "Registered",
      "applyDate": "2024-01-18",
      "exclusivePeriodEnd": "2035-05-27"
    },
    {
      "tmid": "tm_20260310_0002",
      "markName": "华源云盾",
      "applicationNo": "2024101234789",
      "registrationNo": "78127890",
      "applicantName": "Chongqing Huayuan Technology Co., Ltd.",
      "classNo": 42,
      "className": "Web Services",
      "status": "Preliminary Announcement",
      "applyDate": "2024-02-06",
      "exclusivePeriodEnd": null
    },
    {
      "tmid": "tm_20260310_0003",
      "markName": "HYMATRIX",
      "applicationNo": "2024101234999",
      "registrationNo": "78129999",
      "applicantName": "Chongqing Huayuan Technology Co., Ltd.",
      "classNo": 35,
      "className": "Advertising & Sales",
      "status": "Registered",
      "applyDate": "2024-02-20",
      "exclusivePeriodEnd": "2035-06-08"
    }
  ]
}
```

### Insufficient Points Example (HTTP 402)

```json
{
  "success": false,
  "error": {
    "code": "POINTS_NOT_ENOUGH",
    "message": "点数不足，请先充值",
    "rechargeUrl": "https://tm.zhengquai.com/billing"
  }
}
```

### Pagination Not Supported Example (no points charged)

```json
{
  "success": false,
  "error": {
    "code": "PAGINATION_NOT_SUPPORTED",
    "message": "Pagination is not currently supported. Each search returns the first page of up to 50 results."
  }
}
```

### Search Failure Auto-Refund Example (HTTP 500)

```json
{
  "success": false,
  "refundedPoints": 1,
  "error": {
    "code": "SERVER_ERROR",
    "message": "Upstream search error. The charged points have been automatically refunded."
  }
}
```

### Not Bound Example

```json
{
  "success": false,
  "error": {
    "code": "BIND_REQUIRED",
    "message": "This account has not completed platform binding."
  }
}
```

---

## 3. GET /v1/openclaw/trademarks/{tmid}

Retrieve details for a specific trademark. Each trademark detail costs 2 points (two upstream calls are required); **viewing a trademark whose detail was already purchased is not charged again**. Upstream failures are automatically refunded with a 502 `UPSTREAM_ERROR` response.

### Request Example

```http
GET /v1/openclaw/trademarks/tm_20260310_0001 HTTP/1.1
Authorization: Bearer tmu_demo_user_token
```

### Response Example

```json
{
  "success": true,
  "estimatedPoints": 2,
  "chargedPoints": 2,
  "alreadyPurchased": false,
  "remainingPoints": 84,
  "trademark": {
    "tmid": "tm_20260310_0001",
    "markName": "华源智造",
    "applicationNo": "2024101234567",
    "registrationNo": "78123456",
    "applicantName": "Chongqing Huayuan Technology Co., Ltd.",
    "agentName": "Chongqing Huayuan Intellectual Property Services Co., Ltd.",
    "classNo": 9,
    "className": "Scientific Instruments",
    "status": "Registered",
    "applyDate": "2024-01-18",
    "announcementDate": "2025-02-27",
    "registrationDate": "2025-05-28",
    "exclusivePeriodStart": "2025-05-28",
    "exclusivePeriodEnd": "2035-05-27",
    "goods": [
      "Downloadable computer software",
      "Recorded computer programs",
      "Interface cards for smart terminals"
    ],
    "riskSummary": {
      "renewalStatus": "Renewal period is far away",
      "monitorSupported": true
    }
  }
}
```

---

## 4. POST /v1/openclaw/trademarks/export

Create an export job. Failed export job creation is automatically refunded.

### Request Example

```json
{
  "queryId": "qry_20260310_0008",
  "selectedTmids": [
    "tm_20260310_0001",
    "tm_20260310_0002",
    "tm_20260310_0003"
  ],
  "channel": "clawhub"
}
```

### Response Example

```json
{
  "success": true,
  "exportJobId": "exp_20260310_0003",
  "status": "queued",
  "selectedCount": 3,
  "estimatedPoints": 1,
  "chargedPoints": 1,
  "remainingPoints": 83,
  "message": "Export job created. Please check export status shortly."
}
```

### Module Not Enabled Example

```json
{
  "success": false,
  "error": {
    "code": "FEATURE_NOT_ENABLED",
    "message": "Module not enabled: Company Page / Client Page"
  }
}
```

---

## 5. GET /v1/openclaw/exports/{exportJobId}

Check export job status.

### Request Example

```http
GET /v1/openclaw/exports/exp_20260310_0003 HTTP/1.1
Authorization: Bearer tmu_demo_user_token
```

### Response Example

```json
{
  "success": true,
  "exportJobId": "exp_20260310_0003",
  "status": "completed",
  "fileName": "Chongqing_Huayuan_Technology_trademark_export_2026-03-10.csv",
  "downloadUrl": "https://tm.zhengquai.com/downloads/exp_20260310_0003.csv",
  "createdAt": "2026-03-10T09:18:00+08:00",
  "completedAt": "2026-03-10T09:18:12+08:00"
}
```

### Processing Example

```json
{
  "success": true,
  "exportJobId": "exp_20260310_0003",
  "status": "processing",
  "fileName": null,
  "downloadUrl": null,
  "createdAt": "2026-03-10T09:18:00+08:00",
  "completedAt": null
}
```

---

## 6. GET /v1/openclaw/modules

Retrieve available modules for the current user or organization.

### Request Example

```http
GET /v1/openclaw/modules HTTP/1.1
Authorization: Bearer tmu_demo_user_token
```

### Response Example

```json
{
  "success": true,
  "modules": [
    {
      "code": "renew_monitor",
      "name": "Renewal Monitoring",
      "enabled": true,
      "description": "Monitor trademark expiration and renewal risks"
    },
    {
      "code": "notifications",
      "name": "Notifications",
      "enabled": true,
      "description": "Enable email, SMS, or in-app notification capabilities"
    },
    {
      "code": "miniapp",
      "name": "WeChat Mini Program",
      "enabled": false,
      "description": "WeChat Mini Program access capability"
    },
    {
      "code": "companies_page",
      "name": "Company Page / Client Page",
      "enabled": false,
      "description": "Client company perspective for trademark aggregation and operations"
    },
    {
      "code": "external_monitor",
      "name": "External Monitoring",
      "enabled": false,
      "description": "Competitor and target company external monitoring"
    },
    {
      "code": "white_label",
      "name": "White-Label Portal",
      "enabled": false,
      "description": "Branded portal and white-label configuration capability"
    }
  ]
}
```

---

## 7. GET /v1/openclaw/bind/help

Retrieve binding instructions.

### Request Example

```http
GET /v1/openclaw/bind/help HTTP/1.1
Authorization: Bearer tmu_demo_user_token
```

### Response Example

```json
{
  "success": true,
  "bound": false,
  "bindUrl": "https://tm.zhengquai.com",
  "registerUrl": "https://tm.zhengquai.com/register",
  "apiKeysUrl": "https://tm.zhengquai.com/settings/api-keys",
  "rechargeUrl": "https://tm.zhengquai.com/billing",
  "steps": [
    "访问 https://tm.zhengquai.com/register 注册账号并创建组织",
    "登录后进入设置页生成 API Key（tmu_ 前缀，仅显示一次）",
    "将 API Key 配置为环境变量 CHINA_TM_USER_TOKEN",
    "将 CHINA_TM_PLATFORM_BASE_URL 配置为 https://tm.zhengquai.com",
    "重试 capabilities 验证绑定状态"
  ],
  "trialNotice": "新注册组织赠送 100 点体验点（90 天有效）；点数用完可在充值页充值，¥1 = 5 点"
}
```

> The `steps` and `trialNotice` fields are returned by the platform in Chinese. In English: register at `https://tm.zhengquai.com/register`, generate an API Key on the settings page after logging in (`tmu_` prefix, shown only once), set it as `CHINA_TM_USER_TOKEN`, set `CHINA_TM_PLATFORM_BASE_URL` to `https://tm.zhengquai.com`, then retry `capabilities`. New organizations receive 10 trial points (valid for 30 days); top up at the billing page, 1 CNY = 5 points.

---

## Error Codes Reference

| Code | Meaning |
|---|---|
| `ENV_MISSING` | Required environment variable is missing |
| `HTTPS_REQUIRED` | Base URL must use HTTPS |
| `BIND_REQUIRED` | Platform account binding is required |
| `POINTS_NOT_ENOUGH` | Insufficient points (HTTP 402, body includes `rechargeUrl`) |
| `PAGINATION_NOT_SUPPORTED` | Pagination is not currently supported (`page` > 1, no points charged) |
| `FEATURE_NOT_ENABLED` | Module is not enabled |
| `UNAUTHORIZED` | Token is invalid or expired |
| `FORBIDDEN` | Current user does not have access to this resource |
| `RATE_LIMITED` | Too many requests |
| `UPSTREAM_TIMEOUT` | Platform API timed out |
| `UPSTREAM_ERROR` | Upstream error (HTTP 502, charged detail points are automatically refunded) |
| `SERVER_ERROR` | Platform internal error (failed searches are automatically refunded; body includes `refundedPoints`) |
| `EXPORT_TIMEOUT` | Export status polling exceeded maximum attempts |
