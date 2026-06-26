# 📰 Industry Daily Brief

> **Turn any industry into a daily intelligence briefing — automated search, filtering, writing, and multi-channel delivery.**
>
> **[中文文档 / Chinese docs →](README_zh.md)**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-5.0.0-brightgreen.svg)](#changelog)
[![Platform](https://img.shields.io/badge/platform-CodeBuddy%20%7C%20WorkBuddy-green.svg)](#)
[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-%E2%9D%A4-pink.svg)](../../sponsors)
[![Bilingual](https://img.shields.io/badge/docs-EN%20%7C%20中文-orange.svg)](README_zh.md)

---

## 🤔 The Problem

You want a daily industry briefing — curated, structured, sourced, delivered to your team every morning. But building one means:

- **Hours of manual searching** across dozens of sources every day
- **No reliable filtering** — noise drowns out real signals
- **Copy-paste hell** — reformatting for Slack, email, WeChat, Teams...
- **No consistency** — some days you skip it, the habit breaks

**What if an AI agent could do all of this in 3 minutes?**

## 💡 The Solution

This is a **ready-to-use Skill** for [CodeBuddy](https://www.codebuddy.ai/) / WorkBuddy that turns your AI assistant into a professional industry intelligence analyst. Just say:

> *"Generate today's industry daily brief"*

The AI will automatically:

1. 🔍 **Search** the web using a 3-phase strategy (targeted → expanded → source-traced)
2. 🎯 **Filter** ruthlessly — only first-hand sources, no noise, no clickbait
3. 📝 **Write** a structured briefing with sources, summaries, and impact analysis
4. 📤 **Deliver** to 9 channels — Slack, Teams, email, WeChat, DingTalk, and more

### 🏭 Works for Any Industry

The default configuration covers **Data + AI infrastructure** (data platforms, lakehouse, streaming, governance, etc.) — but **you can customize it for any domain**:

| Your Industry | Just Change `focus_areas` + `SKILL.md` Prompt |
|---|---|
| FinTech / Banking | Payments, digital banking, RegTech, DeFi |
| HealthTech / BioAI | Clinical AI, drug discovery, EHR, FDA approvals |
| Cybersecurity | Threat intel, zero-trust, CVEs, vendor updates |
| DevTools / Platform Eng | CI/CD, observability, IaC, developer experience |
| E-commerce / Retail Tech | Personalization, logistics tech, marketplace |
| *Your niche here* | Any industry with public news sources |

👉 See [Customization](#-customization) for a step-by-step guide.

## ✨ Features

- 🔍 **3-phase search strategy** — targeted vendor search → expanded discovery → mandatory source tracing
- 🎯 **Strict signal-to-noise filtering** — first-hand sources only, no rewrites or clickbait
- 📝 **Structured output** — Top Signals, Product & Tech, Views & Research, Capital & Corporate, Watchlist
- 🎯 **Quality over quantity** — sections left empty rather than filled with low-relevance content ("less is more" principle)
- 🌐 **9 delivery channels** — WeChat Work · DingTalk · Feishu · Slack · Discord · Telegram · Teams · Email · GitHub Pages
- 🎨 **Beautiful HTML reports** — card-based layout with clickable source links (links only in HTML, summaries stay clean text)
- 📊 **Smart 3-layer summary extraction** — title + top changes + section headlines + per-item sentence summaries, strictly within 4096-byte WeChat limit
- 🔒 **Duplicate push prevention** — lock-file mechanism prevents re-sending the same day's brief
- 📅 **Monday weekend catch-up** — 72-hour window on Mondays covers Friday–Sunday, with expanded item limits
- ⚙️ **Fully customizable** — industry focus, vendor lists, output language, delivery channels
- 🌍 **Bilingual** — works in Chinese or English (or any language you configure)

## 📦 Project Structure

```
data-ai-daily-brief-skill/
├── SKILL.md                    # Skill definition (core instructions)
├── README.md                   # This file (English)
├── README_zh.md                # 中文文档
├── LICENSE                     # MIT License
├── CONTRIBUTING.md             # Contribution guide
├── scripts/
│   ├── init_config.py          # Initialize default config
│   ├── send_wecom.py           # 🇨🇳 WeChat Work (3-layer summary + lock)
│   ├── send_dingtalk.py        # 🇨🇳 DingTalk
│   ├── send_feishu.py          # 🇨🇳 Feishu / Lark
│   ├── send_slack.py           # 🌍 Slack
│   ├── send_discord.py         # 🌍 Discord
│   ├── send_telegram.py        # 🌍 Telegram
│   ├── send_teams.py           # 🌍 Microsoft Teams
│   ├── send_email.py           # 📧 Email (SMTP)
│   └── deploy_github.py        # 🌐 GitHub Pages
├── .github/
│   └── FUNDING.yml             # GitHub Sponsors config
└── assets/
    └── report-template.html    # HTML report template
```

## 🚀 Quick Start

### Option 1: As a CodeBuddy / WorkBuddy Skill

1. **Copy the Skill into your project**:
   ```bash
   cp -r data-ai-daily-brief-skill .codebuddy/skills/data-ai-daily-brief
   ```

2. **Talk to your AI**:
   - *"Generate today's Data+AI daily brief"*
   - *"Create a daily report for 2026-03-10"*
   - The Skill triggers automatically and runs the full pipeline.

3. **Configure delivery** (optional):
   ```bash
   python .codebuddy/skills/data-ai-daily-brief/scripts/init_config.py
   ```
   Edit the generated `daily-brief-config.json` to add your webhook URLs.

### Option 2: Import the Skill

1. Open CodeBuddy / WorkBuddy Settings
2. Navigate to **Skills** management
3. Click **"Import Skill"**
4. Select this folder

### Option 3: Use Scripts Standalone

```bash
# Initialize config
python scripts/init_config.py

# === China channels ===
python scripts/send_wecom.py 2026-03-11          # WeChat Work
python scripts/send_wecom.py 2026-03-11 --force   # Force re-send
python scripts/send_dingtalk.py 2026-03-11       # DingTalk
python scripts/send_feishu.py 2026-03-11         # Feishu
python scripts/send_feishu.py --card --link-url https://...  # Feishu interactive card

# === Global channels ===
python scripts/send_slack.py 2026-03-11          # Slack
python scripts/send_discord.py 2026-03-11        # Discord
python scripts/send_telegram.py 2026-03-11       # Telegram
python scripts/send_teams.py 2026-03-11          # Microsoft Teams

# === Universal ===
python scripts/send_email.py 2026-03-11          # Email
python scripts/deploy_github.py 2026-03-11       # GitHub Pages
```

## ⚙️ Configuration

### daily-brief-config.json

```json
{
  "version": "2.0",
  "adapters": {
    "wechatwork": { "enabled": true, "webhook_url": "YOUR_WEBHOOK_URL" },
    "dingtalk":   { "enabled": true, "webhook_url": "YOUR_URL", "secret": "optional" },
    "feishu":     { "enabled": true, "webhook_url": "YOUR_URL", "secret": "optional" },
    "slack":      { "enabled": true, "webhook_url": "YOUR_URL" },
    "discord":    { "enabled": true, "webhook_url": "YOUR_URL" },
    "telegram":   { "enabled": true, "bot_token": "YOUR_TOKEN", "chat_id": "YOUR_ID" },
    "teams":      { "enabled": true, "webhook_url": "YOUR_URL" },
    "email":      { "enabled": true, "smtp_host": "smtp.example.com", "smtp_user": "..." },
    "github":     { "enabled": true, "github_user": "your_username", "github_repo": "daily-brief" }
  },
  "customization": {
    "language": "zh-CN",
    "max_items": 12,
    "max_items_monday": 18,
    "monday_window_hours": 72,
    "focus_areas": ["Big Data", "Data Platform", "Data Governance", "..."]
  }
}
```

### Environment Variables

#### 🇨🇳 China Channels

| Variable | Purpose | Required |
|----------|---------|----------|
| `WECOM_WEBHOOK_URL` | WeChat Work webhook | When using WeChat |
| `DINGTALK_WEBHOOK_URL` | DingTalk webhook | When using DingTalk |
| `DINGTALK_SECRET` | DingTalk signing secret | When signing enabled |
| `FEISHU_WEBHOOK_URL` | Feishu webhook | When using Feishu |
| `FEISHU_SECRET` | Feishu signing secret | When signing enabled |

#### 🌍 Global Channels

| Variable | Purpose | Required |
|----------|---------|----------|
| `SLACK_WEBHOOK_URL` | Slack Incoming Webhook | When using Slack |
| `DISCORD_WEBHOOK_URL` | Discord Webhook | When using Discord |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | When using Telegram |
| `TELEGRAM_CHAT_ID` | Telegram Chat/Channel ID | When using Telegram |
| `TEAMS_WEBHOOK_URL` | Teams Incoming Webhook | When using Teams |

#### 📧 Universal

| Variable | Purpose | Required |
|----------|---------|----------|
| `SMTP_HOST` | SMTP server address | When using email |
| `SMTP_USER` | SMTP username | When using email |
| `SMTP_PASSWORD` | SMTP password | When using email |
| `EMAIL_TO` | Recipients (comma-separated) | When using email |
| `GITHUB_TOKEN` | GitHub Personal Access Token | When using GitHub |
| `GITHUB_USER` | GitHub username | When using GitHub |

## 🔌 Channel Setup Guides

<details>
<summary><b>🇨🇳 DingTalk</b></summary>

1. **Create Bot**: Target group → Settings → Smart Assistant → Add Robot → Custom
2. **Security** (choose one):
   - ✅ **Custom keywords** (recommended): Set keywords like `daily`, `report`
   - 🔐 **Signing**: Copy Secret → set `DINGTALK_SECRET`
   - 🌐 **IP whitelist**: Add your server IP
3. **Copy Webhook URL** → set `DINGTALK_WEBHOOK_URL`
</details>

<details>
<summary><b>🇨🇳 Feishu / Lark</b></summary>

1. **Create Bot**: Target group → Settings → Bots → Add Bot → Custom Bot
2. **Security** (optional): Enable signing → set `FEISHU_SECRET`
3. **Copy Webhook URL** → set `FEISHU_WEBHOOK_URL`
4. **Interactive card mode**: `python scripts/send_feishu.py --card --link-url https://...`
5. ⚠️ Rate limit: 5/min, 100/hour
</details>

<details>
<summary><b>🌍 Slack</b></summary>

1. Visit https://api.slack.com/apps → Create New App
2. Features → Incoming Webhooks → Enable
3. "Add New Webhook to Workspace" → select channel
4. **Copy Webhook URL** → set `SLACK_WEBHOOK_URL`
</details>

<details>
<summary><b>🌍 Discord</b></summary>

1. Channel → Edit Channel (⚙️) → Integrations → Webhooks → New Webhook
2. Customize name and avatar
3. **Copy Webhook URL** → set `DISCORD_WEBHOOK_URL`
4. ⚠️ Embed description limit: 4096 chars, 5 requests/sec
</details>

<details>
<summary><b>🌍 Telegram</b></summary>

1. Search `@BotFather` → `/newbot` → get **Bot Token**
2. **Get Chat ID**: Add `@userinfobot` to group, or use `@channel_username`
3. Set `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`
4. ⚠️ 30 msg/sec, 20 msg/min in groups
</details>

<details>
<summary><b>🌍 Microsoft Teams</b></summary>

1. Channel → `···` → Workflows → "Post to a channel when a webhook request is received"
2. **Copy Webhook URL** → set `TEAMS_WEBHOOK_URL`
3. Legacy mode: `python scripts/send_teams.py --legacy`
4. ⚠️ Adaptive Card ~28KB, ~4 req/sec
</details>

## 🎨 Customization

### Switch to Your Industry

The default covers Data+AI, but adapting is simple — just two changes:

**1. Edit `daily-brief-config.json`** — change `focus_areas`:

```json
{
  "customization": {
    "focus_areas": ["FinTech", "Digital Banking", "Payment Infrastructure", "RegTech"]
  }
}
```

**2. Edit `SKILL.md`** — update the prompt instructions:

- Change the industry scope and vendor watchlist
- Adjust source requirements for your domain
- Modify output sections (e.g., add "Regulatory Updates" for FinTech)
- Set your preferred output language

**Example: FinTech daily brief**
```
Replace "数据平台" → "金融科技"
Replace vendor list → Stripe, Plaid, Adyen, Ant Group, etc.
Replace open source list → Hyperledger, OpenBanking APIs, etc.
```

### Customize the HTML Template

Edit `assets/report-template.html` to change colors, layout, and branding.

## 📋 Default Coverage (Data+AI)

The built-in configuration covers:

- **Domains**: Big Data · Data Platforms · Data Infrastructure · Data Governance · Data Engineering · Lakehouse · Query Engines · Stream/Batch Processing · Vector Search · Open Source Data Ecosystem
- **Tier 1 Vendors**: AWS · Google Cloud · Azure · Databricks · Snowflake · Alibaba Cloud · Tencent Cloud · Huawei Cloud · Volcengine
- **Open Source**: Iceberg · Hudi · Paimon · Delta Lake · Trino · Spark · Flink · Kafka · DuckDB · StarRocks · Doris · SeaTunnel · Amoro
- **Analysts**: Gartner · Forrester · IDC · a16z · Sequoia · CAICT · CCID · iResearch

## 📝 Changelog

| Version | Date | Summary |
|---------|------|---------|
| **5.0.0** | 2026-06-23 | **Major rework — English-first + industry-agnostic.** SKILL.md body fully rewritten in English; framework (workflow / confidence tiers / section definitions / format contract / hard rules) separated from a clearly-marked `[Default Profile: Data+AI]` block so the engine reads as truly domain-switchable. Display name changed to **Industry Daily Brief**. Value-first description. Backfilled all format/quality rules accumulated since 4.3.5: **source links must be Markdown `[text](url)`** (bare URLs broke HTML links); **WeChat-summary cap relaxed 30–80 → ≤120 chars**; **Step 4.5 expanded** with source-link format, `---` item-separator, WeChat-summary ≤120, and Top-3 char-count (15–30) assertions; numbering-reset and field-order assertions; stale-news guard; **Stability-first** promoted to Hard Rule #1; non-ASCII filename detection via `find` not `ls`. |
| **4.3.3** | 2026-05-29 | Major architectural refactor: 3-layer separation (Editorial Principles / Section Definitions / Workflow) + 2 appendices (MD Format Contract A.1-A.5 / Failure Handling B.1-B.3); **new Step 4.5 mandatory format pre-flight** — generate-then-assert N1 (item count) / N2 (WeChat summary count) / N3 (section count) with strict equality (N1>0, N1==N2, N3==5) and content gates (English section titles, no bold/numbers in 3-points, verdict ≤120 chars); generation-stage failure → mandatory regenerate (no patch-style fixing in review stage); Rule Maintenance Protocol introduced as Section 0 (locate→optimize→record, no patch piling); unified 6-dimension mapping (cost/perf/architecture/governance/eng-efficiency/market-landscape); replace failed site-search with keyword search for CN policy sources; fix cross-month date arithmetic; 0 content deletion — all v4.2 rules preserved as in-place reorganization |
| **4.2** | 2026-04-14 | Complete rewrite aligned with PROMPT.md v4.2: 6-step workflow with mandatory Review gate (Step 5); confidence tiers (A/B/C) with source-type labeling; hard rules section (6 rules — timeliness, source-only, dedup, Monday 72h, less-is-more, no-link-in-summary); failure handling (6 scenarios); deterministic vs LLM step labeling; actual delivery channels (wecom/github_pages/email) replacing 9 virtual channels; corrected section structure (C.Views & Research / D.Capital & Corporate); config filename fix (config.json not daily-brief-config.json) |
| **3.1** | 2026-03-25 | WeChat Work summary fix: D/E section regex `\s+` → `\s*` for empty-body sections; link-length optimization |
| **3.0** | 2026-03-20 | Major restructure: merge C.People & Views + D.Analyst Insights → C.Views & Research; add D.Capital & Corporate (funding/earnings/IPO/M&A with inline type tags); add 3-level information confidence (Level A/B/C); mandatory cross-section dedup self-check; new Step 5 Review & Fix (6 checks before publish); "Top 3 Points" now 15-30 char trend judgments (no product names/numbers); verdict ≤120 chars, no event detail repetition; add dedicated funding/M&A search queries; item count 10-14 (Monday 14-20) |
| **2.1** | 2026-03-17 | No-truncation summary rewrite: complete-sentence-only extraction (never hard-truncate); `_smart_shorten` with progressive degradation (sentence-level → title-only → remove line) replacing `_truncate_line_to_bytes`; eliminates all `...` ellipsis artifacts |
| **2.0** | 2026-03-16 | 3-phase search strategy with mandatory source tracing; 3-layer priority summary extraction; Monday 72-hour weekend catch-up window; duplicate push prevention; strict timeliness red-line rules; source labeling standards |
| **1.0** | 2026-03-09 | Initial release with 9 delivery channels, structured 5-section output, bilingual docs |

## ❤️ Support This Project

If this project helps you, consider [becoming a sponsor](https://github.com/sponsors/haiyangchenbj). Your support keeps it maintained and improved.

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

[MIT License](LICENSE) — free to use, modify, and distribute.

---

**Built with ❤️ by the community, for anyone who needs structured industry intelligence.**
