---
name: api-cost-optimizer
description: "Analyze OpenClaw agent configuration and API usage patterns to identify cost-saving opportunities. Diagnose inefficient heartbeat configs, estimate daily/weekly API spend, and generate actionable recommendations to reduce LLM API costs. Essential for any agent operator running 24/7 on a budget. Use when: agent costs are higher than expected, heartbeat config needs review, or monthly API bill surprises you."
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["curl", "python3"] },
        "install": [],
      },
  }
---

# API Cost Optimizer

Diagnose, estimate, and optimize LLM API costs for OpenClaw agents running 24/7.

## What This Skill Does

- **Estimates API spend** from agent configuration (model, heartbeat interval, task complexity)
- **Diagnoses heartbeat waste** — the #1 cause of runaway API bills
- **Counts and categorizes tools** the agent has access to
- **Produces a cost report** with prioritized recommendations
- **Estimates time-to-payback** for any recommended changes

## The Problem This Solves

Documented cases show agents burning **$8–$250 per week** in API costs due to misconfigured heartbeats and inefficient task patterns. A properly tuned heartbeat alone can reduce costs by 60–90%.

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `API_COST_MODEL` | No | `openai` | Provider: `openai`, `anthropic`, `minimax`, `lmstudio` |
| `API_COST_INTERVAL` | No | `weekly` | Report interval: `daily`, `weekly`, `monthly` |
| `HEARTBEAT_INTERVAL` | No | `auto` | Override heartbeat interval in seconds (auto-detect if not set) |
| `MODEL_PRICE_INPUT` | No | auto | Price per 1M input tokens (auto-selected by provider) |
| `MODEL_PRICE_OUTPUT` | No | auto | Price per 1M output tokens (auto-selected by provider) |

## Provider Default Pricing (per 1M tokens)

| Provider | Model | Input | Output |
|----------|-------|-------|--------|
| OpenAI | GPT-4o | $2.50 | $10.00 |
| OpenAI | GPT-4o-mini | $0.15 | $0.60 |
| OpenAI | GPT-4-turbo | $10.00 | $30.00 |
| Anthropic | Claude 3.5 Sonnet | $3.00 | $15.00 |
| Anthropic | Claude 3 Opus | $15.00 | $75.00 |
| MiniMax | MiniMax-M2 | $0.10 | $0.10 |
| MiniMax | MiniMax-M2.1 | $0.20 | $0.40 |

## Scripts

### analyze.sh — Full Cost Analysis

Runs a complete cost diagnostic on the current OpenClaw configuration.

```bash
./scripts/analyze.sh
```

**Output:** Detailed markdown report with:
- Estimated API spend (daily / weekly / monthly)
- Heartbeat cost analysis
- Tool count risk factor
- Top 3 cost reduction recommendations
- Estimated savings after optimization

### heartbeat_diagnosis.sh — Find Heartbeat Waste

Checks OpenClaw heartbeat configuration and calculates wasted API calls.

```bash
./scripts/heartbeat_diagnosis.sh
```

**Output:** Heartbeat efficiency score (0–100%), wasted calls per day, estimated annual waste.

### estimate.sh — Quick Cost Estimate

One-shot estimate with optional custom parameters.

```bash
./scripts/estimate.sh <heartbeat_seconds> <tasks_per_day> <avg_input_tokens> <avg_output_tokens>
```

**Output:** Daily, weekly, and monthly cost estimates for the given parameters.

## Cost Reduction Recommendations

Priority order:

1. **Increase heartbeat interval** — If heartbeat is under 5 minutes, increase to 10–30 min for idle agents
2. **Switch to cheaper model** — MiniMax M2 at $0.10/1M is 25x cheaper than GPT-4o for most tasks
3. **Batch tasks** — Run 5–10 tasks per session instead of 1 task per heartbeat cycle
4. **Cache responses** — Use memory skills to avoid repeated context
5. **Disable verbose logging** — Reduces token churn in long conversations

## Usage Example

```bash
# Full analysis with MiniMax pricing
export API_COST_MODEL=minimax
./scripts/analyze.sh

# Quick estimate
./scripts/estimate.sh 300 20 8000 2000

# Heartbeat-only diagnosis
./scripts/heartbeat_diagnosis.sh
```

## Notes

- Estimates are based on configuration analysis, not live API metering
- For actual spend tracking, enable provider cost logs and compare
- MiniMax models offer best price/performance for volume workloads
- Heartbeat waste is typically the single largest cost lever
