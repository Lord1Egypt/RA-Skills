# Creator SKILL — 错误与处理

**Skill MCP：** `https://skill.deinai.ai/mcp`  
**Skill REST 搜索：** `POST https://skill.deinai.ai/api/v1/search/influencers`

## HTTP 层（/mcp 与 REST）

| 状态 / 字段 | 含义 | Agent 建议 |
|-------------|------|------------|
| 401 `TOKEN_REQUIRED` | 缺少或无效 `sk_live_` | 检查 Bearer；勿用 `sk_sess_` 调业务接口 |
| 401 `SESSION_REQUIRED` | Session 无效（仅门户接口） | 重新 `POST /api/v1/auth/login` |
| 401 `SKILL_TOKEN_REQUIRED` | 用 session 访问了 MCP/搜索 | 改用 `sk_live_` |
| 403 | 用 `sk_live_` 创建 API Token | 创建 token 必须用 session |
| 4xx/5xx | 网关或服务异常 | 稍后重试 |

## 业务 `code` 字段（工具 / REST 统一）

| code | errorCode | 说明 |
|------|-----------|------|
| 0 | — | 成功 |
| 402 | `RECHARGE_REQUIRED` | 余额为 0，搜索前门控或 REST 返回 |
| 402 | `RENEWAL_REQUIRED` | 订阅过期，需续费 |
| 402 | `CREDITS_INSUFFICIENT` | 余额不足以支付本次返回条数 |

**Agent 行为：**

- `RECHARGE_REQUIRED` → 引导 [skill.deinai.ai/recharge](https://skill.deinai.ai/recharge)
- `RENEWAL_REQUIRED` → 引导 [skill.deinai.ai/subscription/renew](https://skill.deinai.ai/subscription/renew)
- `CREDITS_INSUFFICIENT` → 同上或减小 `pageSize`

## account/status 门控

```http
GET /api/v1/account/status
```

| 字段 | 含义 |
|------|------|
| `canSearch` | `false` 时不应调用搜索 |
| `needsRecharge` | 需充值 |
| `needsRenewal` | 需续费 |

## Legacy（deinai.ai）

| 现象 | 说明 |
|------|------|
| `Invalid MCP token type` | 误用登录 JWT 调 legacy MCP |
| `CREDITS_INSUFFICIENT` + `feature: search` | Legacy backend 积分不足 |

Legacy 与 Skill 积分 **不互通**。

## 调试

- Skill 服务日志：`[MCP] searchInfluencers`、`[SkillAuth]`
- OpenClaw：`openclaw logs --level debug`
- 本地：`python scripts/seed_dev_account.py` 快速造测试 token
