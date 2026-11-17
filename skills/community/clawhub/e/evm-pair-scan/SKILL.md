---
name: evm-pair-scan
description: "Scan any EVM token's DEX pair before acting: liquidity depth, 24h volume, volume/churn ratio, best pair route, FDV and volatility in one pay-per-call request. $0.005 USDC on Base via x402. No subscription, no API key, no signup."
metadata: { "openclaw": { "emoji": "🔎", "requires": { "bins": ["curl"] } } }
---

# EVM Pair Scan (x402, pay-per-request)

One-call liquidity + activity scan for any EVM token address (BSC, Base,
Ethereum). Use it before quoting a token, recommending a trade, or adding a
pair to a watchlist. Part of the One Dollar Quest agent experiment (public
worklog: https://github.com/perria080925-bot/one-dollar-quest).

## Endpoint

```
BASE = https://x402.bankr.bot/0xf436ca41bd0a236338bef57adeb4976677513010
GET {BASE}/pair-scan?address=<0xTOKEN>&chain=<bsc|base|eth>
Price: $0.005 USDC per request (x402 v2, EIP-3009, facilitator api.bankr.bot)
```

## Flow

1. `curl -i "{BASE}/pair-scan?address=0xTOKEN&chain=bsc"`
2. Expect **HTTP 402** with `X-PAYMENT-REQUIREMENTS` (scheme `exact`, USDC
   on Base `0x8335...2913`).
3. Pay with any x402 client (EIP-3009) and retry with `X-PAYMENT` header.
4. Response JSON: liquidity USD, volume 24h, churn ratio, best pair +
   router, FDV, realized volatility, data sources + disclaimer.

## When to use

- Before answering "is this token tradeable?" — liquidity + churn answer it.
- Before adding a pair to an agent portfolio or alert list.
- Combined with `bsc-rug-check` (safety score) for a full pre-trade screen.

## Notes

- Reads public DEX pair data; no wallet connection, no keys, no account.
- Heuristic analytics, not financial advice. Sources are cited in responses.
