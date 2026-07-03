# Frankfurter v1 API (legacy)

Read this only when maintaining existing code that uses v1 URLs. For new work,
use the v2 API in `endpoints.md` — v1 is not being retired, but v2 has more
currencies, more providers, and more features.

Key differences from v2: v1 serves **ECB reference rates only** (~30
currencies, data from 1999), and its response is an object keyed by currency
(or by date for series) instead of v2's flat array of rows.

Base URL: `https://api.frankfurter.dev/v1` (the older host
`api.frankfurter.app` also still resolves).

## Endpoints

| Task | Request |
|---|---|
| Latest rates | `GET /v1/latest` |
| Base + filter | `GET /v1/latest?base=USD&symbols=EUR,GBP` |
| Built-in conversion | `GET /v1/latest?amount=100&base=USD&symbols=EUR` |
| Historical date | `GET /v1/1999-01-04` |
| Time series | `GET /v1/2026-01-01..2026-01-07?symbols=USD` |
| Series to today | `GET /v1/2026-01-01..` |
| Currencies | `GET /v1/currencies` |

Note the v1 parameter names: `base` and `symbols` (v2 uses `base` and
`quotes`). Unlike v2, v1 has an `amount` parameter that multiplies rates for
you.

## Response shapes (verified)

```json
// GET /v1/latest?amount=100&base=USD&symbols=EUR
{"amount": 100.0, "base": "USD", "date": "2026-07-02", "rates": {"EUR": 87.73}}

// GET /v1/2026-01-01..2026-01-07?symbols=USD
{
  "amount": 1.0,
  "base": "EUR",
  "start_date": "2025-12-31",
  "end_date": "2026-01-07",
  "rates": {
    "2025-12-31": {"USD": 1.175},
    "2026-01-02": {"USD": 1.1721},
    "2026-01-05": {"USD": 1.1664}
  }
}

// GET /v1/currencies
{"AUD": "Australian Dollar", "EUR": "Euro", "USD": "US Dollar"}
```

Gotchas:
- Weekends/holidays roll back to the last business day (see the returned
  `date`), and a series' `start_date` may be adjusted to the prior business day.
- Requesting a currency v1 doesn't carry (e.g. TWD) silently drops it from
  `rates` on `/latest`, or returns `{"message": "not found"}` elsewhere.
