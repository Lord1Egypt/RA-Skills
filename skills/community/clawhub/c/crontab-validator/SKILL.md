---
name: crontab-validator
description: Validate, explain, lint, and calculate next run times for cron expressions. Use when asked to check cron syntax, explain a crontab entry, find next scheduled runs, or lint cron expressions for common mistakes. Triggers on "crontab", "cron expression", "cron schedule", "cron syntax", "cron explain", "cron next run", "*/5 * * * *".
---

# Crontab Validator & Explainer

Validate cron syntax, get human-readable explanations, calculate next run times, and lint for common mistakes.

## Validate

```bash
# Single expression
python3 scripts/cron_check.py validate "*/15 * * * *"

# Multiple expressions with lint
python3 scripts/cron_check.py validate --lint "0 2 * * *" "* * * * *" "0 0 31 2 *"
```

## Explain in Detail

```bash
python3 scripts/cron_check.py explain "30 4 1,15 * 1-5"
```

## Next Run Times

```bash
# Next 5 runs (default)
python3 scripts/cron_check.py next "0 9 * * 1-5"

# Next 10 runs
python3 scripts/cron_check.py next "0 */6 * * *" --count 10

# From specific time
python3 scripts/cron_check.py next "0 9 * * *" --from-time 2026-01-01T00:00:00
```

## Lint

```bash
# Check for common mistakes
python3 scripts/cron_check.py lint "* * * * *" "0 0 31 2 *" "0 0 29 2 *"

# Strict mode (exit 1 on warnings)
python3 scripts/cron_check.py lint --strict "0 0 31 4 *"
```

## Output Formats

```bash
python3 scripts/cron_check.py -f json explain "0 9 * * 1-5"
python3 scripts/cron_check.py -f markdown validate --lint "*/5 * * * *"
```

## Supported Syntax

| Feature | Example | Description |
|---------|---------|-------------|
| Wildcard | `*` | Every value |
| Specific | `5` | Exact value |
| Range | `1-5` | Values 1 through 5 |
| List | `1,3,5` | Values 1, 3, and 5 |
| Step | `*/15` | Every 15th value |
| Range+Step | `1-30/2` | Odd values 1-30 |
| Names | `mon-fri` | Day/month names |
| Shortcuts | `@daily` | Predefined schedules |

## Shortcuts

| Shortcut | Equivalent | Meaning |
|----------|-----------|---------|
| `@yearly` | `0 0 1 1 *` | Once a year |
| `@monthly` | `0 0 1 * *` | First of month |
| `@weekly` | `0 0 * * 0` | Every Sunday |
| `@daily` | `0 0 * * *` | Every midnight |
| `@hourly` | `0 * * * *` | Every hour |

## Lint Checks

| Check | Level | Description |
|-------|-------|-------------|
| Every-minute | Warning | `* * * * *` runs 1440 times/day |
| Day 31 in short months | Warning | Apr, Jun, Sep, Nov have 30 days |
| Feb 29-31 | Warning | Only runs in leap years (29) or never |
| DOM + DOW conflict | Info | Both specified = OR logic |
| High frequency | Info | More than 288 runs/day |
