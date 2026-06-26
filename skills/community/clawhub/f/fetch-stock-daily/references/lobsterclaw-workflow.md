# LobsterClaw Workflow Notes

Use this note only when you need the JS implementation details or the parity notes versus the repo's Python workflow.

## Publishable JS Path

The bundled script is pure Node.js and avoids Python runtime dependencies:

1. Resolve code input directly, or resolve Chinese stock names through the Eastmoney A-share list API.
2. Cache the symbol list at `data/cache/eastmoney/a_share_symbols.json`.
3. Fetch daily bars from `https://push2his.eastmoney.com/api/qt/stock/kline/get`.
4. Convert each `kline` row into record objects with Chinese field names.
5. Archive the result at `data/raw/eastmoney/daily_history/YYYYMMDD/<symbol>_<HHMMSS>.json`.

## Python Parity Notes

The original LobsterClaw Python flow is still the reference for the workflow shape:

1. `tools/connectors/stock_data_collector.py`
2. `StockDataCollector.resolve_symbol(raw_symbol)`
3. `StockDataCollector.fetch_daily_history_df(symbol, start_date, end_date, adjust)`
4. `tools/repositories/files/raw_archive.py`
5. `RawArchiveWriter.archive_json(provider="akshare", dataset="daily_history", ...)`

The JS version keeps the same high-level steps but swaps the Python-only resolver and AkShare dependency for direct HTTP calls so the skill is easier to publish and run.

## Supported Inputs

`resolve_symbol()` currently handles:

- `600519`
- `300750.SZ`
- `600519.SH`
- Chinese stock names such as `贵州茅台`

Do not use `sh600519` or `sz300750`. That format is not part of the current resolver.

## Archive Convention

Daily history files are stored as:

```text
data/raw/eastmoney/daily_history/YYYYMMDD/<symbol>_<HHMMSS>.json
```

The JSON payload is an array of row objects. Column names stay close to the current LobsterClaw archive style and include Chinese labels such as `日期`, `开盘`, `收盘`, `最高`, `最低`, `成交量`, `成交额`, `振幅`, `涨跌幅`, `涨跌额`, and `换手率`.

## Date Defaults

If the user does not provide `--start-date`, follow the same rolling-window rule used by `core/data_sync/planner.py`:

- reference end date: today or the explicit `--end-date`
- history start: `reference_date - (365 * years + 10)` days
- default `years`: `5`
- default `adjust`: `qfq`

## Scope Guardrail

This skill is for raw daily-history export only. Do not switch into the full PostgreSQL backfill flow unless the user explicitly asks for DB sync.
