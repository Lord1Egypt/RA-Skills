# Creator SKILL — 错误与处理

**MCP 端点：** `https://deinai.ai/mcp`

## HTTP 层（/mcp）

| 状态 | 含义 | Agent 建议 |
|------|------|------------|
| 401 | 缺少或无效 `Authorization` | 检查 Bearer 是否为 MCP Token（`type: mcp`） |
| 401 | `Invalid MCP token type` | 误用登录 JWT；应使用 `POST https://deinai.ai/api/v1/mcp/tokens` 创建的 token |
| 4xx/5xx | 网关或服务异常 | 稍后重试 |

## 工具返回 `code` 字段

| code | 说明 |
|------|------|
| 0 | 成功 |
| 402 | 积分不足，`errorCode`: `CREDITS_INSUFFICIENT`，`feature`: `search` |

用户可在 [https://deinai.ai](https://deinai.ai) 充值或升级套餐。

## 调试

- 服务端日志：`[MCP] searchInfluencers`、`[MCP Auth]`
- OpenClaw：`openclaw logs --level debug`
