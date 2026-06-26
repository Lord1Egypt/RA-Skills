---
name: daily-cost-report
description: Generate daily OpenClaw cost reports with breakdown by agent/model/channel. Use when: daily cron job, on-demand cost analysis, cost auditing. Generates HTML-formatted email reports.
emoji: 📊
requires:
  env:
    - OPENAI_API_KEY
---

# Daily Cost Report 📊

Generate comprehensive OpenClaw usage and cost reports with breakdowns by agent, model, and channel. Supports both on-demand analysis and automated daily email delivery.

## Quick Start

```bash
# Generate report for yesterday (markdown)
{baseDir}/scripts/daily-cost-report.sh yesterday

# Generate report for a specific date
{baseDir}/scripts/daily-cost-report.sh 2026-03-18

# Generate report for today
{baseDir}/scripts/daily-cost-report.sh today

# Generate HTML-formatted email report
{baseDir}/scripts/daily-cost-report-email.sh yesterday

# Send email report to recipient
{baseDir}/scripts/send-cost-report.sh kjvarga@gmail.com yesterday
```

## What It Does

The daily cost report analyzes OpenClaw session data for a specified date range and generates:

- **Total cost and token usage** across all agents, models, and channels
- **Per-agent breakdown** showing which agents consumed the most resources
- **Per-model breakdown** showing cost distribution across Claude models, Deepseek, GPT, etc.
- **Per-channel breakdown** showing usage from Telegram, CLI, web, etc.
- **Top sessions by cost** identifying the most expensive individual sessions
- **Prompt cache metrics** showing cache write/read tokens and cost savings

Reports use the current pricing for:
- Claude Haiku 4.5
- Claude Sonnet 4.5
- Claude Opus 4.6
- Deepseek V3.2
- OpenAI GPT-4o-mini

Cache pricing (read/write) is factored into cost calculations.

## Scripts

### `daily-cost-report.sh`

Core report generator. Queries OpenClaw sessions via `openclaw sessions --all-agents --json`, filters by date range, calculates costs using model-specific pricing, and generates markdown output.

**Output:** `/tmp/cost-report-YYYY-MM-DD.md`

### `daily-cost-report-email.sh`

Wraps the markdown report in an HTML email template with styled tables, summary metrics, and visual hierarchy.

**Output:** `/tmp/cost-report-YYYY-MM-DD.html`

### `send-cost-report.sh`

Sends the HTML report via email using the `mail` command. Falls back to saving the file if mail delivery fails.

**Usage:** `send-cost-report.sh <recipient-email> [date]`

## Cron Usage

The daily cost report is typically scheduled as a cron job in `~/.openclaw/cron/jobs.json`:

```json
{
  "id": "daily-cost-report",
  "agentId": "worker",
  "name": "main-daily-cost-report",
  "enabled": true,
  "schedule": {
    "kind": "cron",
    "expr": "0 8 * * *",
    "tz": "America/Vancouver"
  },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Generate yesterday's cost report and send to kjvarga@gmail.com"
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "7918443630"
  }
}
```

The cron job invokes the skill, which then calls the appropriate scripts.

## Manual Invocation from Agent

When Karl asks for a cost report:

```bash
# From any agent with exec access
exec(command: "bash ~/.openclaw/workspace/skills/daily-cost-report/scripts/daily-cost-report.sh yesterday")

# Or to generate and send email
exec(command: "bash ~/.openclaw/workspace/skills/daily-cost-report/scripts/send-cost-report.sh kjvarga@gmail.com yesterday")
```

## Report Format

The report includes:

1. **Summary section** - Total cost, tokens, cache metrics, savings
2. **Cost by Agent** - Which agents are most active/expensive
3. **Cost by Model** - Model-level resource consumption
4. **Cost by Channel** - Usage by Telegram, CLI, web, etc.
5. **Top Sessions** - Highest-cost individual sessions

All monetary values are in USD with 4 decimal precision. Token counts are formatted with thousands separators for readability.

## Date Handling

Scripts accept:
- `yesterday` (default) - Previous calendar day
- `today` - Current calendar day
- `YYYY-MM-DD` - Specific date

Date parsing is compatible with both macOS (`date -v-1d`) and Linux (`date -d "yesterday"`).

## Requirements

- OpenClaw CLI: `openclaw sessions --all-agents --json`
- `jq` for JSON processing
- `awk` for aggregation
- `mail` command (for email delivery)
- bash 4+ (for associative arrays)

## Cost

**This skill costs nothing** — it only reads session metadata that OpenClaw already tracks. No external API calls.

## Example Output

```
# OpenClaw Daily Cost Report 🐈‍⬛
**Date:** 2026-03-18  
**Generated:** 2026-03-19 08:00:00 PDT

---

## Summary

| Metric | Value |
|--------|-------|
| **Total Cost** | $2.4567 |
| **Total Tokens** | 1,234,567 |
| **Input Tokens** | 987,654 |
| **Output Tokens** | 246,913 |
| **Cache Write Tokens** | 123,456 |
| **Cache Read Tokens** | 456,789 |
| **Cache Savings** | $0.3245 |

---

## Cost by Agent

| Agent | Cost | Tokens | Input | Output |
|-------|------|--------|-------|--------|
| main | $1.2345 | 654,321 | 543,210 | 111,111 |
| worker | $0.8901 | 400,000 | 320,000 | 80,000 |
| research | $0.3321 | 180,246 | 124,444 | 55,802 |
...
```
