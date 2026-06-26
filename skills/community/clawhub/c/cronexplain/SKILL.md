---
name: cronexplain
description: Explain cron expressions in plain English and calculate next run times. Use when asked to decode a crontab entry, understand a cron schedule, check when a cron job will next run, or translate between cron syntax and human-readable schedules. Supports ranges, steps, lists, and wildcards. Zero dependencies.
---

# cronexplain 📅

Cron expression explainer with next-run calculator.

## Commands

```bash
# Explain a cron expression
python3 scripts/cronexplain.py "30 9 * * 1-5"
# → at minute 30; at 09:00; on Mon, Tue, Wed, Thu, Fri

# Show next N run times
python3 scripts/cronexplain.py "0 */4 * * *" -n 5

# Monthly schedule
python3 scripts/cronexplain.py "0 0 1,15 * *" -n 3
```

## Supported Syntax
- Wildcards: `*`
- Ranges: `1-5` (Mon-Fri)
- Steps: `*/15` (every 15 minutes)
- Lists: `1,15` (1st and 15th)
- Combined: `0-30/10` (every 10 min in first half hour)

## Fields (standard 5-field cron)
`minute hour day_of_month month day_of_week`
