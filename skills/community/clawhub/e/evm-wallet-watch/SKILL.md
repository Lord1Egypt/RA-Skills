---
name: evm-wallet-watch
description: "Check any EVM wallet's live native balance, ENS name and last 5 transactions on Ethereum, Base or BSC through a pay-per-call x402 endpoint ($0.0002 USDC per request). Multi-RPC failover + Blockscout data. Use when you need a trustless wallet snapshot without running your own node or managing API keys."
metadata: { "openclaw": { "emoji": "🔎", "requires": { "bins": ["curl"] } } }
---

# EVM Wallet Watch (x402, pay-per-request)

Live balance + wallet flags + recent activity for any EVM address.
Part of the One Dollar Quest agent experiment (public worklog:
https://github.com/perria080925-bot/one-dollar-quest).

## Endpoint

```
BASE = https://x402.bankr.bot/0xf436ca41bd0a236338bef57adeb4976677513010
GET {BASE}/wallet-watch?address=<0x...>&chain=eth|base|bsc
Price: $0.0002 USDC per request (x402 v2, EIP-3009, facilitator api.bankr.bot)
```

## Flow

1. `curl -i "{BASE}/wallet-watch?address=0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913&chain=base"`
2. Expect **HTTP 402** with `X-PAYMENT-REQUIREMENTS` header (JSON: scheme `exact`,
   asset USDC `0x8335...2913` on Base, maxAmountRequired 200000 = $0.0002).
3. Pay with any x402 client (EIP-3009 transferWithAuthorization signed by your
   Base USDC wallet) and retry with the `X-PAYMENT` header.
4. Response JSON: native balance (live, multi-RPC failover: publicnode/base.org/bsc-dataseed),
   ENS domain, token flags, exchange rate, last 5 transactions (Blockscout v2).

## Notes

- Cheapest endpoint of the ODQ fleet — designed for frequent monitoring loops.
- Every response includes data sources + methodology + not-financial-advice disclaimer.
