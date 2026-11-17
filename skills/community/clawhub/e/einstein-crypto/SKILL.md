---
name: einstein-crypto
description: Crypto and market intelligence from Agent Einstein (emc2ai.io) over a public MCP endpoint. 18 free read-only tools, no account or key - AI price forecasts with a published accuracy record, market sentiment, whale and smart-money flows, prediction-market signals, Bitcoin cycle position, token safety screen, US Congress trades. 22 more paid tools use a prepaid credit balance. Use for questions about crypto prices, forecasts, on-chain flows, token safety or prediction markets.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    homepage: https://emc2ai.io/mcp
---

# Agent Einstein

Public MCP server (Streamable HTTP, JSON-RPC): `https://emc2ai.io/api/mcp`

If your agent has native MCP support, add that URL as a server and skip the curl below.
No API key, account or environment variable is needed for the free tools. This skill reads
no local files and sends nothing except the arguments you pass.

## Call a free tool with curl

```bash
curl -s https://emc2ai.io/api/mcp \
  -H 'content-type: application/json' -H 'accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_price_forecast","arguments":{}}}'
```

The answer is in `result.structuredContent` (and a text summary in `result.content`).
List every tool and its argument schema with `"method":"tools/list"`. Call
`list_einstein_capabilities` for the live free/paid split and prices.

## Free tools (18, read-only)

- `get_price_forecast` - dual-model (TimesFM + Kronos) forecast for BTC, ETH, SOL, BNB
- `get_forecast_accuracy` - measured error and direction hit rate of those forecasts
- `get_market_sentiment` - Fear & Greed variants and altcoin season
- `get_top_movers` - 24h gainers and losers among major caps
- `get_smart_money_flow`, `get_smart_money_inflow` - where profitable wallets rotate
- `get_hyperliquid_whales` - perp whale positioning and funding
- `get_robinhood_whale_prints` - large DEX trades on Robinhood Chain
- `get_polymarket_whales`, `get_prediction_market_catalysts` - prediction-market signals
- `get_bitcoin_cycle_position` - on-chain cycle position
- `check_token_safety` - honeypot/risk screen; argument `contract` (0x EVM address)
- `get_congress_trades`, `get_government_contracts` - US disclosures
- `get_analyst_accuracy` - graded track record of crypto commentators
- `get_social_hype`, `get_launchpad_radar` - social buzz and fresh launches
- `list_einstein_capabilities` - the live tool catalog

## Paid tools

22 deeper tools (token security analysis, wallet analysis, backtests, trade signals, and
others) cost $0.05-$2.00 per call from a prepaid credit balance, or x402 USDC on Base.
Top up at https://emc2ai.io. A paid call without credit returns the payment instructions
instead of data; tell the user rather than retrying. Never ask the user for a private key.

## Rules for answering

- Everything here is analysis, not financial advice. State that outputs are indicators.
- A snapshot that is "not warm yet" is not an error; say so and try later.
- Report the forecast accuracy next to any forecast you quote.
- 39 of 40 tools only read data. None moves funds.

Source and docs: https://github.com/ChuXo/einstein-claude-plugin - MCP registry: `io.emc2ai/einstein`.
