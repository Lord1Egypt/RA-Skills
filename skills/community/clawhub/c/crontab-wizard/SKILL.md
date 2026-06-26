---
name: crontab-wizard
description: Explain, generate, validate, and preview crontab expressions. Use when a user needs to understand what a cron expression means, create a new cron schedule, check if a cron expression is valid, or see when a cron job will run next. Supports standard 5-field cron syntax and shortcuts like @daily, @hourly, @weekly. No dependencies required.
---

# Crontab Wizard

Decode, generate, validate, and preview cron schedules from the command line. Zero dependencies.

## Quick Start

```bash
# Explain what a cron expression does
python3 scripts/cronwiz.py explain "*/5 * * * *"

# Generate an expression from options
python3 scripts/cronwiz.py generate --every 5m

# Check if an expression is valid
python3 scripts/cronwiz.py validate "0 9 * * 1-5"

# See when it runs next
python3 scripts/cronwiz.py next "0 9 * * 1-5" --count 10
```

## Commands

### explain — Decode cron to plain English

```bash
python3 scripts/cronwiz.py explain "30 2 * * 0"
# → At 02:30, on Sunday

python3 scripts/cronwiz.py explain "@daily"
# → At 00:00

python3 scripts/cronwiz.py explain "0 */6 * * *"
# → At minute 0, every 6 hours
```

### validate — Check for errors

```bash
python3 scripts/cronwiz.py validate "0 9 * * 1-5"
# → VALID: 0 9 * * 1-5

python3 scripts/cronwiz.py validate "0 25 * * *"
# → INVALID: hour: 25 out of range (0-23)
```

### next — Preview upcoming runs

```bash
python3 scripts/cronwiz.py next "0 9 * * 1-5" --count 5
# Shows next 5 weekday 9 AM runs with dates
```

### generate — Build expressions from options

```bash
python3 scripts/cronwiz.py generate --every 5m
# → */5 * * * *

python3 scripts/cronwiz.py generate --every daily --at 09:00
# → 0 9 * * *

python3 scripts/cronwiz.py generate --every week --at 14:30 --on friday
# → 30 14 * * 5
```

#### Generate options

| Flag | Values | Description |
|------|--------|-------------|
| `--every` | `5m`, `2h`, `daily`, `weekly`, `monthly` | Interval |
| `--at` | `HH:MM` | Time of day |
| `--on` | `mon`–`sun`, `weekdays`, `weekends` | Day of week |

## Supported Shortcuts

`@yearly`, `@annually`, `@monthly`, `@weekly`, `@daily`, `@midnight`, `@hourly`

## Dependencies

None — pure Python, no pip installs required.
