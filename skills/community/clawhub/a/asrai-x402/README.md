# Asrai — Crypto Analysis Skill

Crypto market analysis skill for AI agents. Powered by [Asrai](https://asrai.me) via x402 — pay $0.005 USDC per call, no subscription needed.

Works with **OpenClaw**, **Claude Desktop**, **Cursor**, **Cline**, and any MCP-compatible or bash-capable agent.

---

## Install

### One command — works everywhere

```bash
npx -y -p asrai-mcp@latest install-skill
```

Auto-detects OpenClaw, Cursor, Cline, and other agents. Copies SKILL.md to the right place. Then restart your agent or run "refresh skills".

### Manual — OpenClaw (if auto-detect fails)

```bash
git clone https://github.com/abuzerasr/asrai-skill.git ~/.openclaw/workspace/skills/asrai
```

Then restart OpenClaw or run "refresh skills".

### Manual — Cursor / Cline / other agents

```bash
npx skills add abuzerasr/asrai-skill
```

Or via [ClawHub](https://clawhub.ai/abuzerasr/asrai-x402) — one-click install.

---

## Setup

### 1. Set your private key

```bash
echo "ASRAI_PRIVATE_KEY=0x<your_private_key>" >> ~/.env
```

Your wallet must hold USDC on Base mainnet (~$1–2 is plenty).

### 2. Connect the MCP server (Cursor, Cline, Claude Desktop)

Add to your MCP config:

```json
{
  "mcpServers": {
    "asrai": {
      "command": "npx",
      "args": ["-y", "asrai-mcp"]
    }
  }
}
```

Config file locations:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

> **OpenClaw users:** skip this step — OpenClaw uses bash automatically, no MCP config needed.

### 3. n8n / remote connections

```
HTTP Streamable: https://mcp.asrai.me/mcp?key=0x<your_private_key>
SSE (legacy):    https://mcp.asrai.me/sse?key=0x<your_private_key>
```

---

## How to use

Just ask your agent naturally — it picks the right tool automatically:

> "Do a technical analysis on BTC 4h"
> "What's the market sentiment right now?"
> "Give me a price forecast for ETH"
> "Show me the top gainers"
> "What does ALSAT signal mean?"
> "Analyze SOL and tell me if I should buy"

### OpenClaw — bash commands

OpenClaw runs these commands directly. Same tool names as MCP:

```bash
npx -y -p asrai-mcp asrai technical_analysis BTC 4h
npx -y -p asrai-mcp asrai sentiment
npx -y -p asrai-mcp asrai forecast ETH
npx -y -p asrai-mcp asrai market_overview
npx -y -p asrai-mcp asrai ask_ai "Is BTC a good buy right now?"
npx -y -p asrai-mcp asrai coin_info SOL
npx -y -p asrai-mcp asrai screener ath
npx -y -p asrai-mcp asrai smart_money BTC 1d
npx -y -p asrai-mcp asrai portfolio
npx -y -p asrai-mcp asrai indicator_guide ALSAT
```

---

## Tools


| Tool | What it does | Cost |
|---|---|---|
| `market_overview` | Full brief: trending, gainers/losers, RSI, screeners, sentiment, cashflow — use for complete reports only | $0.095 |
| `trending` | Currently trending coins | $0.005 |
| `gainers_losers` | Top gainers and losers | $0.005 |
| `top_bottom` | RSI extremes, top/bottom signals, bounce/dip candidates | $0.015 |
| `volume_spikes` | Coins with unusually high volume | $0.005 |
| `high_volume_low_cap` | Low market cap coins with high volume | $0.005 |
| `ath_tracker` | Coins near or at all-time high | $0.005 |
| `dominance` | BTC & altcoin dominance signals | $0.01 |
| `macro` | S&P 500 & Nasdaq signals — global market context | $0.01 |
| `sentiment` | CBBI, CMC sentiment, AI insights, channel news, Galaxy Score, social dominance | $0.03 |
| `late_unlocked_coins` | Post-vesting coins with low remaining selling pressure | $0.005 |
| `trade_signals` | Trade setups: trending movers, bounces, SAR & MACD entries, RSI, Galaxy Score, today's indicator signals | $0.04 (8 calls) |
| `technical_analysis(symbol, timeframe)` | Signals, ALSAT, SuperALSAT, PSAR, MACD-DEMA, AlphaTrend, TD, SMC, S/R, Elliott Wave, Ichimoku | $0.055 |
| `forecast(symbol)` | AI 3-7 day price prediction | $0.005 |
| `screener(type)` | Find coins by criteria (ichimoku-trend, rsi, vwap, volume, bounce-dip...) | $0.005 |
| `smart_money(symbol, timeframe)` | Order blocks, fair value gaps, support/resistance | $0.01 |
| `elliott_wave(symbol, timeframe)` | Elliott Wave analysis | $0.005 |
| `ichimoku(symbol, timeframe)` | Ichimoku cloud analysis | $0.005 |
| `cashflow(mode, symbol)` | Capital flow data | $0.005 |
| `coin_info(symbol)` | Stats, price, tags, CMC AI + auto DEX data | $0.025–$0.03 |
| `dexscreener(contract)` | DEX trading data | $0.005 |
| `chain_tokens(chain, max_mcap)` | Low-cap tokens on a specific chain | $0.005 |
| `portfolio` | Abu's curated model portfolio — investment reference | $0.005 |
| `ask_ai(question)` | AI analyst freeform answer | $0.01 |
| `positions` | Your live open positions across connected exchanges (MEXC, Binance, Lighter) | $0.005–$0.015 |
| `indicator_guide(name)` | Reference guide for Asrai-specific indicators | FREE |

Session spend cap: $2.00 USDC (configurable via `ASRAI_MAX_SPEND` env var).

---

## Exchange positions setup

To use the `positions` tool, add your exchange API keys to `~/.env`:

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

---

## Links

- Website: [asrai.me/agents](https://asrai.me/agents)
- MCP npm package: [npmjs.com/package/asrai-mcp](https://www.npmjs.com/package/asrai-mcp)
- ClawHub: [clawhub.ai/abuzerasr/asrai-x402](https://clawhub.ai/abuzerasr/asrai-x402)
- x402 protocol: [x402.org](https://x402.org)

## License

MIT
