---
name: carrier-reliability
description: 30-day carrier on-time performance prediction for any carrier and trade lane via 5-factor model
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://datasig.ai/signals/carrier-reliability
    emoji: "🚢"
---
# carrier-reliability

## What It Does

Predicts a carrier's on-time performance for a specific trade lane
over the next 30 days using a 5-factor scoring model:
Sea-Intelligence baseline (30%), AISstream schedule deviation (25%),
destination berth congestion (20%), blank sailing probability (15%),
and Freightos FBX rate volatility (10%).

Returns a reliability score (0-100), reliability level, trend
direction, named action signal, alternative carrier options,
and cost of inaction if you do not rebook.

At probability above 0.75, the REBOOK_NOW signal fires.

## When to Use

- Before booking ocean freight on a specific carrier and trade lane
- When evaluating whether to rebook to an alternative carrier
- When blank sailing risk is elevated and you need to compare options
- For daily monitoring of top carriers across your core trade lanes

## How to Use

`GET https://datasig.ai/signals/carrier-reliability?carrier=MSC&origin=CNSHA&destination=USSAV`

Parameters:
- `carrier` — MSC, MAERSK, CMACGM, HAPAG, EVERGREEN, COSCO, ONE, ZIM, YANGMING
- `origin` — CNSHA, CNYTN, CNNGB, CNQIN, KRPUS
- `destination` — USLAX, USLGB, USOAK, USSEA, USSAV, USNYK

## Example Response

```json
{
  "signal": "BOOK_WITH_CONFIDENCE",
  "carrier": "MSC",
  "trade_lane": "CNSHA→USSAV",
  "reliability_score": 78,
  "reliability_level": "MEDIUM",
  "trend": "improving",
  "urgency": "LOW",
  "action_window": "monitor",
  "alternative_carriers": [
    { "carrier": "GEMINI", "reliability_score": 87 },
    { "carrier": "HAPAG", "reliability_score": 79 }
  ],
  "cost_of_inaction": "If reliability drops below 65: est. $500-2,000/container rebooking fees",
  "confidence": 0.78,
  "n_factors_available": 4
}
```

## Signal Vocabulary

- `BOOK_WITH_CONFIDENCE` — score >= 75, trend stable or improving
- `MONITOR_SCHEDULE` — score 60-74, or trending down
- `CONSIDER_ALTERNATIVES` — score 50-59
- `REBOOK_NOW` — score < 50, or blank sailing prob > 0.75

## Pricing

- **$0.50/call** — reliability score + signal only (base tier)
- **$2.00/call** — full 30-day projection with factor breakdown,
  alternative carriers, and cost of inaction
  (Early adopter: $1.40 through 2026-09-21)

All via x402 micropayment on Base mainnet (USDC).

## Accuracy Ledger

Public accuracy tracking at https://datasig.ai/accuracy/stats

## Related Signals

- [blank-sailing](https://datasig.ai/signals/blank-sailing)
- [berth-congestion](https://datasig.ai/signals/berth-congestion)
