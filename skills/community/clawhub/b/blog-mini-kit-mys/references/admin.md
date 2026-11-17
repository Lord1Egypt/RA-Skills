# 后台管理 API（4 端点）

路径前缀：`{base_url}` · 需 admin 登录 token · 默认账号 admin/admin（以实际部署为准）

> 后台管理使用 session token 机制：
> 1. `admin-login` 提交表单获取 token（Set-Cookie: admin_token）
> 2. `admin-delete-articles` 在 JSON body 中携带 token
> 3. `admin-logout` 注销 token
>
> token 有效期 2 小时，存储在服务端内存（`_admin_sessions`）。

## 1. GET /admin — 后台管理页面

**子命令**：`admin-page`

> 未登录时返回登录页 HTML；已登录（cookie admin_token 有效）返回管理页面 HTML。

```bash
curl -s --max-time 30 "{base_url}/admin"
```

响应：`text/html` — 登录页或管理页面

## 2. POST /admin/login — 后台登录

**子命令**：`admin-login`

Body（application/x-www-form-urlencoded）：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 账号（默认 admin） |
| password | string | 是 | 密码（默认 admin） |

```bash
curl -s --max-time 30 -X POST -d "username=admin&password=admin" -D - \
  "{base_url}/admin/login" -o /dev/null
```

响应（成功）：`302` 重定向到 `/admin`，`Set-Cookie: admin_token=<token>; HttpOnly`
响应（失败）：`200` 返回登录页 HTML（含错误提示）

> 脚本 `admin-login` 子命令自动提取 cookie 中的 `admin_token` 返回 JSON：
> `{"code":200,"data":{"token":"<token>"},"message":"登录成功"}`

## 3. GET /admin/logout — 退出登录

**子命令**：`admin-logout`

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| t | query | string | 是 | 登录 token |

```bash
curl -s --max-time 30 "{base_url}/admin/logout?t=<token>"
```

响应：`302` 重定向到 `/admin`，删除 cookie

## 4. POST /admin/api/delete — 批量删除文章

**子命令**：`admin-delete-articles`

Body（JSON）：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| token | string | 是 | 登录 token |
| ids | int[] | 是 | 文章 ID 列表 |

```bash
curl -s --max-time 30 -X POST -H "Content-Type: application/json" \
  -d '{"token":"<token>","ids":[1,2,3]}' "{base_url}/admin/api/delete"
```

响应（成功）：`{"code":200,"deleted":3,"message":"成功删除 3 篇文章"}`
响应（未授权）：`{"code":401,"message":"未登录或登录已过期"}`
响应（空列表）：`{"code":400,"message":"未选择文章"}`

> ⚠️ 此操作为硬删除（DELETE FROM article），不可恢复。需先 `admin-login` 获取 token。
