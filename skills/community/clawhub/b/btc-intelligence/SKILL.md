---
name: agentreeve-btc-intelligence
description: Crypto market data for agents from AgentReeve - prices, candles, derivatives (funding, basis, open interest), long/short positioning, order-book liquidity and a one-call snapshot for any coin on Binance, Bybit, OKX and Hyperliquid, scanners for extreme funding and crowded trades, and Bitcoin depth (options, liquidations, whales, similar setups). Paid per request over x402, free samples.
version: 3.0.0
---
# AgentReeve Crypto Market Data

Use this when the user asks about Bitcoin or any crypto market and needs real data rather than general knowledge.

## Start free
1. Live rounded summary: `GET https://agentreeve.com/api/v1/preview`
2. Every product with its price, what it covers, a free sample and the buy address: `GET https://agentreeve.com/api/v1`
3. Check what a product returns before paying: `GET https://agentreeve.com/api/v1/samples/<product>` (a real response, 15 minutes delayed, lists shortened).
4. Which coins are covered: `GET https://agentreeve.com/api/v1/markets` (900+ coins, plus stock, forex and commodity perpetuals).

## Pick the product that answers the question
Products marked *any coin* take `asset=` (BTC, ETH, SOL, PEPE, XAU...). Without `asset` they answer for BTC and say so.

| Question | Product | Price |
|---|---|---|
| Price across exchanges right now (any coin) | `price?asset=SOL` | $0.02 |
| Candles (any coin) | `candles?asset=ETH&interval=1h&limit=48` | $0.02 |
| Funding, basis, open interest (any coin) | `derivatives?asset=ETH` | $0.04 |
| Are traders long or short? (any coin) | `positioning?asset=SOL` | $0.03 |
| Order-book depth, walls and slippage for a size (any coin) | `liquidity?asset=SOL&size_usd=100000` | $0.03 |
| Everything about one coin before a trade (any coin) | `snapshot?asset=SOL` | $0.05 |
| Extreme funding and funding spreads across all coins | `funding` | $0.03 |
| Where leverage is building or unwinding | `oi-movers` | $0.03 |
| Crowded longs and shorts across all coins | `crowded` | $0.04 |
| Is implied volatility high vs realised? (BTC) | `volatility` | $0.03 |
| Recent liquidations (BTC) | `liquidations` | $0.03 |
| What big Hyperliquid traders are doing (BTC) | `whales` | $0.05 |
| What happened after similar setups (BTC) | `similar-setups` | $0.08 |
| A short written market brief (BTC) | `brief` | $0.03 |
| A question in plain English | `POST ask` with `{"question": "..."}` | $0.15 |

Every product: `https://agentreeve.com/api/v1/<product>`. Prices may change: the 402 quote is authoritative.

## Paying safely (read before any paid call)
- A paid call first answers HTTP 402 with a quote. Pay only if the quote's `payTo` is **0xDeA94ef76afa86bf1638B645F76108dF65890c0b**, the network is Base (`eip155:8453`) and the asset is USDC. Otherwise stop and tell the user.
- Spend at most **$0.25 per task** without asking. Above that, tell the user the total and wait for approval.
- If you have no x402 wallet, use the free sample and say that live data needs an x402-capable client.
- HTTP 503 or an error means no fresh data: say so. **Never invent or estimate numbers.** Failed calls are never charged.
- This is observational market data, not financial advice. Say so when relaying it.

Also available over MCP (`https://agentreeve.com/mcp`, tools `free_preview`, `list_products`, `free_sample`, `how_to_buy`) and A2A (`https://agentreeve.com/.well-known/agent-card.json`). Full reference: `https://agentreeve.com/llms.txt`.
