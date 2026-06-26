---
name: agentic-payment-daily
description: Generate and deliver daily Agentic Payment news briefing for Visa Greater China VIC lead. Covers Visa dynamics, China/APAC market, competitor protocols, and regulatory signals. Use when setting up, editing, or debugging the daily cron job, or when asked to generate an Agentic Payment daily report. Triggers: agentic payment daily, 日报, AP日报, agentic payment report.
---

# Agentic Payment Daily Report

Daily briefing for Visa Greater China Agentic Payment lead (Visa Intelligent Commerce).

## Workflow

### 0. Deduplicate against previous reports

Before searching, read the previous 2 days' reports from Obsidian:
- `/Users/juncai/Documents/OBVault-MacMini/02_work/Visa工作/VIC/Agentic-Payment-Daily-Report/YYYY-MM-DD.md`

Extract each reported news item's headline and source URL. During curation (step 1), filter out items that are:
- **Exact duplicate:** same URL already reported
- **Near duplicate:** same topic/event with no meaningful new development
- **Keep if updated:** same topic but significant new development (merge update into existing entry)

### 1. Search & Curate (max 10 items)

Search for Agentic Payment news. Priority order:
1. **Visa dynamics** — Agentic Ready, VIC, Trusted Agent Protocol, APAC/China partnerships
2. **China/APAC market** — agentic payment adoption, pilots, launches
3. **Competitor protocols** — Mastercard Agent Pay, Stripe MPP/Tempo, Google AP2, Coinbase x402, MoonPay OWS
4. **Regulatory & data** — compliance signals, industry data, trend analysis

### 2. Format each item

```
### [Tag] Headline
- **摘要 / Summary:** 2-3 sentences (bilingual if English source)
- 💡 **So What:** Why this matters for Visa Greater China VIC
- 🎯 **Action Item:** What to consider doing based on this
- 🔗 Source: [title](url)
```

Tags: 🔴 重点必读 / 🟡 值得关注 / 🟢 背景信息

### 3. Deliver

**A) Write to Obsidian**

Path: `/Users/juncai/Documents/OBVault-MacMini/02_work/Visa工作/VIC/Agentic-Payment-Daily-Report/YYYY-MM-DD.md`

Frontmatter:
```yaml
---
title: "Agentic Payment 日报 - YYYY-MM-DD"
date: YYYY-MM-DD
tags: agentic-payment, visa, daily-report
---
```

**B) Generate PDF**

```bash
node scripts/convert-ap-report.mjs <obsidian-md-path> "/tmp/Agentic Payment日报-YYYY-MM-DD.pdf"
```

**C) Push to WeChat**

1. Send PDF as document via `message` tool: `action: send`, `channel: openclaw-weixin`, `target: o9cq80wFt50OIoe6Wk8BEIOaC6x4@im.wechat`, `accountId: 26eb1d27b81b-im-bot`, `media: /tmp/Agentic Payment日报-YYYY-MM-DD.pdf`, `forceDocument: true`
2. Output report text as final reply (system will auto-deliver via announce)

## Cron Setup

Schedule: `50 8 * * *` Asia/Shanghai (delivered to WeChat).

To create/update the cron job, use the payload message below as the agent prompt, with delivery configured for the target WeChat account.

### Cron Prompt

```
按照 agentic-payment-daily skill 生成今日日报。

步骤A：写入 Obsidian（路径 YYYY-MM-DD.md，短横线格式）→ echo "STEP A DONE"
步骤B：生成 PDF → echo "STEP B DONE"
步骤C：微信推送 PDF（channel: openclaw-weixin, target: o9cq80wFt50OIoe6Wk8BEIOaC6x4@im.wechat, accountId: 26eb1d27b81b-im-bot）→ echo "STEP C DONE"
步骤D：输出日报全文 → echo "STEP D DONE"

如果任何步骤失败，修复并重试。
```

## Notes

- Timeout budget: ~10 minutes (search + write + PDF + push)
- If WeChat push fails, ensure Obsidian file and PDF are still saved (they are the primary artifacts)
- Quality over quantity
