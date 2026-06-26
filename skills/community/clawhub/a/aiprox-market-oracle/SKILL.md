---
name: aiprox-market-oracle
description: Get trading signals for single or batch Polymarket markets. Supports timeframe framing ranked by edge.
acceptLicenseTerms: true
metadata:
  clawdbot:
    emoji: "🔮"
    homepage: https://aiprox.dev
    requires:
      env:
        - AIPROX_SPEND_TOKEN
---

# Market Oracle

Get trading signals for Polymarket prediction markets. Analyzes market data, news, and sentiment to provide actionable BUY/AVOID/SELL recommendations with edge estimates. Supports batch comparison of up to 5 markets ranked by opportunity, and timeframe framing for short, medium, or long-term analysis.

## When to Use

- Evaluating Polymarket betting opportunities
- Comparing multiple markets to find the best edge
- Getting a second opinion on market positions
- Researching prediction market fundamentals
- Identifying mispriced markets

## Usage Flow

1. Provide a single `market` slug **or** a `markets` array (up to 5) for batch comparison
2. Optionally set `timeframe`: `short` (days), `medium` (weeks, default), or `long` (months)
3. AIProx routes to the market-oracle agent
4. Single: returns signal, edge, confidence, reasoning. Batch: returns ranked array with best opportunity first.

## Security Manifest

| Permission | Scope | Reason |
|------------|-------|--------|
| Network | aiprox.dev | API calls to orchestration endpoint |
| Env Read | AIPROX_SPEND_TOKEN | Authentication for paid API |

## Make Request — Single

```bash
curl -X POST https://aiprox.dev/api/orchestrate \
  -H "Content-Type: application/json" \
  -H "X-Spend-Token: $AIPROX_SPEND_TOKEN" \
  -d '{
    "task": "should I bet on this",
    "market": "will-bitcoin-reach-100k-by-end-of-2024",
    "timeframe": "short"
  }'
```

### Response — Single

```json
{
  "mode": "single",
  "signal": "BUY",
  "edge": 12.5,
  "confidence": 68,
  "reasoning": "Current YES price of 0.42 undervalues probability given recent ETF inflows. Fair value estimate: 0.54.",
  "timeframe": "short"
}
```

## Make Request — Batch

```bash
curl -X POST https://aiprox.dev/api/orchestrate \
  -H "Content-Type: application/json" \
  -H "X-Spend-Token: $AIPROX_SPEND_TOKEN" \
  -d '{
    "task": "compare these markets",
    "markets": ["will-bitcoin-reach-100k-by-end-of-2024", "will-fed-cut-rates-in-q1-2025"],
    "timeframe": "medium"
  }'
```

### Response — Batch

```json
{
  "mode": "batch",
  "timeframe": "medium",
  "best_market": "will-fed-cut-rates-in-q1-2025",
  "ranked": [
    {"rank": 1, "market": "will-fed-cut-rates-in-q1-2025", "signal": "BUY", "edge": 18.2, "confidence": 74},
    {"rank": 2, "market": "will-bitcoin-reach-100k-by-end-of-2024", "signal": "AVOID", "edge": 3.1, "confidence": 45}
  ]
}
```

## Trust Statement

Market Oracle provides analysis for informational purposes only. Not financial advice. Signals are AI-generated estimates and may be wrong. Always do your own research. Your spend token is used for payment only.
