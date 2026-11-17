# forecast-consensus-comparison — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**17 endpoints across 3 platform group(s).**

## Polymarket (6)

### `polymarket_event_detail`

- **HTTP:** `GET /polymarket/event/{slug}`
- **What:** Get Polymarket event detail. Returns one Polymarket event. This endpoint does not require a Polymarket user token, wallet signature, cookies, or personal account authentication.
- **Params:** `slug` (string, **required**) — Polymarket event slug

### `polymarket_market_detail`

- **HTTP:** `GET /polymarket/market/{id}`
- **What:** Get Polymarket market detail by id. Returns one Polymarket market. This endpoint does not require a Polymarket user token, wallet signature, cookies, or personal account authentication.
- **Params:** `id` (string, **required**) — Polymarket market id

### `polymarket_search`

- **HTTP:** `GET /polymarket/search`
- **What:** Search Polymarket events. Searches Polymarket and returns event results. The `status` enum accepts `open`, `closed`, and `all`; the `sort` enum accepts `relevance`, `volume24hr`, `volume`, `liquidity`, and `endDate`.
- **Params:** `ascending` (boolean, optional) — Sort ascending when true; `include_profiles` (boolean, optional) — Include matching profiles; `include_tags` (boolean, optional) — Include matching tags; `limit` (integer, optional) — Maximum events, defaults to 10 and supports up to 50; `q` (string, **required**) — Search query; `sort` (string, optional) — Search sort; `status` (string, optional) — Event status filter

### `polymarket_token_midpoint`

- **HTTP:** `GET /polymarket/token/{token_id}/midpoint`
- **What:** Get Polymarket token midpoint. Returns the current midpoint price for one Polymarket outcome token, identified by the required `token_id`, as a single `midpoint` number such as 0.285. It is a read-only snapshot, returned with a `fetched_at` time and the `token_id`, and is not investment advice.
- **Params:** `token_id` (string, **required**) — Polymarket CLOB token id

### `polymarket_token_price_history`

- **HTTP:** `GET /polymarket/token/{token_id}/price-history`
- **What:** Get Polymarket token price history. Returns price history points for one Polymarket outcome token, identified by the required `token_id`. `interval` is one of `1m`, `1h`, `6h`, `1d` (default), `1w`, `all` or `max`; `fidelity` sets minutes per point (0 means 60, max 1440); `start_ts` and `end_ts` bound the range. Each point has a Unix `timestamp` and `price`. No points returns 404.
- **Params:** `end_ts` (integer, optional) — Optional Unix timestamp upper bound; `fidelity` (integer, optional) — Data point resolution in minutes; 0 uses the default 60; maximum 1440; `interval` (string, optional) — History interval; `start_ts` (integer, optional) — Optional Unix timestamp lower bound; `token_id` (string, **required**) — Polymarket CLOB token id

### `polymarket_token_spread`

- **HTTP:** `GET /polymarket/token/{token_id}/spread`
- **What:** Get Polymarket token spread. Returns the current bid-ask spread for one Polymarket outcome token, identified by the required `token_id`, as a single `spread` number. It is a read-only snapshot with a `fetched_at` time and is not investment advice.
- **Params:** `token_id` (string, **required**) — Polymarket CLOB token id

## Kalshi (5)

### `kalshi_event`

- **HTTP:** `GET /kalshi/event/{event_ticker}`
- **What:** Kalshi event detail. Returns one Kalshi event by `event_ticker` (such as `KXELONMARS-99`) together with its markets. The event has its series ticker, title, subtitle, category, strike period and mutually-exclusive flag; each market has prices, bid and ask, volume, open interest, status and rules. An unknown ticker returns a not-found error.
- **Params:** `event_ticker` (string, **required**) — Kalshi event ticker

### `kalshi_market`

- **HTTP:** `GET /kalshi/market/{ticker}`
- **What:** Kalshi market detail. Returns one Kalshi market by `ticker` (such as `KXELONMARS-99`). The response has the title, subtitle, event ticker, status, result, open, close and expiration times, last and previous price, yes and no bid and ask, volume, 24-hour volume, open interest, liquidity and rules text. An unknown ticker returns a not-found error.
- **Params:** `ticker` (string, **required**) — Kalshi market ticker

### `kalshi_market_history`

- **HTTP:** `GET /kalshi/market/{ticker}/history`
- **What:** Kalshi market history. Returns candlesticks for one Kalshi market by `ticker`. `series_ticker` defaults to the ticker prefix before the last dash, `start_ts` to 7 days ago, `end_ts` to now and `period_interval` to 1440 minutes. `include_latest_before_start` adds the last candle before the start. Ranges are capped at 366 days.
- **Params:** `end_ts` (integer, optional) — Unix end timestamp in seconds. Defaults to now.; `include_latest_before_start` (boolean, optional) — Include the latest candle before start_ts when supported upstream.; `period_interval` (integer, optional) — Candlestick interval in minutes. Default: 1440.; `series_ticker` (string, optional) — Kalshi series ticker. Defaults to the market ticker prefix before the last dash.; `start_ts` (integer, optional) — Unix start timestamp in seconds. Defaults to 7 days ago.; `ticker` (string, **required**) — Kalshi market ticker

### `kalshi_market_orderbook`

- **HTTP:** `GET /kalshi/market/{ticker}/orderbook`
- **What:** Kalshi market orderbook. Returns the order book for one Kalshi market by `ticker`: bid levels for the `yes` side and the `no` side, each with `price` and `size`. Kalshi publishes bids only, so ask levels are not listed. The response also carries a `raw_unit_hint` for the price unit.
- **Params:** `ticker` (string, **required**) — Kalshi market ticker

### `kalshi_markets`

- **HTTP:** `GET /kalshi/markets`
- **What:** Kalshi markets. Lists Kalshi markets, up to `limit` rows (default 25, max 200), continued with `cursor`. Filter by `event_ticker`, `series_ticker`, `ticker`, or `status` (`unopened`, `open`, `closed` or `settled`). Each market has its title, status, prices, bid and ask, volume, open interest and rules text. A returned status can read `active` even though the filter does not accept it.
- **Params:** `cursor` (string, optional) — Pagination cursor from a previous Kalshi response; `event_ticker` (string, optional) — Kalshi event ticker filter; `limit` (integer, optional) — Rows to return, default 25, max 200; `series_ticker` (string, optional) — Kalshi series ticker filter; `status` (string, optional) — Market status filter; `ticker` (string, optional) — Kalshi market ticker filter

## Metaculus (6)

### `metaculus_question`

- **HTTP:** `GET /metaculus/question/{id}`
- **What:** Metaculus question detail. Returns one Metaculus question by numeric `id` (a question or post id). The response has the title, status, question type, unit, open, close and resolve times, forecaster and forecast counts, comment count, latest forecast center and bounds, categories, projects and URL.
- **Params:** `id` (string, **required**) — Metaculus question or post id

### `metaculus_question_forecast_history`

- **HTTP:** `GET /metaculus/question/{id}/forecast-history`
- **What:** Metaculus question forecast history. Returns public aggregation forecast history points for one Metaculus question. The `method` enum accepts `recency_weighted`, `unweighted`, and `single_aggregation`.
- **Params:** `id` (string, **required**) — Metaculus question or post id; `max_points` (integer, optional) — Maximum history points to return, default 500, max 2000; `method` (string, optional) — Aggregation method

### `metaculus_question_forecasts`

- **HTTP:** `GET /metaculus/question/{id}/forecasts`
- **What:** Metaculus question forecasts. Returns the latest forecast summary per aggregation method for one Metaculus question, by numeric `id`. Each method has its name, forecaster count, center, lower and upper values, and number of history points. `recency_weighted`, `unweighted` and `single_aggregation` are listed first when present. The question details come with it.
- **Params:** `id` (string, **required**) — Metaculus question or post id

### `metaculus_question_metadata`

- **HTTP:** `GET /metaculus/question/{id}/metadata`
- **What:** Metaculus question metadata. Returns public metadata for one Metaculus question, including option labels, option history, scaling metadata, resolution fields, and timing fields when present.
- **Params:** `id` (string, **required**) — Metaculus question or post id

### `metaculus_question_options`

- **HTTP:** `GET /metaculus/question/{id}/options`
- **What:** Metaculus question options. Returns public multiple-choice option labels and latest option-level forecast values for one Metaculus question. The `method` enum accepts `recency_weighted`, `unweighted`, and `single_aggregation`.
- **Params:** `id` (string, **required**) — Metaculus question or post id; `method` (string, optional) — Aggregation method

### `metaculus_questions`

- **HTTP:** `GET /metaculus/questions`
- **What:** Metaculus questions. Returns Metaculus question rows. The endpoint fails closed, returning an error instead of partial data, when the source responds with an authenticated-only response or a challenge page.
- **Params:** `limit` (integer, optional) — Rows to return, default 10, max 25; `topic` (string, optional) — Optional Metaculus topic slug
