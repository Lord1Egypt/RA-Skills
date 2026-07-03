# Creator SKILL — 安装与鉴权

**Skill 名称：** Creator SKILL v2（Clawhub / OpenClaw 包名：`creator-skill-v2`）

**Skill 服务（推荐）：**

| 项 | 值 |
|----|-----|
| 门户 / API 根地址 | `https://skill.deinai.ai` |
| MCP 端点 | `https://skill.deinai.ai/mcp` |
| Transport | `streamable-http` |
| Coze REST 搜索 | `POST https://skill.deinai.ai/api/v1/search/influencers` |

## Token 体系

| 类型 | 前缀 | 用途 |
|------|------|------|
| Session | `sk_sess_` | 门户登录后管理 API Token、充值（**不要**用于 MCP/OpenClaw/Coze 搜索） |
| API Token | `sk_live_` | MCP、REST 搜索、钱包查询 |

## 1. 部署前提（运营侧）

- Skill 服务已在 `https://skill.deinai.ai` 提供 HTTPS。
- 反向代理将 `/mcp` 转发到 FastMCP（`stateless_http`）。
- 独立 PostgreSQL 库 `skills`（与 legacy backend 分离）。

## 2. 用户获取 API Token

### 2.1 注册 / 登录

```http
POST https://skill.deinai.ai/api/v1/auth/register
Content-Type: application/json

{ "email": "you@example.com", "password": "your-password", "displayName": "My Team" }
```

```http
POST https://skill.deinai.ai/api/v1/auth/login
Content-Type: application/json

{ "email": "you@example.com", "password": "your-password" }
```

响应：

```json
{
  "code": 0,
  "data": {
    "sessionToken": "sk_sess_...",
    "expiresAt": "2026-06-19T12:00:00+00:00"
  }
}
```

### 2.2 充值积分

在门户 [skill.deinai.ai/recharge](https://skill.deinai.ai/recharge) 完成微信/支付宝充值，或运营侧调账。

创建 API Token 前账户需 **余额 > 0**。

### 2.3 创建 API Token

```http
POST https://skill.deinai.ai/api/v1/tokens
Authorization: Bearer <sk_sess_...>
Content-Type: application/json

{
  "name": "openclaw-home",
  "expires_in_days": 365
}
```

响应 `data.token`（`sk_live_...`）**只显示一次**，请妥善保存。

### 2.4 管理 Token

```http
GET https://skill.deinai.ai/api/v1/tokens
Authorization: Bearer <sk_sess_...>

DELETE https://skill.deinai.ai/api/v1/tokens/{token_id}
Authorization: Bearer <sk_sess_...>
```

### 2.5 登出 Session

```http
POST https://skill.deinai.ai/api/v1/auth/logout
Authorization: Bearer <sk_sess_...>
```

## 3. OpenClaw 配置 MCP Server

将 `<SKILL_API_TOKEN>` 替换为 `sk_live_...`：

```bash
openclaw mcp set creator-skill-v2 '{
  "url": "https://skill.deinai.ai/mcp",
  "transport": "streamable-http",
  "headers": {
    "Authorization": "Bearer <SKILL_API_TOKEN>"
  },
  "connectionTimeoutMs": 180000,
  "timeoutMs": 180000
}'
```

验证：

```bash
openclaw mcp list
# Agent 中调用 ping 或 searchInfluencers
```

安装 Creator SKILL 后：

```bash
clawhub install creator-skill-v2
openclaw gateway restart
```

## 4. 本地开发

Skill 服务仓库：`apps/skill-service`

```bash
# 初始化 DB + 种子账号
python scripts/init_db.py
python scripts/seed_dev_account.py --email dev@demo.com --password "12345678" --credits 5000

# 启动
uvicorn main:app --host 0.0.0.0 --port 8080
```

OpenClaw 临时指向本地：

```bash
openclaw mcp set creator-skill-v2 '{
  "url": "http://localhost:8080/mcp",
  "transport": "streamable-http",
  "headers": { "Authorization": "Bearer <sk_live_...>" },
  "connectionTimeoutMs": 180000,
  "timeoutMs": 180000
}'
```

## 5. Coze 扣子配置

扣子工作流密钥名建议：`SKILL_API_TOKEN`（值为 `sk_live_...`）。

完整 SOP：[../../../coze/PATH-A-SOP.md](../../../coze/PATH-A-SOP.md)

## 6. Legacy（deinai.ai backend）

| 项 | 值 |
|----|-----|
| MCP | `https://deinai.ai/mcp` |
| Token | `POST /api/v1/mcp/tokens`（登录 JWT + MCP JWT） |

与 Skill 服务 **积分不互通**，新接入请勿混用。

## 7. 安全提示

- 不要把真实 Token 写进 Skill、GitHub 或截图。
- `sk_live_` 泄露后于门户 **吊销** 并重新创建。
- Session（`sk_sess_`）过期后重新登录即可。
