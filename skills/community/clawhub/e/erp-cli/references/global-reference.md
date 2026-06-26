# 全局参考

本文档包含 erp-cli 的全局规则：配置、认证、Token 管理、API 兜底命令、退出码、输出格式。

## 配置管理

### 初始化

首次使用需运行：

```bash
erp-cli --as me config init
```

默认连接生产环境 `https://club.erp.windaka.com/prod-api`，如需指定其他地址：

```bash
erp-cli --as me config init --base-url https://your-erp-server.com/prod-api
```

### 查看配置

```bash
erp-cli --as me config show
```

### 修改配置

**RAGFlow 知识库配置：**

```bash
# 交互式配置 URL + API Key + 知识库 ID（AI 应使用此方式，让用户自己填写）
erp-cli --as me config ragflow
```

命令会依次提示输入 URL、API Key，并自动查询列出可用知识库让用户选择。

**逐项手动配置：**

```bash
# 设置 RAGFlow 地址和 API Key
erp-cli --as me config set ragflow.baseUrl http://223.80.101.21:39054
erp-cli --as me config set ragflow.apiKey ragflow-xxxxxxxx

# 设置默认检索的知识库 ID（JSON 数组或逗号分隔都支持）
erp-cli --as me config set ragflow.defaultDatasetIds '["id1","id2"]'
erp-cli --as me config set ragflow.defaultDatasetIds id1,id2
```

### 多环境支持

```bash
erp-cli --as me config init --name staging --base-url https://staging.example.com/prod-api
erp-cli --profile staging workorder +list
```

## 多用户隔离（--as 参数，强制必传）

**所有命令都必须带 `--as <id>`**，否则 CLI 拒绝执行：

```json
{"ok":false,"error":{"type":"validation","code":4,"message":"--as is required for all commands","hint":"..."}}
```

CLI 按命名空间（namespace）隔离 token，多用户互不影响。

**namespace 清洗规则**：仅保留 `[a-zA-Z0-9_.-]`，非法字符（含中文、空格）替换为 `_`，长度截断到 64。

**token 存储路径**：`~/.erp-cli/tokens/{profile}/{namespace}.json`

**各场景使用方式**：

| 场景 | 命令示例 | namespace |
|------|---------|-----------|
| 企业微信 / OpenClaw | `erp-cli --as XingWenKai workorder +list` | `XingWenKai` |
| 本地 Claude Code | `erp-cli --as me workorder +list` | `me` |
| CI / 自动化 | `erp-cli --as ci_bot workorder +list` | `ci_bot` |

**注意**：一个 namespace 同时只能保存一个 ERP 账号的 token。重复登录会覆盖旧的。

## 认证（Device Flow）

### 两步登录（AI Agent 必须使用）

AI Agent 平台（OpenClaw、Claude Code 等）采用"一次调用→一次输出"模型，不能处理中间输出。因此登录必须拆成两步：

```bash
# Step 1: 申请验证链接（立即返回，不阻塞）
erp-cli --as <namespace> auth login-start

# Step 2: 轮询等待授权结果
erp-cli --as <namespace> auth login-wait --device-code <device_code>
```

**AI 必须严格按以下流程执行**：

```
Step 1 — 执行 erp-cli --as <身份> auth login-start
         命令立即返回，输出包含：
         - device_code: 轮询时用的设备码
         - verification_uri_complete: 用户在浏览器中打开的链接
         - expires_in: 有效期（秒）

Step 2 — 立即给用户回复：
         "请点击此链接完成登录：<verification_uri_complete>
          在浏览器中选择集团并输入账号密码，我会等你授权完成"

Step 3 — 执行 erp-cli --as <身份> auth login-wait --device-code <device_code>
         此命令会阻塞，每 5 秒轮询一次，最长等待 5 分钟
         等待期间不要做其他操作

Step 4 — 命令返回后，根据最终输出告诉用户：
         成功 → "登录成功！欢迎 <username>（<group>）"
         超时 → "授权超时（5 分钟内未完成），请告诉我'重新登录'"
```

**❌ 绝对禁止的行为**：
- 只调 login-start 不调 login-wait — 错误！token 不会保存到本地，等于没登录
- 给完链接就把任务结束 — 错误！必须执行 Step 3 和 Step 4
- 两步使用不同的 `--as` 值 — 错误！会保存到错误的 namespace
- 不带 `--as` 但企业微信场景下 — 错误！会用系统用户名做 namespace 导致串号

**✅ 正确的心智模型**：
- `login-start` = 拿链接（快速返回）
- `login-wait` = 等结果（阻塞轮询）+ 保存 token 到 namespace
- 两步必须用相同的 `--as` 值

### 一步登录（仅 CLI 直接使用）

```bash
erp-cli --as <namespace> auth login
```

此命令合并了 login-start + login-wait，会阻塞最长 5 分钟。适用于 CLI 直接在终端运行。AI Agent 不要用这个命令。

**命令行为**：
1. 调用后端 `POST /auth/device/code` 获取设备码和验证链接
2. 自动尝试打开浏览器，同时输出验证链接 JSON
3. 每 5 秒轮询 `POST /auth/device/token`，最长等待 5 分钟
4. 用户在浏览器中完成授权后，命令自动检测到并保存 Token

**输出示例**：

验证链接（命令启动后立即输出）：
```json
{
  "ok": true,
  "data": {
    "verification_uri_complete": "https://club.erp.windaka.com/aloneDevice?code=dc_xxx",
    "expires_in": 300,
    "hint": "Open verification_uri_complete in a browser to complete login..."
  }
}
```

授权成功：
```json
{"ok": true, "data": {"username": "admin", "group": "荣管家集团", "group_id": "100", "expires_at": "2026-05-22 15:00:00"}}
```

授权超时：
```json
{"ok": false, "error": {"type": "auth", "message": "authorization timed out"}}
```

### 查看认证状态

```bash
erp-cli --as <namespace> auth status   # 查看指定 namespace
erp-cli --as <namespace> auth list     # 列出当前 profile 下所有已登录 namespace（--as 必传但不影响结果）
```

返回当前登录用户、所属集团、Token 有效期。`auth list` 还会标记哪个是当前 namespace。

### 退出登录

```bash
erp-cli --as <namespace> auth logout    # 只删除该 namespace 的 token
```

### Token 管理

- Token 有效期 720 分钟（12 小时）
- Token 过期后**不会自动重新登录** — 业务命令返回 `{"ok":false,"error":{"type":"auth"}}`，AI 必须按 hint 重新执行两步登录
- Token 按 namespace 隔离，保存在 `~/.erp-cli/tokens/{profile}/{namespace}.json`
- 登录成功后 Token 中的 `topLevelId` 会自动注入到工单等接口的请求体中

## API 兜底命令

当 Shortcut 不满足需求时，可直接调用原始 API：

```bash
# GET 请求
erp-cli --as <身份> api GET /workorder/master/323407/301619

# POST 请求
erp-cli --as <身份> api POST /workorder/master/list --data '{"pageNum":1,"pageSize":10}'

# 带查询参数
erp-cli --as <身份> api GET /system/dept/topLevelList --params '{"deptName":"荣管家"}'
```

**注意**：`api` 命令自动注入 Bearer Token，路径相对于 Base URL（如 `/workorder/master/list` 实际请求 `https://club.erp.windaka.com/prod-api/workorder/master/list`）。

## 退出码

| 退出码 | 含义 | 处理 |
|--------|------|------|
| 0 | 成功 | 解析 `data` 返回结果给用户 |
| 1 | 一般错误 | 读取 `error.message` 告知用户 |
| 2 | 配置错误 | 执行 `erp-cli --as me config init` |
| 3 | 认证错误 | 执行 `erp-cli --as <身份> auth login-start` 并把链接发给用户 |
| 4 | 参数校验错误 | 补充缺少的参数重新执行 |
| 5 | 网络错误 | 检查网络连接，稍后重试 |

## 输出格式

所有命令输出为统一的 JSON 信封格式：

```json
{"ok": true, "data": {"id": 323407, "workOrderNumber": "GD20260521001"}}

{"ok": false, "error": {"type": "auth", "code": 3, "message": "token expired", "hint": "run `erp-cli auth login` to re-authenticate"}}
```

**判断成功或失败：检查 `ok` 字段，`true` 表示成功，`false` 表示失败。失败时从 `error` 中提取信息。**