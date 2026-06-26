---
name: alpaca-trading
description: >-
  Trade stocks, ETFs, options, and crypto via Alpaca's REST API using curl.
  Full options support (buy/sell calls & puts, covered calls, cash-secured puts,
  spreads, exercise, contract lookup, option chain data). Manage orders,
  positions, watchlists, account activities, and portfolio history. Access
  real-time and historical market data for stocks, options, and crypto including
  quotes, bars, snapshots, news, screener (most active, top movers), and
  corporate actions. Use when the user mentions "buy," "sell," "trade,"
  "options," "call," "put," "market data," "stock price," "stock quote,"
  "portfolio," "account balance," "positions," "orders," "alpaca," "market
  clock," "watchlist," "top movers," "most active," or any stock/crypto/options
  trading task. No external CLI binary required — uses curl + jq directly.
---

# Alpaca Trading Skill

Trade and manage portfolios via Alpaca's REST API using `scripts/alpaca.sh`.

## Setup

### Required env vars

| Variable | Purpose |
|----------|---------|
| `APCA_API_KEY_ID` | Alpaca API key |
| `APCA_API_SECRET_KEY` | Alpaca API secret |

### Optional env vars

| Variable | Default | Purpose |
|----------|---------|---------|
| `APCA_API_BASE_URL` | `https://paper-api.alpaca.markets` | Trading endpoint. Set to `https://api.alpaca.markets` for live |
| `APCA_DATA_API_BASE_URL` | `https://data.alpaca.markets` | Market data endpoint |

**Paper trading is the default.** Always confirm with the user before switching to live.

### Helper script

Source `scripts/alpaca.sh` from this skill directory. Usage:

```bash
alpaca METHOD PATH [JSON_BODY]
# Market data:
ALPACA_DATA=1 alpaca METHOD PATH
```

## Quick Reference

### Account & portfolio

```bash
alpaca GET /v2/account                                          # balance, equity, buying power
alpaca GET /v2/account/configurations                           # trading config
alpaca GET '/v2/account/portfolio/history?period=1M&timeframe=1D'  # portfolio chart
alpaca GET '/v2/account/activities?activity_types=FILL,DIV'     # trade/dividend history
alpaca GET /v2/clock                                            # market open/closed
alpaca GET '/v2/calendar?start=2026-03-01&end=2026-03-31'       # trading days
```

### Orders — Equities & Crypto

```bash
# Market buy (by qty or dollar amount)
alpaca POST /v2/orders '{"symbol":"AAPL","qty":"10","side":"buy","type":"market","time_in_force":"day"}'
alpaca POST /v2/orders '{"symbol":"AAPL","notional":"1000","side":"buy","type":"market","time_in_force":"day"}'

# Crypto (24/7)
alpaca POST /v2/orders '{"symbol":"BTC/USD","qty":"0.001","side":"buy","type":"market","time_in_force":"gtc"}'

# Limit / stop / stop-limit / trailing stop / bracket / OTO / OCO — see references/api.md

# List / get / replace / cancel
alpaca GET /v2/orders
alpaca GET /v2/orders/ORDER_ID
alpaca PATCH /v2/orders/ORDER_ID '{"qty":"20","limit_price":"190.00"}'
alpaca DELETE /v2/orders/ORDER_ID
alpaca DELETE /v2/orders                                        # cancel ALL
```

### Orders — Options

```bash
# Buy call (Level 2+)
alpaca POST /v2/orders '{"symbol":"AAPL260418C00260000","qty":"1","side":"buy","type":"market","time_in_force":"day"}'

# Sell covered call (Level 1+, must own 100 shares per contract)
alpaca POST /v2/orders '{"symbol":"AAPL260418C00270000","qty":"1","side":"sell","type":"limit","limit_price":"2.00","time_in_force":"day"}'

# Buy/sell puts, cash-secured puts, spreads (Level 3) — see references/api.md

# Exercise option
alpaca POST /v2/positions/AAPL260418C00260000/exercise

# Look up contracts
alpaca GET '/v2/options/contracts?underlying_symbols=AAPL&expiration_date_gte=2026-04-01&type=call&limit=10'
alpaca GET /v2/options/contracts/AAPL260418C00260000
```

### Positions

```bash
alpaca GET /v2/positions                                        # all open
alpaca GET '/v2/positions?asset_class=us_option'                # options only
alpaca GET /v2/positions/AAPL                                   # single equity
alpaca GET /v2/positions/NVDA260417C00220000                     # single option
alpaca DELETE /v2/positions/AAPL                                # close
alpaca DELETE '/v2/positions/AAPL?qty=5'                        # close partial
alpaca DELETE '/v2/positions?cancel_orders=true'                # close ALL
```

### Market data — Stocks

```bash
ALPACA_DATA=1 alpaca GET /v2/stocks/AAPL/snapshot               # quote + trade + bar
ALPACA_DATA=1 alpaca GET '/v2/stocks/snapshots?symbols=AAPL,MSFT,GOOGL'  # multi-snapshot
ALPACA_DATA=1 alpaca GET '/v2/stocks/AAPL/bars?timeframe=1Day&start=2026-03-01&limit=30'
ALPACA_DATA=1 alpaca GET /v1beta1/screener/stocks/most-actives
ALPACA_DATA=1 alpaca GET '/v1beta1/screener/stocks/movers?top=10'
ALPACA_DATA=1 alpaca GET '/v1beta1/news?symbols=AAPL&limit=5'
```

### Market data — Options

```bash
ALPACA_DATA=1 alpaca GET '/v1beta1/options/snapshots/AAPL?feed=indicative&limit=10'  # option chain
ALPACA_DATA=1 alpaca GET '/v1beta1/options/bars?symbols=NVDA260417C00220000&timeframe=1Day&limit=10'
ALPACA_DATA=1 alpaca GET '/v1beta1/options/quotes/latest?symbols=NVDA260417C00220000'
ALPACA_DATA=1 alpaca GET '/v1beta1/options/trades/latest?symbols=NVDA260417C00220000'
# feed: indicative (free/delayed) or opra (subscription required)
```

### Market data — Crypto

```bash
ALPACA_DATA=1 alpaca GET '/v1beta3/crypto/us/latest/quotes?symbols=BTC/USD'
ALPACA_DATA=1 alpaca GET '/v1beta3/crypto/us/bars?symbols=BTC/USD&timeframe=1Day&limit=30'
ALPACA_DATA=1 alpaca GET '/v1beta3/crypto/us/snapshots?symbols=BTC/USD,ETH/USD'
```

### Corporate Actions

```bash
ALPACA_DATA=1 alpaca GET '/v1/corporate-actions?symbols=AAPL&types=cash_dividend'
# Types: forward_split, reverse_split, cash_dividend, stock_dividend, spin_off, etc.
```

### Assets & Watchlists

```bash
alpaca GET /v2/assets/AAPL                                      # asset info
alpaca GET '/v2/assets?status=active&attributes=has_options'     # options-enabled stocks
alpaca GET /v2/watchlists                                       # list watchlists
alpaca POST /v2/watchlists '{"name":"Tech","symbols":["AAPL","MSFT","GOOGL"]}'
```

## Full API reference

Read `references/api.md` for complete endpoint documentation including:
- All order types (limit, stop, stop-limit, trailing stop, bracket, OCO, OTO)
- Order field reference (side, type, time_in_force, order_class)
- Watchlist CRUD
- Options contracts
- Historical bars/trades/quotes with all query params
- Crypto endpoints
- Market calendar

## Safety Rules

1. **Default to paper trading.** Never set `APCA_API_BASE_URL` to live without explicit user confirmation.
2. **Show the order JSON before submitting.** Let the user confirm symbol, qty, side, and type.
3. **Check market clock** before placing orders — stocks only trade during market hours (9:30-16:00 ET) unless `extended_hours: true` on limit orders.
4. **Verify buying power** via `GET /v2/account` before large orders.
5. **Never provide financial advice.** Present data; let the user decide.
6. **Warn about irreversible actions** — closing all positions, canceling all orders.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `HTTP 401` | Check `APCA_API_KEY_ID` / `APCA_API_SECRET_KEY` are set and valid |
| `HTTP 403` | Paper keys on live URL or vice versa; check `APCA_API_BASE_URL` |
| `HTTP 422` (insufficient qty) | Check buying power, fractional support, or symbol validity |
| `HTTP 429` | Rate limited — wait and retry; Alpaca allows 200 req/min |
| Order rejected outside hours | Add `"extended_hours":true` (limit orders only) or wait for market open |
| `jq: command not found` | Script falls back to `python3 -m json.tool`; install jq for better output |
