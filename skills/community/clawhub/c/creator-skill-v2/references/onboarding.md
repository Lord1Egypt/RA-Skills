# Creator SKILL — OpenClaw 首次开通闭环



本文描述 **ClawHub 安装 creator-skill-v2 后**，OpenClaw Agent 应自动完成的开通流程（注册 → 订阅 → Token → MCP 搜索）。



**生产环境：** `https://skill.deinai.ai`



| 变量 | 说明 |

|------|------|

| `SKILL_API_BASE_URL` | API 根地址 |

| `SKILL_OPENCLAW_AUTOMATION_KEY` | 测试全自动支付（见 [stripe-payment-automation.md](./stripe-payment-automation.md)） |



---



## Agent 必须遵守的顺序



```

1. GET  /health

2. POST /api/v1/auth/register   （新用户；或 login 复用）

3. GET  /api/v1/subscriptions/plans

4. POST /api/v1/subscriptions/checkout  （plan_code=starter, channel=stripe）

5. 支付 — 按 stripe-payment-automation.md 路径 A → B → C（禁止等用户说 paid）

6. GET  /api/v1/subscriptions/orders/{order_no} 轮询至 paymentSucceeded

7. POST /api/v1/tokens  → sk_live_

8. openclaw mcp set creator-skill-v2

9. GET  /api/v1/account/status  （canSearch=true）

10. MCP ping → get_location_ids → searchInfluencers

```



**禁止：** 用 `sk_sess_` 调 MCP；`canSearch=false` 时搜索；支付后依赖用户口头确认而不轮询。



---



## Step 5 — 支付（详见 stripe-payment-automation.md）



| 路径 | 何时用 | 用户操作 |

|------|--------|----------|

| **A 全自动** | 测试机配置了 `SKILL_OPENCLAW_AUTOMATION_KEY` | **无** |

| **B 浏览器自动化** | 有 browser Skill + 测试模式 Stripe | 通常 **无**（自动填 4242） |

| **C 人工+轮询** | 生产或无法自动化 | **仅** Stripe 绑卡/支付页 |



路径 A 示例：



```http

POST {SKILL_API_BASE_URL}/api/v1/subscriptions/automation/complete-checkout

Authorization: Bearer <sk_sess_...>

X-Skill-Automation-Key: <SKILL_OPENCLAW_AUTOMATION_KEY>

Content-Type: application/json



{ "orderNo": "SUB..." }

```



路径 C 轮询：



```http

GET {SKILL_API_BASE_URL}/api/v1/subscriptions/orders/{order_no}

Authorization: Bearer <sk_sess_...>

```



每 5s，最多 2 分钟，直到 `paymentSucceeded: true`。



---



## Step 1–4、6–10



（注册、登录、checkout、Token、MCP、搜索 — 同前，见 install.md）



### Step 4 — 创建 API Token



```http

POST {SKILL_API_BASE_URL}/api/v1/tokens

Authorization: Bearer <sk_sess_...>



{ "name": "openclaw", "expires_in_days": 365 }

```



### Step 5 — OpenClaw MCP



```bash

openclaw mcp set creator-skill-v2 '{

  "url": "{SKILL_API_BASE_URL}/mcp",

  "transport": "streamable-http",

  "headers": { "Authorization": "Bearer <sk_live_...>" },

  "connectionTimeoutMs": 180000,

  "timeoutMs": 180000

}'

```



---



## OpenClaw 对话 Prompt（一键粘贴）

| 环境 | 文件 | 说明 |
|------|------|------|
| **生产** | [openclaw-tui-prompt.txt](https://clawhub.ai/api/v1/skills/creator-skill-v2/file?path=references/openclaw-tui-prompt.txt) · [SkillHub](https://skill.deinai.ai/portal/docs/creator-skill-v2/references/openclaw-tui-prompt.txt) | `skill.deinai.ai`，真实 Stripe 支付，路径 C |

仓库内同步副本（发版前可 diff）：

- 生产：`apps/skill-service/scripts/openclaw_tui_prompt_prod.txt`

**用法：** `clawhub install creator-skill-v2` 后，在 `openclaw tui` 中粘贴对应 Prompt 全文；Agent 会结合 `SKILL.md` + 本目录文档执行。

**发布：** Prompt 随 ClawHub 包 `references/` 一并上传，无需单独上传；`clawhub publish --name creator-skill-v2` 即可。



---



## 自动化脚本



```bash

export SKILL_OPENCLAW_AUTOMATION_KEY=...

python scripts/e2e_openclaw_flow.py --suite happy --use-automation-api

```



详见 `apps/skill-service/docs/OPENCLAW_E2E_TEST.md`。

