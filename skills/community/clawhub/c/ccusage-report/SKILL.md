---
name: ccusage-report
description: "Report Claude Code token consumption and costs using ccusage. Use when the user asks about their Claude Code usage, token consumption, API costs, spending, or wants a daily/weekly/monthly usage summary."
metadata: {"openclaw":{"requires":{"bins":["bunx"]}}}
---

# Claude Code Usage Report

Uses `bunx ccusage` to report token consumption and costs from Claude Code sessions.

**IMPORTANT: The ONLY valid subcommands are `daily`, `weekly`, `monthly`. Do NOT use `today`, `this_week`, `this_month`, or any other subcommand — they will crash.**

## Workflow

### 1. Determine the subcommand

Map the user's intent to one of the three valid subcommands:

| User intent | Subcommand | Extra flags |
|-------------|------------|-------------|
| "today" / "how much today" / default | `daily` | `--since $(date +%Y%m%d) --until $(date +%Y%m%d)` |
| "this week" / "weekly" | `weekly` | (none) |
| "this month" / "monthly" | `monthly` | (none) |
| "last 7 days" | `daily` | `--since $(date -d '7 days ago' +%Y%m%d)` |
| "in February" / specific month | `daily` | `--since 20260201 --until 20260228` |

### 2. Run ccusage

```json
{ "tool": "exec", "command": "bunx ccusage daily --no-color -z Europe/Paris -o desc --since $(date +%Y%m%d) --until $(date +%Y%m%d)" }
```

Replace `daily` with `weekly` or `monthly` as needed. Add `--breakdown` if the user asks for per-model details.

### 3. Format the output

```
📊 Claude Code Usage — <period>

Date/Period : <value>
Models      : <comma-separated list>
Input       : <n> tokens
Output      : <n> tokens
Cache read  : <n> tokens
Total       : <n> tokens
Cost        : $<amount> USD
```

For multi-row output (e.g. last 7 days), summarize totals and list each row briefly.

### 4. Deliver

- **Chat**: Send the formatted message directly
- **Telegram (cron context)**: Reply with ONLY the formatted message in a code block — no extra commentary

### 5. Error handling

- If `bunx ccusage` fails → check if bun/bunx is installed, report the error
- If no data for the requested period → inform the user clearly ("No usage data found for this period")
- If the output is empty → suggest checking a broader date range

## Examples

| User says | Period | Flags |
|-----------|--------|-------|
| "Show my claude code usage" | daily | (none) |
| "How much did I spend this week?" | weekly | (none) |
| "Monthly report with model breakdown" | monthly | `--breakdown` |
| "Usage for the last 7 days" | daily | `--since $(date -d '7 days ago' +%Y%m%d)` |
