# Website DNS - 1Panel API

## 模块说明
Website DNS 模块接口，用于管理 DNS 账户，支持通过 DNS API 自动验证域名所有权。

## 接口列表 (4 个)

---

### POST /websites/dns/search
**功能**: 分页查询 DNS 账户列表
**描述**: 获取所有 DNS 账户的分页列表

**参数 (Body)**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| page | int | 是 | 页码 | >= 1 |
| pageSize | int | 是 | 每页数量 | 1-100 |

**响应示例**:
```json
{
  "total": 10,
  "items": [
    {
      "id": 1,
      "name": "Cloudflare Account",
      "type": "cloudflare",
      "authorization": {...}
    }
  ]
}
```

---

### POST /websites/dns
**功能**: 创建 DNS 账户
**描述**: 添加新的 DNS 账户，用于自动 DNS 验证

**参数 (Body)**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| name | string | 是 | DNS 账户名称 | 最大 64 字符 |
| type | string | 是 | DNS 提供商类型 | 详见下方支持类型 |
| authorization | object | 是 | DNS API 授权信息 | 根据 type 不同而变化 |

**Authorization 参数 (根据 type 不同)**:

| type 类型 | authorization 字段 | 说明 |
|-----------|-------------------|------|
| cloudflare | api_key | Cloudflare API Key |
| aliyun | access_key_id, access_key_secret | 阿里云 AccessKey |
| tencent | secret_id, secret_key | 腾讯云 Secret |
| dnspod | id, token | DNSPod API Token |
| namesilo | key | Namesilo API Key |
| godaddy | key, secret | GoDaddy API Key/Secret |
| aws | access_key_id, secret_access_key | AWS Access Key |
| google | service_account_json | Google Cloud Service Account JSON |

**请求示例**:
```json
{
  "name": "My Cloudflare",
  "type": "cloudflare",
  "authorization": {
    "api_key": "your-cloudflare-api-key"
  }
}
```

---

### POST /websites/dns/update
**功能**: 更新 DNS 账户
**描述**: 修改已有的 DNS 账户信息

**参数 (Body)**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | DNS 账户 ID | > 0 |
| name | string | 是 | DNS 账户名称 | 最大 64 字符 |
| type | string | 是 | DNS 提供商类型 | 需与原类型一致 |
| authorization | object | 是 | DNS API 授权信息 | 根据 type 不同而变化 |

**请求示例**:
```json
{
  "id": 1,
  "name": "Updated Cloudflare",
  "type": "cloudflare",
  "authorization": {
    "api_key": "your-new-cloudflare-api-key"
  }
}
```

---

### POST /websites/dns/del
**功能**: 删除 DNS 账户
**描述**: 删除指定的 DNS 账户

**参数 (Body)**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | DNS 账户 ID | > 0 |

**请求示例**:
```json
{
  "id": 1
}
```

---

## 错误响应格式

所有接口的错误响应格式如下：

```json
{
  "code": 400,
  "message": "错误描述信息"
}
```

## 常用状态码

| code | 说明 |
|------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 500 | 服务器内部错误 |
