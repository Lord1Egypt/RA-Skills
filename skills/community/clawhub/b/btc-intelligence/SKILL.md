---
name: agentreeve-btc-intelligence
description: Bitcoin market data for agents from AgentReeve, plus funding, basis and open interest for every crypto perpetual on Binance, Bybit, OKX and Hyperliquid - prices and candles across exchanges, derivatives, options and volatility, long/short positioning, liquidations, order-book walls, Hyperliquid whale flow and historical analogues. Free preview and free samples; live data per request over x402 (USDC on Base), no account or API key.
version: 2.2.0
---
# AgentReeve BTC Intelligence

Use this when the user asks about the Bitcoin market and needs real data rather than general knowledge.

## Start free
1. Live rounded summary: `GET https://agentreeve.com/api/v1/btc/preview`
2. Every product with its price, free sample and buy address: `GET https://agentreeve.com/api/v1/btc`
3. Check what a product returns before paying: `GET https://agentreeve.com/api/v1/btc/samples/<product>` (a real response, 15 minutes delayed, lists shortened).

## Pick the product that answers the question
| Question | Product | Price |
|---|---|---|
| Price across exchanges right now | `market` | $0.02 |
| Everything at once (market, derivatives, network) | `snapshot` | $0.06 |
| Hourly or daily candles | `candles?interval=1h&limit=48` | $0.02 |
| Funding, basis, open interest | `derivatives`, `basis`, `oi` | $0.02-0.04 |
| Are traders long or short? | `positioning` | $0.03 |
| Is implied volatility high vs realised? | `volatility` | $0.03 |
| Recent liquidations | `liquidations` | $0.03 |
| What big Hyperliquid traders are doing | `whale-flow` | $0.05 |
| Where large resting orders sit | `walls` | $0.03 |
| What happened after similar setups | `similar-setups` | $0.08 |
| A short written market brief | `brief` | $0.03 |
| A question in plain English | `POST ask` with `{"question": "..."}` | $0.15 |
| Extreme funding across all coins, funding spreads | `crypto/funding` | $0.03 |
| One coin's funding, basis, OI on every exchange | `crypto/perp?asset=ETH` | $0.02 |
| Where leverage is building or unwinding | `crypto/oi-movers` | $0.03 |
| Crowded longs and shorts across all coins | `crypto/crowded` | $0.04 |
| Everything about one coin before a trade | `crypto/coin?asset=SOL` | $0.05 |
| Order-book liquidity and slippage, any coin | `crypto/coin-liquidity?asset=SOL` | $0.03 |
| Long/short positioning, any coin | `crypto/coin-positioning?asset=SOL` | $0.03 |
| Candles, any coin | `crypto/coin-candles?asset=SOL` | $0.02 |

Bitcoin products: `https://agentreeve.com/api/v1/btc/<product>`; all-coin products: `https://agentreeve.com/api/v1/crypto/<product>`. Prices may change: the 402 quote is authoritative.

## Paying safely (read before any paid call)
- A paid call first answers HTTP 402 with a quote. Pay only if the quote's `payTo` is **0xDeA94ef76afa86bf1638B645F76108dF65890c0b**, the network is Base (`eip155:8453`) and the asset is USDC. Otherwise stop and tell the user.
- Spend at most **$0.25 per task** without asking. Above that, tell the user the total and wait for approval.
- If you have no x402 wallet, use the free sample and say that live data needs an x402-capable client.
- HTTP 503 or an error means no fresh data: say so. **Never invent or estimate numbers.** Failed calls are never charged.
- This is observational market data, not financial advice. Say so when relaying it.

Also available over MCP (`https://agentreeve.com/mcp`, tools `btc_free_preview`, `btc_list_products`, `btc_free_sample`, `btc_product`) and A2A (`https://agentreeve.com/.well-known/agent-card.json`). Full reference: `https://agentreeve.com/llms.txt`.
