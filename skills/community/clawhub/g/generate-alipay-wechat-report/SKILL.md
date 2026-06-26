---
name: generate-alipay-wechat-report
description: Generate an interactive local HTML spending report from native Alipay CSV exports and WeChat Pay XLSX exports. Use when an agent needs to turn 支付宝交易明细 or 微信支付账单流水文件 into a digital dashboard for expense categorization, monthly trend review, recurring merchant analysis, spending habit diagnosis, and budget optimization.
---

# Generate Alipay Wechat Report

## Overview

Turn native Alipay and WeChat Pay bill exports into a self-contained local HTML report.
Prefer the bundled script so the workflow stays deterministic and does not depend on the current repo.

## Workflow

1. Look for native bill files first.
2. Use `scripts/generate_spending_report.py` to build the report.
3. Open the generated HTML if the user wants to review it immediately.
4. Summarize the key findings in plain language after generation.

## Inputs

Support these native exports:
- Alipay CSV named like `支付宝交易明细(...).csv`
- WeChat Pay XLSX named like `微信支付账单流水文件(...).xlsx`

If only the WeChat ZIP exists, stop and ask the user to unzip it locally first. The ZIP is commonly password-protected and this skill expects the extracted `.xlsx` file.

## Commands

Use auto-discovery inside a directory:

```bash
python /Users/codefriday/.codex/skills/generate-alipay-wechat-report/scripts/generate_spending_report.py \
  --input-dir /path/to/bills \
  --output /path/to/bills/reports/spending_report.html
```

Use explicit files:

```bash
python /Users/codefriday/.codex/skills/generate-alipay-wechat-report/scripts/generate_spending_report.py \
  --alipay /path/to/支付宝交易明细(...).csv \
  --wechat /path/to/微信支付账单流水文件(...).xlsx \
  --output /path/to/reports/spending_report.html
```

Open the report after generation:

```bash
python /Users/codefriday/.codex/skills/generate-alipay-wechat-report/scripts/generate_spending_report.py \
  --input-dir /path/to/bills \
  --open
```

## Output

Generate a self-contained HTML report with:
- total outflow, consumption-only spend, and habit pool
- category structure and merchant concentration
- monthly trend, daily line chart, weekday/time heatmap
- top transactions and recurring merchants
- habit diagnosis and concrete optimization suggestions

## Notes

Explain the three report scopes when handing results back:
- `账户总流出`: all effective outflow
- `消费型支出`: outflow excluding tax and pure transfers
- `习惯池`: outflow excluding non-routine major items so habit analysis stays clean

Do not treat rent, tax, renovation, travel, or one-off major purchases as ordinary daily bad habits.
