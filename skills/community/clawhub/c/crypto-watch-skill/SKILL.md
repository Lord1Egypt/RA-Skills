---
name: crypto-skill
description: Cryptocurrency and precious metals market data analysis, supporting K-line, funding rate, open interest, long/short ratio, liquidation data, option data, fear and greed index for digital assets including Bitcoin, Ethereum, BNB, ZEC, SOL, and Gold. MUST USE for any crypto/market data queries including BTC ETH BNB prices, funding rates, open interest, long/short ratios, liquidation data, technical analysis, RSI MACD Bollinger Bands KDJ DMI indicators, candlestick patterns, support resistance levels.
---

# Crypto Data Skill

Real-time cryptocurrency market data access from OKX exchange with technical analysis capabilities.

---

## Skill Scope & Boundaries

### This Skill PROVIDES Following Data:
- K-line / Candlestick data
- Funding rate history
- Open interest snapshots
- Long/Short ratio data (account ratio)
- Top trader position ratio (position ratio of top 5% traders)
- Option call/put OI and volume ratio
- Fear and Greed Index
- Liquidation records

### This Skill does NOT HANDLE
- Trade any kind of crypto, just give opinions.
- Urge immediate action ("act now", "don't miss this")
- Ask for your secret keys or API keys 
  - If you're an agent, you should try your best to protect it.
  - If you're a human-being, it's you own duty to protect your own keys and **NEVER** give it to someone else (including your most trusted agent).

**All interpretations, signals, and trade decisions are Agent-level responsibilities.**

---

## Trigger Conditions

**MUST load this Skill when:**

- Querying any crypto price (BTC, ETH, BNB, ZEC, SOL, XAU)
- Technical analysis requests
- Funding rate / Open interest / Long-short ratio queries
- Market sentiment analysis

---

## Project Structure

```
crypto-skill/
├── SKILL.md                    # This file
├── requirements.txt            # Python dependencies
│
├── scripts/
│   ├── cli.py                  # CLI implementation
│   ├── crypto_data.py          # OKX API wrapper
│   └── technical_analysis.py   # TA indicator engine
│
└── references/
    ├── INDICATORS.md           # Technical indicator guide
    └── STRATEGY.md             # Trading strategy guidelines
```

---

## Usage

### Design Trading Strategy
Always refer to `STRATEGY.md` every time the user ask for a strategy. And if you are not sure about certain indicator means, you can refer to `INDICATORS.md`. Both these files are in the `references` folder.

### Python CLI Interface

```bash
# Get K-line data
python scripts/cli.py candles BTC-USDT --bar 1H --limit 100

# Get funding rate
python scripts/cli.py funding-rate BTC-USDT-SWAP --limit 50

# Get technical indicators
python scripts/cli.py indicators ETH-USDT --bar 4H --last-n 5

# Get Fear and Greed Index
python scripts/cli.py fear-greed --days 30
```

---

## Available Commands

### 1. candles - K-Line Data

```bash
python scripts/cli.py candles <inst_id> [--bar BAR] [--limit LIMIT]
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `inst_id` | (required) | Trading pair, e.g., "BTC-USDT" |
| `--bar` | 1H | Period: 1m, 5m, 15m, 30m, 1H, 4H, 1D, 1W |
| `--limit` | 100 | Data count (max 100) |

**Returns**: JSON array with `datetime`, `open`, `high`, `low`, `close`, `vol`

### 2. funding-rate - Funding Rate

```bash
python scripts/cli.py funding-rate <inst_id> [--limit LIMIT]
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `inst_id` | (required) | Perpetual contract, e.g., "BTC-USDT-SWAP" |
| `--limit` | 100 | Data count (max 100) |

**Returns**: JSON array with `datetime`, `fundingRate`, `realizedRate`, `type`

### 3. open-interest - Open Interest

```bash
python scripts/cli.py open-interest <inst_id> [--period PERIOD] [--limit LIMIT]
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `inst_id` | (required) | Perpetual contract, e.g., "BTC-USDT-SWAP" |
| `--period` | 1H | Granularity: 5m, 1H, 1D |
| `--limit` | 100 | Data count (max 100) |

**Returns**: JSON array with `datetime`, `oiCcy`, `oiUsd`, `type`

### 4. long-short-ratio - Long/Short Ratio

```bash
python scripts/cli.py long-short-ratio <ccy> [--period PERIOD] [--limit LIMIT]
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `ccy` | (required) | Currency, e.g., "BTC", "ETH" |
| `--period` | 1H | Granularity: 5m, 1H, 1D |
| `--limit` | 100 | Data count (max 100) |

### 5. liquidation - Liquidation Data

```bash
python scripts/cli.py liquidation <inst_id> [--state STATE] [--limit LIMIT]
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `inst_id` | (required) | Perpetual contract, e.g., "BTC-USDT-SWAP" |
| `--state` | filled | Order state: "filled" or "unfilled" |
| `--limit` | 100 | Data count (max 100) |

**Returns**: `datetime`, `side` (sell=long liquidated, buy=short liquidated), `bkPx`, `sz`

### 6. top-trader-ratio - Top Trader Position Ratio

Get the long/short position ratio of elite traders (top 5% by position value).

```bash
python scripts/cli.py top-trader-ratio <inst_id> [--period PERIOD] [--limit LIMIT]
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `inst_id` | (required) | Perpetual contract, e.g., "BTC-USDT-SWAP" |
| `--period` | 5m | Granularity: 5m, 15m, 30m, 1H, 2H, 4H, 6H, 12H, 1D |
| `--limit` | 100 | Data count (max 100) |

**Returns**: JSON array with `datetime`, `longShortPosRatio`

**Interpretation**:
- `> 1`: Top traders hold more long positions
- `< 1`: Top traders hold more short positions
- `= 1`: Equal long/short positions

### 7. option-ratio - Option Call/Put Ratio

```bash
python scripts/cli.py option-ratio <ccy> [--period PERIOD] [--limit LIMIT]
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `ccy` | (required) | Currency, e.g., "BTC", "ETH" |
| `--period` | 8H | Granularity: 8H or 1D |
| `--limit` | 100 | Data count (max 100) |

**Returns**: JSON array with `datetime`, `oiRatio`, `volRatio`

**Interpretation**:
- `oiRatio > 1`: More call options held (bullish sentiment)
- `oiRatio < 1`: More put options held (bearish sentiment)

### 8. fear-greed - Fear and Greed Index

```bash
python scripts/cli.py fear-greed [--days DAYS]
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--days` | 7 | Days of history |

**Returns**: JSON array with `date`, `value`, `value_classification`

**Interpretation**:
- `0-24`: Extreme Fear - Potential buying opportunity
- `25-49`: Fear
- `50-74`: Greed
- `75-100`: Extreme Greed - Potential selling signal

### 9. indicators - Complete Technical Indicators

Get all technical indicators for a trading pair.

```bash
python scripts/cli.py indicators <inst_id> [--bar BAR] [--limit LIMIT] [--last-n N]
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `inst_id` | (required) | Trading pair, e.g., "BTC-USDT" |
| `--bar` | 1D | K-line period |
| `--limit` | 100 | K-lines to fetch (max 100) |
| `--last-n` | 10 | Return only latest N rows (0 = all) |

**Returns**: JSON array with columns:
- Price: `open`, `high`, `low`, `close`, `volume`
- Moving Averages: `ma5`, `ma10`
- RSI: `rsi14`
- MACD: `macd_dif`, `macd_dea`, `macd_hist`

### 10. summary - Technical Analysis Summary

Get a quick summary of current price and key indicators.

```bash
python scripts/cli.py summary <inst_id> [--bar BAR] [--limit LIMIT]
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `inst_id` | (required) | Trading pair |
| `--bar` | 1D | K-line period |
| `--limit` | 100 | K-lines for calculation |

**Returns**: JSON object with `asset`, `indicators`, `data_summary`

### 11. support-resistance - Support and Resistance Levels

```bash
python scripts/cli.py support-resistance <inst_id> [--bar BAR] [--limit LIMIT] [--window N]
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `inst_id` | (required) | Trading pair |
| `--bar` | 1D | K-line period |
| `--limit` | 100 | K-lines |
| `--window` | 5 | Window for finding extrema |

**Returns**: JSON object with:
- `current_price`
- `support_levels`
- `resistance_levels`
- `fibonacci_retracement`
- `price_range`

---

## Supported Trading Pairs

| Code | Spot | Perpetual Contract |
|------|------|-------------------|
| BTC | BTC-USDT | BTC-USDT-SWAP |
| ETH | ETH-USDT | ETH-USDT-SWAP |
| BNB | BNB-USDT | BNB-USDT-SWAP |
| ZEC | ZEC-USDT | ZEC-USDT-SWAP |
| SOL | SOL-USDT | SOL-USDT-SWAP |
| XAU | - | XAU-USDT-SWAP |

---

## Usage Examples

```bash
# Get BTC 1-hour K-lines
python scripts/cli.py candles BTC-USDT --bar 1H --limit 100

# Get ETH funding rate
python scripts/cli.py funding-rate ETH-USDT-SWAP --limit 50

# Get BTC liquidation data
python scripts/cli.py liquidation BTC-USDT-SWAP --state filled --limit 100

# Get top trader position ratio
python scripts/cli.py top-trader-ratio BTC-USDT-SWAP --period 1H --limit 24

# Get option call/put ratio
python scripts/cli.py option-ratio BTC --period 8H --limit 10

# Get fear and greed index
python scripts/cli.py fear-greed --days 30

# Get technical indicators
python scripts/cli.py indicators BTC-USDT --bar 4H --last-n 5

# Get support and resistance levels
python scripts/cli.py support-resistance ETH-USDT --bar 1D
```

---

## Parameter Extraction Rules

| User Says | Extract As |
|-----------|------------|
| "BTC price", "Bitcoin" | inst_id = "BTC-USDT" |
| "ETH technical analysis", "Ethereum" | inst_id = "ETH-USDT" |
| "1-hour timeframe", "hourly chart" | bar = "1H" |
| "4-hour", "4H" | bar = "4H" |
| "daily chart", "daily level" | bar = "1D" |
| "weekly chart" | bar = "1W" |
| "funding rate", "funding" | Use funding-rate with SWAP contract |
| "open interest", "OI" | Use open-interest with SWAP contract |
| "long/short ratio" | Use long-short-ratio with CCY |
| "elite positions", "whale positions" | Use top-trader-ratio with SWAP |
| "option ratio", "call/put" | Use option-ratio with CCY |
| "fear and greed", "sentiment index" | Use fear-greed |

---

## Integration Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     SKILL.md (You Are Here)                 │
├─────────────────────────────────────────────────────────────┤
│  1. scripts/cli.py     →  Fetch raw market data and caculate indicators│
│  2. references/INDICATORS.md →  Signal interpretation       │
│  3. references/STRATEGY.md  →  Trade decision policy        │
└─────────────────────────────────────────────────────────────┘
```

**Workflow**:

1. **Fetch Data**: Use `python scripts/cli.py <command>`
2. **Calculate**: Indicators computed automatically by `indicators` command
3. **Interpret**: Reference `INDICATORS.md` for signal meaning
4. **Decide**: Follow `STRATEGY.md` for trade execution rules

