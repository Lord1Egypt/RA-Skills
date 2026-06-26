---
name: ashare
description: Use AKShare to answer Chinese market-data questions about A-shares, China indexes, open-end mutual funds, macro indicators, macro calendar events, and finance news flashes. Trigger on requests such as A股行情, 个股价格, 历史K线, 指数走势, 基金净值, 宏观数据, 财联社快讯, market overview, stock quote, fund NAV, macro calendar, or news flash. Prefer this skill when OpenClaw needs structured market data from AKShare instead of free-form web browsing.
homepage: https://akshare.akfamily.xyz/data/index.html
user-invocable: true
metadata: {"openclaw":{"requires":{"bins":["python"]}}}
---

# A股市场数据

Use this skill to query a fixed whitelist of AKShare market datasets through the bundled CLI.

## Workflow

1. Convert relative dates to absolute `YYYYMMDD` before calling the script.
2. Map the user's request to one of the supported subcommands in [`references/datasets.md`](references/datasets.md).
3. Run only the bundled script with OpenClaw `exec`:

```bash
python "{baseDir}/scripts/query_akshare.py" <subcommand> [args...]
```

4. Read the JSON envelope from stdout.
5. Reply in Chinese with a short summary plus the most relevant values from the returned `rows`.

## Hard Rules

- Use only `python "{baseDir}/scripts/query_akshare.py" ...`.
- Do not paste the user's raw request into shell pipelines.
- Do not generate ad-hoc Python snippets to call AKShare directly.
- Do not guess when a symbol match is ambiguous; surface the returned candidates.
- Keep dates in `YYYYMMDD`.
- Treat missing `akshare` as an environment issue and relay the install command from the error payload.

## Supported Commands

- `market-overview`
  - Return A-share market breadth, major indices, top 10 gainers, and top 10 losers.
- `stock-quote <symbol>`
  - Real-time A-share quote by code or exact name.
- `stock-history <symbol> [--start-date YYYYMMDD] [--end-date YYYYMMDD] [--period daily|weekly|monthly] [--adjust none|qfq|hfq] [--limit N]`
- `stock-profile <symbol>`
  - Company and security profile from Eastmoney.
- `index-quote <symbol>`
  - Real-time China index quote by code or exact name.
- `index-history <symbol> [--start-date YYYYMMDD] [--end-date YYYYMMDD] [--period daily|weekly|monthly] [--limit N]`
- `fund-quote <symbol>`
  - Open-end mutual fund daily NAV snapshot by code or exact name.
- `fund-history <symbol> [--indicator unit_nav|acc_nav|acc_return] [--period 1m|3m|6m|1y|3y|5y|ytd|all] [--limit N]`
- `macro-series <alias>`
  - Supported aliases: `china_cpi`, `china_pmi`, `china_rmb`.
- `macro-calendar [--date YYYYMMDD] [--limit N]`
- `news-flash [--scope all|important] [--limit N]`

## Command Examples

```bash
python "{baseDir}/scripts/query_akshare.py" market-overview
python "{baseDir}/scripts/query_akshare.py" stock-quote 000001
python "{baseDir}/scripts/query_akshare.py" stock-history 600519 --start-date 20260101 --end-date 20260313
python "{baseDir}/scripts/query_akshare.py" index-history 000300 --limit 60
python "{baseDir}/scripts/query_akshare.py" fund-history 000001 --indicator unit_nav --limit 60
python "{baseDir}/scripts/query_akshare.py" macro-series china_pmi
python "{baseDir}/scripts/query_akshare.py" macro-calendar --date 20260313
python "{baseDir}/scripts/query_akshare.py" news-flash --limit 10
```

## Output Contract

Every success response is a JSON object with:

- `ok`
- `dataset`
- `akshare_function`
- `resolved`
- `params`
- `columns`
- `rows`
- `row_count`
- `truncated`
- `as_of`

Every failure response is a JSON object with:

- `ok: false`
- `error.type`
- `error.message`
- optional `error.details`

Error types are limited to:

- `missing_dependency`
- `invalid_argument`
- `unsupported_query`
- `ambiguous_symbol`
- `runtime_error`

## Summary Style

- Lead with the direct answer in Chinese.
- Mention the symbol or dataset that was resolved.
- For quotes, include latest price and change fields when present.
- For history, describe the date range covered by the returned rows.
- For market overview, mention breadth and the main index moves.
- For macro/news results, surface the latest or most important rows instead of dumping the whole payload.
