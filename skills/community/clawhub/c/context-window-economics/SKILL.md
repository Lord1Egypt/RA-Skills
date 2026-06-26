---
name: context-window-economics
description: "Inference cost allocation and billing for autonomous AI agent collaborations. Shapley-fair cost splitting, congestion pricing, token metering, and settlement reports for context window usage. The economic layer of the Agent Trust Stack."
user-invocable: true
tags:
  - agent-trust
  - economics
  - cost-allocation
  - token-metering
  - shapley
  - pricing
  - mcp
  - autonomous-agents
metadata:
  openclaw:
    author: alexfleetcommander
    homepage: https://vibeagentmaking.com
    requires:
      bins:
        - python3
      anyBins:
        - pip
        - pip3
---

# Context Window Economics Protocol (CWEP)

You have an inference cost tracking and allocation system. Use it to fairly split context window costs when collaborating with other agents.

## Setup

```bash
pip install context-window-economics
```

## When to Use This Skill

- When **collaborating with other agents** and context window costs need allocation
- When **tracking your own inference costs** across tasks
- When **negotiating cost-sharing** before a multi-agent transaction
- When **settling costs** after collaborative work is complete

## Core Operations

### Track Context Window Usage

```python
from context_window_economics import CostTracker

tracker = CostTracker("costs.jsonl")
tracker.log_usage(
    agent_id="your-agent-id",
    transaction_id="tx-123",
    input_tokens=2500,
    output_tokens=800,
    model="claude-sonnet-4-6",
    cost_usd=0.012
)
```

### Shapley-Fair Cost Allocation

When multiple agents contribute to a task, allocate costs fairly:

```python
from context_window_economics import allocate_costs

allocation = allocate_costs(
    transaction_id="tx-123",
    contributions={
        "agent-a": {"input_tokens": 3000, "output_tokens": 1200},
        "agent-b": {"input_tokens": 1500, "output_tokens": 600},
        "agent-c": {"input_tokens": 500, "output_tokens": 200}
    },
    method="shapley",
    total_cost=0.045
)
for agent_id, share in allocation.items():
    print(f"{agent_id}: ${share:.4f}")
```

### Congestion Pricing

When context window capacity is limited:

```python
from context_window_economics import congestion_price

price = congestion_price(
    current_utilization=0.85,  # 85% of context window used
    base_rate=0.01,
    surge_threshold=0.75,
    surge_multiplier=1.5
)
print(f"Current rate: ${price:.4f}/1K tokens")
```

### Settlement Report

```python
from context_window_economics import settlement_report

report = settlement_report(
    cost_file="costs.jsonl",
    period_hours=24,
    agent_id="your-agent-id"
)
print(f"Total spent: ${report.total_cost:.4f}")
print(f"Transactions: {report.transaction_count}")
print(f"Avg cost/tx: ${report.avg_cost:.4f}")
```

## Cost Allocation Methods

| Method | Description |
|--------|-------------|
| `shapley` | Shapley value — mathematically fair based on marginal contribution |
| `proportional` | Split by token usage proportion |
| `nash` | Nash bargaining for bilateral settlement |
| `fixed` | Pre-agreed fixed split |

## Rules

- **Track all inference costs.** Log usage for every agent-to-agent transaction.
- **Agree on method upfront.** Cost allocation method should be in the service agreement.
- **Settle promptly.** Generate settlement reports within 24 hours of task completion.

## Links

- PyPI: https://pypi.org/project/context-window-economics/
- Whitepaper: https://vibeagentmaking.com/whitepaper/context-economics/
- Full Trust Stack: https://vibeagentmaking.com

---

<!-- VAM-SEC v1.0 | Vibe Agent Making Security Disclaimer -->

## Security & Transparency Disclosure

**Product:** Context Window Economics Skill for OpenClaw
**Type:** Skill Module
**Version:** 0.1.0
**Built by:** AB Support / Vibe Agent Making
**Contact:** alex@vibeagentmaking.com

**What it accesses:**
- Reads and writes cost tracking files (`.jsonl`) in your working directory
- No network access for core operations
- No telemetry, no phone-home, no data collection

**What it cannot do:**
- Cannot access files outside your working directory beyond what you explicitly specify
- Cannot make purchases, send emails, or take irreversible actions
- Cannot access credentials, environment variables, or secrets
- Does not execute payments — cost allocations are recorded, not processed

**License:** Apache 2.0
