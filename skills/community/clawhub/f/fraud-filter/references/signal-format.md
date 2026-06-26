# Signal Format & Score Calculation

Documentation of the anonymous signal schema and trust score formula used by fraud-filter.

---

## Trust Database Schema (`trust.json`)

The trust database is a flat JSON file keyed by SHA-256 hash of the normalized endpoint URL.

```json
{
  "version": "2026-03-15",
  "generated_at": "2026-03-15T04:00:00Z",
  "endpoint_count": 2847,
  "endpoints": {
    "<sha256_hex>": {
      "url_hint": "stockdata.xyz",
      "report_count": 347,
      "success_rate": 0.97,
      "median_price_usd": 0.03,
      "price_p10_usd": 0.02,
      "price_p90_usd": 0.05,
      "first_seen": "2026-01-20",
      "last_success": "2026-03-15",
      "last_failure": "2026-03-14",
      "failure_types": {
        "post_payment": 8,
        "pre_payment": 3
      },
      "warnings": [],
      "score": 94
    }
  }
}
```

### Field Definitions

| Field | Type | Description |
|---|---|---|
| `url_hint` | string | Hostname only (no path/query). For display in dashboards. |
| `report_count` | integer | Total number of anonymous signals received for this endpoint. |
| `success_rate` | float | Fraction of signals reporting success (0.0–1.0). |
| `median_price_usd` | float | Median price observed across all signals, in USD. |
| `price_p10_usd` | float | 10th percentile price (cheap end of normal). |
| `price_p90_usd` | float | 90th percentile price (expensive end of normal). |
| `first_seen` | date | Earliest signal date for this endpoint. |
| `last_success` | date | Most recent successful signal date. |
| `last_failure` | date \| null | Most recent failure signal date, or null if none. |
| `failure_types` | object | Counts by failure category: `post_payment` (paid but bad result), `pre_payment` (failed before payment completed). |
| `warnings` | string[] | Active warning flags (see Warning Flags below). |
| `score` | integer | Trust score 0–100 (see Score Calculation below). |

### URL Hashing

Endpoint URLs are normalized before hashing:

1. Lowercase the scheme and hostname
2. Remove default ports (`:80` for http, `:443` for https)
3. Remove trailing slashes from the path
4. Remove query parameters and fragments
5. SHA-256 hash the resulting string

Example:
```
Input:  https://API.StockData.xyz/report/AAPL?key=abc
Normal: https://api.stockdata.xyz/report/AAPL
Hash:   sha256:<hex>
```

The hash is used as the key in `trust.json` and in all signals. The `url_hint` field contains only the hostname for human readability.

---

## Signal Schema

### Anonymous outcome signal

Sent to `POST https://api.fraud-filter.com/reports`:

```json
{
  "endpoint_hash": "sha256:<hex>",
  "outcome": "success | post_payment_failure | pre_payment_failure",
  "amount_range": "0.01-0.10",
  "timestamp_bucket": "2026-03-15",
  "reporter_hash": "sha256:<install_id_hash>"
}
```

### Field Definitions

| Field | Type | Description |
|---|---|---|
| `endpoint_hash` | string | `sha256:` + hex hash of the normalized endpoint URL. |
| `outcome` | string | One of: `success`, `post_payment_failure`, `pre_payment_failure`. |
| `amount_range` | string | Bucketed price range (see Price Bucketing below). Never the exact amount. |
| `timestamp_bucket` | string | ISO date (day precision). Never exact timestamps. |
| `reporter_hash` | string | `sha256:` + hex hash of the local installation ID. For deduplication only. |

### Price Bucketing

Exact transaction amounts are never sent. Instead, amounts are bucketed:

| Actual Amount | Bucket |
|---|---|
| $0.001–$0.01 | `0.001-0.01` |
| $0.01–$0.10 | `0.01-0.10` |
| $0.10–$1.00 | `0.10-1.00` |
| $1.00–$10.00 | `1.00-10.00` |
| $10.00–$100.00 | `10.00-100.00` |
| $100.00+ | `100.00+` |

---

## Score Calculation

Trust score is an integer from 0 to 100, computed from five weighted factors.

### Formula

```
score = clamp(0, 100, round(
    base
  + success_factor
  + volume_factor
  + recency_penalty
  + stability_factor
  + age_factor
))
```

### Factors

#### Base Score
Every endpoint with at least one report starts at **50**.

#### Success Factor (weight: up to +40 / -40)

```
success_factor = (success_rate - 0.5) * 80
```

- 100% success → +40
- 97% success → +37.6
- 50% success → 0
- 20% success → -24

#### Volume Factor (weight: up to +10)

```
volume_factor = min(10, log10(report_count) * 5)
```

- 1 report → 0
- 10 reports → +5
- 100 reports → +10
- More reports increase confidence, capped at +10.

#### Recency Penalty (weight: up to -20)

Applied only when there are recent failures:

```
days_since_failure = (now - last_failure) in days
recency_penalty = days_since_failure < 7
  ? -20 + (days_since_failure * 2.86)   // -20 to 0 over 7 days
  : 0
```

- Failure today → -20
- Failure 3 days ago → -11.4
- Failure 7+ days ago → 0

#### Stability Factor (weight: up to -10)

Based on price volatility (p90/p10 ratio):

```
price_ratio = price_p90 / price_p10
stability_factor = price_ratio > 5 ? -10
                 : price_ratio > 3 ? -5
                 : 0
```

- Tight pricing (ratio < 3) → 0
- Moderate spread (3-5x) → -5
- Wild pricing (>5x) → -10

#### Age Factor (weight: up to -15)

New endpoints get a penalty regardless of success rate:

```
days_active = (now - first_seen) in days
age_factor = days_active < 30
  ? -15 + (days_active * 0.5)   // -15 to 0 over 30 days
  : 0
```

- Brand new → -15
- 2 weeks old → -8
- 30+ days → 0

### Warning Flags

Warning flags are derived from the endpoint data:

| Flag | Condition |
|---|---|
| `high_failure_rate` | success_rate < 0.70 |
| `volatile_pricing` | price_p90 / price_p10 > 5 |
| `recent_complaints` | last_failure within 3 days |
| `new_endpoint` | first_seen within 14 days |
| `limited_data` | report_count < 5 |
| `price_spike` | current median > 2x the 30-day-ago median (requires price history) |

### Recommendation Mapping

| Score | Recommendation |
|---|---|
| 70–100 | `allow` |
| 40–69 | `caution` |
| 0–39 | `block` |
| unknown | `allow` (absence of reports is not a risk signal) |

---

## Deduplication

- One signal per `reporter_hash` + `endpoint_hash` + `timestamp_bucket` (day) per outcome class.
- A reporter can send one `success` and one `post_payment_failure` for the same endpoint on the same day — these are distinct events.
- Duplicate signals (same reporter, endpoint, day, outcome) are silently dropped.

## Rate Limits

- Max 100 signals per `reporter_hash` per day (server-enforced).
- Clients should not send more than 1 signal per endpoint per outcome per day.
