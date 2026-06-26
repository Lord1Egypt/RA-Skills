---
name: fullrun
description: Manage Google Ads campaigns — diagnose, optimize, and create campaigns
requires:
  bins: [fullrun]
  env: [FULLRUN_API_KEY]
user-invocable: true
---

# Fullrun — Google Ads Management for AI Agents

Manage Google Ads campaigns using the `fullrun` CLI. All commands return JSON by default.

## Setup

```bash
npm install -g fullrun
fullrun login <YOUR_API_KEY>
```

Or set env: `export FULLRUN_API_KEY=frun_...`

## Workflow

Always start with triage to understand account health:

1. `fullrun triage` — see prioritized issues (CRITICAL > HIGH > MEDIUM > LOW)
2. Fix the highest-priority issues using `fullrun run`
3. `fullrun triage` — confirm issues resolved

## Commands

### Diagnose
- `fullrun triage` — Account health report with prioritized issues
- `fullrun campaigns:list` — All campaigns with status, budget, and metrics
- `fullrun performance --days 7` — Account metrics: clicks, impressions, conversions, CPA
- `fullrun keywords:list --campaign <id>` — Keywords with performance data

### Act
- `fullrun run` — Trigger a full AI-powered optimization run. The agent triages the account and fixes the highest-priority issues automatically. Rate limited to 1 per hour.

### Options
- `--format human` — Readable output instead of JSON
- `--days <n>` — Look-back period for performance data (default 7, max 90)
- `--campaign <id>` — Filter keywords by campaign

## Output

All commands return structured JSON by default for easy parsing by AI agents.

Exit codes:
- `0` — Success
- `1` — Error (check the `error` field in JSON output)
- `2` — Guardrail blocked (the action was prevented to protect the ad account)

## Rules

- Always run `fullrun triage` before taking action
- The `fullrun run` command is rate-limited to 1 per hour
- Respect guardrail errors (exit code 2) — they protect the ad account from harmful changes
- Never call `fullrun run` repeatedly — check triage first to see if action is needed
- Don't increase daily budget more than 20% in one action
- Don't pause campaigns without checking conversion data first
