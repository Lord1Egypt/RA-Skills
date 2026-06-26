---
name: costlens
description: Calculate OpenClaw usage cost from offline event logs, apply budget thresholds, and export operator-facing reports.
homepage: https://github.com/mike007jd/openclaw-skills/tree/main/costlens
metadata: {"openclaw":{"emoji":"💸","requires":{"bins":["node"]}}}
---

# CostLens

Turn JSON usage events into cost summaries, budget checks, and offline reports.

## When to use

- You already have token usage events and need a quick spend summary.
- You want a simple budget gate in local automation or CI.
- You need an exportable JSON report without relying on a hosted billing dashboard.

## Commands

```bash
node {baseDir}/bin/costlens.js monitor --events ./events.json --budget 10.00 --threshold 80
node {baseDir}/bin/costlens.js budget check --events ./events.json --budget 5.00 --format json
node {baseDir}/bin/costlens.js report --events ./events.json --out ./reports/cost-report.json
```

## Built-in default rates

| Model | Input/1k | Output/1k |
| --- | --- | --- |
| gpt-4.1 | $0.01 | $0.03 |
| gpt-4o-mini | $0.00015 | $0.0006 |
| claude-3-5-sonnet | $0.003 | $0.015 |
| default | $0.002 | $0.008 |

Events can override the defaults with `inputCostPer1k` and `outputCostPer1k`.

## Event shape

```json
[
  {
    "model": "gpt-4.1",
    "promptTokens": 1500,
    "completionTokens": 800,
    "timestamp": "2026-02-26T10:00:00Z"
  }
]
```

## Output

- Total calls, total tokens, and total cost
- Per-model breakdowns for calls, tokens, and cost
- Per-day spend trends
- Budget usage percentage and alert level (`ok`, `warning`, or `critical`)

## Boundaries

- Pricing is based on built-in defaults plus per-event overrides. It is not a live pricing feed.
- CostLens is optimized for offline JSON analysis, not streaming metering or invoice reconciliation.
