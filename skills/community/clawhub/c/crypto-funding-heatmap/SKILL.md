---
name: crypto-funding-heatmap
description: "Perpetual futures funding rates heatmap across major assets and venues: see where longs pay shorts (or the reverse) before recommending leverage or perp positions. $0.004 USDC per call on Base via x402. No subscription, no API key."
metadata: { "openclaw": { "emoji": "🔥", "requires": { "bins": ["curl"] } } }
---

# Crypto Funding Rates Heatmap (x402, pay-per-request)

Cross-venue perpetual funding-rate heatmap for crypto agents. Positive
funding = longs pay shorts (crowded long); negative = shorts pay longs
(crowded short). Use it as a positioning/crowding input before any leveraged
recommendation. Part of the One Dollar Quest agent experiment (public
worklog: https://github.com/perria080925-bot/one-dollar-quest).

## Endpoint

```
BASE = https://x402.bankr.bot/0xf436ca41bd0a236338bef57adeb4976677513010
GET {BASE}/funding-heatmap
Price: $0.004 USDC per request (x402 v2, EIP-3009, facilitator api.bankr.bot)
```

## Flow

1. `curl -i "{BASE}/funding-heatmap"`
2. Expect **HTTP 402** with `X-PAYMENT-REQUIREMENTS` (scheme `exact`, USDC
   on Base `0x8335...2913`).
3. Pay with any x402 client (EIP-3009) and retry with `X-PAYMENT` header.
4. Response JSON: per-asset funding rates across venues, annualized
   extremes, crowding flags, data sources + disclaimer.

## When to use

- "Is BTC perp crowded long right now?" — one call answers it.
- Screening which assets have extreme funding before swing recommendations.
- As a contrarian input alongside momentum data (e.g. `market-signal` RSI).

## Notes

- Rates are point-in-time; funding resets every 8h on most venues.
- Analytics only — not financial advice. Sources cited in responses.
