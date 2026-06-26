---
name: ai-model-team
category: trading
model: prediction
description: AI Model Team - Multi-model prediction system (Kronos + Chronos-2 + TimesFM + VADER) for OKX crypto and US stocks. Features error handling, retry logic, HTTP caching, unit tests, and correct data source routing (OKX for crypto, Yahoo Finance for stocks).
version: 2.9.0
---

# AI Model Team

Multi-model collaborative prediction system: Kronos + Chronos-2 + TimesFM + VADER FinBERT

## Models

- **Kronos-base**: K-line specialist (NeoQuasar)
- **Chronos-2**: Macro cycle prediction (Amazon)
- **TimesFM-2.5-200M**: General time series (Google)
- **VADER FinBERT**: Financial sentiment (<1s load)

## Supported Assets

| Type | Examples | Data Source |
|------|----------|-------------|
| Crypto | BTC, ETH, SOL | OKX API |
| US Stocks | NVDA, AAPL, MSFT | Yahoo Finance |

## Usage

```bash
# 4-model analysis
python scripts/model_team.py BTC-USDT-SWAP --models kronos,chronos-2,timesfm,finbert

# Run tests
python -m pytest tests/ -v
```

## Robustness

- Full error handling (Kronos, Chronos, TimesFM)
- Reddit API retry (3 retries, 429 handling)
- HTTP caching (lru_cache, 60s TTL)
- Yahoo Finance for US stocks
- Unit tests (pytest, 9 tests)
