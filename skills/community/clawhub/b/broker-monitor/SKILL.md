---
name: broker-weekly-monitor
description: "Generate a weekly monitoring report for US retail brokerage stocks (IBKR, SCHW, HOOD, FUTU) AND the broader trading ecosystem including US equity/options market-wide volume (Cboe, OCC), crypto market (market cap, volume, exchange market share from The Block/CCData), and prediction markets (Polymarket/Kalshi volume from Dune Analytics). Use this skill whenever the user asks to update, generate, or review a broker monitoring report, weekly trading ecosystem update, or mentions tracking DARTs, client assets, trading volumes, margin loans, EPS revisions, US equity volume, options volume, 0DTE, put/call ratio, crypto exchange market share, prediction market volume, Polymarket, Kalshi, Dune Analytics, or The Block data. Also trigger for '券商监控', '周度监控', '零售券商', '全市场交易生态', 'weekly monitor', 'equity volume', 'options volume'."
---

# US Retail Broker & Trading Ecosystem Weekly Monitoring Report

## Overview

This skill generates a structured **weekly** monitoring report covering five pillars:

1. **US equity & options market-wide volume** — Consolidated tape equity volume, OCC options volume, 0DTE share, Put/Call ratio, VIX (Cboe, OCC, NYSE, NASDAQ, FINRA ATS)
2. **Four US-listed retail brokerages** — IBKR, SCHW, HOOD, FUTU monthly/quarterly operating data
3. **Crypto market** — Total market cap, trading volume, BTC/ETH prices, stablecoin supply, Fear & Greed (CoinGecko/CoinMarketCap)
4. **Exchange market share** — CEX/DEX spot & derivatives volume, per-exchange share (The Block, CCData, CoinDesk)
5. **Prediction markets** — Polymarket, Kalshi, HOOD Events volume & growth (Dune Analytics)

Published weekly (weekend or Monday). Each metric includes a **牛熊周期定位** (bull/bear spectrum) comparing current levels to historical extremes.

## When to Use

- User asks to "update the broker report", "weekly update", or "generate the weekly monitor"
- User asks about retail broker metrics (DARTs, client assets, trading volumes, margin loans)
- User wants to compare IBKR/SCHW/HOOD/FUTU on key metrics
- User asks about EPS revisions, valuation, or analyst target price changes
- User asks about crypto market cap, CEX volume, exchange market share
- User asks about prediction market volume, Polymarket, Kalshi, Dune Analytics
- User asks about US equity trading volume, options volume, 0DTE, put/call ratio
- User mentions "券商监控", "周度监控", "零售券商", "全市场交易生态", "weekly monitor"

## Workflow

### Step 1: Determine Data Freshness

| Source | Cadence | Where to Find |
|--------|---------|---------------|
| **Cboe equity volume** | Daily (aggregate weekly) | cboe.com/us/equities/market_statistics |
| **OCC options volume** | Daily/Monthly | optionsclearing.com/data/volume |
| **Cboe options/VIX** | Daily | cboe.com/us/options/market_statistics |
| **IBKR** | Monthly (~1st biz day) | Business Wire / interactivebrokers.com/ir |
| **SCHW** | Monthly (~15th) | Business Wire / aboutschwab.com |
| **HOOD** | Monthly (~12th) | GlobeNewsWire / investors.robinhood.com |
| **FUTU** | Quarterly (March/June/Sept/Dec) | PR Newswire / futuhk.com/newsroom |
| **CoinGecko/CMC** | Real-time (snapshot weekly) | coingecko.com / coinmarketcap.com |
| **The Block** | Monthly dashboards | theblock.co/data |
| **Dune Analytics** | Real-time dashboards | dune.com (@polymarket, @rchen8) |
| **Kalshi** | Monthly blog/PR | kalshi.com/blog |

### Step 2: Smart Data Freshness Check (Avoid Redundant Searches)

**CRITICAL: Before searching, check dates to avoid wasting tokens.**

```
DATE_CHECK_LOGIC:
1. Determine today's date and the report week (Mon–Fri).
2. For each data source, check if new data should be available:
   - IBKR: New data ~1st biz day of month. If today < 2nd AND last report already has prior month → SKIP, carry forward with ⏭️.
   - SCHW: New data ~15th. If today < 16th AND last report has prior month → SKIP.
   - HOOD: New data ~12th. If today < 13th AND last report has prior month → SKIP.
   - FUTU: Quarterly only (Mar/Jun/Sep/Dec earnings). If not earnings month → SKIP.
   - The Block CEX: Monthly. If same month as last report → SKIP.
   - Crypto / VIX / equity volume / prediction markets: ALWAYS refresh (weekly).
3. In report header "📋 本期数据覆盖范围" table, mark each module:
   - ✅ = searched and updated this week
   - ⏭️ = carried forward (not yet due)
   - 🆕 = first time this month/quarter's data appears
```

**Weekly-refresh data (ALWAYS search):**
```
"US equity market volume week [DATE]"
"Cboe daily equity volume [MONTH] [YEAR]"
"OCC options volume [MONTH] [YEAR]"
"0DTE options share [MONTH] [YEAR]"
"Cboe put call ratio"
"VIX close [DATE]"
"crypto total market cap [MONTH] [YEAR]"
"bitcoin dominance stablecoin market cap [MONTH] [YEAR]"
"crypto fear greed index"
"Polymarket volume [MONTH] [YEAR]"
"Polymarket trading volume Dune Analytics"
"Kalshi trading volume [MONTH] [YEAR]"
```

**Monthly/quarterly data (search ONLY when due):**
```
"Interactive Brokers [MONTH] [YEAR] monthly metrics DARTs accounts"
"Charles Schwab [MONTH] [YEAR] monthly activity report client assets"
"Robinhood [MONTH] [YEAR] operating data funded customers"
"Futu Holdings [QUARTER] [YEAR] earnings paying clients AUM"
"crypto exchange market share [MONTH] [YEAR] The Block"
"CEX spot volume [MONTH] [YEAR]"
"Binance Coinbase OKX market share [MONTH] [YEAR]"
"SCHW IBKR HOOD FUTU EPS estimate revision [YEAR]"
"[TICKER] analyst price target [MONTH] [YEAR]"
```

### Step 3: Generate the Report

Read `references/report-template.md` and fill in data. The report has **nine mandatory sections**:

### Step 4: Update the Excel Database

The Excel file `券商监控数据库.xlsx` has **16 sheets**. See `references/excel-structure.md` for full schema.

1. Check if user uploaded the file in `/mnt/user-data/uploads/`.
2. Read with `openpyxl` (NOT pandas, to preserve formatting).
3. Append new rows to relevant sheets (NEVER overwrite existing rows).
4. If new sheets don't exist (upgrading from old template), CREATE them with headers.
5. Save to `/mnt/user-data/outputs/券商监控数据库.xlsx`.

### Step 5: Output

- Save Excel to `/mnt/user-data/outputs/券商监控数据库.xlsx`
- Save report to `/mnt/user-data/outputs/美股零售券商_[YYYY]W[WW]_周度监控报告.md`
- Present BOTH files; remind user to re-upload Excel next time.

---

## Report Structure (9 Sections) — Complete Specification

### Section 0: 全市场交易生态总览

Four sub-sections, each with a data table AND a **📊 牛熊周期定位** spectrum table:

**0.1 美股全市场交易量**
- Equity: daily avg volume (B shares), daily avg notional ($B), NYSE volume, NASDAQ volume, dark pool share
- Options: daily avg contracts (M), equity/index/ETF options breakdown, 0DTE share (%), Put/Call Ratio, VIX
- Each metric has a 4-tier spectrum: 🟢 熊底 → 🔵 常态 → 🟡 牛市活跃 → 🔴 极端亢奋, with historical reference points
- Paragraph linking to broker relevance (SCHW DAT vs market, IBKR DARTs vs market)

**0.2 加密市场快照**
- Total market cap ($T), 24h volume ($B), BTC price, BTC dominance (%), ETH price, stablecoin market cap ($B), Fear & Greed index
- 7-metric 牛熊定位 spectrum: market cap, BTC price, BTC dominance, 24h volume, stablecoin supply, Fear & Greed, CEX monthly spot volume
- Historical anchors: 2022.11 FTX crash (bear bottom) → 2023 recovery → 2024-25 bull → 2021.11/2024.10 ATH (extreme)
- Paragraph linking to HOOD crypto revenue, FUTU crypto, Schwab BTC/ETH entry

**0.3 交易所市占率 (CEX)**
- Per-exchange spot market share: Binance, Coinbase, OKX, Bybit, Upbit (with MoM change)
- Aggregate: CEX spot total ($B), CEX derivatives total ($T), DEX spot total ($B), DEX/CEX ratio (%)
- Monthly data from The Block; carry forward with ⏭️ when no new month available

**0.4 预测市场**
- Per-platform weekly volume: Polymarket ($M), Kalshi ($M), HOOD Events (亿张)
- Active markets count, open interest ($M)
- Total volume with WoW and YoY
- Trend judgment paragraph

### Section 1: 🚩 核心发现与预警信号

- 3–5 positive signals (⬆️) with specific numbers and sources
- 3–5 warning flags (⚠️🚩) with specific numbers and sources
- Must cover ALL five pillars (equity volume, brokers, crypto, CEX, prediction markets)
- Each signal cites a data source with date
- Flag any metric with >10% MoM decline, any EPS downgrade, margin at historical highs

### Section 2: 跨公司横向对比

Four comparison tables across all 4 brokers, latest 3 months:
1. **客户数/账户数** — SCHW active accounts, HOOD funded customers, IBKR accounts, FUTU funded accounts
2. **客户资产/AUM** — SCHW total client assets ($T), IBKR client equity ($B), HOOD platform assets ($B), FUTU client assets ($B)
3. **交易活跃度** — SCHW DAT, IBKR DARTs, HOOD equity trading volume, FUTU quarterly trading volume
4. **净资金流入** — SCHW Core NNA, HOOD Net Deposits, IBKR credit balance changes, FUTU quarterly NNA

Each row must be marked with ✅/⏭️/🆕 to show data freshness.

### Section 2.5: 📐 衍生指标（二次计算）

Six sub-tables, each with formula, raw inputs, and source footnote:
1. **AUC/Account ($K)** — Total Client Assets ÷ Total Accounts
2. **年化ARPU ($)** — (Latest Quarter Revenue × 4) ÷ End-of-Period Accounts
3. **杠杆率 (%)** — Margin Loans ÷ Client Assets (IBKR ~11%, track vs 2022 bear 11.8%)
4. **收入结构 (%)** — Commission / NII / Other as % of Total Revenue (from latest 8-K)
5. **平台特色指标** — Gold Adoption (HOOD), DARTs/Account (IBKR), Cash/Assets (SCHW), Gross Margin (FUTU), crypto/total revenue (HOOD), event contracts/total (HOOD)
6. **加密/预测市场衍生指标** — HOOD crypto % of global CEX, Coinbase share trend, prediction market penetration, HOOD Events market share, crypto cap / US equity cap

### Section 3: 个股三个月滚动仪表盘

One table per broker with 3-month trailing data. Each row includes:
- Metric name, 3 months of data, MoM%, YoY%, 历史牛熊定位 (where vs 2020 COVID low / 2021 Meme peak / 2022 bear / current)

**IBKR metrics**: DARTs (M), client accounts (万), client equity ($B), margin loans ($B), credit balances ($B), avg commission/order ($), options contracts (M), futures contracts (M)

**SCHW metrics**: DAT (M), total client assets ($T), Core NNA ($B), new accounts (万), margin ($B), sweep cash ($B), active accounts (万)

**HOOD metrics**: Funded customers (万), platform assets ($B), net deposits ($B), equity trading vol ($B), options contracts, crypto trading vol ($B), event contracts (亿张), margin ($B)

**FUTU metrics**: Paying accounts (万), client assets ($B), trading volume ($B), revenue ($M), net income ($M), WM AUM ($B), net new accounts (万)

### Section 4: 关键趋势分析（牛熊周期视角）

Six sub-sections:
1. **交易活跃度** — Current SCHW DAT / IBKR DARTs vs historical cycle table (2018→present). Is growth accelerating or decelerating? Structural vs cyclical?
2. **客户资产** — SCHW asset milestones table ($4T 2019 → $12T+ 2026). Market-driven vs organic?
3. **保证金贷款** — Margin/equity ratio analysis. IBKR杠杆率 vs 2022 bear (11.8%). SCHW $120B+ record.
4. **FUTU的特殊位置** — Growth vs valuation disconnect. China risk premium.
5. **加密交易生态演变** — Crypto cycle positioning table (2022 FTX bear → 2024 ETF ATH → current). CEX volume trends, DEX share growth, Coinbase vs Binance dynamics, Schwab entry impact.
6. **预测市场发展轨迹** — Volume evolution table (pre-2024 niche → 2024 election peak → post-election). Polymarket/Kalshi/HOOD dynamics. CFTC regulatory posture.

### Section 5: 估值深度分析

Four sub-sections:
1. **四家券商估值横向对比** — Stock price, market cap, TTM PE, Forward PE, TTM EPS, FY+1 EPS estimate, FY+1 EPS growth %, analyst consensus rating. All with source citations.
2. **历史牛熊市PE区间对比** — Bear bottom PE, cycle average PE, bull peak PE, current PE, positioning for each broker. SCHW (13x bear → 31.5x bull), IBKR (~15x bear → ~40x bull), HOOD (N/A → 134x peak), FUTU (~8x bear → 45x+ bull).
3. **估值判断摘要** — One paragraph per broker with specific judgment.
4. **Forward EPS 下修追踪** — Table: 公司, 此前共识, 最新共识, 变化幅度, 时间, 方向, 驱动因素, 来源. Flag any broker with >5% EPS downgrade.

### Section 6: 宏观环境与利率敏感性

Table of 8 macro variables with current state and impact:
1. Fed Funds Rate — status, impact on NII (SCHW/IBKR)
2. VIX波动率 — level with 牛熊定位, impact on trading volumes
3. S&P 500走势 — level, weekly range, impact on client assets
4. 关税/贸易战 — status, impact on sentiment
5. Forward EPS增速 — market-wide, direction impact
6. 加密市场(BTC/总市值) — BTC price + cap, impact on HOOD/FUTU crypto revenue
7. 预测市场监管(CFTC) — regulatory posture, impact on HOOD Events growth ceiling
8. CEX监管(SEC) — enforcement actions, impact on Coinbase/Binance compliance costs, HOOD crypto boundary

### Section 7: 下周/下月关注重点

Table of upcoming events: earnings dates (SCHW, IBKR, HOOD, FUTU), data releases (monthly operating data), FOMC meetings, policy events, crypto events (ETF decisions, protocol upgrades), prediction market milestones.

### Section 8: 风险预警检查

10-item dashboard with status indicators (❌ not triggered / ⚠️ warning / 🔴 triggered):
1. 交易量持续萎缩
2. 客户资产大规模外流
3. 保证金贷款过高
4. Cash Sorting恶化
5. 监管冲击
6. 利率急变
7. 中概风险(FUTU)
8. 加密市场崩盘(>30%回撤)
9. 预测市场监管收紧
10. CEX流动性危机

---

## Data Source Citation Rules

- Every number must have a footnote with source name and date
- Acceptable sources:
  - **Equity/Options**: Cboe Global Markets, OCC, NYSE, NASDAQ, FINRA ATS
  - **Brokers**: SEC filings, Business Wire, GlobeNewsWire, PR Newswire, company IR
  - **Estimates**: Seeking Alpha, Zacks, TipRanks, WallStreetZen, StockAnalysis
  - **Crypto**: CoinGecko, CoinMarketCap, DefiLlama
  - **Exchange share**: The Block Data Dashboard, CCData, Kaiko, CoinDesk
  - **Prediction markets**: Dune Analytics (@polymarket, @rchen8), Polymarket blog, Kalshi blog
  - **Macro**: FRED, CME FedWatch
- Footnotes numbered sequentially, listed at end of report

## Key Reference Files

- `references/report-template.md` — Full report template with placeholder markers (9 sections)
- `references/metrics-by-broker.md` — Complete list of metrics tracked per broker
- `references/excel-structure.md` — Data schema for the 16-sheet Excel database
- `references/dashboard-schema.md` — Data schema for the React dashboard
