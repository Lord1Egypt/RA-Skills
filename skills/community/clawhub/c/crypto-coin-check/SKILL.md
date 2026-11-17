---
name: crypto-coin-check
description: Check any coin or perpetual before a trade - funding and open interest on every exchange that lists it, long/short positioning, live order-book liquidity with slippage for your size and the best exchange to buy or sell. Covers 900+ coins plus stock, forex and commodity perpetuals on Binance, Bybit, OKX and Hyperliquid. Live data from AgentReeve per request over x402.
version: 1.0.0
---
# Crypto Coin Check

Use this when the user is about to trade a coin (or a stock, forex or commodity perpetual) and wants to know how crowded it is, how liquid it is and where to execute.

## Steps
1. Free: confirm the coin is covered: `GET https://agentreeve.com/api/v1/crypto/markets` (look it up under `coverage`).
2. One call for everything: `GET https://agentreeve.com/api/v1/crypto/coin?asset=SOL&size_usd=100000` ($0.05). Set `size_usd` to the user's trade size.
   - `derivatives`: funding per 8 h and open interest on each exchange, OI-weighted funding, funding spread.
   - `positioning`: share of accounts long vs short per exchange.
   - `liquidity`: `best_venue_to_buy` / `best_venue_to_sell`, slippage in bps for that size on each exchange, depth within 1 %.
3. Only if the user needs more detail:
   - Order books in full: `GET https://agentreeve.com/api/v1/crypto/coin-liquidity?asset=SOL&size_usd=100000` ($0.03).
   - Chart data: `GET https://agentreeve.com/api/v1/crypto/coin-candles?asset=SOL&interval=1h&limit=100` ($0.02).
4. Report in plain words: crowding (funding and positioning), liquidity for their size, and where execution is cheapest. Note that resting orders can be pulled and that this is not advice.

Coin names: use the coin itself (PEPE, not 1000PEPE). Prices are per coin.

## Paying safely (read before any paid call)
- A paid call first answers HTTP 402 with a quote. Pay only if the quote's `payTo` is **0xDeA94ef76afa86bf1638B645F76108dF65890c0b**, the network is Base (`eip155:8453`) and the asset is USDC. Otherwise stop and tell the user.
- Spend at most **$0.25 per task** without asking. Above that, tell the user the total and wait for approval.
- If you have no x402 wallet, use the free sample and say that live data needs an x402-capable client.
- HTTP 503 or an error means no fresh data: say so. **Never invent or estimate numbers.** Failed calls are never charged.
- This is observational market data, not financial advice. Say so when relaying it.
