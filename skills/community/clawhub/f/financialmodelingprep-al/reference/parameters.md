# FMP Query Parameters Reference

All requests are GET against `https://financialmodelingprep.com/stable/`. Parameters are query-string values.

| Param | Meaning | Required? | Default | When to change |
|-------|---------|-----------|---------|----------------|
| `apikey` | Your FMP API key (`FMP_API_KEY`). Auth for every request. | Yes | — | Never. Read from env; **never expose**. In examples show `apikey=YOUR_FMP_API_KEY`. |
| `symbol` | The ticker to query (e.g. `AAPL`). Some endpoints accept comma-separated lists for batch. | Yes (most endpoints) | — | Set to the **resolved, confirmed** ticker (see symbol-resolution). Batch multiple symbols to save calls where supported. |
| `query` | Free-text for search endpoints (company name or partial symbol). | Yes (search) | — | Use for symbol resolution before pulling data. |
| `period` | Statement/metric granularity: `annual` or `quarter`. | No | Usually `annual` | Set `quarter` for quarterly analysis or to build TTM (sum last 4 quarters). Always label which you used. |
| `limit` | Number of periods/rows to return. | No | Endpoint-dependent | Lower it to save calls/payload; raise it for multi-year trends. Don't exceed plan history. |
| `from` | Start date `YYYY-MM-DD` (history, calendars). | No (history) | Endpoint-dependent | Narrow to the window you need — wide ranges are large and costly. |
| `to` | End date `YYYY-MM-DD` (history, calendars). | No (history) | Often today | Pair with `from` to bound the range. |
| `exchange` | Filter search/data to an exchange (where supported). | No | All | Use to disambiguate cross-listed names (e.g. ADR vs local listing). |

## Notes

- **Dates** use ISO `YYYY-MM-DD`. Avoid inverted ranges (`from` after `to`).
- **`period` discipline:** never compare an `annual` row against a `quarter` row without labeling each. TTM is *derived* from four quarters, not a built-in `period` value (unless a TTM endpoint exists — see "Verification needed" in endpoints.md).
- **`limit` and cost:** every period returned counts toward payload size; on the free tier (~250 calls/day) keep `limit` to what you need.
- **`symbol` resolution:** a wrong `symbol` returns an empty array, not an error — always confirm via search + profile first.
- **`apikey` placement:** query string is standard; header auth may also be supported. Either way, keep it secret.

> Verification needed: confirm per-endpoint defaults for `limit` and whether `period`/`exchange` are accepted on every endpoint at https://site.financialmodelingprep.com/developer/docs.
