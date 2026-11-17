---
name: ephemeris-forecasting
description: Probabilistic time-series forecasting API. Forecast any numeric series the user supplies with uncertainty bands (quantile forecasts / prediction intervals) from a panel of zero-shot foundation models (Chronos-2, TimesFM, Toto, TiRex and more) that can route, run one model, or ensemble them. Use for sales and demand forecasting, inventory and capacity planning, web traffic and app metrics, energy load and solar/wind output, crypto and stock price ranges, weather and sensor/IoT readings, KPIs and budgets, with optional covariates such as price, promotions or holidays. Do not use for non-numeric prediction or to invent missing data.
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["EPHEMERIS_API_KEY"], "bins": ["curl"] },
        "primaryEnv": "EPHEMERIS_API_KEY",
        "emoji": "📈",
        "homepage": "https://ephemeris.cascade.industries"
      }
  }
---

# Forecasting with Ephemeris

Ephemeris forecasts numeric time series with a panel of zero-shot foundation models. It returns quantile forecasts (for example the 10th, 50th and 90th percentiles), so every forecast carries its own uncertainty band. Nothing is trained on the user's data. Full reference: https://ephemeris.cascade.industries/llms-full.txt

## Setup

1. Sign up at https://ephemeris.cascade.industries/sign-up (new accounts start with free credits) and create an API key in the dashboard. Keys start with `pc_live_`.
2. Give the key to OpenClaw as `EPHEMERIS_API_KEY` (for example `skills.entries.ephemeris-forecasting.apiKey` in `openclaw.json`, or your secret store). Never paste it into chat, code or files in a repository.

## Use cases

- **Sales and demand**: next weeks of orders, units or revenue per product or store, with promotions and prices as covariates; ranges for inventory and staffing.
- **Capacity and operations**: web traffic, API calls, queue depth, CPU and storage, call-centre volume.
- **Energy**: electricity load, solar and wind output, consumption per meter or site.
- **Markets**: crypto, stock, FX or commodity price and volatility ranges from the user's price history. These are statistical ranges, not trading advice; say so.
- **Weather and sensors**: temperature, humidity, air quality or any IoT reading the user has recorded (Ephemeris forecasts their series; it does not fetch weather data).
- **Business KPIs**: sign-ups, churn, budgets and spend.

Many series at once (up to 64 per call) suits per-SKU, per-store or per-sensor batches.

## Calling the API

Base URL `https://ephemeris.cascade.industries`, bearer auth on every call. Read the key from the environment; never print it.

Check the live panel once per session (model names, health, `max_horizon`, covariate support and prices):

```bash
curl -s https://ephemeris.cascade.industries/api/v1/models \
  -H "Authorization: Bearer $EPHEMERIS_API_KEY"
```

Forecast:

```bash
curl -s -X POST https://ephemeris.cascade.industries/api/v1/forecast \
  -H "Authorization: Bearer $EPHEMERIS_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: sales-2026-10-07-001" \
  -d '{
    "mode": "route",
    "series": [{ "values": [100.2, 101.4, 99.8, 103.1, 104.6, 102.2], "freq": "D" }],
    "horizon": 14,
    "quantiles": [0.1, 0.5, 0.9]
  }'
```

The response has one entry in `forecasts` per input series, each mapping a quantile level (`"0.1"`, `"0.5"`, ...) to `horizon` values, plus `meta.models_used`, `meta.notes` and `meta.billing` (`settled_mc` spent, `balance_mc` left; 1 credit = 1,000 mc). `GET /api/v1/balance` returns spendable credits.

Prefer MCP? Ephemeris is also a remote MCP server (Streamable HTTP) at `https://ephemeris.cascade.industries/api/mcp` with the same bearer header, exposing `forecast`, `list_models`, `get_balance` and `get_usage`.

## Workflow

1. **Get the data right first.** Use only the history the user gives you, oldest first. Do not pad, interpolate or invent points. Work out the sampling frequency (`"H"`, `"D"`, `"15min"`, ...) and the horizon in steps of that frequency (1 to 512).
2. **Pick the mode:**
   - `route` by default: Ephemeris picks the model that suits the data, at the cost of about one model.
   - `ensemble` when calibrated uncertainty matters more than cost (risk, capacity planning, anything the user will act on).
   - `explicit` with `"model": "<name>"` only when the user names a model; check in `/api/v1/models` that it supports the request.
3. **Several series?** Send up to 64 in one call. A multivariate series is an array of equal-length arrays, one per variate.
4. **Covariates** (known drivers such as price, promotions, holidays, weather): add `"covariates": {"past": {"price": [...same length as values...]}, "future": {"price": [...horizon values...]}}`. Only covariate-capable models use them; route and ensemble narrow to those automatically.
5. **Choose quantiles that answer the question**, e.g. `[0.1, 0.5, 0.9]` for an 80% interval, `[0.05, 0.5, 0.95]` for 90%.
6. **Report the band, not just the median.** Say what the interval means, which models were used, anything in `meta.notes`, and the credits spent.

## Costs, errors and safety

- Every successful forecast spends the user's credits. Do not forecast speculatively or in loops the user did not ask for; check the balance before large batches.
- Reuse the same `Idempotency-Key` when retrying so a retry is not charged twice.
- 400: fix the field the message names. 401: the key is missing or revoked. 402: out of credits; tell the user to top up (the response has a `topup_url`) rather than retrying. 429 and 503: wait (honour `Retry-After`) and retry with backoff.
