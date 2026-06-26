# Website Acme - 1Panel API

## 模块说明
Website Acme 模块接口，用于管理 ACME 证书账户（Let's Encrypt、ZeroSSL 等）

## 接口列表 (4 个)

---

### POST /websites/acme/search
**功能**: Page website acme accounts - 分页获取 ACME 账户列表
**认证**: ApiKeyAuth, Timestamp
**日志**: -

**请求参数 (PageInfo)**:

| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| page | int | 是 | 页码 | > 0 |
| pageSize | int | 是 | 每页数量 | > 0 |

**返回示例**:
```json
{
  "total": 1,
  "items": [
    {
      "ID": 1,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z",
      "email": "admin@example.com",
      "url": "https://.api.letsencryptacme-v02.org/directory",
      "type": "letsencrypt",
      "keyType": "2048",
      "useProxy": false,
      "caDirURL": "",
      "eabKid": "",
      "eabHmacKey": "",
      "useEAB": false
    }
  ]
}
```

---

### POST /websites/acme
**功能**: Create website acme account - 创建 ACME 账户
**认证**: ApiKeyAuth, Timestamp
**日志**: 创建网站 acme [email]

**请求参数 (WebsiteAcmeAccountCreate)**:

| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| email | string | 是 | ACME 账户邮箱地址 | 有效的邮箱格式 |
| type | string | 是 | ACME 服务提供商类型 | `letsencrypt`, `zerossl`, `buypass`, `google`, `custom` |
| keyType | string | 是 | 密钥类型 | `P256`, `P384`, `2048`, `3072`, `4096`, `8192` |
| eabKid | string | 否 | EAB Key ID（外部账户绑定） | - |
| eabHmacKey | string | 否 | EAB HMAC Key（外部账户绑定） | - |
| useProxy | bool | 否 | 是否使用代理 | `true`, `false` |
| caDirURL | string | 否 | CA Directory URL（自定义 ACME 服务时使用） | - |
| useEAB | bool | 否 | 是否使用 EAB（外部账户绑定） | `true`, `false` |

**返回示例**:
```json
{
  "ID": 1,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",
  "email": "admin@example.com",
  "url": "https://acme-v02.api.letsencrypt.org/directory",
  "type": "letsencrypt",
  "keyType": "2048",
  "useProxy": false,
  "caDirURL": "",
  "eabKid": "",
  "eabHmacKey": "",
  "useEAB": false
}
```

---

### POST /websites/acme/del
**功能**: Delete website acme account - 删除 ACME 账户
**认证**: ApiKeyAuth, Timestamp
**日志**: 删除网站 acme [email]

**请求参数 (WebsiteResourceReq)**:

| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | ACME 账户 ID | > 0 |

**返回**: 成功时返回空对象

---

### POST /websites/acme/update
**功能**: Update website acme account - 更新 ACME 账户
**认证**: ApiKeyAuth, Timestamp
**日志**: 更新 acme [email]

**请求参数 (WebsiteAcmeAccountUpdate)**:

| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | ACME 账户 ID | > 0 |
| useProxy | bool | 否 | 是否使用代理 | `true`, `false` |

**返回示例**:
```json
{
  "ID": 1,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",
  "email": "admin@example.com",
  "url": "https://acme-v02.api.letsencrypt.org/directory",
  "type": "letsencrypt",
  "keyType": "2048",
  "useProxy": true,
  "caDirURL": "",
  "eabKid": "",
  "eabHmacKey": "",
  "useEAB": false
}
```

---

## 数据模型

### WebsiteAcmeAccount (数据库模型)

| 字段 | 类型 | 说明 |
|------|------|------|
| ID | uint | 主键 ID |
| created_at | timestamp | 创建时间 |
| updated_at | timestamp | 更新时间 |
| email | string | ACME 账户邮箱 |
| url | string | ACME 服务目录 URL |
| type | string | ACME 提供商类型 |
| keyType | string | 密钥类型 |
| useProxy | bool | 是否使用代理 |
| caDirURL | string | 自定义 CA Directory URL |
| eabKid | string | EAB Key ID |
| eabHmacKey | string | EAB HMAC Key（敏感，不返回） |
| useEAB | bool | 是否使用 EAB |

---

## 使用说明

1. **创建 ACME 账户**: 使用 `POST /websites/acme` 创建账户，需要提供邮箱、类型和密钥类型
2. **查询账户列表**: 使用 `POST /websites/acme/search` 进行分页查询
3. **更新账户**: 使用 `POST /websites/acme/update` 更新账户配置（目前仅支持更新 useProxy）
4. **删除账户**: 使用 `POST /websites/acme/del` 删除账户

### 常用场景

- **Let's Encrypt**: `type=letsencrypt`, `keyType=2048`
- **ZeroSSL**: `type=zerossl`, `keyType=2048`
- **自定义 ACME**: `type=custom`, `caDirURL` 设置为自定义服务 URL
- **使用 EAB**: 设置 `useEAB=true`, 并配置 `eabKid` 和 `eabHmacKey`
