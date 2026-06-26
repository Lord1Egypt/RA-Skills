# Recipe — Year-over-Year Change

## Goal

Report the **year-over-year (YoY) percent change** of a series — the standard way to express inflation and growth.

## When

The user asks "What is the inflation rate?", "How fast is X growing year over year?", or any YoY comparison. Especially for **index** series (CPI), where the raw level is not directly meaningful.

## Inputs

- A concept or known `series_id`.
- Optional: how many recent months/quarters.

## Steps

1. **Resolve the series** (`fred_series_search` if needed; e.g. CPI → `CPIAUCSL`).
2. **Confirm it's an index/level** with `fred_series` — confirming why YoY is appropriate.
3. **Fetch with `units=pc1`** (percent change from a year ago) via `fred_series_observations`.
4. **Cite**, noting the transform.

> Use `pc1` — let FRED compute the YoY change. Do **not** subtract index values by hand.

## Output

YoY % values per period, the latest reading, and a citation.

## Example

User: *"What's the current U.S. inflation rate?"*

```json
{ "tool": "fred_series_observations",
  "arguments": { "series_id": "CPIAUCSL", "units": "pc1", "observation_start": "2023-04-01", "sort_order": "desc", "limit": 6 } }
```

```json
{
  "observations": [
    { "date": "2024-04-01", "value": "3.4", "realtime_start": "2024-05-15", "realtime_end": "9999-12-31" },
    { "date": "2024-03-01", "value": "3.5", "realtime_start": "2024-04-10", "realtime_end": "9999-12-31" },
    { "date": "2024-02-01", "value": "3.2", "realtime_start": "2024-03-12", "realtime_end": "9999-12-31" }
  ],
  "count": 6, "units": "pc1"
}
```

Answer:

> U.S. headline CPI inflation was **3.4% year-over-year** in April 2024 (vs. 3.5% in March).
> *Source: FRED, series `CPIAUCSL` (`units=pc1`), retrieved 2026-05-31, <https://fred.stlouisfed.org/series/CPIAUCSL>. Seasonally adjusted; subject to revision.*

## Edge cases

- **Range too short** → `pc1` needs a year of prior data; start at least 12+ periods earlier.
- **Missing periods (`"."`)** → skip them; don't interpolate.
- **NSA vs. SA** → for headline inflation, SA (`CPIAUCSL`) is standard; mention if you use NSA (`CPIAUCNS`).

## Production notes

- One call returns the full YoY series — don't loop per month.
- Cache results; CPI updates monthly.
