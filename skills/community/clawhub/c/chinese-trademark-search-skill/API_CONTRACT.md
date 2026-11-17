# 自有平台 API 契约说明

本文档说明的是“自有商标 SaaS 平台 API”的开放契约，不是上游商标数据商接口契约。

所有请求均由 Skill 发往平台 API，再由平台自行处理绑定、点数、模块、审计与上游数据访问。

## 统一约定

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

### 幂等请求头（计费可靠性）

客户端可在请求头传 `X-OC-Request-Id`（8-64 位，字符集 `[A-Za-z0-9_-]`）作为幂等键；网络重试时复用同一 ID 不会重复扣点。CLI 已自动处理。

```http
X-OC-Request-Id: req_a1B2c3D4e5F6
```

### 失败自动退点

- 查询失败（上游异常）自动退点，返回 500 `SERVER_ERROR` 且 body 含 `refundedPoints`
- 详情上游失败自动退点，返回 502 `UPSTREAM_ERROR`
- 导出任务创建失败自动退点

> **退点会释放幂等键**：平台按 `X-OC-Request-Id` 永久去重，若退点后仍保留该键，客户端带同一 ID 重试就会命中去重、拿到结果却不扣点（详情的幂等键与 tmid 绑定，等于该商标永久免费）。因此退点成功后平台会把对应 `usage_events.request_id` 改名释放，**退点之后的重试按正常扣点处理**；未退点的重试仍由原键防重复扣。

### 点数不足（HTTP 402）

点数不足时返回 HTTP 402，body：

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

读取当前用户的绑定状态、点数余额、收费动作提示与可用能力。

### 请求示例

```http
GET /v1/openclaw/capabilities HTTP/1.1
Authorization: Bearer tmu_demo_user_token
```

### 响应示例

```json
{
  "success": true,
  "user": {
    "userId": "usr_20260310_001",
    "organizationId": "org_20260310_001",
    "organizationName": "重庆华源知识产权服务有限公司",
    "bound": true
  },
  "wallet": {
    "totalPoints": 86,
    "giftedPoints": 18,
    "paidPoints": 68
  },
  "metering": {
    "search": { "estimatedPoints": 1, "label": "查询预计消耗 1 点" },
    "detail": { "estimatedPoints": 2, "label": "详情预计消耗 2 点" },
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
    { "code": "renew_monitor", "name": "续展监控", "enabled": true },
    { "code": "notifications", "name": "通知提醒", "enabled": true },
    { "code": "miniapp", "name": "微信端", "enabled": false }
  ]
}
```

---

## 2. POST /v1/openclaw/trademarks/search

执行商标查询。每次查询扣 1 点，固定返回第一页前 50 条结果。

**翻页暂不支持**：`page` 大于 1 会返回 `PAGINATION_NOT_SUPPORTED` 错误且不扣点。

### 请求示例

```json
{
  "query": "重庆华源科技有限公司",
  "page": 1,
  "pageSize": 50,
  "channel": "clawhub"
}
```

### 响应示例

```json
{
  "success": true,
  "queryId": "qry_20260310_0008",
  "query": "重庆华源科技有限公司",
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
      "applicantName": "重庆华源科技有限公司",
      "classNo": 9,
      "className": "科学仪器",
      "status": "已注册",
      "applyDate": "2024-01-18",
      "exclusivePeriodEnd": "2035-05-27"
    },
    {
      "tmid": "tm_20260310_0002",
      "markName": "华源云盾",
      "applicationNo": "2024101234789",
      "registrationNo": "78127890",
      "applicantName": "重庆华源科技有限公司",
      "classNo": 42,
      "className": "网站服务",
      "status": "初审公告",
      "applyDate": "2024-02-06",
      "exclusivePeriodEnd": null
    },
    {
      "tmid": "tm_20260310_0003",
      "markName": "HYMATRIX",
      "applicationNo": "2024101234999",
      "registrationNo": "78129999",
      "applicantName": "重庆华源科技有限公司",
      "classNo": 35,
      "className": "广告销售",
      "status": "已注册",
      "applyDate": "2024-02-20",
      "exclusivePeriodEnd": "2035-06-08"
    }
  ]
}
```

### 点数不足示例（HTTP 402）

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

### 翻页不支持示例（不扣点）

```json
{
  "success": false,
  "error": {
    "code": "PAGINATION_NOT_SUPPORTED",
    "message": "暂不支持翻页，每次查询固定返回第一页前 50 条结果"
  }
}
```

### 查询失败自动退点示例（HTTP 500）

```json
{
  "success": false,
  "refundedPoints": 1,
  "error": {
    "code": "SERVER_ERROR",
    "message": "上游查询异常，已自动退回本次扣点"
  }
}
```

### 未绑定示例

```json
{
  "success": false,
  "error": {
    "code": "BIND_REQUIRED",
    "message": "当前账号尚未完成平台绑定"
  }
}
```

---

## 3. GET /v1/openclaw/trademarks/{tmid}

读取指定商标详情。每条商标详情扣 2 点（因需调用上游两次）；**同一商标已购详情后再次查看不重复扣点**。上游失败自动退点，返回 502 `UPSTREAM_ERROR`。

### 请求示例

```http
GET /v1/openclaw/trademarks/tm_20260310_0001 HTTP/1.1
Authorization: Bearer tmu_demo_user_token
```

### 响应示例

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
    "applicantName": "重庆华源科技有限公司",
    "agentName": "重庆华源知识产权服务有限公司",
    "classNo": 9,
    "className": "科学仪器",
    "status": "已注册",
    "applyDate": "2024-01-18",
    "announcementDate": "2025-02-27",
    "registrationDate": "2025-05-28",
    "exclusivePeriodStart": "2025-05-28",
    "exclusivePeriodEnd": "2035-05-27",
    "goods": [
      "可下载计算机软件",
      "已录制的计算机程序",
      "智能终端用接口卡"
    ],
    "riskSummary": {
      "renewalStatus": "距离续展期较远",
      "monitorSupported": true
    }
  }
}
```

---

## 4. POST /v1/openclaw/trademarks/export

创建导出任务。导出任务创建失败自动退点。

### 请求示例

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

### 响应示例

```json
{
  "success": true,
  "exportJobId": "exp_20260310_0003",
  "status": "queued",
  "selectedCount": 3,
  "estimatedPoints": 1,
  "chargedPoints": 1,
  "remainingPoints": 83,
  "message": "导出任务已创建，请稍后查询导出状态"
}
```

### 模块未开通示例

```json
{
  "success": false,
  "error": {
    "code": "FEATURE_NOT_ENABLED",
    "message": "模块未开通：公司页 / 客户页"
  }
}
```

---

## 5. GET /v1/openclaw/exports/{exportJobId}

查询导出任务状态。

### 请求示例

```http
GET /v1/openclaw/exports/exp_20260310_0003 HTTP/1.1
Authorization: Bearer tmu_demo_user_token
```

### 响应示例

```json
{
  "success": true,
  "exportJobId": "exp_20260310_0003",
  "status": "completed",
  "fileName": "重庆华源科技有限公司_商标导出_2026-03-10.csv",
  "downloadUrl": "https://tm.zhengquai.com/downloads/exp_20260310_0003.csv",
  "createdAt": "2026-03-10T09:18:00+08:00",
  "completedAt": "2026-03-10T09:18:12+08:00"
}
```

### 排队中示例

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

读取当前用户或组织可用模块。

### 请求示例

```http
GET /v1/openclaw/modules HTTP/1.1
Authorization: Bearer tmu_demo_user_token
```

### 响应示例

```json
{
  "success": true,
  "modules": [
    {
      "code": "renew_monitor",
      "name": "续展监控",
      "enabled": true,
      "description": "监控商标到期与续展风险"
    },
    {
      "code": "notifications",
      "name": "通知提醒",
      "enabled": true,
      "description": "开启邮件、短信或站内通知能力"
    },
    {
      "code": "miniapp",
      "name": "微信端",
      "enabled": false,
      "description": "微信小程序端访问能力"
    },
    {
      "code": "companies_page",
      "name": "公司页 / 客户页",
      "enabled": false,
      "description": "客户公司视角的商标归集与运营页"
    },
    {
      "code": "external_monitor",
      "name": "外部监控",
      "enabled": false,
      "description": "竞品与目标企业外部监控"
    },
    {
      "code": "white_label",
      "name": "白牌门户",
      "enabled": false,
      "description": "品牌化门户与白牌配置能力"
    }
  ]
}
```

---

## 7. GET /v1/openclaw/bind/help

读取绑定说明。

### 请求示例

```http
GET /v1/openclaw/bind/help HTTP/1.1
Authorization: Bearer tmu_demo_user_token
```

### 响应示例

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

---

## 错误码建议

| code | 含义 |
|---|---|
| `ENV_MISSING` | 环境变量缺失 |
| `BIND_REQUIRED` | 尚未绑定平台 |
| `POINTS_NOT_ENOUGH` | 点数不足（HTTP 402，body 含 `rechargeUrl`） |
| `PAGINATION_NOT_SUPPORTED` | 暂不支持翻页（`page` > 1，不扣点） |
| `FEATURE_NOT_ENABLED` | 模块未开通 |
| `UNAUTHORIZED` | token 无效或已过期 |
| `FORBIDDEN` | 当前用户无权访问该资源 |
| `RATE_LIMITED` | 请求过于频繁 |
| `UPSTREAM_TIMEOUT` | 平台接口超时 |
| `UPSTREAM_ERROR` | 上游异常（HTTP 502，详情已扣点自动退回） |
| `SERVER_ERROR` | 平台内部错误（查询失败自动退点，body 含 `refundedPoints`） |
