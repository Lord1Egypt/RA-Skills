---
name: artifact-share
description: Use when you need to share static web content (HTML/CSS/JS/images) via a publicly accessible URL — uploading generated files, creating shareable pages, or deploying single-page web artifacts
---

# Artifact Share

## Overview

Artifact Share 是面向 Agent 的静态资源上传与分享服务。上传 HTML/CSS/JS/图片等文件，立即获取可分享的公开 URL。

## When to Use

- 生成了 HTML/CSS/JS 内容，需要生成一个公开可访问的 URL 供用户查看
- 需要部署单页面 Web 作品，让用户在浏览器中预览
- 需要托管静态网页文件并提供分享链接
- 生成的设计稿、交互原型需要在线展示

## When NOT to Use

- 上传二进制可执行文件、视频、音频（不在支持文件类型白名单中）
- 部署需要后端服务器的动态应用（仅支持静态内容）
- 项目总大小超过 5MB、超过 5 个文件、或需要超过 1 个项目（免费限制）

## Prerequisites — Service URL

BASE_URL 值为 `https://artifact-share.youthol.top`。

下文所有 `{BASE_URL}` 均指此配置值。

## Registration — First-Time Setup

**首次使用必须注册，获取 API Key 后才能进行任何上传操作。注册是一次性的，之后所有操作复用同一个 API Key。**

Agent 场景下无需邮箱和密码，使用设备 ID（device_id）注册即可。用户后续可在 Web 平台绑定邮箱和设置昵称。

Web 管理页面地址为 BASE_URL。

### 生成 device_id

Agent 在注册前需要生成一个设备标识。推荐方式：

- **方式一（推荐）：** 使用本地机器的唯一标识组合，如 `username@hostname`（通过 `whoami` + `hostname` 命令获取）
- **方式二：** 生成随机 UUID 并保存到本地文件 `~/.artifact-share-device-id`，后续复用
- **方式三：** 使用 Agent 自身的会话标识符

device_id 规则：4-64 字符，仅允许字母、数字、下划线、点、连字符和 @。

### 注册请求

```bash
curl -s -X POST {BASE_URL}/api/v1/register \
  -H "Content-Type: application/json" \
  -d '{"device_id": "yangyc@macbook-pro", "nickname": "Yang"}'
```

`nickname` 为可选字段，用于 Web 平台展示，最多 50 字符。

### 注册响应

```json
{
  "user_id": "uid_xxxx",
  "api_key": "ak_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

用户还会获得一个自动生成的 `slug`（路径标识），用于分享 URL。如注册后 `GET /api/v1/me` 可查看完整信息包括 slug。

### 重复注册

如果使用相同的 device_id 再次注册，会返回错误：

```json
{
  "error": {
    "code": "DEVICE_ALREADY_REGISTERED",
    "message": "该设备已注册，请使用已有的 API Key"
  }
}
```

### Token（API Key）存储

**注册成功后必须立即保存 API Key，它是后续所有操作的唯一凭证。**

**唯一存储位置：`~/.config/artifact-share/config.yml`**

```yaml
device_id: yangyc@macbook-pro
api_key: ak_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
base_url: https://artifact-share.youthol.top
```

注册成功后，Agent 必须将 `device_id`、`api_key` 和 `base_url` 写入此文件。后续所有操作从该文件读取 api_key。

写入命令：

```bash
mkdir -p ~/.config/artifact-share
cat > ~/.config/artifact-share/config.yml << EOF
device_id: {YOUR_DEVICE_ID}
api_key: {YOUR_API_KEY}
base_url: {BASE_URL}
EOF
```

**⚠️ 注意事项：**
- API Key 不设过期时间，视为永久凭证，请妥善保管
- 同一 device_id 只能注册一次 — 如果丢失 API Key，当前无找回机制，需使用新 device_id 重新注册
- 不要将 API Key 写入公开代码仓库
- 不要与其他用户共享 API Key

## Query API Key

在执行任何操作之前，先查询本地配置文件获取 API Key：

```bash
cat ~/.config/artifact-share/config.yml
```

**判断逻辑：**
- 文件存在且包含 `api_key` → 读取 api_key 值，用于后续 API 调用的 `X-API-Key` header
- 文件不存在或 api_key 为空 → **提示用户"还未注册，请先调用 register 注册获取 API Key"**，然后执行注册流程

**示例：**

> 用户要求上传文件时，Agent 应先检查 `~/.config/artifact-share/config.yml`：
> - 有 api_key → 直接使用该 key 上传
> - 没有 api_key → 告知用户"还未注册，我先帮你注册"，然后注册并保存到 config.yml

## Operations

### 1. Create Project & Upload File

创建项目并获取分享 URL。**文件可选**——可以只填项目名先建空项目、稍后再上传文件;也可以同时上传单个文件或 ZIP 压缩包。默认创建的项目不带密码。

**仅名称创建（占位项目,稍后上传）:**

```bash
curl -s -X POST {BASE_URL}/api/v1/projects \
  -H "X-API-Key: {YOUR_API_KEY}" \
  -F "name=my-page"
```

响应 `url` 为项目根 `{BASE_URL}/s/{slug}/{pid}`;在上传文件前访问会 404,上传文件（见第 2 节）后即可访问。

**单文件上传:**

```bash
curl -s -X POST {BASE_URL}/api/v1/projects \
  -H "X-API-Key: {YOUR_API_KEY}" \
  -F "file=@/local/path/to/aa.html"
```

**ZIP 包上传（多文件项目）:**

```bash
curl -s -X POST {BASE_URL}/api/v1/projects \
  -H "X-API-Key: {YOUR_API_KEY}" \
  -F "file=@/local/path/to/project.zip"
```

**带密码上传（可选）:**

```bash
curl -s -X POST {BASE_URL}/api/v1/projects \
  -H "X-API-Key: {YOUR_API_KEY}" \
  -F "password=my-secret-password" \
  -F "file=@/local/path/to/project.zip"
```

`name` 与 `password` 均为可选字段:

- `name` 在**带文件上传**时不传会自动从文件名派生（如 `aa.html` → 项目名 `aa.html`);**不带文件时必填**。项目名**仅作展示,不参与分享 URL**——URL 直接以本地文件名为结尾,本地叫什么、访问路径就是什么。
- `password` 不传或为空则项目公开访问;设置了密码则访问者需先输入密码才能查看。

**响应:**

```json
{
  "project_id": "pid_xxxx",
  "name": "aa.html",
  "url": "{BASE_URL}/s/{slug}/pid_xxxx/aa.html"
}
```

`url` 末尾就是上传文件的原始文件名;`project_id` 是当前项目的唯一标识,**后续要在同一项目下反复修改文件时复用它**（见第 2 节）。

**项目名规则:** 1-60 字符;自动去除首尾空格;不允许控制字符（含制表符/换行/NUL 等)。带文件上传时可选（从文件名派生）,仅建空项目时必填。仅作展示,不在 URL 中出现。

**支持文件类型:** html, css, js, png, jpg, jpeg, gif, svg, webp, ico, bmp, woff, woff2, ttf, otf, eot

**免费限制:** 每用户最多 1 个项目,每项目最多 5 个文件,项目总大小不超过 5MB（单次上传不超过 3MB）。

### 2. Update Project Files

替换或新增项目中的文件。

```bash
curl -s -X PUT {BASE_URL}/api/v1/projects/{PROJECT_ID}/files \
  -H "X-API-Key: {YOUR_API_KEY}" \
  -F "file_path=css/style.css" \
  -F "file=@/local/path/to/new-style.css"
```

**响应：**

```json
{
  "project_id": "pid_xxxx",
  "name": "aa.html",
  "url": "{BASE_URL}/s/{slug}/pid_xxxx/aa.html"
}
```

响应回显 `project_id` 与 `name`，便于调用方在**同一个对话里持续编辑**：只要复用同一个 `project_id` 并保持 `file_path` 不变，重新上传后 URL 保持不变、内容被替换——无需新建项目。

### 3. List Project Files — `GET /api/v1/projects/{PROJECT_ID}/files`

查看某个项目内的所有文件及其分享 URL（每个文件的 URL 末尾即其原始路径）。

```bash
curl -s {BASE_URL}/api/v1/projects/{PROJECT_ID}/files \
  -H "X-API-Key: {YOUR_API_KEY}"
```

**响应：**

```json
{
  "files": [
    {
      "id": "file-uuid",
      "file_path": "aa.html",
      "url": "{BASE_URL}/s/{slug}/{PROJECT_ID}/aa.html",
      "size": 1234,
      "mime_type": "text/html; charset=utf-8",
      "access_count": 0,
      "created_at": "2026-06-23T12:00:00Z"
    }
  ]
}
```

### 4. Delete Project File — `DELETE /api/v1/projects/{PROJECT_ID}/files/{FILE_ID}`

删除项目中的单个文件（同时清理存储与记录，并重算项目大小/文件数）。`FILE_ID` 来自第 3 节列表响应的 `id`。操作不可恢复。

```bash
curl -s -X DELETE {BASE_URL}/api/v1/projects/{PROJECT_ID}/files/{FILE_ID} \
  -H "X-API-Key: {YOUR_API_KEY}"
```

**响应：**

```json
{
  "message": "deleted"
}
```

### 5. List Projects

查看当前用户的所有项目。

```bash
curl -s {BASE_URL}/api/v1/projects \
  -H "X-API-Key: {YOUR_API_KEY}"
```

**响应：**

```json
{
  "projects": [
    {
      "id": "pid_xxxx",
      "name": "my-project",
      "url": "{BASE_URL}/s/{slug}/pid_xxxx",
      "has_password": false,
      "size": 1234,
      "file_count": 3,
      "created_at": "2026-06-23T12:00:00Z"
    }
  ]
}
```

### 6. Delete Project

删除项目及其所有文件，操作不可恢复。

```bash
curl -s -X DELETE {BASE_URL}/api/v1/projects/{PROJECT_ID} \
  -H "X-API-Key: {YOUR_API_KEY}"
```

**响应：**

```json
{
  "message": "deleted"
}
```

### 7. Update Project Password — `PUT /api/v1/projects/{PROJECT_ID}/password`

设置或取消项目的访问密码。空字符串表示取消密码保护（公开访问）。

```bash
# 设置密码
curl -s -X PUT {BASE_URL}/api/v1/projects/{PROJECT_ID}/password \
  -H "X-API-Key: {YOUR_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"password": "new-secret"}'

# 取消密码（改为公开访问）
curl -s -X PUT {BASE_URL}/api/v1/projects/{PROJECT_ID}/password \
  -H "X-API-Key: {YOUR_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"password": ""}'
```

**响应：**

```json
{
  "message": "密码已更新"
}
```

### 8. Share Link — Access Control

分享 URL 格式：`{BASE_URL}/s/{slug}/{pid}/{filename}`

- `{slug}` 是用户的路径标识（注册时自动生成，暂不支持修改）
- `{pid}` 是项目唯一标识（如 `pid_xxxx`，全局唯一，不暴露内部 user_id）
- `{filename}` 是上传文件的原始路径——本地叫什么，URL 就是

访问根地址 `{BASE_URL}/s/{slug}/{pid}` 时，服务器动态挑选入口文件返回（优先 `index.html`，否则第一个 `.html`，否则第一个文件）。直接访问 `{BASE_URL}/s/{slug}/{pid}/{filename}` 则返回该文件本身；HTML 里的相对资源引用会自然解析到同前缀的兄弟文件，无需额外重写。

- **无密码项目** → 直接返回内容
- **有密码项目** → 返回密码输入页面，验证通过后设置 Cookie（作用域为 `/s/{slug}/{pid}`，覆盖该项目下所有文件），后续访问自动放行

所有资源都走 `/s/{slug}/{pid}/...` 同一前缀代理转发，用户始终只看到 `{BASE_URL}/s/...` 的干净路径，七牛 CDN 链接不会暴露。

密码验证接口：`POST /s/{slug}/{pid}/verify`（仅接受 JSON 请求，body `{"password":"..."}`，成功返回 `{"redirect":"/s/{slug}/{pid}"}` 并下发 HttpOnly cookie）

### 9. Get User Info — `GET /api/v1/me`

获取当前登录用户的信息，包括邮箱绑定状态。

```bash
curl -s {BASE_URL}/api/v1/me \
  -H "X-API-Key: {YOUR_API_KEY}"
```

**响应：**

```json
{
  "id": "uid_xxxx",
  "device_id": "yangyc@macbook-pro",
  "nickname": "Yang",
  "email": "",
  "slug": "7e3e7bb2",
  "plan": "free",
  "has_bound_email": false,
  "created_at": "2026-06-23T12:00:00Z"
}
```

`slug` 是用户在分享 URL 中的路径标识，注册时自动生成，暂不支持修改。

### 10. Send Verification Code — `POST /api/v1/bind-email/send`

向指定邮箱发送 6 位数字验证码（5 分钟有效，60 秒内不可重复发送）。

```bash
curl -s -X POST {BASE_URL}/api/v1/bind-email/send \
  -H "X-API-Key: {YOUR_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'
```

**响应：**

```json
{
  "message": "验证码已发送",
  "expires": "2026-06-23T12:05:00Z"
}
```

**前置条件：** 当前用户未绑定邮箱。如已绑定，返回 `EMAIL_ALREADY_BOUND`。

### 11. Verify & Bind Email — `POST /api/v1/bind-email/verify`

验证验证码并绑定邮箱。验证成功后 `has_bound_email` 变为 `true`。

```bash
curl -s -X POST {BASE_URL}/api/v1/bind-email/verify \
  -H "X-API-Key: {YOUR_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "code": "123456"}'
```

**响应：**

```json
{
  "message": "邮箱绑定成功",
  "email": "user@example.com"
}
```

**限制：** 验证码最多尝试 5 次，超过后需重新发送。

### 12. Generate QR Code — `GET /api/v1/qr?url=...`

把任意文本/URL 编码成 base64 PNG 二维码（用于让用户扫码在手机上调试分享页面）。**公开接口，无需 API Key**。

```bash
curl -s "{BASE_URL}/api/v1/qr?url=https://artifact-share.youthol.top/s/{slug}/{pid}/aa.html"
```

**响应：**

```json
{
  "qr_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUg..."
}
```

`qr_base64` 是可直接内联的 data URI，在 Markdown/HTML 里以 `![qrcode](<data URI>)` 渲染即可扫码。**限制：** 内容最长 2000 字符，超出返回 `INVALID_INPUT`。

## Complete Workflow

```
1. 查询 API Key → cat ~/.config/artifact-share/config.yml
   ├─ 有 api_key → 直接使用，进入步骤 3
   └─ 无 api_key → 执行步骤 2 注册
2. 注册 → POST /api/v1/register {device_id, nickname} → 获取 API Key → 写入 ~/.config/artifact-share/config.yml
3. 登录 → GET /api/v1/me → 检查 has_bound_email
4. 绑定邮箱（如果 has_bound_email=false，可选）:
   a. 发送验证码 → POST /api/v1/bind-email/send {email}
   b. 验证并绑定 → POST /api/v1/bind-email/verify {email, code}
5. 上传 → POST /api/v1/projects → 获取 project_id + name + 分享 URL（可仅传 name 建空项目稍后上传,或带 file 直接上传;URL 以本地文件名结尾）
6. 分享 → 将 URL 与项目名返回给用户 → 调 GET /api/v1/qr?url=<URL> 取 qr_base64 一并返回（扫码调试）→ 同时附上 Web 管理后台地址 {BASE_URL}（用 API Key 登录可在线管理）→ 用户在浏览器中打开
7. 更新 → 复用同一 project_id 调用 PUT /api/v1/projects/{id}/files → 内容替换、URL 保持不变
8. 删除 → DELETE /api/v1/projects/{id} → 移除项目
```

## Returning Share Links to Users

上传成功后，从响应中提取分享 URL 并明确展示给用户，**同时告知当前项目名与 project_id，并提醒用户可在同一项目下反复修改文件，以及在线管理后台地址**：

1. 解析 `create_project` 的 JSON 响应
2. 提取 `url`、`name`、`project_id` 字段
3. 以清晰格式呈现给用户（`url` 即为分享链接，无需手动拼接）
4. **生成扫码二维码**：调用 `GET /api/v1/qr?url=<分享URL>`（见第 12 节，公开免鉴权），取 `qr_base64`，以 `![qrcode](<qr_base64>)` 一并返回给用户，方便手机扫码调试
5. **告知 Web 管理后台地址**：附上 `{BASE_URL}`，提示用户可用自己的 API Key 登录在浏览器中在线管理项目与文件（上传/替换/删除、设置访问密码、查看用量等）

**示例 — Agent 上传后应返回给用户的信息：**

> ✅ 已上传成功！你的页面已上线：
> 🔗 {BASE_URL}/s/{slug}/pid_xxxx/aa.html
> 📁 当前项目：aa.html（project_id: pid_xxxx）
> 📱 扫码在手机上预览：
> ![qrcode](<data:image/png;base64,...qr_base64...>)
> 🌐 在线管理后台：{BASE_URL}（用你的 API Key 登录，可在浏览器中上传/替换/删除文件、设置访问密码、查看用量）
>
> 💡 后续如需修改/修复这个页面，无需重新创建项目——直接把新版本上传到同一项目即可，URL 保持不变：
> `PUT /api/v1/projects/pid_xxxx/files -F file_path=aa.html -F file=@新版本.html`

**带密码项目：**

> ✅ 已上传成功！你的页面已上线：
> 🔗 {BASE_URL}/s/{slug}/pid_xxxx/aa.html
> 📁 当前项目：aa.html（project_id: pid_xxxx）
> 🔒 访问密码：my-secret-password
> 📱 扫码在手机上预览：
> ![qrcode](<data:image/png;base64,...qr_base64...>)
> 🌐 在线管理后台：{BASE_URL}（用你的 API Key 登录，可在浏览器中管理项目与文件）
>
> 💡 修改页面请复用同一 project_id 重新上传，URL 不变。

如果项目设置了密码，应告知用户访问者需要输入密码才能查看。

## Error Handling

| Error Code | 含义 | HTTP Status |
|-----------|------|-------------|
| INVALID_FILE_TYPE | 文件类型不在白名单 | 400 |
| FILE_TOO_LARGE | 单次上传文件超过 3MB | 400 |
| PROJECT_LIMIT_EXCEEDED | 项目数超过 1 个 | 403 |
| INVALID_API_KEY | API Key 无效或缺失 | 401 |
| PROJECT_NOT_FOUND | 项目不存在 | 404 |
| PROJECT_NOT_OWNER | 不是项目所有者 | 403 |
| EMAIL_EXISTS | 邮箱已绑定 | 409 |
| DEVICE_ALREADY_REGISTERED | 该设备已注册 | 409 |
| EMAIL_ALREADY_BOUND | 当前账号已绑定邮箱 | 409 |
| EMAIL_BOUND_BY_OTHER | 邮箱已被其他账号绑定 | 409 |
| CODE_INVALID | 验证码错误 | 400 |
| CODE_EXPIRED | 验证码已过期 | 400 |
| CODE_MAX_ATTEMPTS | 验证码尝试次数超限 | 400 |
| CODE_SEND_TOO_FREQUENT | 验证码发送过于频繁 | 429 |
| INVALID_INPUT | 输入验证失败 | 400 |
| WRONG_PASSWORD | 访问密码不正确 | 401 |
| RATE_LIMIT_EXCEEDED | 请求频率超限 (>60/min) | 429 |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| 未注册就尝试上传 | 先检查 ~/.config/artifact-share/config.yml，无 api_key 则先注册 |
| 丢失 API Key | 注册后立即写入 config.yml，同一 device_id 只能注册一次 |
| device_id 格式错误 | 仅允许字母、数字、下划线、点和连字符，长度 4-64 |
| 上传不支持的文件类型 | 检查白名单：html/css/js/png/jpg/jpeg/gif/svg/webp/ico/bmp/woff/woff2/ttf/otf/eot |
| 项目名含大写/特殊字符 | 项目名 1-60 字符（自动 trim、拒控制字符）；带文件上传时可省略（从文件名派生），仅建空项目时必填 |
| 项目超过大小限制 | 项目总大小 ≤ 5MB（5 文件以内）；单次上传 ≤ 3MB |
| 每次修改都新建项目 | 复用 project_id 走 PUT /projects/{id}/files，URL 不变；只有需要全新独立页面时才新建 |
| 上传后未返回分享链接给用户 | 必须提取 URL 并明确展示给用户 |
