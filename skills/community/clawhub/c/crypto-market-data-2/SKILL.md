---
name: crypto-market-data
description: Fetch reusable cryptocurrency realtime spot prices and historical price/K-line data for a symbol or coin id. Use when a user asks to get crypto realtime data, historical candles, full price history, Binance spot data, CoinGecko market-chart data, or wants to reuse market data in another project.
license: MIT
metadata:
  version: 1.0.0
  author: cryptoworldB1
  tags:
    - crypto
    - market-data
    - realtime
    - historical-prices
    - binance
    - coingecko
  dependencies:
    commands:
      - node
    tools: []
  source_repository: https://github.com/cryptoworldB1/skills
  skill_path: crypto-market-data
---

# Crypto Market Data

Use this skill to retrieve clean JSON market data that can be copied into any project.

## Quick Start

When this skill is installed from ClawHub or copied into an OpenClaw skills folder, run the bundled Node script from the skill directory:

```bash
node scripts/fetch-market-data.mjs BTC --realtime --history --interval 1d --range max
```

If the skill is installed in Codex locally, the same command can be run with the local path:

```bash
node ~/.codex/skills/crypto-market-data/scripts/fetch-market-data.mjs BTC --realtime --history --interval 1d --range max
```

Import it from another Node or OpenClaw project:

```js
import { fetchCryptoMarketData } from "~/.codex/skills/crypto-market-data/scripts/fetch-market-data.mjs";

const data = await fetchCryptoMarketData({
  symbol: "BTC",
  realtime: true,
  history: true,
  interval: "1d",
  range: "max",
});
```

## Source Selection

- Use `--history-source binance` for exchange K-lines. This is best for trading charts, but history starts when the pair listed on Binance.
- Use `--history-source coingecko --coin-id bitcoin --range max` for coin/project price history. This is better when the user asks for “全部历史价格”.
- Use Binance realtime for spot ticker data when the asset has a liquid `USDT`, `USDC`, or `FDUSD` spot pair.
- Do not invent market cap, supply, or history. If a source is missing, return an error or mark the field missing.

## Common Commands

Realtime only:

```bash
node ~/.codex/skills/crypto-market-data/scripts/fetch-market-data.mjs SOL --realtime
```

Binance full K-line history:

```bash
node ~/.codex/skills/crypto-market-data/scripts/fetch-market-data.mjs ETH --history --interval 1d --range max --history-source binance
```

CoinGecko full price history:

```bash
node ~/.codex/skills/crypto-market-data/scripts/fetch-market-data.mjs BTC --history --history-source coingecko --coin-id bitcoin --range max
```

Write JSON to a file:

```bash
node ~/.codex/skills/crypto-market-data/scripts/fetch-market-data.mjs TRUMP --realtime --history --range 30d --out trump-market.json
```

## OpenClaw Usage

When an OpenClaw agent needs market data, use this skill and execute the script with the requested symbol, source, interval, and range. Prefer JSON output and keep source errors non-fatal.

Example prompts after installation:

- “Use crypto-market-data to fetch BTC realtime spot data and full historical prices.”
- “Use crypto-market-data to fetch SOL 1d Binance K-lines for the last year.”
- “Use crypto-market-data to fetch CoinGecko full history for bitcoin.”

## Output Shape

The script returns:

- `query`: requested symbol, pair, interval, range and source choice.
- `realtime`: latest spot ticker from Binance when requested.
- `history`: candle/price series with source metadata.
- `errors`: non-fatal source errors.

Read `references/data-sources.md` when deciding between Binance, CoinGecko, and CMC semantics.
