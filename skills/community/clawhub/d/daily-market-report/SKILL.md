---
name: daily-market-report
description: Generate daily US stock market analysis reports for user holdings, including portfolio P&L, 52-week range, analyst ratings, and actionable suggestions. Data sourced from Yahoo Finance (yfinance, no API key required).
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    install:
      - kind: uv
        packages:
          - yfinance
    os:
      - windows
      - linux
      - darwin
---

# Daily Market Report

A Python-based skill that generates a daily US stock market analysis report covering your portfolio holdings, market indices, and actionable suggestions.

## How It Works

The skill uses Yahoo Finance (via `yfinance`) — **no API key required**. It reads your current holdings from `HOLDINGS` config in the script, fetches live/recent market data, and prints a formatted report.

## Holdings Configuration

Edit the `HOLDINGS` dict in `scripts/get_market_data.py` to match your portfolio:

```python
HOLDINGS = {
    "BMI": {"name": "Badger Meter", "cost": 123.0, "shares": None},
    "PDD": {"name": "PDD Holdings", "cost": 110.0, "shares": None},
}
```

Supported tickers: any valid Yahoo Finance symbol (US stocks, ETFs, crypto, forex).

## Setup

### 1. Install uv (Python package manager)

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Homebrew (macOS):**
```bash
brew install uv
```

**pip:**
```bash
pip install uv
```

### 2. Verify yfinance is installed

```bash
uv pip install yfinance
# or
pip install yfinance
```

## Usage

Run the report generator directly:

```bash
python scripts/get_market_data.py
```

### Sample Output

```
============================================================
  Daily US Stock Report
  2026-05-28 15:00 (Weekend - data from last Friday)
============================================================

=== Market Overview ===

  Nasdaq QQQ: $478.32  +2.15 (+0.45%)
  ...

=== Holdings Analysis ===

  BMI (Badger Meter)
     Price: $119.50 | Cost: $123.00
     P&L: -$3.50 (-2.85%)
     52W Range: $256.08 / $112.09
     Analysts: Buy=16 Hold=1 Sell=1

  PDD (PDD Holdings)
     Price: $95.83 | Cost: $110.00
     P&L: -$14.17 (-12.88%)
     52W Range: $139.41 / $93.81
     Market Cap: $128.45B
     PE: 10.23
     ...
```

## Market Indices Tracked

The script tracks these indices by default:
- **QQQ** — Nasdaq 100 ETF
- **DIA** — Dow Jones ETF
- **SPY** — S&P 500 ETF

Edit the `INDICES` dict in `scripts/get_market_data.py` to customize.

## Data Points Retrieved

| Field | Description |
|-------|-------------|
| Price & Change | Current price, daily change ($ and %) |
| 52-Week Range | High / Low with distance from current price |
| Market Cap | Formatted (T/B/M) |
| PE Ratio | Trailing P/E |
| Beta | Stock beta vs market |
| Analyst Ratings | Buy / Hold / Sell / Strong Buy / Strong Sell counts |

## Requirements

- Python 3.8+
- `yfinance` library
- `uv` package manager (recommended, or plain `pip`)

## Troubleshooting

### "Module not found: yfinance"
Run: `uv pip install yfinance` (or `pip install yfinance`)

### Rate limiting
Yahoo Finance may throttle rapid consecutive requests. The script includes a 3-retry mechanism with 2-second delays. Wait a few minutes if rate-limited.

### No data for a symbol
Verify the ticker is valid on Yahoo Finance: `yf ticker` should return data on the Yahoo Finance website.

## License

Published on ClawHub under MIT-0 license.