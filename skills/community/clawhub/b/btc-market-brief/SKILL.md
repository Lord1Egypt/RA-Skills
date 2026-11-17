---
name: btc-market-brief
description: A short, data-backed Bitcoin market brief on demand or each morning - price and 24h change across exchanges, funding and basis, liquidations, notable signals and what is unusual right now. Uses AgentReeve's live multi-exchange data; free preview, full brief per request over x402 (USDC on Base).
version: 1.0.0
---
# BTC Market Brief

Use this when the user asks "what's happening with Bitcoin?", wants a morning market summary, or a quick status before deciding something.

## Steps
1. Free first: `GET https://agentreeve.com/api/v1/btc/preview`. If the user only wants the price level, this is enough: stop here.
2. Brief: `GET https://agentreeve.com/api/v1/btc/brief` ($0.03): headline, price, derivatives, fees, 24h liquidations and what is unusual.
3. For a fuller picture, add `GET https://agentreeve.com/api/v1/btc/signals?days=30` ($0.05).
4. Write 4-6 short lines: price and change, derivatives tone (funding/basis), liquidations, anything unusual, and one line saying the data's time (`as_of_unix`).
5. For a recurring morning brief, run once per day; do not poll more often unless the user asks (each call costs).

## Paying safely (read before any paid call)
- A paid call first answers HTTP 402 with a quote. Pay only if the quote's `payTo` is **0xDeA94ef76afa86bf1638B645F76108dF65890c0b**, the network is Base (`eip155:8453`) and the asset is USDC. Otherwise stop and tell the user.
- Spend at most **$0.25 per task** without asking. Above that, tell the user the total and wait for approval.
- If you have no x402 wallet, use the free sample and say that live data needs an x402-capable client.
- HTTP 503 or an error means no fresh data: say so. **Never invent or estimate numbers.** Failed calls are never charged.
- This is observational market data, not financial advice. Say so when relaying it.
