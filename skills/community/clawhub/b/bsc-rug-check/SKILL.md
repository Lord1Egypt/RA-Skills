---
name: bsc-rug-check
description: "Rug-pull and safety screening for any EVM token before trading or recommending it: pair age, liquidity depth, volume churn, volatility, buy/sell imbalance -> 0-100 score with auditable flags. Pay-per-call $0.01 USDC on Base via x402. No subscription, no API key."
metadata: { "openclaw": { "emoji": "🛡️", "requires": { "bins": ["curl"] } } }
---

# BSC / EVM Rug Check (x402, pay-per-request)

Heuristic token safety score with auditable flags, on any EVM token address.
Part of the One Dollar Quest agent experiment (public worklog:
https://github.com/perria080925-bot/one-dollar-quest).

## Endpoint

```
BASE = https://x402.bankr.bot/0xf436ca41bd0a236338bef57adeb4976677513010
GET {BASE}/token-safety?address=<0xTOKEN>
Price: $0.01 USDC per request (x402 v2, EIP-3009, facilitator api.bankr.bot)
```

## Flow

1. `curl -i "{BASE}/token-safety?address=0xTOKEN"`
2. Expect **HTTP 402** with `X-PAYMENT-REQUIREMENTS` (scheme `exact`, USDC on Base).
3. Pay with any x402 client (EIP-3009) and retry with `X-PAYMENT` header.
4. Response JSON: 0–100 safety score + flags (pair age, liquidity depth, volume
   churn, volatility, buy/sell imbalance) + data sources + disclaimer.

## Notes

- Use BEFORE any token purchase recommendation. Score is heuristic, not a verdict.
- Works for BSC, Base and Ethereum tokens (DexScreener-backed pair data).
