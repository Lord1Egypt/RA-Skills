---
name: btc-similar-setups
description: When the Bitcoin market looks like it does now, what happened next? Finds past moments with similar funding, basis, positioning, volatility and order-book signals in AgentReeve's recorded history and reports BTC's move over the next 4, 24 and 72 hours against normal - with sample size and an honest quality grade. Free sample; live per request over x402.
version: 1.0.0
---
# BTC Similar Setups

Use this when the user asks "has this happened before?", "what usually happens next?" or wants historical context for the current market.

## Steps
1. Optional, free: `GET https://agentreeve.com/api/v1/btc/samples/similar-setups`.
2. Live: `GET https://agentreeve.com/api/v1/btc/similar-setups?k=20&days=180` ($0.08).
3. Report:
   - `after_similar_setups` for 4h, 24h and 72h (median move and `up_share`), **next to** `baseline_all_hours` so the user sees whether it differs from normal.
   - `analogues_found`, `history_days` and `sample_quality` (thin, moderate or solid), every time.
   - If `history_sources` shows archive data, say part of the history comes from exchange archives.
4. If `sample_quality` is "thin", lead with that: the result is indicative only.

Never present this as a forecast. Past tendencies in a limited sample, not a prediction and not advice.

## Paying safely (read before any paid call)
- A paid call first answers HTTP 402 with a quote. Pay only if the quote's `payTo` is **0xDeA94ef76afa86bf1638B645F76108dF65890c0b**, the network is Base (`eip155:8453`) and the asset is USDC. Otherwise stop and tell the user.
- Spend at most **$0.25 per task** without asking. Above that, tell the user the total and wait for approval.
- If you have no x402 wallet, use the free sample and say that live data needs an x402-capable client.
- HTTP 503 or an error means no fresh data: say so. **Never invent or estimate numbers.** Failed calls are never charged.
- This is observational market data, not financial advice. Say so when relaying it.
