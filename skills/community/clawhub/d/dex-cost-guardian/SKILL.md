---
name: cost-guardian
description: "Monitor and control OpenClaw API costs. Tracks token usage across all sessions, estimates spend by model, alerts on budget overruns, and recommends cheaper model routing for routine tasks. Use when: asking about costs, checking spend, setting budgets, or optimizing API usage."
metadata: { "openclaw": { "emoji": "🛡️", "requires": { "bins": ["python3"] } } }
---

# Cost Guardian — OpenClaw Cost Monitor & Optimizer

Know what your agent costs. Before it becomes a problem.

## When to Use

✅ **USE this skill when:**
- "How much am I spending?"
- "What's my API cost?"
- "Which sessions cost the most?"
- "Am I over budget?"
- "How can I reduce costs?"
- Setting up daily/weekly cost reports
- Optimizing model usage for crons and automated tasks

❌ **DON'T use this skill for:**
- Billing issues with Anthropic/OpenAI (contact providers directly)
- Managing API keys (use OpenClaw's secrets system)

## Quick Start

### Get a Cost Report (All Time)
```bash
python3 scripts/cost-report.py --all
```

### Last 24 Hours
```bash
python3 scripts/cost-report.py --hours 24
```

### With Budget Alert ($5/day)
```bash
python3 scripts/cost-report.py --budget 5.00
```

### JSON Output (for dashboards)
```bash
python3 scripts/cost-report.py --all --json
```

## What It Reports

- **Estimated cost** by model and session
- **Token breakdown** — input, output, context (cached)
- **Top spending sessions** — find what's burning tokens
- **Model efficiency** — how much you'd save switching routine tasks to cheaper models
- **Budget alerts** — 🟡 at 80% and 🔴 when over budget
- **Cron cost tracking** — automated jobs often account for 30-50% of spend

## Setting Up Automated Reports

### Daily Cost Report via Cron
Tell your agent:
> "Set up a daily cost report that runs at 8 AM and alerts me if I'm over $5/day"

The agent should create a cron job that:
1. Runs `python3 <skill-dir>/scripts/cost-report.py --hours 24 --budget 5.00`
2. Delivers the report via your preferred channel

### Model Optimization
The report flags when expensive models (Opus) are being used for routine tasks that Sonnet handles fine:
- Email checking crons → Sonnet
- Heartbeat checks → Sonnet  
- Site health monitoring → Sonnet or Haiku
- Complex reasoning, strategy, writing → Keep on Opus

## Supported Models & Pricing

| Model | Input $/1M | Output $/1M | Cache $/1M |
|-------|-----------|------------|-----------|
| Claude Opus 4 | $15.00 | $75.00 | $1.875 |
| Claude Sonnet 4 | $3.00 | $15.00 | $0.30 |
| Claude Haiku 3.5 | $0.80 | $4.00 | $0.08 |
| GPT-4o | $2.50 | $10.00 | $1.25 |
| GPT-4.1 | $2.00 | $8.00 | $0.50 |
| GPT-4.1-mini | $0.40 | $1.60 | $0.10 |
| GPT-4.1-nano | $0.10 | $0.40 | $0.025 |
| OpenRouter/auto | ~$3.00 | ~$15.00 | ~$0.30 |

Pricing is estimated and may vary. Update `scripts/cost-report.py` MODEL_PRICING dict for current rates.

## Roadmap
- [ ] Auto model-switching recommendations per session type
- [ ] Historical trend tracking (daily/weekly/monthly)
- [ ] Cost anomaly detection (sudden spikes)
- [ ] Per-project cost allocation
- [ ] Web dashboard with charts
