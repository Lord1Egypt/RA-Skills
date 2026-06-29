---
name: clawbba-api
description: "ClawBBA × OpenClaw — One API key, 369+ models, supporting all instant messaging channels (web chat, WeChat, Telegram)."
metadata: {"openclaw":{"requires":{"env":["CLAWBBA_API_KEY"]},"always":true,"emoji":"🦞","homepage":"https://www.clawbba.com/agent/api-keys"}}
---

# ClawBBA × OpenClaw

**One API key · 369+ models · Chat, image & video**  
**一个 Key · 369+ 模型 · 对话 / 生图 / 生视频**

API: `https://www.clawbba.com/api/v1` · Key 前缀: `cbb_sk_live_`

---

## 中文

### 这是什么

将 OpenClaw 接入 [ClawBBA](https://www.clawbba.com)：用 **Platform API Key** 调用站内全部模型（对话、生图、生视频）。支持 WebChat、微信、Telegram 等渠道。

### 使用前（浏览器完成）

1. [注册 / 登录](https://www.clawbba.com)
2. [充值 CDKey](https://www.clawbba.com/product/CDKEY)
3. [创建 API Key](https://www.clawbba.com/agent/api-keys)（`cbb_sk_live_`，仅显示一次）

### 安装与配置（两步都要做）

> **重要：`skills install` 只下载技能，不会自动写好 OpenClaw 配置。必须再跑 `setup.sh`。**

**推荐 — 一键安装（下载技能 + 自动配置）：**

```bash
export CLAWBBA_API_KEY='cbb_sk_live_你的密钥'
curl -fsSL https://www.clawbba.com/downloads/install-clawbba-api.sh | bash
openclaw gateway restart
```

**已从 ClawHub 安装 — 补跑配置：**

```bash
export CLAWBBA_API_KEY='cbb_sk_live_你的密钥'
bash ~/.openclaw/skills/clawbba-api/scripts/setup.sh --yes
openclaw config validate
openclaw gateway restart
```

`setup.sh` 会：校验 Key、拉取模型、写入 `openclaw.json`、同步 `models.json`、注入媒体 patch。详见 `references/onboarding.md`。

### 使用

| 场景 | 做法 |
|------|------|
| 文本对话 | `/model clawbba/<model-id>` |
| 生图 / 生视频 | 自然语言描述；Agent 调用 `image_generate` / `video_generate` |
| 切换模型 | `openclaw models set clawbba/<id>` 或聊天内 `/model` |

生图示例：`请使用 ClawBBA 生成图片，16:9 横图：海边日落`  
指定模型：`模型 google/gemini-3.1-flash-image-preview，9:16 竖图：…`

完成后 Agent 在回复中写 **`MEDIA:<本地路径>`**（文件在 `~/.openclaw/media/`）。详见 `references/media-delivery-local.md`。

### 常见问题

| 现象 | 处理 |
|------|------|
| 装了 skill 但不能用 | 未跑 `setup.sh` → 见上文「补跑配置」 |
| 没有生图/生视频工具 | OpenClaw ≥ 2026.5.28，重跑 `setup.sh` 并重启 Gateway |
| Key 无效 / 余额不足 | 重新创建 Key 或 [充值 CDKey](https://www.clawbba.com/product/CDKEY) |
| 有图但 WebChat 不显示 | 重跑 `setup.sh`；`node scripts/verify-openclaw-patch.mjs` |
| 已扣费无图/无视频 | `action=tasks` 查 jobId → `action=recover jobId=… timeoutMs=600000`（同一 job，勿重新 generate） |
| 会话锁 / 卡住 | 停 Gateway → 删 `~/.openclaw/agents/main/sessions/*.lock` → 新开对话 |

更多：`references/onboarding.md` · 完整排障：`references/SKILL-troubleshooting.md` · API：`references/api-endpoints.md`

---

## English

### What this is

Connect [OpenClaw](https://docs.openclaw.ai/) to [ClawBBA](https://www.clawbba.com) with a **Platform API Key** — chat, image, and video models via one OpenAI-compatible API. Works with WebChat, WeChat, Telegram, and other channels.

### Before you start (browser)

1. [Sign in / register](https://www.clawbba.com)
2. [Top up with CDKey](https://www.clawbba.com/product/CDKEY)
3. [Create API Key](https://www.clawbba.com/agent/api-keys) (`cbb_sk_live_`, shown once)

### Install & configure (both steps required)

> **Important: `skills install` only downloads the skill. It does not configure OpenClaw. You must run `setup.sh`.**

**Recommended — one-line install (skill + config):**

```bash
export CLAWBBA_API_KEY='cbb_sk_live_YOUR_KEY'
curl -fsSL https://www.clawbba.com/downloads/install-clawbba-api.sh | bash
openclaw gateway restart
```

**Already installed from ClawHub — run setup:**

```bash
export CLAWBBA_API_KEY='cbb_sk_live_YOUR_KEY'
bash ~/.openclaw/skills/clawbba-api/scripts/setup.sh --yes
openclaw config validate
openclaw gateway restart
```

### Usage

| Task | How |
|------|-----|
| Text chat | `/model clawbba/<model-id>` |
| Image / video | Describe in natural language; Agent uses `image_generate` / `video_generate` |
| Switch model | `openclaw models set clawbba/<id>` or `/model` in chat |

On success, Agent replies with **`MEDIA:<local-path>`** under `~/.openclaw/media/`. See `references/media-delivery-local.md`.

### Troubleshooting

| Issue | Fix |
|-------|-----|
| Skill installed but nothing works | Run `setup.sh` (see above) |
| No image/video tools | OpenClaw ≥ 2026.5.28; re-run `setup.sh`; restart Gateway |
| Invalid key / low balance | Recreate key or [top up CDKey](https://www.clawbba.com/product/CDKEY) |
| Image generated but not in WebChat | Re-run `setup.sh`; run `verify-openclaw-patch.mjs` |
| Billed but no image/video received | `action=tasks` → `action=recover jobId=… timeoutMs=600000` (same job; do not regenerate) |

More: `references/onboarding.md` · Full troubleshooting: `references/SKILL-troubleshooting.md`

---

## Agent（技能加载时必读 · Agent essentials）

本技能负责：**引导用户完成 Key + `setup.sh`**，并按 ClawBBA 规范使用媒体工具。

**对用户只称 ClawBBA**（不说第三方上游品牌名）。工具报错须读 `references/error-translation.md` 翻译后再回复，勿原样粘贴日志。

**完整规则（必读）：**

- 行为：`references/openclaw-agent-behavior.md`
- 错误话术：`references/error-translation.md`
- 媒体能力表：`references/media-capabilities.json`
- 模型与工具参数：`references/media-model-ref.md`
- 架构：`references/openclaw-integration-spec.md`

**摘要：**

- 文本对话：`/model clawbba/<text-model-id>`；生图/生视频只用 `image_generate` / `video_generate`
- 未指定模型时用 `setup.sh` 写入的默认（`imageGenerationModel.primary` / `videoGenerationModel.primary`）
- `Background task started` → 勿重复 generate，等待 completion
- **已扣费 / timeout / 用户未收到** → `action=tasks` 查 jobId，再 `action=recover jobId=<id> timeoutMs=600000`（生图 `image_generate`、生视频 `video_generate`）；**禁止**重新 generate
- 本地已有文件但用户没看到 → redeliver 已有 `MEDIA:` 路径（勿 recover、勿 regenerate）
- WebChat 完成回复用 `MEDIA:<path>`，勿用 `message` 工具发媒体
- ClawHub 仅安装技能时 → **主动引导用户执行 `setup.sh --yes` 并 `gateway restart`**

---

## 安全 · Security

- 勿将 `CLAWBBA_API_KEY` 提交到 Git  
- Key 写入本机 `~/.openclaw/`（`setup.sh`，权限 600）

## 链接 · Links

- 网站 / Site: https://www.clawbba.com  
- 充值 / Top-up: https://www.clawbba.com/product/CDKEY  
- API Keys: https://www.clawbba.com/agent/api-keys
