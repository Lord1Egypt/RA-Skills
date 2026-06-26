# Reference — Series IDs, Units & Frequency

Quick lookups for choosing the right series and the right transform.

---

## Popular series IDs

| ID | Series | Native frequency | Native units |
|----|--------|------------------|--------------|
| `GDP` | Gross Domestic Product (nominal) | Quarterly | Billions of $ |
| `GDPC1` | Real GDP (chained 2017 $) | Quarterly | Billions of chained $ |
| `UNRATE` | Unemployment Rate | Monthly | Percent |
| `CPIAUCSL` | CPI, All Urban Consumers (SA) — inflation | Monthly | Index 1982-84=100 |
| `CPIAUCNS` | CPI, All Urban Consumers (NSA) | Monthly | Index 1982-84=100 |
| `FEDFUNDS` | Federal Funds Effective Rate | Monthly | Percent |
| `DGS10` | 10-Year Treasury Yield | Daily | Percent |
| `DGS2` | 2-Year Treasury Yield | Daily | Percent |
| `T10Y2Y` | 10Y–2Y Treasury Spread | Daily | Percent |
| `M2SL` | M2 Money Supply | Monthly | Billions of $ |
| `PAYEMS` | Total Nonfarm Payrolls | Monthly | Thousands of persons |
| `SP500` | S&P 500 Index | Daily | Index |
| `MORTGAGE30US` | 30-Year Fixed Mortgage Rate | Weekly | Percent |
| `DEXUSEU` | USD/EUR Exchange Rate | Daily | $ per Euro |

> Notes: prefer **SA** (seasonally adjusted) for trend reading. `CPIAUCSL` is an **index** — to report inflation use `units=pc1` (YoY %). Distinguish nominal (`GDP`) from real (`GDPC1`).

When unsure of an ID, use `fred_series_search` (prefer high `popularity` + exact-title match), then confirm with `fred_series`.

---

## Units enum (`units` parameter)

Apply the transform that matches the question — let FRED compute it; do **not** do the math by hand.

| Value | Meaning | Typical use |
|-------|---------|-------------|
| `lin` | Levels (no transform) — **default** | Raw value in native units |
| `chg` | Change | Absolute period-over-period change |
| `ch1` | Change from a year ago | Absolute YoY change |
| `pch` | Percent change | Period-over-period % |
| `pc1` | Percent change from a year ago (**YoY**) | Inflation rate, YoY growth |
| `pca` | Compounded annual rate of change | Annualized quarterly GDP growth |
| `cch` | Continuously compounded change | Log-difference change |
| `cca` | Continuously compounded annual rate | Annualized log change |
| `log` | Natural log | Log-scale modeling |

Common pairings:
- Inflation from CPI → `CPIAUCSL` + `pc1`.
- Monthly % change in payrolls → `PAYEMS` + `pch`.
- Annualized real GDP growth → `GDPC1` + `pca`.

---

## Frequency enum (`frequency` parameter)

You may **down-sample** to a coarser frequency than native; you cannot up-sample.

| Value | Meaning |
|-------|---------|
| `d` | Daily |
| `w` | Weekly |
| `bw` | Biweekly |
| `m` | Monthly |
| `q` | Quarterly |
| `sa` | Semiannual |
| `a` | Annual |

---

## Aggregation method (`aggregation_method`, used when down-sampling)

| Value | Meaning | Use when |
|-------|---------|----------|
| `avg` | Average (default) | Rates / indexes over a period |
| `sum` | Sum | Flows (e.g. monthly → annual total) |
| `eop` | End of period | Snapshot at period end (e.g. a rate) |

> Verification needed: confirm enums, defaults, and series specifics at <https://fred.stlouisfed.org/docs/api/fred/>.
