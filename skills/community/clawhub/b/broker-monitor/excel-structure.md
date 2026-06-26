# Excel Database Structure — 券商监控数据库.xlsx

## Sheet Structure (16 sheets)

### 0-3. Derived Metric Time-Series (4 sheets, one per broker)

Each derived sheet is a **time-series table** — new rows are appended each update, never overwritten. This preserves full history.

#### IBKR衍生 (Monthly)
| Col | Field | Type | Formula |
|-----|-------|------|---------|
| A | 月份 | Key | YYYY-MM |
| B-G | Raw: DARTs, 账户, 权益, 保证金, 信用余额, 季度收入 | 原始值 | From IBKR monthly sheet |
| H | AUC/户($K) | 📐计算 | =D/C*100 (权益÷账户×100) |
| I | ARPU($/yr) | 📐计算 | =G*400/C (季度收入×400÷账户) |
| J | 杠杆率(%) | 📐计算 | =E/D*100 (保证金÷权益×100) |
| K | 每户DART | 📐计算 | =B/C*252 |
| L-N | MoM% | 📈增长 | =(本行-上行)/上行 for H,I,J |
| O-Q | YoY% | 📈增长 | =(本行-12行前)/12行前 for H,I,J |
| R | 数据来源 | text | |

#### SCHW衍生 (Monthly)
Same pattern. Derived: AUC/户, ARPU, 杠杆率(‰, permille), 现金/资产(%).

#### HOOD衍生 (Monthly)
Derived: AUC/户, Gold订阅率(%), Net Dep增速(%). ARPU is company-disclosed (quarterly update only).

#### FUTU衍生 (Quarterly)
Derived: AUC/户, ARPU, 净利率(%). Growth: QoQ% and YoY% (4 quarters back).

**Key rules for derived sheets:**
- ALWAYS append new rows, never delete old ones
- Raw data columns are copied from the corresponding raw data sheet
- Derived columns use Excel formulas referencing same-row raw data
- MoM% formulas reference the previous row
- YoY% formulas reference 12 rows back (monthly) or 4 rows back (quarterly)
- Quarterly metrics (季度收入, ARPU for HOOD) stay constant within a quarter, update only on earnings release
- Each sheet has footnotes at the bottom explaining every formula

### 4. IBKR (Monthly)
| Column | Field | Unit | Notes |
|--------|-------|------|-------|
| A | 月份 | YYYY-MM | Primary key |
| B | DARTs | M trades | Daily Average Revenue Trades |
| C | 客户账户 | 万 | Ending accounts |
| D | 客户权益 | $B | Ending client equity |
| E | 保证金 | $B | Ending margin loan balances |
| F | 信用余额 | $B | Ending client credit balances |
| G | 单笔佣金 | $ | Avg commission per cleared order |
| H | 数据来源 | text | Source name + date |

### 5. SCHW (Monthly)
| Column | Field | Unit | Notes |
|--------|-------|------|-------|
| A | 月份 | YYYY-MM | Primary key |
| B | DAT | M trades | Daily Average Trades |
| C | 客户资产 | $T | Total client assets |
| D | Core NNA | $B | Exclude one-time items |
| E | 新开户 | 万 | New brokerage accounts |
| F | 保证金 | $B | Margin loan balances |
| G | Sweep Cash | $B | Transactional sweep cash |
| H | 活跃账户 | 万 | Active brokerage accounts |
| I | 数据来源 | text | |

### 6. HOOD (Monthly)
| Column | Field | Unit | Notes |
|--------|-------|------|-------|
| A | 月份 | YYYY-MM | Primary key |
| B | Funded客户 | 万 | Funded Customers |
| C | 平台资产 | $B | Total Platform Assets |
| D | Net Deposits | $B | Monthly net deposits |
| E | 股票交易量 | $B | Equity notional trading vol |
| F | 期权 | 百万张 | Options contracts traded |
| G | 加密交易 | $B | Crypto notional vol (App+Bitstamp) |
| H | 事件合约 | 亿张 | Event contracts traded |
| I | 数据来源 | text | |

### 7. FUTU (Quarterly)
| Column | Field | Unit | Notes |
|--------|-------|------|-------|
| A | 季度 | QN YYYY | e.g. "Q1 2026" |
| B | 付费账户 | 万 | Funded/paying accounts |
| C | 客户资产 | $B | Total client assets |
| D | 交易量 | $B | Quarterly trading volume |
| E | 收入 | $M | Quarterly revenue |
| F | 净利润 | $M | Non-GAAP net income |
| G | WM AUM | $B | Wealth management AUM |
| H | 新增账户 | 万 | Net new funded accounts |
| I | 数据来源 | text | |

---

### 8. 美股全市场交易量 (Weekly — NEW)

Tracks US equity and options market-wide volume. Append one row per week (Friday close).

| Column | Field | Unit | Notes |
|--------|-------|------|-------|
| A | 周末日期 | YYYY-MM-DD | Friday of the trading week |
| B | 股票日均成交量 | B shares | Consolidated tape daily avg for the week |
| C | 股票日均成交额 | $B | Notional daily avg for the week |
| D | NYSE成交量 | B shares | NYSE composite weekly avg |
| E | NASDAQ成交量 | B shares | NASDAQ weekly avg |
| F | 暗池占比 | % | FINRA ATS share of total volume |
| G | 期权日均合约量 | M contracts | OCC total daily avg for the week |
| H | 股票期权日均量 | M contracts | Equity options daily avg |
| I | 指数期权日均量 | M contracts | Index options daily avg |
| J | ETF期权日均量 | M contracts | ETF options daily avg |
| K | 0DTE占比 | % | Zero-day-to-expiry share of SPX options |
| L | Put/Call Ratio | ratio | Cboe equity put/call ratio |
| M | VIX收盘 | index | Friday close VIX |
| N | 数据来源 | text | e.g. "Cboe + OCC 2026.4.11" |

> **数据来源**: Cboe Global Markets (cboe.com/us/equities/market_statistics, cboe.com/us/options/market_statistics), OCC (optionsclearing.com/data/volume), NYSE market data, NASDAQ market statistics, FINRA ATS transparency data
> **搜索关键词**: `US equity market volume week [DATE]`, `Cboe daily equity volume`, `OCC options volume [MONTH] [YEAR]`, `0DTE options share`, `Cboe put call ratio`

### 9. 加密市场 (Weekly — NEW)

Tracks global crypto market metrics. Append new rows each update.

| Column | Field | Unit | Notes |
|--------|-------|------|-------|
| A | 日期 | YYYY-MM-DD | Snapshot date |
| B | 总市值 | $T | Total crypto market cap |
| C | 24h交易量 | $B | Global 24h spot trading volume |
| D | BTC市值占比 | % | BTC dominance |
| E | ETH市值占比 | % | ETH dominance |
| F | BTC价格 | $ | BTC/USD |
| G | ETH价格 | $ | ETH/USD |
| H | 稳定币总市值 | $B | Total stablecoin market cap (USDT+USDC+DAI+etc.) |
| I | 恐惧贪婪指数 | 0-100 | Crypto Fear & Greed Index |
| J | 数据来源 | text | e.g. "CoinGecko 2026.4.8" |

> **数据来源**: CoinGecko (coingecko.com), CoinMarketCap (coinmarketcap.com)
> **搜索关键词**: `crypto total market cap [DATE]`, `bitcoin dominance [DATE]`, `stablecoin market cap [DATE]`

### 10. 交易所市占率 (Monthly — NEW)

Tracks centralized exchange (CEX) market share data from The Block.

| Column | Field | Unit | Notes |
|--------|-------|------|-------|
| A | 月份 | YYYY-MM | Monthly |
| B | CEX现货总量 | $B | Total CEX spot volume for the month |
| C | CEX衍生品总量 | $T | Total CEX derivatives volume |
| D | Binance现货占比 | % | Binance spot market share |
| E | Coinbase现货占比 | % | Coinbase spot share |
| F | OKX现货占比 | % | OKX spot share |
| G | Bybit现货占比 | % | Bybit spot share |
| H | Upbit现货占比 | % | Upbit spot share |
| I | DEX现货总量 | $B | Total DEX spot volume |
| J | DEX/CEX比 | % | DEX volume as % of CEX volume |
| K | 数据来源 | text | e.g. "The Block Data Dashboard 2026.4" |

> **数据来源**: The Block Data Dashboard (theblock.co/data), CCData, Kaiko
> **搜索关键词**: `crypto exchange market share [MONTH] [YEAR] The Block`, `CEX spot volume [MONTH] [YEAR]`, `DEX vs CEX volume [MONTH]`

### 11. 预测市场 (Weekly — NEW)

Tracks prediction market volume and growth from Dune Analytics and platform data.

| Column | Field | Unit | Notes |
|--------|-------|------|-------|
| A | 日期 | YYYY-MM-DD | Snapshot/period end date |
| B | Polymarket周交易量 | $M | Polymarket weekly trading volume |
| C | Polymarket活跃市场数 | 个 | Number of active markets |
| D | Polymarket未平仓量 | $M | Open interest |
| E | Kalshi周交易量 | $M | Kalshi weekly volume |
| F | HOOD事件合约量 | 亿张 | Robinhood event contracts (cross-ref HOOD sheet) |
| G | 全平台预测市场总量 | $B | Sum of all platforms |
| H | WoW增长 | % | Week-over-week total volume growth |
| I | 数据来源 | text | e.g. "Dune Analytics @polymarket 2026.4.8, Kalshi blog 2026.4" |

> **数据来源**: Dune Analytics (dune.com, dashboard: @polymarket, @rchen8/prediction-markets), Polymarket blog, Kalshi press releases, HOOD monthly operating data
> **搜索关键词**: `Polymarket volume [MONTH] [YEAR] Dune Analytics`, `Kalshi trading volume [MONTH] [YEAR]`, `prediction market volume [MONTH] [YEAR]`, `Polymarket open interest`

---

### 12. 估值 (Snapshot, overwrite each update)
Fixed structure — update values in place, do NOT append rows.

### 13. EPS修正 (Append)
Append new rows when analyst revisions occur. Keep old rows for history.

### 14. 跨公司对比 (Rebuild each update)
Rebuild with latest 3-month window each time.

### 15. 使用说明 (Static)
Do not modify. Updated to note new sheets 8-11.

---

## How to Append Data (Python)

```python
from openpyxl import load_workbook

wb = load_workbook('券商监控数据库.xlsx')

# Example: append IBKR March data
ws = wb['IBKR']
ws.append(["2026-03", 432.9, 475.4, 789.4, 86.0, 168.8, 2.74, "Business Wire 2026.4.1"])

# Example: append weekly US equity/options volume
ws_eq = wb['美股全市场交易量']
ws_eq.append(["2026-04-04", 12.8, 685, 4.2, 5.1, 42.5, 52.3, 38.1, 8.7, 5.5, 48.2, 0.82, 18.5, "Cboe + OCC 2026.4.7"])

# Example: append crypto market snapshot
ws_crypto = wb['加密市场']
ws_crypto.append(["2026-04-08", 3.12, 128.5, 58.2, 16.1, 84500, 3920, 198.5, 72, "CoinGecko 2026.4.8"])

# Example: append exchange market share
ws_exch = wb['交易所市占率']
ws_exch.append(["2026-03", 1250, 5.8, 38.2, 12.5, 8.1, 7.6, 6.2, 180, 14.4, "The Block 2026.4"])

# Example: append prediction market data
ws_pred = wb['预测市场']
ws_pred.append(["2026-04-08", 1.85, 420, 285, 180, 3.2, 2.21, 12.5, "Dune Analytics 2026.4.8"])

wb.save('券商监控数据库_updated.xlsx')
```

## How to Create a New Seed File

If the user doesn't have an existing Excel file, create one using the openpyxl script pattern shown above. Include:
- All 16 sheets with proper headers and formatting
- Seed data for the most recent 3 months/quarters
- MoM% formula rows
- Color-coded headers (dark blue with white text)
- Auto-adjusted column widths
- New sheets (美股全市场交易量, 加密市场, 交易所市占率, 预测市场) with proper headers
