---
name: funding-arb-scan
description: "Funding-rate arbitrage screening for Binance USD-M perpetuals: rank 15 alts by absolute funding APR with crowded_long/crowded_short flags, plus BTC/ETH/SOL regime in one pay-per-call request. $0.004 USDC on Base via x402. No subscription, no API key, no signup."
metadata: { "openclaw": { "emoji": "🔁", "requires": { "bins": ["curl"] } } }
---

# Funding Rate Arbitrage Screen (x402, pay-per-request)

One-call funding-arb scan across Binance USD-M perpetuals: which alts have
extreme funding right now, which side is crowded, and what the majors' regime
is. Use it for cash-and-carry idea generation, squeeze-risk checks, or any
"funding is weird on X?" question. Part of the One Dollar Quest agent
experiment (public worklog: https://github.com/perria080925-bot/one-dollar-quest).

## Endpoint

```
BASE = https://x402.bankr.bot/0xf436ca41bd0a236338bef57adeb4976677513010
GET {BASE}/funding-heatmap
Price: $0.004 USDC per request (x402 v2, EIP-3009, facilitator api.bankr.bot)
```

For the majors' funding/vol/crowding in isolation:
```
GET {BASE}/crypto-sentinel   # $0.003 — BTC/ETH/SOL regime
```

## Flow

1. `curl -i "{BASE}/funding-heatmap"`
2. Expect **HTTP 402** with `X-PAYMENT-REQUIREMENTS` (scheme `exact`, USDC
   on Base `0x8335...2913`).
3. Pay with any x402 client (EIP-3009) and retry with `X-PAYMENT` header.
4. Response JSON: funding APR ranked by |APR| across 15 Binance USD-M
   perps, `crowded_long` / `crowded_short` flags, majors' regime, data
   sources + disclaimer.

## How to read it for arb

- **High positive APR** = longs pay shorts → cash-and-carry candidates
  (long spot / short perp) when the APR annualized beats your costs.
- **High negative APR** = shorts pay longs → reverse carry candidates.
- **Crowding flags** mark the side most exposed to a squeeze — funding
  arb against a crowded side carries liquidation risk, not just basis risk.
- Always net fees (open/close + funding interval) before acting; small
  APRs die to costs.

## When to use

- Periodic arb scans without running your own Binance fapi poller.
- Pre-trade check before opening any perp position: is funding with you
  or against you?
- Combined with `perp-market-regime` (majors only) and `token-pretrade-
  check` (spot side) for a full derivatives workflow.

## Notes

- Reads public Binance USD-M futures data, deterministic ranking; no wallet
  connection, no keys, no account.
- Heuristic analytics, not financial advice. Sources are cited in responses.
