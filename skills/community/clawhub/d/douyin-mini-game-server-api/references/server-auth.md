# 接口调用凭证

## getAccessToken — 获取接口调用凭证

### 接口说明

access_token 是小游戏的全局唯一调用凭据，开发者调用小游戏支付时需要使用 access_token。access_token 的有效期为 2 个小时，需要定时刷新 access_token，重复获取会导致之前一次获取的 access_token 的有效期缩短为 5 分钟。

**Tip**: 
- token 是小游戏级别 token，不要为每个用户单独分配
- 建议每小时更新一次即可
- 原域名仍然可用，建议迁移到新域名

### 基本信息

| 属性 | 值 |
|------|------|
| HTTP URL | `https://minigame.zijieapi.com/mgplatform/api/apps/v2/token` |
| HTTP Method | POST |
| Scope | open.ttgame.mgplatform |

### 请求参数

**请求头**

| 参数名 | 类型 | 必填 | 说明 |
|------|------|------|------|
| content-type | String | 是 | 固定值 `"application/json"` |

**Body**

| 参数名 | 类型 | 必填 | 说明 |
|------|------|------|------|
| appid | String | 是 | 小游戏 ID |
| secret | String | 是 | 小游戏的 APP Secret，可在开发者后台获取 |
| grant_type | String | 否 | 获取 access_token 时值为 `client_credential` |

### 响应参数

**Body**

| 参数名 | 类型 | 说明 |
|------|------|------|
| err_no | Int64 | 错误码，0 为成功 |
| err_tips | String | 错误信息 |
| data | Struct | 数据体 |
| data.access_token | String | 获取到的凭证 |
| data.expires_in | Int64 | 凭证有效时间，单位：秒（默认 7200） |

**响应示例**

```json
{
  "err_no": 0,
  "err_tips": "success",
  "data": {
    "access_token": "0801121***********",
    "expires_in": 7200
  }
}
```

### 错误码

| HTTP 状态码 | 错误码 | 描述 | 排查建议 |
|------|------|------|------|
| 200 | 0 | 请求成功 | - |
| 200 | -1 | 系统错误 | - |
| 200 | 40015 | appid 错误 | 检查 AppID 是否正确 |
| 200 | 40017 | secret 错误 | 检查 AppSecret 是否正确 |
| 200 | 40020 | grant_type 不是 client_credential | 修正 grant_type 参数 |

---

## genStableAccessToken — 获取稳定版接口调用凭证

### 接口说明

区别于 getAccessToken 每次调用生成新的 access_token 并将上次 token 有效期缩短为 5 分钟，genStableAccessToken 用于获取在有效期内稳定不变的 access_token，支持开发者任意服务需要时直接调用获取。

**两种模式**：
- **普通模式**（force_refresh=false）：有效期内的 access_token 不变，重复调用直接返回当前值
- **强制刷新模式**（force_refresh=true）：使当前 token 立即失效，重新生成新的 access_token

开发者需妥善保护稳定版 access_token，若泄露需使用强制刷新模式生成新 token。

### 使用限制

| 模式 | 限制 |
|------|------|
| 普通模式 | 单个 appid 每分钟最多 1 万次，每天 50 万次 |
| 强制刷新模式 | 单个 appid 每天最多 20 次 |

### 基本信息

| 属性 | 值 |
|------|------|
| HTTP URL | `https://minigame.zijieapi.com/mgplatform/api/apps/stable_token` |
| HTTP Method | POST |
| Scope | open.ttgame.mgplatform |

### 请求参数

**请求头**

| 参数名 | 类型 | 必填 | 说明 |
|------|------|------|------|
| content-type | String | 是 | 固定值 `"application/json"` |

**Body**

| 参数名 | 类型 | 必填 | 说明 |
|------|------|------|------|
| appid | String | 是 | 小游戏 AppID |
| secret | String | 是 | 小游戏 AppSecret |
| grant_type | String | 是 | 固定值 `client_credential` |
| force_refresh | Bool | 否 | 是否强制刷新，默认 false |

### 响应参数

**Body**

| 参数名 | 类型 | 说明 |
|------|------|------|
| err_no | Int32 | 错误码，0 为成功 |
| err_msg | String | 错误信息 |
| log_id | String | 请求日志 ID |
| data | Struct | 数据体 |
| data.access_token | String | 获取到的凭证 |
| data.expires_in | Int64 | 凭证有效剩余时间，单位：秒 |

**响应示例**

```json
{
  "data": {
    "access_token": "080112184745453432574e56596b44504a385579365368416b413d3d",
    "expires_in": 7200
  },
  "err_msg": "",
  "err_no": 0,
  "log_id": "20250520193036E7194E7CB37873E5C680"
}
```

### 错误码

| HTTP 状态码 | 错误码 | 描述 | 排查建议 |
|------|------|------|------|
| 200 | 28005139 | 请求过于频繁 | 等待一段时间后再请求 |
| 200 | 28001038 | 参数错误 | 检查 appid、secret、grant_type 等参数 |
| 200 | 28001005 | 系统内部错误 | 重试请求或联系 oncall 排查 |
