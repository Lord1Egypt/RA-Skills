# Creator SKILL — 安装与鉴权

**Skill 名称：** Creator SKILL（Clawhub / OpenClaw 包名：`creator-skill`）

**生产环境：**

| 项 | 值 |
|----|-----|
| 产品 / API 根地址 | `https://deinai.ai` |
| MCP 端点 | `https://deinai.ai/mcp` |
| Transport | `streamable-http` |

## 1. 部署前提（Deinai 运营侧）

- `deinai_backend` 已在 `https://deinai.ai` 提供 HTTPS。
- 反向代理需将 `/mcp` 转发到应用（FastMCP `stateless_http`）。

## 2. 用户申请 MCP Token（Deinai 产品内）

MCP Token 与普通登录 JWT 不同（payload 含 `type: "mcp"`）。

1. 用户登录 [https://deinai.ai](https://deinai.ai)，取得 **用户 access token**（常规 API 鉴权）。
2. 创建 MCP Token：

```http
POST https://deinai.ai/api/v1/mcp/tokens
Authorization: Bearer <用户登录JWT>
Content-Type: application/json

{
  "token_name": "openclaw-home",
  "comment": "Creator SKILL / OpenClaw",
  "expired_type": "1year"
}
```

`expired_type` 可选：`1 day` | `1month` | `3month` | `1year` | `forever`

3. 响应 `data.jwt_token` 即为 **MCP Bearer Token**（只显示一次，请妥善保存）。
4. 管理：`GET/PATCH https://deinai.ai/api/v1/mcp/tokens`（列表、禁用）。

## 3. OpenClaw 配置 MCP Server

将 `<MCP_JWT_TOKEN>` 替换为上一节创建的 token：

```bash
openclaw mcp set creator-skill '{
  "url": "https://deinai.ai/mcp",
  "transport": "streamable-http",
  "headers": {
    "Authorization": "Bearer <MCP_JWT_TOKEN>"
  },
  "connectionTimeoutMs": 180000,
  "timeoutMs": 180000
}'
```

验证：

```bash
openclaw mcp list
# 在 Agent 中调用 ping 或 searchInfluencers
```

安装 Creator SKILL 后：

```bash
clawhub install creator-skill
openclaw gateway restart
```

## 4. 本地开发（可选）

若本地 `uvicorn` 运行在 8000，可临时改用：

```bash
openclaw mcp set creator-skill '{
  "url": "http://localhost:8000/mcp",
  "transport": "streamable-http",
  "headers": {
    "Authorization": "Bearer <MCP_JWT_TOKEN>"
  },
  "connectionTimeoutMs": 180000,
  "timeoutMs": 180000
}'
```

生产上架请使用 `https://deinai.ai/mcp`。

## 5. 安全提示

- 不要把真实 Token 写进 Skill、GitHub 或截图。
- Token 泄露后于 Deinai 控制台 **禁用** 该 token 并重新创建。
