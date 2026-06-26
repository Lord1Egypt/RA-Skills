# Pricing Reference — April 2026

## Model rates

| Model             | Input /MTok | Output /MTok | Cached /MTok |
|-------------------|-------------|--------------|--------------|
| claude-opus-4-6   | $15.00      | $75.00       | $1.50        |
| claude-sonnet-4-6 | $3.00       | $15.00       | $0.30        |
| claude-haiku-4-5  | $0.25       | $1.25        | $0.025       |

## Savings formula (500K tokens/day baseline)

Baseline assumptions: 15M input tokens/mo, 5M output tokens/mo, single model
for all agents.

### Lever 1 — Prompt caching

Assume 80% cache hit rate after enabling `cacheRetention`.

```
savings = input_tokens × 0.8 × (input_rate − cached_rate)
```

Opus example: 15M × 0.8 × ($15.00 − $1.50) / 1M = **~$162/mo** saved on
input alone (72% input cost reduction).

### Lever 2 — Model routing

Route ~30% of tasks to Haiku, ~50% to Sonnet, ~20% to Opus.

```
blended_input_rate = 0.20×$15.00 + 0.50×$3.00 + 0.30×$0.25 = $4.575/MTok
savings_pct = 1 − (blended_rate / opus_rate) ≈ 70%
```

### Lever 3 — Thinking scope

Adaptive thinking adds ~2× token overhead per call. Scoping `thinking:
adaptive` to the planner only (vs. all agents) reduces thinking overhead by
~60–80% depending on agent mix.

### Lever 4 — context1m surcharge

Enabling `context1m: true` triggers the 1M context beta header, which adds a
~15–20% surcharge on all tokens for that agent. Removing it where not needed
saves proportionally.

### Lever 5 — Fast mode

`fastMode: true` on Sonnet reduces per-call latency and lowers costs 5–10% on
high-frequency agents through improved batching.

## Monthly cost estimate formula

```
monthly_cost = (input_tokens_per_day  × 30 × input_rate  / 1_000_000)
             + (output_tokens_per_day × 30 × output_rate / 1_000_000)
```

Apply per-lever reduction factors sequentially to compute before/after totals.

**Example at baseline (Opus-only, no caching):**
- Input:  15,000,000 × $15.00 / 1,000,000 = $225/mo
- Output:  5,000,000 × $75.00 / 1,000,000 = $375/mo
- **Total: ~$600/mo**

**After caching + routing:**
- Blended input rate after routing: ~$4.575/MTok
- With 80% cache hit: effective input rate ≈ $4.575 × 0.2 + $0.30 × 0.8 = $1.155/MTok
- Input: 15M × $1.155 / 1M ≈ $17/mo
- Output (Sonnet-weighted): 5M × $15.00 × 0.5 / 1M + 5M × $75 × 0.2 / 1M ≈ $112/mo
- **Total: ~$130/mo (~78% reduction)**
