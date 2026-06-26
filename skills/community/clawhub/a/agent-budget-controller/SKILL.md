---
name: agent-budget-controller
description: "Control LLM API spending per agent. Set daily/weekly/monthly limits with real-time tracking and alerts."
license: "MIT-0"
metadata:
  openclaw:
    emoji: "💰"
    requires:
      bins: ["uv", "python3"]
---

# Agent Budget Controller

> **💰 Stop LLM cost overruns before they happen**

Track, limit, and alert on LLM API costs per agent with daily/weekly/monthly budgets.

## What It Does

- **Set budget limits** — Global or per-agent, daily/weekly/monthly
- **Track usage** — Automatic cost calculation for 10+ LLM models
- **Alert on thresholds** — 70% warning, 90% critical, 100% blocked
- **Generate reports** — Usage summaries and cost breakdowns
- **Zero dependencies** — Pure Python stdlib, local-only

## Quick Start

```bash
# Initialize
budget init

# Set limits
budget set --daily 3.00 --weekly 15.00 --monthly 50.00
budget set --agent ubik-pm --daily 1.00

# Log usage (manual - see Integration below)
budget log --agent ubik-pm --model "claude-sonnet-4-5" \
  --input-tokens 5000 --output-tokens 1500

# Check status
budget status
budget status --agent ubik-pm

# Check limits (exit code)
budget check  # exit 0=ok, 1=exceeded
```

## Commands

| Command | Purpose |
|---------|---------|
| `init` | Initialize budget tracking |
| `set` | Set budget limits |
| `log` | Log API usage |
| `status` | Show current usage vs limits |
| `check` | Check if limits exceeded (exit code) |
| `report` | Generate detailed period report |
| `agents` | List agents with limits or activity |
| `pricing` | Show/update model pricing |
| `history` | Show recent usage history |

## Supported Models

Built-in pricing for:
- **OpenAI**: gpt-4o, gpt-4o-mini, o1, o1-mini
- **Anthropic**: claude-sonnet-4-5, claude-opus-4, claude-haiku-3.5
- **Google**: gemini-2.5-flash, gemini-2.5-pro, gemini-2.0-flash

Custom models:
```bash
budget pricing --update --model my-model \
  --input-price 1.50 --output-price 5.00
```

## Integration

### OpenClaw Heartbeat

Add to `HEARTBEAT.md`:
```markdown
## Budget Monitoring

Every 4 hours:
1. Check budget status: `budget status`
2. If any agent >90%, notify Director
3. If any exceeded, escalate immediately
```

### Pre-call Hook (Future)

```bash
# In agent wrapper script
budget check --agent $AGENT_NAME || {
  echo "❌ Budget exceeded for $AGENT_NAME"
  exit 1
}

# Call LLM API...
# Log after call
budget log --agent $AGENT_NAME \
  --model "$MODEL" \
  --input-tokens $INPUT_TOKENS \
  --output-tokens $OUTPUT_TOKENS
```

### Cron (Daily Report)

```bash
# Send daily report to Telegram
0 9 * * * budget report --period day | \
  openclaw msg --channel telegram --target @director
```

## Alert Levels

| Usage | Level | Symbol | Action |
|-------|-------|--------|--------|
| <70% | OK | ✅ | Continue |
| 70-89% | Warning | ⚠️ | Monitor |
| 90-99% | Critical | 🔴 | Alert Director |
| ≥100% | Exceeded | 🚫 | Block calls |

## Data Storage

```
~/.openclaw/budget/
├── config.json       # Budget limits
├── pricing.json      # Model pricing (optional override)
└── usage.jsonl       # Append-only usage log
```

**Privacy**: All data stored locally. No network calls.

## Examples

See [EXAMPLE.md](./EXAMPLE.md) for complete usage scenarios.

## Testing

```bash
cd ~/ubik-collective/systems/ubik-pm/skills/agent-budget-controller
python3 tests/test_budget.py
```

## Security

- ✅ Zero external dependencies
- ✅ No network calls
- ✅ Local-only data storage
- ✅ Pure Python stdlib

Safe for ClawHub distribution.

## License

MIT-0 (public domain equivalent)
