# Finnhub API Reference Notes

> Lightweight reference for building a read-only Finnhub market-data skill.

## Base URL

```text
https://finnhub.io/api/v1
```

Authentication:

```text
token=<FINNHUB_API_KEY>
```

---

## 1. Quote

```text
GET /quote?symbol=AAPL&token=...
```

Typical fields:
- `c` current price
- `d` change
- `dp` percent change
- `h` high
- `l` low
- `o` open
- `pc` previous close
- `t` timestamp

---

## 2. Stock Candles

```text
GET /stock/candle?symbol=AAPL&resolution=D&from=1711584000&to=1712188800&token=...
```

Typical params:
- `symbol`
- `resolution`: `1`, `5`, `15`, `30`, `60`, `D`, `W`, `M`
- `from`: unix timestamp
- `to`: unix timestamp

Typical fields:
- `c` close[]
- `h` high[]
- `l` low[]
- `o` open[]
- `s` status
- `t` timestamp[]
- `v` volume[]

---

## 3. Company Profile

```text
GET /stock/profile2?symbol=AAPL&token=...
```

Useful fields often include:
- `country`
- `currency`
- `exchange`
- `finnhubIndustry`
- `ipo`
- `marketCapitalization`
- `name`
- `shareOutstanding`
- `ticker`
- `weburl`

---

## 4. Company News

```text
GET /company-news?symbol=AAPL&from=2026-03-01&to=2026-03-30&token=...
```

Typical params:
- `symbol`
- `from` (YYYY-MM-DD)
- `to` (YYYY-MM-DD)

---

## 5. Market News

```text
GET /news?category=general&token=...
```

Common categories may include:
- `general`
- `forex`
- `crypto`
- `merger`

---

## 6. Earnings Calendar

```text
GET /calendar/earnings?from=2026-03-30&to=2026-04-06&token=...
```

Useful for upcoming earnings windows.

---

## 7. Economic Calendar

```text
GET /calendar/economic?from=2026-03-30&to=2026-04-06&token=...
```

Useful for macro releases.

---

## 8. Crypto / Forex Notes

Finnhub supports crypto and forex datasets, but symbol formats and plan coverage can vary.
When in doubt:
1. confirm the exact symbol the user wants
2. verify the endpoint supported by the user plan
3. avoid guessing exchange-specific formats

---

## Request Safety Rules

- Read-only only
- No secret in logs
- No fabricated data on auth/rate-limit errors
- Ask for clarification on ambiguous symbols
- Keep broad requests narrow by default

---

## Security Notes

- Restrict requests to the official Finnhub domain only
- Never print the API token in logs or error messages
- Treat this skill as read-only market data access
- Reject insecure `http://` base URLs

## Plan Limitation Note

Finnhub access can differ by account tier.
If `/stock/candle` returns 403 or similar permission errors:
- treat it as a plan restriction, not as a symbol error
- fall back to quote + news only
- clearly tell the user that volume / candle detail is unavailable under the current plan

## Suggested Future Expansion

Possible future additions:
- symbol normalization helpers
- date/range parsing helpers
- richer table output helpers
- optional websocket helpers (still read-only)
