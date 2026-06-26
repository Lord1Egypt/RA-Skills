# Alpaca REST API Reference

All endpoints use `alpaca.sh` wrapper: `alpaca METHOD PATH [JSON_BODY]`.
For market data endpoints, prefix with `ALPACA_DATA=1`.

## Trading API (`/v2`)

### Account

```bash
# Get account info (balance, buying power, equity, status, options level)
alpaca GET /v2/account

# Get/update account config (fractional trading, margin, PDT check, etc.)
alpaca GET /v2/account/configurations
alpaca PATCH /v2/account/configurations '{"dtbp_check":"both","fractional_trading":true,"max_options_trading_level":2}'

# Portfolio history
alpaca GET '/v2/account/portfolio/history?period=1M&timeframe=1D'
# period: 1D, 1W, 1M, 3M, 6M, 1A, all  |  timeframe: 1Min, 5Min, 15Min, 1H, 1D
```

### Account Activities

```bash
# All activities
alpaca GET /v2/account/activities

# Filter by type (FILL, DIV, CSD, TRANS, OPTEXP, OPTASN, OPTEXT)
alpaca GET '/v2/account/activities?activity_types=FILL,DIV'

# Paginate
alpaca GET '/v2/account/activities?activity_types=FILL&after=2026-03-01&direction=desc&page_size=50'

# Activity types:
#   FILL     — order fill
#   DIV      — dividend
#   TRANS    — fund transfer (ACH/wire)
#   CSD      — cash deposit
#   CSW      — cash withdrawal
#   OPTEXP   — option expiration
#   OPTASN   — option assignment
#   OPTEXT   — option exercise
#   SPIN     — spinoff
#   SPLIT    — stock split
#   MA       — merger/acquisition
```

### Orders — Equities & Crypto

```bash
# Market order (by qty)
alpaca POST /v2/orders '{"symbol":"AAPL","qty":"10","side":"buy","type":"market","time_in_force":"day"}'

# Market order (by dollar amount — fractional)
alpaca POST /v2/orders '{"symbol":"AAPL","notional":"1000","side":"buy","type":"market","time_in_force":"day"}'

# Limit order
alpaca POST /v2/orders '{"symbol":"AAPL","qty":"10","side":"buy","type":"limit","limit_price":"185.00","time_in_force":"gtc"}'

# Stop order
alpaca POST /v2/orders '{"symbol":"AAPL","qty":"10","side":"sell","type":"stop","stop_price":"180.00","time_in_force":"day"}'

# Stop-limit order
alpaca POST /v2/orders '{"symbol":"AAPL","qty":"10","side":"sell","type":"stop_limit","stop_price":"180.00","limit_price":"179.00","time_in_force":"day"}'

# Trailing stop (percent)
alpaca POST /v2/orders '{"symbol":"AAPL","qty":"10","side":"sell","type":"trailing_stop","trail_percent":"5","time_in_force":"gtc"}'

# Trailing stop (dollar)
alpaca POST /v2/orders '{"symbol":"AAPL","qty":"10","side":"sell","type":"trailing_stop","trail_price":"10.00","time_in_force":"gtc"}'

# Bracket order (entry + take-profit + stop-loss)
alpaca POST /v2/orders '{
  "symbol":"AAPL","qty":"10","side":"buy","type":"market","time_in_force":"day",
  "order_class":"bracket",
  "take_profit":{"limit_price":"200.00"},
  "stop_loss":{"stop_price":"175.00","limit_price":"174.00"}
}'

# OTO (one-triggers-other)
alpaca POST /v2/orders '{
  "symbol":"AAPL","qty":"10","side":"buy","type":"limit","limit_price":"185.00","time_in_force":"day",
  "order_class":"oto",
  "stop_loss":{"stop_price":"175.00"}
}'

# OCO (one-cancels-other)
alpaca POST /v2/orders '{
  "symbol":"AAPL","qty":"10","side":"sell","type":"limit","limit_price":"200.00","time_in_force":"day",
  "order_class":"oco",
  "stop_loss":{"stop_price":"175.00"}
}'

# Extended hours (limit orders only)
alpaca POST /v2/orders '{"symbol":"AAPL","qty":"5","side":"buy","type":"limit","limit_price":"250.00","time_in_force":"day","extended_hours":true}'

# Crypto order (24/7, same endpoint)
alpaca POST /v2/orders '{"symbol":"BTC/USD","qty":"0.001","side":"buy","type":"market","time_in_force":"gtc"}'

# List orders (default: open)
alpaca GET /v2/orders
alpaca GET '/v2/orders?status=all&limit=50&direction=desc'
alpaca GET '/v2/orders?status=closed&after=2026-03-01&until=2026-03-15'
# status: open, closed, all

# Get order by ID
alpaca GET /v2/orders/ORDER_ID

# Get order by client order ID
alpaca GET '/v2/orders:by_client_order_id?client_order_id=MY_ID'

# Replace (modify) order
alpaca PATCH /v2/orders/ORDER_ID '{"qty":"20","limit_price":"190.00"}'

# Cancel order
alpaca DELETE /v2/orders/ORDER_ID

# Cancel ALL open orders
alpaca DELETE /v2/orders
```

#### Order fields reference

| Field | Values |
|-------|--------|
| `side` | `buy`, `sell` |
| `type` | `market`, `limit`, `stop`, `stop_limit`, `trailing_stop` |
| `time_in_force` | `day`, `gtc`, `opg`, `cls`, `ioc`, `fok` |
| `order_class` | (empty for simple), `bracket`, `oco`, `oto` |
| `extended_hours` | `true` for extended hours (limit orders only) |
| `position_intent` | `buy_to_open`, `buy_to_close`, `sell_to_open`, `sell_to_close` (options) |

### Orders — Options

Options use the same `/v2/orders` endpoint with contract symbols.

```bash
# Buy a call (Level 2+)
alpaca POST /v2/orders '{"symbol":"AAPL260418C00260000","qty":"1","side":"buy","type":"market","time_in_force":"day"}'

# Buy a put (Level 2+)
alpaca POST /v2/orders '{"symbol":"AAPL260418P00240000","qty":"1","side":"buy","type":"limit","limit_price":"3.50","time_in_force":"day"}'

# Sell covered call (Level 1+, must own 100 shares per contract)
alpaca POST /v2/orders '{"symbol":"AAPL260418C00270000","qty":"1","side":"sell","type":"limit","limit_price":"2.00","time_in_force":"day"}'

# Sell cash-secured put (Level 1+)
alpaca POST /v2/orders '{"symbol":"AAPL260418P00230000","qty":"1","side":"sell","type":"limit","limit_price":"1.50","time_in_force":"day"}'

# Close an option position (sell to close)
alpaca POST /v2/orders '{"symbol":"NVDA260417C00220000","qty":"1","side":"sell","type":"limit","limit_price":"0.44","time_in_force":"gtc","position_intent":"sell_to_close"}'

# Multi-leg spread orders (Level 3) — use order_class
# Buy call spread
alpaca POST /v2/orders '{
  "symbol":"AAPL260418C00260000","qty":"1","side":"buy","type":"limit","limit_price":"2.00","time_in_force":"day",
  "order_class":"oco",
  "legs":[
    {"symbol":"AAPL260418C00260000","side":"buy","qty":"1"},
    {"symbol":"AAPL260418C00270000","side":"sell","qty":"1"}
  ]
}'
```

#### Options trading levels

| Level | Supported Trades |
|-------|-----------------|
| 0 | Options disabled |
| 1 | Covered calls, cash-secured puts |
| 2 | Level 1 + buy calls, buy puts |
| 3 | Level 1-2 + call/put spreads |

#### Options validation rules

- `qty` must be whole number (no fractional)
- `notional` must NOT be set
- `time_in_force` must be `day` or `gtc`
- `extended_hours` must be `false` or omitted
- `type` must be `market`, `limit`, `stop`, or `stop_limit` (stop/stop_limit only for single-leg)

### Options — Exercise & Contract Lookup

```bash
# Exercise an option position (all held contracts)
alpaca POST /v2/positions/AAPL260418C00260000/exercise

# List option contracts for underlying
alpaca GET '/v2/options/contracts?underlying_symbols=AAPL&expiration_date_gte=2026-04-01&type=call&limit=10'
alpaca GET '/v2/options/contracts?underlying_symbols=AAPL&expiration_date_gte=2026-04-01&expiration_date_lte=2026-06-30&strike_price_gte=240&strike_price_lte=280'

# Get single contract by symbol or ID
alpaca GET /v2/options/contracts/AAPL260418C00260000
alpaca GET /v2/options/contracts/CONTRACT_ID

# Query params for /v2/options/contracts:
#   underlying_symbols  — comma-separated (e.g. AAPL,MSFT)
#   expiration_date_gte — min expiration (YYYY-MM-DD)
#   expiration_date_lte — max expiration
#   strike_price_gte    — min strike
#   strike_price_lte    — max strike
#   type                — call or put
#   style               — american or european
#   status              — active or inactive
#   limit               — max results (default 100)
#   page_token          — pagination
```

### Positions

```bash
# List all open positions
alpaca GET /v2/positions

# List positions by asset class
alpaca GET '/v2/positions?asset_class=us_option'
alpaca GET '/v2/positions?asset_class=crypto'

# Get position for symbol
alpaca GET /v2/positions/AAPL

# Get option position
alpaca GET /v2/positions/NVDA260417C00220000

# Close a position (market sell all)
alpaca DELETE /v2/positions/AAPL
# Close partial (by qty)
alpaca DELETE '/v2/positions/AAPL?qty=5'
# Close partial (by percentage)
alpaca DELETE '/v2/positions/AAPL?percentage=50'

# Close ALL positions
alpaca DELETE '/v2/positions?cancel_orders=true'
```

### Assets

```bash
# List tradeable assets
alpaca GET '/v2/assets?status=active&asset_class=us_equity'
alpaca GET '/v2/assets?status=active&asset_class=crypto'

# Find options-enabled assets
alpaca GET '/v2/assets?status=active&attributes=has_options'

# Get asset by symbol
alpaca GET /v2/assets/AAPL
alpaca GET /v2/assets/BTC/USD
```

### Market Clock & Calendar

```bash
# Market clock (open/closed, next open/close)
alpaca GET /v2/clock

# Trading calendar (trading days with session hours)
alpaca GET '/v2/calendar?start=2026-03-01&end=2026-03-31'
```

### Watchlists

```bash
# List watchlists
alpaca GET /v2/watchlists

# Create watchlist
alpaca POST /v2/watchlists '{"name":"Tech","symbols":["AAPL","MSFT","GOOGL","NVDA"]}'

# Get watchlist
alpaca GET /v2/watchlists/WATCHLIST_ID

# Update watchlist (full replace)
alpaca PUT /v2/watchlists/WATCHLIST_ID '{"name":"Tech Leaders","symbols":["AAPL","MSFT","GOOGL","NVDA","META"]}'

# Add symbol to watchlist
alpaca POST /v2/watchlists/WATCHLIST_ID '{"symbol":"AMZN"}'

# Remove symbol from watchlist
alpaca DELETE /v2/watchlists/WATCHLIST_ID/SYMBOL

# Delete watchlist
alpaca DELETE /v2/watchlists/WATCHLIST_ID
```

---

## Market Data API

Prefix all commands with `ALPACA_DATA=1`.

### Stock Data

```bash
# Latest quote
ALPACA_DATA=1 alpaca GET /v2/stocks/AAPL/quotes/latest

# Latest trade
ALPACA_DATA=1 alpaca GET /v2/stocks/AAPL/trades/latest

# Snapshot (quote + trade + bar + prev close)
ALPACA_DATA=1 alpaca GET /v2/stocks/AAPL/snapshot

# Multi-snapshot
ALPACA_DATA=1 alpaca GET '/v2/stocks/snapshots?symbols=AAPL,MSFT,GOOGL'

# Historical bars
ALPACA_DATA=1 alpaca GET '/v2/stocks/AAPL/bars?timeframe=1Day&start=2026-03-01&end=2026-03-15&limit=50'
# timeframe: 1Min, 5Min, 15Min, 30Min, 1Hour, 1Day, 1Week, 1Month

# Multi-stock bars
ALPACA_DATA=1 alpaca GET '/v2/stocks/bars?symbols=AAPL,MSFT&timeframe=1Day&start=2026-03-01&limit=10'

# Historical trades
ALPACA_DATA=1 alpaca GET '/v2/stocks/AAPL/trades?start=2026-03-15&limit=100'

# Historical quotes
ALPACA_DATA=1 alpaca GET '/v2/stocks/AAPL/quotes?start=2026-03-15&limit=100'

# Auctions (open/close)
ALPACA_DATA=1 alpaca GET '/v2/stocks/AAPL/auctions?start=2026-03-01&limit=10'

# Conditions/exchange codes
ALPACA_DATA=1 alpaca GET '/v2/stocks/meta/conditions/trade'
ALPACA_DATA=1 alpaca GET '/v2/stocks/meta/exchanges'
```

### Options Data

```bash
# Option chain snapshot (all contracts for underlying)
ALPACA_DATA=1 alpaca GET '/v1beta1/options/snapshots/AAPL?feed=indicative&limit=10'

# Option bars (historical OHLCV)
ALPACA_DATA=1 alpaca GET '/v1beta1/options/bars?symbols=NVDA260417C00220000&timeframe=1Day&limit=10'

# Latest option trade
ALPACA_DATA=1 alpaca GET '/v1beta1/options/trades/latest?symbols=NVDA260417C00220000'

# Latest option quote
ALPACA_DATA=1 alpaca GET '/v1beta1/options/quotes/latest?symbols=NVDA260417C00220000'

# Option snapshot (single contract — quote + trade + greeks)
ALPACA_DATA=1 alpaca GET '/v1beta1/options/snapshots?symbols=NVDA260417C00220000&feed=indicative'

# Feed options: indicative (free, delayed), opra (requires subscription)
```

### Crypto Data

```bash
# Latest crypto quote
ALPACA_DATA=1 alpaca GET '/v1beta3/crypto/us/latest/quotes?symbols=BTC/USD'

# Latest crypto trade
ALPACA_DATA=1 alpaca GET '/v1beta3/crypto/us/latest/trades?symbols=BTC/USD'

# Crypto bars
ALPACA_DATA=1 alpaca GET '/v1beta3/crypto/us/bars?symbols=BTC/USD&timeframe=1Day&limit=30'

# Crypto snapshot
ALPACA_DATA=1 alpaca GET '/v1beta3/crypto/us/snapshots?symbols=BTC/USD,ETH/USD'

# Available crypto pairs
# Common pairs: BTC/USD, ETH/USD, SOL/USD, DOGE/USD, AVAX/USD, LINK/USD, etc.
```

### News

```bash
# Latest news
ALPACA_DATA=1 alpaca GET '/v1beta1/news?limit=10'

# News for symbol(s)
ALPACA_DATA=1 alpaca GET '/v1beta1/news?symbols=AAPL,TSLA&limit=10'

# News with date range
ALPACA_DATA=1 alpaca GET '/v1beta1/news?start=2026-03-01&end=2026-03-15&limit=50'
```

### Screener

```bash
# Most active stocks
ALPACA_DATA=1 alpaca GET /v1beta1/screener/stocks/most-actives
ALPACA_DATA=1 alpaca GET '/v1beta1/screener/stocks/most-actives?top=20'

# Top movers (gainers/losers by % change)
ALPACA_DATA=1 alpaca GET '/v1beta1/screener/stocks/movers?top=10'
```

### Corporate Actions

```bash
# Corporate actions for symbol(s)
ALPACA_DATA=1 alpaca GET '/v1/corporate-actions?symbols=AAPL&types=cash_dividend'

# Types: forward_split, reverse_split, stock_dividend, spin_off,
#   cash_merger, stock_merger, stock_and_cash_merger, unit_split,
#   cash_dividend, redemption, name_change, worthless_removal,
#   rights_distribution, contract_adjustment, partial_call

# Date range
ALPACA_DATA=1 alpaca GET '/v1/corporate-actions?symbols=AAPL,MSFT&types=cash_dividend,forward_split&ca_on_or_after=2025-01-01&ca_on_or_before=2026-03-31'
```
