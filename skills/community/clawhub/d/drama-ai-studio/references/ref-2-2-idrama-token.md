> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 2.2 通过iDrama的账号和密码获取 Token

- 接口：`POST /openapi/uaa/oauth/token`
- 内容类型：`application/x-www-form-urlencoded`

请求参数：

| 字段       | 位置 | 必填 | 说明     |
|------------|------|------|----------|
| `username` | form | 是   | 用户名   |
| `password` | form | 是   | 登录密码 |

成功响应示例（HTTP 200）：

```json
{
  "code": 1,
  "msg": "登录成功",
  "data": {
    "access_token": "xxxx...",
    "token_type": "Bearer",
    "expires_in": 3600
  }
}
```

失败示例（认证失败，HTTP 200 但 `code=-1`）：

```json
{
  "code": -1,
  "msg": "用户名或密码错误"
}
```

拿到 `access_token` 后，在所有需要鉴权的接口请求头中统一携带：

```text
Authorization: Bearer <access_token>
```
