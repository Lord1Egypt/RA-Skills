# Request and output contract

The self-contained Node 20+ helper has two commands. The npm corpus CLI exposes them as `defi-data-skills snapshot` and `defi-data-skills history`.

## Snapshot

`node scripts/market-data.mjs snapshot --ids bitcoin,ethereum --provider both --max-age 300 --max-skew 120`

- `--ids`: 1–10 distinct lowercase CoinGecko IDs, each up to 100 characters. Default `bitcoin,ethereum`; ticker-only identification is not performed.
- `--provider`: `both` (default), `coingecko` or `defillama`.
- `--max-age`: 1–86,400 seconds. Default 300; a provider observation more than 60 seconds in the future fails.
- `--max-skew`: 0–3,600 seconds. Default 120. Only aligned fresh rows get a numerical price spread.

CoinGecko uses the public `https://api.coingecko.com/api/v3/simple/price` endpoint with bounded IDs, USD and `include_last_updated_at=true`. DefiLlama uses `https://coins.llama.fi/prices/current/` with `coingecko:<id>` keys. There is at most one request per provider. No environment values are read.

The result includes `status` (`complete`, `partial`, `unavailable`), normalized parameters, `reads`, comparisons and limitations. `reads` retain provider/source, SHA-256 of successful raw bytes and row-level observations. A valid row includes a finite `priceUsd` from `1e-12` to `1e12`, exact identity, observed/retrieved ISO times and age. Missing, stale or malformed rows include `ok:false` and a stable error. Source URLs contain no credentials.

For both providers, spread = absolute mark difference / arithmetic mean × 100, provided each row passed freshness and the timestamp difference is within `maxSkewSeconds`. The documented price bounds also prevent intermediate arithmetic overflow. It is a discrepancy measure, not a consensus price or oracle test. `incomplete` and `unaligned` comparisons have `spreadPct:null`.

## History

`node scripts/market-data.mjs history --id bitcoin --days 180`

`--days` is 91–365 so automatic CoinGecko granularity is daily; defaults are Bitcoin and 180. No interval override, Pro host, API key or paid fallback is used. One fixed public market-chart GET is bounded to 2 MiB and 10 seconds. Public keyless access is tested separately from the documented Demo key requirement.

A successful envelope includes `parameters`, `dataset`, `excludedTrailingObservation` and limitations. The dataset uses schema version 1, USD, interval 86,400 seconds, `priceType:aggregate-snapshot`, exact provider identity, source/retrieval/raw SHA-256 and `{timestamp,close}` rows at 00:00 UTC. The word `close` is a model field; this is an aggregate sample, not a venue candle close.

All response timestamps must be ascending, unique and no later than retrieval. Only one trailing non-midnight observation on the current UTC day is excluded. Other intraday samples fail. Daily gaps fail; at least `days-1` samples are required, and the most recent daily sample must be today or yesterday. A young or partially covered asset reports insufficient history rather than shortening the experiment silently.

The standalone strategy CLI accepts this successful envelope as its data input and hashes its exact file bytes. You can also extract the `dataset` object using the host's existing JSON tooling. A history failure is not a valid dataset.

## Failures and local handling

Malformed options fail before network access. HTTP 401/403 map to `authentication_required`, 402 to `payment_required`, and 429 to `rate_limited`; numeric Retry-After up to one hour is retained. The helper performs no retries. Other transport/schema failures use `network_error`, `timeout`, `http_error`, `invalid_content_type`, `invalid_json`, `response_too_large`, `missing_observation`, `stale_observation`, `future_timestamp`, `invalid_confidence`, `invalid_history_observation`, `unexpected_history_granularity`, `gapped_history`, `insufficient_history`, `unexpected_history_range` or `stale_history`.

Raw network errors, response bodies and headers are never echoed. Preserve useful partial evidence and original timestamps. Use the existing authorized provider path to resolve access or coverage; do not silently widen a query, enroll a plan, lower the freshness rule or turn errors into zeros.
