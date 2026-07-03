---
name: creator-skill-v2
description: Creator SKILL v2 (SKILL-02) — standalone influencer search on TikTok, Instagram, YouTube via skill.deinai.ai. Register, Stripe subscribe, sk_live_ token, MCP search. Not the legacy deinai.ai creator-skill (SKILL-01).
version: 2.0.6
homepage: https://skill.deinai.ai/portal/docs/creator-skill-v2/SKILL.md
metadata:
  openclaw:
    requires:
      env: []
    primaryEnv: null
  displayName: Creator SKILL v2
---

# Creator SKILL v2

**SKILL-02（无耦合版）** — 独立账号、Stripe 订阅、`sk_live_` 鉴权，与 DeiNai 主平台（SKILL-01 / `creator-skill`）**账号与积分不互通**。

**服务：** [https://skill.deinai.ai](https://skill.deinai.ai) · MCP: `https://skill.deinai.ai/mcp`

> **附件在线阅读（双端可点开）：** [ClawHub 文件索引](https://clawhub.ai/api/v1/skills/creator-skill-v2/file?path=references/online-read.md) · [SkillHub 文件索引](https://skill.deinai.ai/portal/docs/creator-skill-v2/references/online-read.md)

## When to use

- User wants influencer/KOL discovery on **tiktok** | **instagram** | **youtube**.
- User can register on Skill portal or you automate onboarding (register → subscribe → token → MCP).

## When NOT to use

- User is on **deinai.ai** platform MCP JWT / team credits → use legacy ClawHub **`creator-skill`** (SKILL-01).
- Outreach, payments inside DeiNai app, or platforms other than the three above.

## Prerequisites

1. Skill account at [skill.deinai.ai](https://skill.deinai.ai) with active subscription / credits.
2. API token `sk_live_...` — [references/install.md](https://clawhub.ai/api/v1/skills/creator-skill-v2/file?path=references/install.md) · [SkillHub](https://skill.deinai.ai/portal/docs/creator-skill-v2/references/install.md)
3. OpenClaw MCP: `openclaw mcp set creator-skill-v2` → `https://skill.deinai.ai/mcp`

## First-time onboarding (OpenClaw TUI)

1. [references/onboarding.md](https://clawhub.ai/api/v1/skills/creator-skill-v2/file?path=references/onboarding.md) · [SkillHub](https://skill.deinai.ai/portal/docs/creator-skill-v2/references/onboarding.md) — full OC-01…OC-12 flow
2. [references/stripe-payment-automation.md](https://clawhub.ai/api/v1/skills/creator-skill-v2/file?path=references/stripe-payment-automation.md) · [SkillHub](https://skill.deinai.ai/portal/docs/creator-skill-v2/references/stripe-payment-automation.md)
3. **生产一键 Prompt：** [references/openclaw-tui-prompt.txt](https://clawhub.ai/api/v1/skills/creator-skill-v2/file?path=references/openclaw-tui-prompt.txt) · [SkillHub](https://skill.deinai.ai/portal/docs/creator-skill-v2/references/openclaw-tui-prompt.txt)（路径 C，粘贴到 `openclaw tui`）

本地安装后 Agent 仍可读相对路径 `references/...`（`clawhub install` 解压目录）。

## Agent workflow

1. Confirm **platform** and **query**; do not guess.
2. `GET /api/v1/account/status` with `sk_live_` — if `canSearch` false → subscription/recharge URLs in response.
3. Location names → `get_location_ids` → `searchInfluencers.locations`.
4. On 402 / `RECHARGE_REQUIRED` → portal subscription page.

## Tools

| Tool | Purpose |
|------|---------|
| `ping` | Health |
| `get_location_ids` | Location name → ID |
| `searchInfluencers` | AI search; credits per row returned |

See [references/tools.md](https://clawhub.ai/api/v1/skills/creator-skill-v2/file?path=references/tools.md) · [SkillHub](https://skill.deinai.ai/portal/docs/creator-skill-v2/references/tools.md), [references/errors.md](https://clawhub.ai/api/v1/skills/creator-skill-v2/file?path=references/errors.md) · [SkillHub](https://skill.deinai.ai/portal/docs/creator-skill-v2/references/errors.md)

## Install

```bash
clawhub install creator-skill-v2
openclaw gateway restart
```

MCP: [references/install.md](https://clawhub.ai/api/v1/skills/creator-skill-v2/file?path=references/install.md) · [SkillHub](https://skill.deinai.ai/portal/docs/creator-skill-v2/references/install.md) (`creator-skill-v2` server name).
