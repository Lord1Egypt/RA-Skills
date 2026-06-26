---
name: asrai-x402
description: Crypto market analysis using Asrai API. Covers technical analysis, screeners, sentiment, forecasting, smart money, Elliott Wave, cashflow, DEX data, and AI-powered insights. Each API call costs $0.005 USDC from your own wallet on Base mainnet via x402.
license: MIT
metadata: {"openclaw":{"emoji":"📈","requires":{"env":["ASRAI_PRIVATE_KEY"]}},"clawdbot":{"emoji":"📈","requires":{"env":["ASRAI_PRIVATE_KEY"]}}}
---

# Asrai — Crypto Analysis via x402

Use Asrai tools when the user asks about crypto prices, market analysis, trading signals, sentiment, or investment advice.

## When to use

- Crypto price / chart / technical analysis → use asrai tools
- Market sentiment, CBBI, fear/greed → use asrai tools
- "What should I buy?" / buy opportunities / entry points → use `trade_signals` + `portfolio`
- Full market overview / morning report → use `market_overview`
- Elliott Wave, smart money, order blocks → use asrai tools
- DEX data, low-cap tokens → use asrai tools
- General knowledge you already know well → answer directly (costs $0.005 per call)

## Tool selection guide

| User asks... | Primary tool | Supporting tools |
|---|---|---|
| "what to buy?" / "buy opportunities" / "entry points" | `trade_signals` | `portfolio`, `sentiment` |
| "market overview" / "morning report" / "full brief" | `market_overview` | — |
| "what's trending?" / "hot coins" | `trending` | `gainers_losers` |
| "BTC analysis" / chart / signals | `technical_analysis` | `smart_money`, `elliott_wave` |
| "price prediction" / "forecast" | `forecast` | `technical_analysis` |
| "market sentiment" / "fear greed" / CBBI | `sentiment` | `dominance`, `macro` |
| "ATH" / "all-time high" coins | `ath_tracker` | `trade_signals` |
| "volume spikes" / unusual volume | `volume_spikes` | `high_volume_low_cap` |
| "find coins" / screener criteria | `screener` | `top_bottom` |
| "cashflow" / capital flow | `cashflow` | `sentiment` |
| "unlocked coins" / vesting pressure | `late_unlocked_coins` | — |
| "low cap gems" / DEX / chain tokens | `chain_tokens` | `dexscreener`, `high_volume_low_cap` |
| "portfolio" / "Abu's picks" | `portfolio` | `coin_info` |
| "my positions" / "open trades" / "my PnL" / "what am I trading" | `positions` | — |

**Important:** For buy opportunity questions ALWAYS call `trade_signals` — it combines trending movers, bounces, SAR & MACD entries, RSI, and Galaxy Score in one call.

## Install

```bash
npx -y -p asrai-mcp install-skill
```

Auto-detects OpenClaw, Cursor, Cline, and other agents. Then set your key:

```
ASRAI_PRIVATE_KEY=0x<your_private_key>  # add to ~/.env
```

For MCP agents (Cursor, Cline, Claude Desktop) also add to config:

```json
{
  "mcpServers": {
    "asrai": { "command": "npx", "args": ["-y", "asrai-mcp"] }
  }
}
```

## How to call

### If asrai MCP tools are available (Cursor, Cline, Claude Desktop)

Call the appropriate MCP tool directly:
```
technical_analysis(symbol, timeframe)
sentiment()
forecast(symbol)
market_overview()
ask_ai(question)
...
```

### If no MCP tool — use bash (OpenClaw and other agents)

Use the same tool names via bash:
```bash
npx -y -p asrai-mcp asrai <tool> [args...]
```

Examples:
```bash
npx -y -p asrai-mcp asrai ask_ai "What is the outlook for BTC today?"
npx -y -p asrai-mcp asrai technical_analysis BTC 4h
npx -y -p asrai-mcp asrai sentiment
npx -y -p asrai-mcp asrai forecast ETH
npx -y -p asrai-mcp asrai market_overview
npx -y -p asrai-mcp asrai coin_info SOL
npx -y -p asrai-mcp asrai portfolio
npx -y -p asrai-mcp asrai indicator_guide ALSAT
```

Requires `ASRAI_PRIVATE_KEY` set in `~/.env` or environment. Payment is signed automatically.

## MCP tools

| Tool | What it does | Cost |
|---|---|---|
| `market_overview` | Full brief: trending, gainers/losers, RSI, screeners, sentiment, cashflow — use for complete reports only | $0.095 (19 calls) |
| `trending` | Currently trending coins | $0.005 |
| `gainers_losers` | Top gainers and losers | $0.005 |
| `top_bottom` | RSI extremes, top/bottom signals, bounce/dip candidates | $0.015 (3 calls) |
| `volume_spikes` | Coins with unusually high volume | $0.005 |
| `high_volume_low_cap` | Low market cap coins with high volume | $0.005 |
| `ath_tracker` | Coins near or at all-time high | $0.005 |
| `dominance` | BTC & altcoin dominance signals | $0.01 (2 calls) |
| `macro` | S&P 500 & Nasdaq signals — global market context | $0.01 (2 calls) |
| `sentiment` | CBBI, CMC sentiment, AI insights, channel news, Galaxy Score, social dominance | $0.03 (6 calls) |
| `late_unlocked_coins` | Post-vesting coins with low remaining selling pressure | $0.005 |
| `trade_signals` | Trade setups: trending movers, bounces, SAR & MACD entries, RSI, Galaxy Score, today's indicator signals | $0.04 (8 calls) |
| `technical_analysis(symbol, timeframe)` | Signals, ALSAT, SuperALSAT, PSAR, MACD-DEMA, AlphaTrend, TD, SMC, S/R, Elliott Wave, Ichimoku | $0.055 (11 calls) |
| `forecast(symbol)` | AI 3-7 day price prediction | $0.005 |
| `screener(type)` | Find coins by criteria (ichimoku-trend, rsi, vwap, volume, bounce-dip...) | $0.005 |
| `smart_money(symbol, timeframe)` | Order blocks, fair value gaps, support/resistance | $0.01 (2 calls) |
| `elliott_wave(symbol, timeframe)` | Elliott Wave analysis | $0.005 |
| `ichimoku(symbol, timeframe)` | Ichimoku cloud analysis | $0.005 |
| `cashflow(mode, symbol)` | Capital flow data | $0.005 |
| `coin_info(symbol)` | Stats, price, tags, CMC AI + auto DEX data | $0.025–$0.03 (5–6 calls) |
| `dexscreener(contract)` | DEX trading data | $0.005 |
| `chain_tokens(chain, max_mcap)` | Low-cap tokens on a specific chain | $0.005 |
| `portfolio` | Abu's curated model portfolio — investment reference | $0.005 |
| `ask_ai(question)` | AI analyst freeform answer | $0.01 |
| `positions` | Your live open positions across connected exchanges (MEXC, Binance, Lighter) — requires exchange keys configured via /exchange_apis in Telegram | $0.005–$0.015 (1–3 calls) |
| `indicator_guide(name)` | Reference guide for Asrai-specific indicators | FREE |

## Exchange positions setup

To use the `positions` tool, add exchange API keys to `~/.env`:

```
# MEXC
MEXC_API_KEY=mx0vgl...
MEXC_SECRET_KEY=your_secret...

# Binance
BINANCE_API_KEY=your_api_key...
BINANCE_SECRET_KEY=your_secret...

# Lighter
LIGHTER_L1_ADDRESS=0x...
LIGHTER_API_PRIVATE_KEY=0x...
```

Only configure the exchanges you use — tool auto-detects which keys are set.

## Output rules

🎨 Output Style — Human-Friendly Format

Non-negotiables

• Use emoji section headers (🌡️ 🚀 📊 😬 ✅)
• Keep it easy to scan: short lines + whitespace
• Do not mention tools/endpoints in user-facing output
• Avoid low-liquidity noise: prefer repeated appearance across lists, meaningful volume, and/or clear catalyst
• Write like an experienced trader explaining to a friend — conversational, confident, direct
• Think like both a trader AND a long-term investor. Default to investor mode. Switch to trader mode only when user asks for entries
• End with 1 clear action bias: accumulate / wait / avoid — and why


## Cost

$0.005 USDC per call (most tools), $0.01 for `ask_ai`, FREE for `indicator_guide`. Signed from the user's own wallet on Base mainnet. Tell the user if they ask.
