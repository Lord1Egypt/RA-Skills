---
name: anchored-vwap-scalper
description: Production single-skill BTC scalper on Lighter DEX with FULL explicit Python strategy engine + accurate incremental Anchored VWAP. 4 strategies, 1% risk, fixed SL + TP. BTC-USD default.
version: 1.6.0
metadata:
  requires:
    env:
      - LIGHTER_API_PRIVATE_KEY
      - LIGHTER_API_KEY_INDEX
      - LIGHTER_ACCOUNT_INDEX
      - SCALPER_SYMBOL          # defaults to BTC-USD
      - SCALPER_TIMEFRAME       # defaults to 5m
      - DRY_RUN                 # true/false
    mcp:
      - ccxt-mcp
    bins:
      - python3
  install:
    - id: ccxt-mcp
---

# Anchored VWAP BTC Scalper for Lighter DEX (Production v1.6)

**Configured for BTC-USD** (daily UTC anchor). All logic lives in `scripts/strategy_engine.py`.

**Workflow:**
1. Set env vars (especially `DRY_RUN=true` first!)
2. `initialize-scalper` (uses BTC-USD by default)
3. `start-scalping`

**Commands:** `status`, `pause`, `set-anchor <ISO-timestamp>`

Start in dry-run mode. This is now 100% production-ready for BTC scalping on Lighter (fixed SL only).