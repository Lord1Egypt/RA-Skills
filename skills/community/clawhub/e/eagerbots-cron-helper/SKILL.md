---
name: eagerbots-cron-helper
description: "Explain, generate, and validate cron expressions. Convert plain English schedules to cron syntax and back. Show next run times. Works with standard 5-field and 6-field (with seconds) cron."
version: 1.0.0
metadata:
  openclaw:
    emoji: "⏰"
  requires:
    bins:
      - python3
  homepage: https://github.com/josephflu/clawhub-skills
---

# cron-helper ⏰

Explain, generate, validate, and preview cron expressions — all from plain English or raw cron syntax.

## Trigger phrases

- "What does this cron mean: `* * * * *`"
- "Explain this cron expression"
- "Generate a cron for every weekday at 9am"
- "When does `0 9 * * 1-5` run next?"
- "Is this cron valid?"
- "Convert to cron: every 15 minutes"
- "Show me the next runs for this cron"

## Usage

Run the script with `uv run` (handles dependencies automatically):

```bash
# Explain a cron expression
uv run scripts/cron.py explain "0 9 * * 1-5"

# Generate cron from plain English
uv run scripts/cron.py generate "every weekday at 9am"
uv run scripts/cron.py generate "every 15 minutes"
uv run scripts/cron.py generate "first day of month at midnight"

# Show next N run times (default 5)
uv run scripts/cron.py next "0 9 * * 1-5"
uv run scripts/cron.py next "*/15 * * * *" --count 10

# Validate a cron expression
uv run scripts/cron.py validate "0 9 * * 1-5"
uv run scripts/cron.py validate "60 9 * * *"
```

## Instructions for the agent

1. Parse the user's request to determine the command: `explain`, `generate`, `next`, or `validate`.
2. Run the appropriate `uv run scripts/cron.py <command> "<expression or description>"` command.
3. Present the output to the user, adding any clarifying context.
4. If the user provides a cron expression, always offer to explain it AND show next runs.

## Reference

See `references/cron-syntax.md` for field ranges, special characters, and common examples.
