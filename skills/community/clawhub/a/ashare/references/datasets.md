# AKShare Dataset Mapping

Use this file to map natural-language requests to the bundled CLI. Keep requests inside this whitelist. If a request falls outside it, return `unsupported_query`.

## A-Shares

- Market snapshot, market breadth, today's A-share overview
  - Command: `market-overview`
  - AKShare: `stock_zh_a_spot_em`, `stock_zh_index_spot_em`
- Single-stock real-time quote, latest price, now, current change
  - Command: `stock-quote <symbol>`
  - AKShare: `stock_zh_a_spot_em`
- Single-stock history, K-line, daily/weekly/monthly trend
  - Command: `stock-history <symbol> [--start-date YYYYMMDD] [--end-date YYYYMMDD] [--period daily|weekly|monthly] [--adjust none|qfq|hfq] [--limit N]`
  - AKShare: `stock_zh_a_hist`
- Single-stock profile, company basics, market cap, industry
  - Command: `stock-profile <symbol>`
  - AKShare: `stock_individual_info_em`

## China Indexes

- Real-time index quote
  - Command: `index-quote <symbol>`
  - AKShare: `stock_zh_index_spot_em`
- Index history and trend
  - Command: `index-history <symbol> [--start-date YYYYMMDD] [--end-date YYYYMMDD] [--period daily|weekly|monthly] [--limit N]`
  - AKShare: `index_zh_a_hist`
- Supported resolver universe
  - `沪深重要指数`
  - `上证系列指数`
  - `深证系列指数`
  - `指数成份`
  - `中证系列指数`

## Open-End Mutual Funds

- Daily quote and latest NAV snapshot
  - Command: `fund-quote <symbol>`
  - AKShare: `fund_open_fund_daily_em`
- Historical net value trend
  - Command: `fund-history <symbol> [--indicator unit_nav|acc_nav|acc_return] [--period 1m|3m|6m|1y|3y|5y|ytd|all] [--limit N]`
  - AKShare: `fund_open_fund_info_em`
  - Indicator aliases
    - `unit_nav` -> `单位净值走势`
    - `acc_nav` -> `累计净值走势`
    - `acc_return` -> `累计收益率走势`

## Macro

- China CPI series
  - Command: `macro-series china_cpi`
  - AKShare: `macro_china_cpi`
- China PMI series
  - Command: `macro-series china_pmi`
  - AKShare: `macro_china_pmi`
- China RMB deposit/reserve series
  - Command: `macro-series china_rmb`
  - AKShare: `macro_china_rmb`
- Macro calendar for a date
  - Command: `macro-calendar [--date YYYYMMDD] [--limit N]`
  - AKShare: `macro_info_ws`

## News

- Latest CLS telegraph/news flash
  - Command: `news-flash [--scope all|important] [--limit N]`
  - AKShare: `stock_info_global_cls`
  - Scope aliases
    - `all` -> `全部`
    - `important` -> `重点`

## Resolver Rules

- Prefer exact code matches first.
- Then prefer exact normalized name matches.
- If fuzzy matching returns exactly one row, use it.
- If fuzzy matching returns multiple rows, return `ambiguous_symbol` and include candidates.
- Do not guess a stock/index/fund from partial natural-language context.
- For stock, index, and fund history commands, if the user gives no absolute date range, use the most recent 60 returned rows.
