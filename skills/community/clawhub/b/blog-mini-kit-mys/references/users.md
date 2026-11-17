# 用户 API（2 端点）

路径前缀：`{base_url}` · 无认证

## 1. GET /api/users — 获取用户列表

**子命令**：`list-users`

```bash
curl -s --max-time 30 "{base_url}/api/users"
```

响应：
```json
{"code":200,"data":[{"id":1,"uname":"admin","phone":"admin","img":"img/moren.jpg","email":"admin@blog.com","address":"","profession":"","createtime":"2026-08-25T02:40:00"}]}
```

> 注意：返回字段不含密码（pwd），仅公开信息。

## 2. POST /api/users — 创建用户

**子命令**：`create-user`

Body（JSON，`UserCreate`）：

| 字段 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| uname | string | 是 | - | 用户名 |
| phone | string | 否 | "" | 手机号 |
| pwd | string | 否 | "" | 密码 |
| email | string | 否 | "" | 邮箱 |
| img | string | 否 | img/moren.jpg | 头像 |

```bash
curl -s --max-time 30 -X POST -H "Content-Type: application/json" \
  -d '{"uname":"newuser","pwd":"123456","email":"u@x.com"}' "{base_url}/api/users"
```

响应：`{"code":200,"data":{"id":2}}`
