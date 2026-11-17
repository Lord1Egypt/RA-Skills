---
name: btc-derivatives-check
description: Before a Bitcoin trade, check the derivatives picture across exchanges - funding and basis, open interest, long/short positioning, recent liquidations and where the large order-book walls are. Live data from AgentReeve; free samples, live data per request over x402 (USDC on Base).
version: 1.0.0
---
# BTC Derivatives Check

Use this when the user is considering a BTC trade or asks whether the market is overheated, crowded or over-leveraged.

## Steps (about $0.13 in total; ask first if the user set a lower limit)
1. `GET https://agentreeve.com/api/v1/btc/derivatives` ($0.04): funding and basis by venue.
2. `GET https://agentreeve.com/api/v1/btc/positioning?hours=24` ($0.03): long/short ratios, top traders vs everyone, 30-day percentile.
3. `GET https://agentreeve.com/api/v1/btc/liquidations?minutes=60` ($0.03): recent forced closures by side.
4. `GET https://agentreeve.com/api/v1/btc/walls?hours=24` ($0.03): large resting orders above and below the price.
5. Summarise as: crowding (positioning + funding), leverage being flushed (liquidations), and nearby support/resistance from walls (price and size).

Do not tell the user what to trade. Present the data, note conflicting signals, and remind them this is not advice.

## Paying safely (read before any paid call)
- A paid call first answers HTTP 402 with a quote. Pay only if the quote's `payTo` is **0xDeA94ef76afa86bf1638B645F76108dF65890c0b**, the network is Base (`eip155:8453`) and the asset is USDC. Otherwise stop and tell the user.
- Spend at most **$0.25 per task** without asking. Above that, tell the user the total and wait for approval.
- If you have no x402 wallet, use the free sample and say that live data needs an x402-capable client.
- HTTP 503 or an error means no fresh data: say so. **Never invent or estimate numbers.** Failed calls are never charged.
- This is observational market data, not financial advice. Say so when relaying it.
