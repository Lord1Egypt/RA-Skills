# 登录相关 API

## code2Session — 登录凭证校验

### 接口说明

通过 `tt.login` 接口获取到登录凭证后，开发者可以通过服务器发送请求的方式获取 session_key 和 openid。

**注意**：
- 登录凭证 code、anonymous_code 只能使用一次
- 非匿名需要 code，非匿名下的 anonymous_code 用于数据同步
- 匿名需要 anonymous_code

### 基本信息

| 属性 | 值 |
|------|------|
| HTTP URL | `https://minigame.zijieapi.com/mgplatform/api/apps/jscode2session` |
| HTTP Method | GET |
| Scope | open.ttgame.mgplatform |

### 请求参数（Query）

| 参数名 | 类型 | 必填 | 说明 |
|------|------|------|------|
| appid | String | 是 | 小游戏 ID |
| secret | String | 是 | 小游戏的 APP Secret |
| code | String | 否 | tt.login 返回的登录凭证（code 和 anonymous_code 至少要有一个） |
| anonymous_code | String | 否 | tt.login 返回的匿名登录凭证 |

### 响应参数

| 参数名 | 类型 | 说明 |
|------|------|------|
| error | Int64 | 错误号，0 为成功 |
| openid | String | 用户在当前小游戏的 ID，有 code 时才返回 |
| anonymous_openid | String | 匿名用户 ID，有 anonymous_code 时才返回 |
| session_key | String | 会话密钥，有 code 时才返回 |
| unionid | String | 用户在小游戏平台的唯一标识，有 code 时才返回 |
| errcode | Int64 | 详细错误号 |
| errmsg | String | 错误信息 |
| message | String | 错误信息（同 errmsg） |

**响应示例**

```json
{
  "error": 0,
  "session_key": "ffaaed37bb05d096***",
  "openid": "36d4bd3c8****",
  "anonymous_openid": "",
  "unionid": "f7510d9ab***********"
}
```

### 错误码

| HTTP 状态码 | 错误码 | 描述 | 排查建议 |
|------|------|------|------|
| 200 | 0 | 请求成功 | - |
| 200 | -1 | 系统错误 | - |
| 200 | 40014 | 未传必要参数 | 检查参数完整性 |
| 200 | 40015 | appid 错误 | 检查 AppID |
| 200 | 40017 | secret 错误 | 检查 AppSecret |
| 200 | 40018 | code 错误 | code 可能已过期或无效 |
| 200 | 40019 | anonymous_code 错误 | 检查匿名 code |

---

## 用户登录态签名

### 签名规则

signature = hmac_sha256(session_key, data)，其中 data 按以下规则拼接：

**GET 请求**：
```
data = http_method + '&' + url_encode(uri_path)
```

**POST 请求**：
```
data = http_method + '&' + url_encode(uri_path) + '&' + post_body
```

**参数说明**：
- `http_method`：请求方法小写字符串，如 `get`、`post`
- `uri_path`：请求的 URI 路径，如 `/mgplatform/api/apps/check_session_key`
- `post_body`：POST 请求的 JSON body 原始字符串

**使用场景**：调用需要用户授权的 API（setUserStorage、removeUserStorage、checkSessionKey、resetSessionKey）时，需在请求参数中传入 sig_method（固定 hmac_sha256）和 signature。

### 签名示例（JavaScript）

```js
const crypto = require('crypto');

function generateSignature(sessionKey, method, uriPath, postBody) {
  let data = method.toLowerCase() + '&' + encodeURIComponent(uriPath);
  if (postBody) {
    data += '&' + postBody;
  }
  return crypto.createHmac('sha256', sessionKey).update(data).digest('hex');
}
```

---

## checkSessionKey — 校验登录态

### 接口说明

校验服务器所保存的登录态 session_key 是否合法。

### 基本信息

| 属性 | 值 |
|------|------|
| HTTP URL | `https://minigame.zijieapi.com/mgplatform/api/apps/check_session_key` |
| HTTP Method | GET |
| Scope | open.ttgame.mgplatform |

### 请求参数（Query）

| 参数名 | 类型 | 必填 | 说明 |
|------|------|------|------|
| access_token | String | 是 | 调用 getAccessToken 生成的 token |
| openid | String | 是 | 用户唯一标识符 |
| sig_method | String | 是 | 用户登录态签名的哈希方法，目前只支持 `hmac_sha256` |
| signature | String | 是 | 用户登录态签名 |

### 响应参数

| 参数名 | 类型 | 说明 |
|------|------|------|
| err_no | Int32 | 错误码，0 为成功 |
| err_msg | String | 错误信息 |
| log_id | String | 请求日志 ID |

**响应示例**

```json
{
  "err_no": 0,
  "err_msg": "",
  "log_id": "20250528154636C3DD5EA834B0BF27F544"
}
```

### 错误码

| HTTP 状态码 | 错误码 | 描述 | 排查建议 |
|------|------|------|------|
| 200 | 28001003 | access_token 无效 | 重新获取有效的 access_token |
| 200 | 28001004 | openid 无效 | 检查 openID 是否有效 |
| 200 | 28001038 | 参数错误 | 检查 sig_method 等参数 |
| 200 | 28001039 | 签名不正确 | 检查 signature 计算过程 |

---

## resetSessionKey — 重置登录态

### 接口说明

重置服务器所保存的登录态 session_key 并返回新值。

### 使用限制

单个 appid 下每分钟不能超过 **6 万次**。

### 基本信息

| 属性 | 值 |
|------|------|
| HTTP URL | `https://minigame.zijieapi.com/mgplatform/api/apps/reset_session_key` |
| HTTP Method | POST |
| Scope | open.ttgame.mgplatform |

### 请求参数（Body JSON）

| 参数名 | 类型 | 必填 | 说明 |
|------|------|------|------|
| access_token | String | 是 | 调用 getAccessToken 生成的 token |
| openid | String | 是 | 用户唯一标识符 |
| sig_method | String | 是 | 签名方法，目前只支持 `hmac_sha256` |
| signature | String | 是 | 用户登录态签名 |

### 响应参数

| 参数名 | 类型 | 说明 |
|------|------|------|
| err_no | Int32 | 错误码，0 为成功 |
| err_msg | String | 错误信息 |
| log_id | String | 请求日志 ID |
| openid | String | 用户唯一标识符 |
| session_key | String | 重置后的用户登录态 key |

**响应示例**

```json
{
  "err_msg": "",
  "err_no": 0,
  "log_id": "20250520145051C7448147A7B8F68A9D52",
  "openid": "_000nHq5DzNNC9QsWOEE_AJBEXS-b01ol-F3",
  "session_key": "dkLWEVhjZBJ0zh3zaPKBOg=="
}
```

### 错误码

| HTTP 状态码 | 错误码 | 描述 | 排查建议 |
|------|------|------|------|
| 200 | 28001003 | access_token 无效 | 获取最新的 access_token |
| 200 | 28001004 | openID 无效 | 检查 openID |
| 200 | 28001038 | 参数错误 | 检查 sig_method |
| 200 | 28001039 | 签名不正确 | 检查 signature 计算过程 |
| 200 | 28005139 | 请求过于频繁 | 等待后重试 |
| 200 | 28001005 | 系统内部错误 | 重试或提 oncall 排查 |
