---
name: frankfurter-api
description: Fetch exchange rates and convert currencies with the free Frankfurter API (no API key). Use for any exchange rate, currency conversion, forex, or historical FX data task, even if Frankfurter isn't mentioned.
---

# Frankfurter API

Frankfurter is a free, open-source exchange rate API. The public API lives at
`https://api.frankfurter.dev` — **no API key, no signup, no monthly quota** (only
abuse-prevention rate limiting). It tracks daily reference rates from 84 central
banks covering 201 currencies, with history back to 1948.

Use the **v2 API** (`/v2/...`) documented below. The older v1 API still works;
see `references/v1-api.md` only if you must maintain existing v1 code.

## Quick reference

Base URL: `https://api.frankfurter.dev`

| Task | Request |
|---|---|
| Latest rates (base EUR) | `GET /v2/rates` |
| Change base currency | `GET /v2/rates?base=USD` |
| Limit target currencies | `GET /v2/rates?quotes=USD,GBP,JPY` |
| Rates on a specific date | `GET /v2/rates?date=1999-01-04` |
| Time series | `GET /v2/rates?from=2026-01-01&to=2026-03-31&quotes=USD` |
| Downsample series | `...&group=week` or `...&group=month` |
| Single currency pair | `GET /v2/rate/EUR/USD` (optional `?date=YYYY-MM-DD`) |
| List currencies | `GET /v2/currencies` (`?scope=all` includes legacy ones) |
| One currency's details | `GET /v2/currency/TWD` |
| List data providers | `GET /v2/providers` |

Currency codes are ISO 4217 (USD, EUR, TWD, JPY...). Dates are `YYYY-MM-DD`.

## Response shape

`/v2/rates` returns a JSON **array** of rows; `/v2/rate/{BASE}/{QUOTE}` returns a
single object:

```json
// GET /v2/rates?base=USD&quotes=EUR,TWD
[
  {"date": "2026-07-03", "base": "USD", "quote": "EUR", "rate": 0.87598},
  {"date": "2026-07-03", "base": "USD", "quote": "TWD", "rate": 31.913}
]

// GET /v2/rate/EUR/USD
{"date": "2026-07-03", "base": "EUR", "quote": "USD", "rate": 1.1416}
```

A time series is the same array with one row per date per quote currency.

## Currency conversion

There is **no conversion endpoint** in v2. Fetch the pair rate and multiply:

```python
import requests

def convert(base: str, quote: str, amount: float, date: str | None = None) -> float:
    url = f"https://api.frankfurter.dev/v2/rate/{base}/{quote}"
    params = {"date": date} if date else {}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return amount * r.json()["rate"]

print(convert("USD", "TWD", 100))  # e.g. 3191.3
```

```javascript
async function convert(base, quote, amount) {
  const r = await fetch(`https://api.frankfurter.dev/v2/rate/${base}/${quote}`);
  const d = await r.json();
  return amount * d.rate;
}
```

## Providers and blended rates

By default, rates are **blended** across all contributing central banks. This is
fine for general use, but the last decimal places can shift as new data arrives.

- For **official/compliance** use, pin a specific source: `?providers=ECB`
  (provider keys come from `/v2/providers` — e.g. ECB, BOE, FRED, CBC).
- To see which sources fed a blended rate, add `?expand=providers`: each row
  gains a `providers` array of `{key, rate}` objects. Pegged currencies omit it
  (their rate comes from the peg, not provider data).

## Output formats

- **JSON** (default).
- **CSV**: append `.csv` to the path (`/v2/rates.csv?...`) or send
  `Accept: text/csv`. Columns: `date,base,quote,rate`.
- **NDJSON**: send `Accept: application/x-ndjson`. Each line is one independent
  JSON object — use this to stream large time series without buffering.

## Errors

Errors return an HTTP status with a JSON body like `{"status": 404, "message": "not found"}`:

- `400` — invalid parameter or malformed request
- `404` — currency, rate, or resource not found (check the ISO code and date)
- `422` — request understood but cannot be processed

## Practical tips

- The public API blocks the default `Python-urllib` User-Agent (Cloudflare
  returns 403). `curl`, `fetch`, and the `requests` library work as-is; if you
  use `urllib`, set any custom `User-Agent` header.
- Rates are **daily reference rates**, not live tick data. Weekends and holidays
  have no new data, so "latest" may be the previous business day — read the
  `date` field in the response rather than assuming today.
- Narrow `quotes` to the currencies you need; it keeps responses small and fast.
- Cache responses when polling — data updates at most daily per provider, so
  requesting more often than hourly is wasted traffic.
- Historical coverage varies by currency: check `start_date` in
  `/v2/currency/{CODE}` before requesting old dates.
- Free for commercial use; see each provider's terms for the underlying data.
- Self-hosting is available via Docker for full control (see frankfurter.dev).

For complete endpoint details with verified request/response examples, read
`references/endpoints.md`.
