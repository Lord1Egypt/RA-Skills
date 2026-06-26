---
name: eagerbots-stock-quote
description: "Get real-time stock, ETF, and crypto prices. Compare tickers, check market cap and volume. Uses Yahoo Finance — no API key required."
version: 1.0.0
metadata:
  openclaw:
    emoji: "📈"
  requires:
    bins:
      - python3
  homepage: https://github.com/josephflu/clawhub-skills
---

# stock-quote

Get real-time stock, ETF, and crypto prices via Yahoo Finance — no API key needed.

## Trigger phrases

- "What's Apple stock at?"
- "What's the price of TSLA?"
- "How is NVDA doing today?"
- "Compare AAPL MSFT GOOG"
- "What's BTC at?"
- "Show me SPY and QQQ"
- "Is the market up today?"
- "How's the market doing?"
- "Quote for [TICKER]"

## Usage

Run `uv run scripts/quote.py` with one or more ticker symbols:

```bash
# Single ticker
uv run scripts/quote.py AAPL

# Crypto
uv run scripts/quote.py BTC-USD

# Multiple tickers (comparison table)
uv run scripts/quote.py AAPL MSFT GOOG NVDA

# Detailed view
uv run scripts/quote.py AAPL --detail
```

## Output

**Single ticker:**
```
╭─────────────────────────────────────────╮
│ 🍎 Apple Inc. (AAPL) NASDAQ            │
│ $213.49 ▲ +2.31 (+1.09%) ● Market Open │
├─────────────────────────────────────────┤
│ 52W Range $164.08 ──────●──── $237.23  │
│ Volume 45.2M (avg 52.1M)               │
│ Market Cap $3.21T                       │
╰─────────────────────────────────────────╯
```

**Multiple tickers:** Rich comparison table with Ticker, Name, Price, Change, % Change, Market Cap — green for gains, red for losses.

## Notes

- Uses Yahoo Finance's unofficial API (free, no key required)
- Crypto tickers use `-USD` suffix: `BTC-USD`, `ETH-USD`, `SOL-USD`
- See `references/common-tickers.md` for popular symbols
- Market status (open/closed) shown automatically
