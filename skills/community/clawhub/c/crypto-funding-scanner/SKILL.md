---
name: crypto-funding-scanner
description: Scan funding rates across every USDT/USDC perpetual on Binance, Bybit, OKX and Hyperliquid - the most extreme funding right now, the widest cross-exchange funding spreads for the same coin, and where open interest is building or unwinding. Real multi-exchange data from AgentReeve, every 5 minutes; free market list, live data per request over x402.
version: 1.1.0
---
# Crypto Funding Scanner

Use this when the user asks which coins have extreme funding, where funding arbitrage might exist, whether a coin is crowded long or short, or where leverage is building.

## Steps
1. Free: which coins and exchanges are covered: `GET https://agentreeve.com/api/v1/crypto/markets`.
2. Funding scan: `GET https://agentreeve.com/api/v1/crypto/funding?min_oi_usd=1000000&limit=20` ($0.03).
   - `highest_funding` / `lowest_funding`: report coin, exchange, `funding_8h_pct` and `funding_annual_pct`, with open interest.
   - `cross_venue_spreads`: the same coin paying different funding on two exchanges. Report `spread_annual_pct`, `long_on` and `short_on`, and `min_leg_oi_usd`.
3. One coin in depth: `GET https://agentreeve.com/api/v1/crypto/perp?asset=ETH&hours=48` ($0.02): funding, basis and open interest on every exchange listing it, with hourly history.
4. Leverage building or unwinding: `GET https://agentreeve.com/api/v1/crypto/oi-movers?window=24h` ($0.03). Report `oi_change_pct`, `price_change_pct` and the `reading`.
5. Crowded trades: `GET https://agentreeve.com/api/v1/crypto/crowded?min_oi_usd=10000000` ($0.04): coins whose funding is extreme for their peers while open interest builds. Report `crowded_long` and `crowded_short` with `crowding_score`; crowded longs can unwind and crowded shorts can squeeze.

Results include the stock, forex and commodity perpetuals these exchanges list; each item has a `category`. Add `category=crypto` (or `stock`, `forex`, ...) to scan one kind only.

Funding is shown per 8 hours even when an exchange settles every 1 or 4 hours. A funding spread is not free money: fees, basis moves, liquidity and liquidation risk on two exchanges all matter. Say so whenever you present one.

## Paying safely (read before any paid call)
- A paid call first answers HTTP 402 with a quote. Pay only if the quote's `payTo` is **0xDeA94ef76afa86bf1638B645F76108dF65890c0b**, the network is Base (`eip155:8453`) and the asset is USDC. Otherwise stop and tell the user.
- Spend at most **$0.25 per task** without asking. Above that, tell the user the total and wait for approval.
- If you have no x402 wallet, use the free sample and say that live data needs an x402-capable client.
- HTTP 503 or an error means no fresh data: say so. **Never invent or estimate numbers.** Failed calls are never charged.
- This is observational market data, not financial advice. Say so when relaying it.
