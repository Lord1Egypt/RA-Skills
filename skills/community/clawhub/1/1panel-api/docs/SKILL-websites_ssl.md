# Website HTTPS, Website SSL - 1Panel API

## 模块说明
Website HTTPS, Website SSL 模块接口，用于管理网站的 SSL 证书

## 接口列表 (13 个)

---

### POST /websites/ssl/search
**功能**: 分页查询 SSL 证书列表
**参数 (Body)**:

| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| page | int | 否 | 页码，默认 1 | - |
| pageSize | int | 否 | 每页数量，默认 20 | - |
| acmeAccountID | string | 否 | ACME 账户 ID 筛选 | - |
| domain | string | 否 | 域名筛选 | - |
| orderBy | string | 否 | 排序字段 | `created_at`, `expire_date` |
| order | string | 否 | 排序方式 | `null`, `ascending`, `descending` |

---

### POST /websites/ssl/list
**功能**: 获取 SSL 证书列表（不分页）
**参数 (Body)**:

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| acmeAccountID | string | 否 | ACME 账户 ID 筛选 |

---

### POST /websites/ssl
**功能**: 创建 SSL 证书
**参数 (Body)**:

| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| primaryDomain | string | **是** | 主域名 | - |
| otherDomains | string | 否 | 其他域名，多个用逗号分隔 | - |
| provider | string | **是** | DNS 提供商类型 | - |
| acmeAccountId | uint | **是** | ACME 账户 ID | - |
| dnsAccountId | uint | 否 | DNS 账户 ID | - |
| autoRenew | bool | 否 | 是否自动续期，默认 true | - |
| keyType | string | 否 | 密钥类型 | `RSA2048`, `RSA4096`, `ECC256`, `ECC384` 等 |
| apply | bool | 否 | 是否立即申请证书 | - |
| pushDir | bool | 否 | 是否推送证书到目录 | - |
| dir | string | 否 | 证书推送目录 | - |
| id | uint | 否 | 网站 ID（关联的网站） | - |
| description | string | 否 | 证书描述 | - |
| disableCNAME | bool | 否 | 禁用 CNAME 验证 | - |
| skipDNS | bool | 否 | 跳过 DNS 验证 | - |
| nameserver1 | string | 否 | 主 DNS 服务器 | - |
| nameserver2 | string | 否 | 备用 DNS 服务器 | - |
| execShell | bool | 否 | 是否执行自定义脚本 | - |
| shell | string | 否 | 自定义脚本内容 | - |
| pushNode | bool | 否 | 是否推送到节点 | - |
| nodes | string | 否 | 节点列表 | - |
| isIp | bool | 否 | 是否为 IP 证书 | - |

---

### POST /websites/ssl/obtain
**功能**: 申请/签发 SSL 证书
**参数 (Body)**:

| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| ID | uint | **是** | SSL 证书 ID | - |
| skipDNSCheck | bool | 否 | 跳过 DNS 检查 | - |
| nameservers | []string | 否 | 自定义 DNS 服务器 | - |
| disableLog | bool | 否 | 禁用日志 | - |

---

### POST /websites/ssl/resolve
**功能**: 获取 DNS 解析信息
**参数 (Body)**:

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| acmeAccountId | uint | **是** | ACME 账户 ID |
| websiteSSLId | uint | **是** | SSL 证书 ID |

**返回 (Response)**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| resolve | string | DNS 解析记录类型 |
| value | string | DNS 记录值 |
| domain | string | 域名 |
| err | string | 错误信息 |

---

### POST /websites/ssl/del
**功能**: 删除 SSL 证书
**参数 (Body)**:

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| ids | []uint | **是** | 要删除的 SSL 证书 ID 列表 |

---

### GET /websites/ssl/website/:websiteId
**功能**: 根据网站 ID 获取 SSL 证书
**参数 (Path)**:

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| websiteId | int | **是** | 网站 ID |

**返回 (Response)**: [WebsiteSSLDTO](#websitessldto)

---

### GET /websites/ssl/:id
**功能**: 根据 ID 获取 SSL 证书详情
**参数 (Path)**:

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | int | **是** | SSL 证书 ID |

**返回 (Response)**: [WebsiteSSLDTO](#websitessldto)

---

### POST /websites/ssl/update
**功能**: 更新 SSL 证书配置
**参数 (Body)**:

| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | **是** | SSL 证书 ID | - |
| autoRenew | bool | 否 | 是否自动续期 | - |
| description | string | 否 | 证书描述 | - |
| primaryDomain | string | **是** | 主域名 | - |
| otherDomains | string | 否 | 其他域名 | - |
| provider | string | **是** | DNS 提供商 | - |
| acmeAccountId | uint | 否 | ACME 账户 ID | - |
| dnsAccountId | uint | 否 | DNS 账户 ID | - |
| keyType | string | 否 | 密钥类型 | - |
| apply | bool | 否 | 是否重新申请证书 | - |
| pushDir | bool | 否 | 是否推送证书到目录 | - |
| dir | string | 否 | 证书推送目录 | - |
| disableCNAME | bool | 否 | 禁用 CNAME 验证 | - |
| skipDNS | bool | 否 | 跳过 DNS 验证 | - |
| nameserver1 | string | 否 | 主 DNS 服务器 | - |
| nameserver2 | string | 否 | 备用 DNS 服务器 | - |
| execShell | bool | 否 | 是否执行自定义脚本 | - |
| shell | string | 否 | 自定义脚本内容 | - |
| pushNode | bool | 否 | 是否推送到节点 | - |
| nodes | string | 否 | 节点列表 | - |

---

### POST /websites/ssl/upload
**功能**: 上传 SSL 证书（粘贴或本地文件）
**参数 (Body)**:

| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| type | string | **是** | 上传方式 | `paste` (粘贴), `local` (本地文件) |
| privateKey | string | 否 | 私钥内容（paste 方式） | - |
| certificate | string | 否 | 证书内容（paste 方式） | - |
| privateKeyPath | string | 否 | 私钥文件路径（local 方式） | - |
| certificatePath | string | 否 | 证书文件路径（local 方式） | - |
| sslID | uint | 否 | SSL 证书 ID（更新时使用） | - |
| description | string | 否 | 证书描述 | - |

---

### POST /websites/ssl/upload/file
**功能**: 通过文件上传 SSL 证书（multipart/form-data）
**参数 (FormData)**:

| 字段名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| type | string | **是** | 上传类型 | `paste`, `local` |
| description | string | 否 | 证书描述 | - |
| sslID | uint | 否 | SSL 证书 ID（更新时使用） | - |
| privateKeyFile | file | **是** | 私钥文件 (.key) | - |
| certificateFile | file | **是** | 证书文件 (.crt/.pem) | - |

---

### POST /websites/ssl/download
**功能**: 下载 SSL 证书文件
**参数 (Body)**:

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | uint | **是** | SSL 证书 ID |

---

### POST /websites/ssl/import
**功能**: 导入-master SSL 证书（从模型直接导入）
**参数 (Body)**:

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| (model.WebsiteSSL 全部字段) | - | **是** | 直接传递 WebsiteSSL 模型字段 |

---

## 响应数据类型

### WebsiteSSLDTO
```json
{
  "id": 1,
  "primaryDomain": "example.com",
  "otherDomains": "www.example.com",
  "acmeAccountID": 1,
  "dnsAccountID": 1,
  "privateKey": "-----BEGIN RSA PRIVATE KEY-----...",
  "certificate": "-----BEGIN CERTIFICATE-----...",
  "ca": "-----BEGIN CERTIFICATE-----...",
  "issuer": "Let's Encrypt",
  "organization": "",
  "organizationUnit": "",
  "country": "",
  "state": "",
  "location": "",
  "commonName": "example.com",
  "dnsMode": "dns_cname",
  "provider": "alidns",
  "keyType": "RSA4096",
  "expireDate": "2025-01-01 00:00:00",
  "autoRenew": true,
  "pushDir": false,
  "dir": "",
  "description": "",
  "createTime": "2024-01-01 00:00:00",
  "updateTime": "2024-01-01 00:00:00",
  "logPath": "/var/log/1panel/website_ssl/1.log"
}
```

### WebsiteDNSRes
```json
{
  "resolve": "TXT",
  "value": "_acme-challenge.example.com",
  "domain": "example.com",
  "err": ""
}
```

---

## 枚举值参考

### DNS Provider (provider)
- `alidns` - 阿里云 DNS
- `dnspod` - 腾讯云 DNSPod
- `cloudflare` - Cloudflare
- `huawei` - 华为云 DNS
- `aws` - AWS Route 53
- `google` - Google DNS
- `manual` - 手动解析

### Key Type (keyType)
- `RSA2048` - RSA 2048 位
- `RSA4096` - RSA 4096 位
- `ECC256` - ECDSA P-256
- `ECC384` - ECDSA P-384

### ACME Account Type (type)
- `letsencrypt` - Let's Encrypt
- `zerossl` - ZeroSSL
- `buypass` - BuyPass
- `google` - Google Trust Services
- `custom` - 自定义 CA

### Upload Type
- `paste` - 粘贴文本内容
- `local` - 本地文件路径
