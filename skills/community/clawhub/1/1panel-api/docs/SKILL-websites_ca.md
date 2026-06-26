# Website CA - 1Panel API

## 模块说明
Website CA 模块接口，用于管理自签名 CA 证书

## 接口列表 (7 个)

---

### GET /websites/ca/{id}

**功能**: 获取网站 CA 证书详情

**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|------|----------|
| id | path | int | 是 | 网站 CA 记录 ID | - |

**返回**: `response.WebsiteCADTO`

---

### POST /websites/ca/search

**功能**: 分页查询网站 CA 列表

**参数** (body):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| Page | int | 否 | 页码 | - |
| PageSize | int | 否 | 每页数量 | - |
| Order | string | 否 | 排序方向 | `null`, `ascending`, `descending` |
| OrderBy | string | 否 | 排序字段 | `created_at` |

**返回**: `dto.PageResult`

---

### POST /websites/ca

**功能**: 创建自签名 CA 证书

**参数** (body):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| commonName | string | 是 | CA 证书通用名称 (CN) | - |
| country | string | 是 | 国家代码 | 如 `CN`, `US` 等 |
| organization | string | 是 | 组织名称 | - |
| organizationUint | string | 否 | 组织单位 | - |
| name | string | 是 | CA 名称 | - |
| keyType | string | 是 | 密钥类型 | `P256`, `P384`, `2048`, `3072`, `4096`, `8192` |
| province | string | 否 | 省份/州 | - |
| city | string | 否 | 城市 | - |

**返回**: `request.WebsiteCACreate`

---

### POST /websites/ca/del

**功能**: 删除网站 CA 证书

**参数** (body):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 网站 CA 记录 ID | - |

**返回**: 空

---

### POST /websites/ca/obtain

**功能**: 自签 SSL 证书

**参数** (body):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 网站 CA 记录 ID | - |
| domains | string | 是 | 域名列表，多个用逗号分隔 | - |
| keyType | string | 是 | 密钥类型 | `P256`, `P384`, `2048`, `3072`, `4096`, `8192` |
| time | int | 是 | 有效期数量 | - |
| unit | string | 是 | 有效期单位 | - |
| pushDir | bool | 否 | 是否推送到目录 | - |
| dir | string | 否 | 推送目录路径 | - |
| autoRenew | bool | 否 | 是否自动续期 | - |
| renew | bool | 否 | 是否为续期操作 | - |
| sslID | uint | 否 | SSL 证书 ID (续期时使用) | - |
| description | string | 否 | 证书描述 | - |
| execShell | bool | 否 | 是否执行自定义脚本 | - |
| shell | string | 否 | 自定义脚本内容 | - |

**返回**: 证书创建结果

---

### POST /websites/ca/renew

**功能**: 续期 SSL 证书

**参数** (body):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| SSLID | uint | 是 | 要续期的 SSL 证书 ID | - |

**返回**: 空

**注意**: 续期时实际使用 `WebsiteCAObtain` 结构体，参数 `renew` 设为 `true`，`unit` 设为 `year`，`time` 设为 `1`

---

### POST /websites/ca/download

**功能**: 下载 CA 证书文件

**参数** (body):
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 网站 CA 记录 ID | - |

**返回**: 文件流 (Content-Disposition: attachment)

---

## 数据模型

### WebsiteCADTO (响应)
| 字段名 | 类型 | 说明 |
|--------|------|------|
| model.WebsiteCA | model | CA 证书模型 |
| CommonName | string | 通用名称 |
| Country | string | 国家代码 |
| Organization | string | 组织名称 |
| OrganizationUint | string | 组织单位 |
| Province | string | 省份 |
| City | string | 城市 |

### WebsiteCA (Model)
| 字段名 | 类型 | 说明 |
|--------|------|------|
| ID | uint | 记录 ID |
| Name | string | CA 名称 |
| KeyType | string | 密钥类型 |
| RootCert | string | 根证书 |
| RootKey | string | 根私钥 |
| Cert | string | 证书 |
| Key | string | 私钥 |
| AutoRenew | bool | 自动续期 |
| ExpireDate | time | 过期时间 |
