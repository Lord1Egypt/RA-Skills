---
name: crypto-wave-scanner
description: Visual crypto futures wave scanner that detects optimal entry and exit points across 10 coins in real time. Scores each coin 0-6 using EMA9/21/50 stack, RSI momentum, volume confirmation, 1h trend, and MACD. Launches a live browser dashboard with candlestick charts, EMA overlays, RSI subplots, entry limit price, TP targets, and stop levels. Also includes a CLI scanner for terminal output. Use when trading crypto futures and needing to identify which coins are starting a wave (enter) vs exhausting a wave (exit). Supports Binance Futures public API — no authentication required for scanning.
---

# Crypto Wave Scanner

Detects crypto futures wave entries and exits using a 6-signal scoring system. Outputs a live browser dashboard (candlestick charts + indicators) and a CLI scanner.

## Quick Start

### Browser Dashboard (recommended)
```bash
# Start the local server
python3 scripts/serve.py

# Opens automatically at http://localhost:7890/wave-scanner.html
```

Dashboard auto-refreshes every 60 seconds. Filter by timeframe (5m/15m/1h/4h) and minimum score.

### CLI Scanner
```bash
python3 scripts/wave_scanner.py
python3 scripts/wave_scanner.py --min-score 5          # strong setups only
python3 scripts/wave_scanner.py --symbols BTC ETH SOL  # specific coins
```

## Scoring System (0-6)

Each coin is scored on 6 signals:

| # | Signal | Bullish Condition |
|---|--------|-------------------|
| 1 | EMA Stack | EMA9 > EMA21 > EMA50 |
| 2 | RSI Zone | RSI 50–80 (sweet spot) |
| 3 | RSI Direction | RSI rising vs previous candle |
| 4 | Volume | Last candle volume > 1.3× 10-candle avg |
| 5 | 1H Trend | EMA9 > EMA21 on 1h chart |
| 6 | MACD | MACD histogram positive |

**Grades:** 5-6 = 🔥 STRONG SETUP · 4 = ✅ VALID · 3 = ⚠️ WEAK · <3 = ❌ SKIP

## Entry / Exit Rules

**Enter when:** Score ≥ 5 AND RSI 50-75. Place LIMIT order at EMA9 level (shown in dashboard).

**Skip when:** RSI > 85 (wave mature). RSI > 88 = do not add longs.

**Exit when (any one):**
- EMA9 crosses below EMA21
- RSI > 85 AND price closes below EMA9
- Volume drops for 3 consecutive candles on new highs
- Large bearish engulfing candle

## Assets

- `assets/wave-scanner.html` — self-contained browser dashboard (TradingView Lightweight Charts)
- `scripts/wave_scanner.py` — CLI scanner with full signal breakdown
- `scripts/serve.py` — local HTTP server launcher

## Data Source

Uses public Binance Futures API (`https://fapi.binance.com`) — no API key needed for scanning.
For testnet trading with the Binance Futures Testnet, swap base URL to `https://testnet.binancefuture.com`.

## Coins Scanned by Default

BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, BNBUSDT, AVAXUSDT, LINKUSDT, DOGEUSDT, LTCUSDT, DOTUSDT
