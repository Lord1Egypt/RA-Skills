---
name: finance-radar
description: >
  Stock and cryptocurrency analysis powered by Yahoo Finance data. Use when a user wants to:
  (1) Analyze stocks or crypto prices/fundamentals, (2) Track investment portfolios,
  (3) Monitor watchlists with alerts, (4) Analyze dividends, (5) Score stocks on 8 dimensions,
  (6) Detect viral trending tickers (hot scanner), (7) Spot rumors and early signals before mainstream,
  (8) Check earnings reactions, (9) Find trending stocks or crypto.
  Integrates SkillPay.me billing at 0.001 USDT per call.
---

# Finance Radar

Stock & crypto intelligence via Yahoo Finance. Charges 0.001 USDT/call via SkillPay.

## Commands

| Command | Script | Description |
|:---|:---|:---|
| **analyze** | `scripts/analyze.py` | Stock/crypto analysis (price, fundamentals, technicals) |
| **score** | `scripts/score.py` | 8-dimension stock scoring |
| **batch** | `scripts/batch.py` | Batch analyze multiple tickers + CSV export |
| **portfolio** | `scripts/portfolio.py` | Portfolio tracking & P/L |
| **watchlist** | `scripts/watchlist.py` | Watchlist with price alerts |
| **dividend** | `scripts/dividend.py` | Dividend yield & history |
| **hot-scan** | `scripts/hot_scan.py` | Viral trend detection |
| **rumor** | `scripts/rumor.py` | Rumor & early signal detection |
| **billing** | `scripts/billing.py` | SkillPay charge/balance/payment |

## Workflow

```
1. Billing:  python3 scripts/billing.py --charge --user-id <id>
2. Execute:  python3 scripts/<command>.py --ticker AAPL
```

## Quick Examples

```bash
# Analyze a stock
python3 scripts/analyze.py --ticker AAPL

# Analyze crypto
python3 scripts/analyze.py --ticker BTC-USD

# Batch analyze (NEW)
python3 scripts/batch.py --tickers AAPL,GOOG,MSFT
python3 scripts/batch.py --tickers AAPL,GOOG,MSFT --export  # Export CSV

# 8-dimension score
python3 scripts/score.py --ticker TSLA
```

## Config

| Env Var | Required | Description |
|:---|:---:|:---|
| `SKILLPAY_API_KEY` | Yes | SkillPay.me API key |

## References

See `references/scoring-model.md` for 8-dimension scoring methodology.
