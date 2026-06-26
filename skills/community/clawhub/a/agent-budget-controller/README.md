# Agent Budget Controller

**Control LLM API costs per agent with real-time tracking and alerts.**

Prevent cost overruns from runaway agents, infinite loops, or malicious skills.

## The Problem

- 🔥 Agent loops → $100/hour API bills
- 🎯 Malicious skills → unlimited API calls
- 🤷 No visibility → surprise invoices
- 😱 Manual tracking → error-prone

## The Solution

Set budget limits (daily/weekly/monthly) and get automatic alerts when approaching limits:

```
📊 Agent Budget Status (2026-03-17)

Global Limits:
  Daily:   $1.82 / $3.00  (60.7%) ⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛
  Weekly:  $8.45 / $15.00 (56.3%) ⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛
  Monthly: $22.10 / $50.00 (44.2%) ⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛

By Agent:
  ubik-pm:     $0.95 today  (claude-sonnet: $0.80, gemini-flash: $0.15)
  chloe-life:  $0.62 today  (gpt-4o-mini: $0.62)
```

## Features

- ✅ **Multi-level budgets** — Global, per-agent, daily/weekly/monthly
- ✅ **Automatic cost calculation** — 10+ built-in model prices
- ✅ **Threshold alerts** — 70% warning, 90% critical, 100% block
- ✅ **Usage reports** — Daily/weekly/monthly summaries
- ✅ **Zero dependencies** — Pure Python stdlib
- ✅ **Local-only** — No network calls, private data

## Installation

```bash
cd ~/ubik-collective/systems/ubik-pm/skills/agent-budget-controller

# Install with uv (recommended)
uv pip install -e .

# Or just use the script directly
python3 scripts/budget.py --help
```

## Quick Start

```bash
# 1. Initialize
budget init

# 2. Set global limits
budget set --daily 5.00 --weekly 25.00 --monthly 100.00

# 3. Set agent-specific limits
budget set --agent ubik-pm --daily 2.00
budget set --agent chloe-life --daily 1.50

# 4. Log usage (after each LLM call)
budget log \
  --agent ubik-pm \
  --model "claude-sonnet-4-5" \
  --input-tokens 5000 \
  --output-tokens 1500

# 5. Check status
budget status
budget status --agent ubik-pm

# 6. Check if exceeded (for scripts)
budget check || echo "Budget exceeded!"
```

## CLI Reference

### `budget init`
Initialize budget tracking (creates `~/.openclaw/budget/`)

### `budget set`
Set budget limits:
```bash
# Global limits
budget set --daily 3.00 --weekly 15.00 --monthly 50.00

# Agent-specific limits
budget set --agent my-agent --daily 1.00
```

### `budget log`
Log API usage:
```bash
budget log \
  --agent <agent-name> \
  --model <model-name> \
  --input-tokens <count> \
  --output-tokens <count>
```

Cost is calculated automatically using built-in pricing.

### `budget status`
Show current usage vs limits:
```bash
budget status              # All agents
budget status --agent foo  # Specific agent
```

### `budget check`
Check if limits exceeded (returns exit code):
```bash
budget check                # Global limits
budget check --agent foo    # Agent limits

# Exit code: 0=ok, 1=exceeded
```

Use in scripts:
```bash
budget check --agent my-agent || {
  echo "Budget exceeded!"
  exit 1
}
```

### `budget report`
Generate detailed period report:
```bash
budget report --period day     # Today
budget report --period week    # This week
budget report --period month   # This month

# Agent-specific
budget report --period day --agent ubik-pm
```

### `budget agents`
List agents with limits or recent activity:
```bash
budget agents
budget agents --days 30  # Active in last 30 days
```

### `budget pricing`
Show or update model pricing:
```bash
budget pricing  # List all models

# Add/update custom model
budget pricing --update \
  --model my-custom-model \
  --input-price 2.00 \
  --output-price 8.00
```

### `budget history`
Show recent usage:
```bash
budget history --last 7d   # Last 7 days
budget history --last 24h  # Last 24 hours
```

## Integration with OpenClaw

### 1. Heartbeat Monitoring

Add to `HEARTBEAT.md`:
```markdown
## Budget Check (every 6 hours)

1. Run: `budget status`
2. If any agent >90%: notify Director
3. If any exceeded: escalate immediately
```

### 2. Pre-call Budget Check

Wrap LLM calls:
```bash
#!/bin/bash
# scripts/safe-llm-call.sh

AGENT=$1
MODEL=$2

# Check budget before call
budget check --agent "$AGENT" || {
  echo "❌ Budget exceeded for $AGENT"
  exit 1
}

# Make LLM call
# ... your API call here ...

# Log usage after call
budget log \
  --agent "$AGENT" \
  --model "$MODEL" \
  --input-tokens $INPUT_TOKENS \
  --output-tokens $OUTPUT_TOKENS
```

### 3. Daily Cron Report

```bash
# Send daily report to Telegram
0 9 * * * cd /path/to/skill && \
  budget report --period day | \
  openclaw message send --target @director
```

### 4. GitHub Actions

```yaml
# .github/workflows/budget-check.yml
name: Budget Check
on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: budget check || echo "⚠️ Budget exceeded"
```

## Model Pricing

Built-in pricing (per 1M tokens, USD):

| Model | Input | Output |
|-------|-------|--------|
| gpt-4o | $2.50 | $10.00 |
| gpt-4o-mini | $0.15 | $0.60 |
| claude-sonnet-4-5 | $3.00 | $15.00 |
| claude-opus-4 | $15.00 | $75.00 |
| claude-haiku-3.5 | $0.80 | $4.00 |
| gemini-2.5-flash | $0.15 | $0.60 |
| gemini-2.5-pro | $1.25 | $10.00 |

For unlisted models, a conservative fallback ($5 input, $20 output) is used.

Update pricing:
```bash
budget pricing --update \
  --model gpt-4o \
  --input-price 2.50 \
  --output-price 10.00
```

## Alert Thresholds

| Usage | Level | Symbol | Description |
|-------|-------|--------|-------------|
| 0-69% | OK | ✅ | Normal operation |
| 70-89% | Warning | ⚠️ | Approaching limit |
| 90-99% | Critical | 🔴 | Near limit |
| ≥100% | Exceeded | 🚫 | Over budget |

## Data Files

All data stored in `~/.openclaw/budget/`:

```
~/.openclaw/budget/
├── config.json       # Budget limits config
├── pricing.json      # Custom model pricing (optional)
└── usage.jsonl       # Append-only usage log
```

**Format**:
- `config.json` — Pretty JSON, safe to edit
- `usage.jsonl` — One JSON object per line (append-only)
- `pricing.json` — Optional overrides (created on first `pricing --update`)

## Testing

Run tests:
```bash
cd ~/ubik-collective/systems/ubik-pm/skills/agent-budget-controller
python3 tests/test_budget.py
```

Tests cover:
- Config save/load
- Usage tracking
- Cost calculation
- Alert levels
- Report generation

## Troubleshooting

### "No module named 'lib'"
Make sure you run from the skill directory or install with `uv pip install -e .`

### "Budget check always returns 0"
No limits set. Run `budget set --daily 5.00` first.

### "Unknown model warning"
Add custom pricing: `budget pricing --update --model your-model ...`

### "Usage log too large"
Archive old data:
```bash
cd ~/.openclaw/budget
mv usage.jsonl usage-$(date +%Y%m%d).jsonl
touch usage.jsonl
```

## Security

- ✅ **Zero external dependencies** — Pure Python stdlib
- ✅ **No network calls** — 100% local
- ✅ **Append-only log** — Tampering visible
- ✅ **No secrets stored** — Only usage data

Safe to distribute on ClawHub.

## FAQ

**Q: How do I reset counters?**  
A: Delete `~/.openclaw/budget/usage.jsonl`. Or wait — daily/weekly/monthly counters reset automatically.

**Q: Can I set different models for different agents?**  
A: Limits are per-agent total, not per-model. Track model breakdown with `budget report`.

**Q: What if I exceed the limit?**  
A: `budget check` returns exit code 1. It doesn't _block_ calls — you must enforce that in your wrapper.

**Q: Can I share limits across agents?**  
A: Use global limits. Each agent also inherits global limits (both are checked).

**Q: How accurate is cost tracking?**  
A: Based on published pricing. May drift if providers change rates. Update with `budget pricing --update`.

## Roadmap

- [ ] Auto-logging via OpenClaw hook
- [ ] Real-time blocking (enforce, not just check)
- [ ] Grafana/Prometheus export
- [ ] Slack/Discord webhooks
- [ ] Multi-currency support

## License

MIT-0 (public domain equivalent)

## Contributing

PRs welcome! Keep it:
- Pure Python stdlib (no deps)
- Local-only (no network)
- Well-tested

## Support

File issues: [GitHub](https://github.com/ubikcollective/ubik-pm/issues)  
Or find us on the OpenClaw Discord.
