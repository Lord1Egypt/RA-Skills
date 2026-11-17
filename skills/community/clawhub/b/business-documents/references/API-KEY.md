# API 密钥

推荐在平台创建通用 Key，并执行 `openclaw config set env.AI_SKILLS_API_KEY "你的平台APIKey"` 和 `openclaw gateway restart`，全平台 Skill 只需配置一次。仍需开通目标产品。下列 `BUSINESS_DOCUMENTS_API_KEY` 配置是兼容的产品专用覆盖项；调用优先使用该变量，为空时回退到 `AI_SKILLS_API_KEY`。两个变量均缺失时停止调用，不发送空 Bearer 请求。不要把旧请求换 Key 自动重试；幂等记录按 Key 隔离。


默认 API 根地址为 `https://ai-skills.open-idea.net/api/v1`；仅在平台运营方明确给出自托管地址时设置 `AI_SKILLS_API_URL`。密钥环境变量为 `BUSINESS_DOCUMENTS_API_KEY`。

每次请求使用：

```text
Authorization: Bearer ${BUSINESS_DOCUMENTS_API_KEY:-$AI_SKILLS_API_KEY}
Content-Type: application/json
Idempotency-Key: 每次新业务动作生成的新 UUID
```

不要在聊天、日志或产物中展示完整密钥。此 Skill 使用平台本地能力，不配置服务提供方，也不需要第三方账号或第三方付费服务。

## 费用与账户

从 ClawHub 安装 Skill 免费。调用 AI Skills 平台需要注册账号、开通“业务单据”并使用平台钱包余额；平台只对成功操作扣费。当前默认价格为：

- 创建单据：¥0.20/份
- 读取单据：免费
- 更新单据：¥0.10/次
- 导出单据：¥0.10/份

价格可能由平台管理员调整，实际金额以[业务单据产品页面](https://ai-skills.open-idea.net/skills/business-documents)及响应中的 `X-AI-Skills-Billing-Charged`、`X-AI-Skills-Billing-Currency` 和 `X-AI-Skills-Billing-Balance` 为准。执行付费操作前向用户说明会扣除平台余额。
