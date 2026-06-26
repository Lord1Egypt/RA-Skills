# Recipe — Fetch a Single Indicator

## Goal

Get the **latest value** (and recent trend) of one economic indicator and report it with a citation.

## When

The user asks "What is the current X?" — e.g. unemployment rate, federal funds rate, 30-year mortgage rate.

## Inputs

- A concept or a known `series_id`.
- Optional: how many recent points to show.

## Steps

1. **Resolve the series.** If the ID is unknown, call `fred_series_search`. Otherwise use the known ID (see `../reference/series-and-units.md`).
2. **Confirm units/frequency** with `fred_series` (so you report it correctly).
3. **Fetch the latest** observations with `fred_series_observations` (`sort_order=desc`, small `limit`, native `units=lin`).
4. **Cite** the value.

## Output

The latest value, its observation date, brief context, and a citation.

## Example

User: *"What is the current U.S. unemployment rate?"*

```json
{ "tool": "fred_series", "arguments": { "series_id": "UNRATE" } }
```

```json
{ "tool": "fred_series_observations",
  "arguments": { "series_id": "UNRATE", "sort_order": "desc", "limit": 3 } }
```

```json
{
  "observations": [
    { "date": "2024-04-01", "value": "3.9", "realtime_start": "2024-05-03", "realtime_end": "9999-12-31" },
    { "date": "2024-03-01", "value": "3.8", "realtime_start": "2024-04-05", "realtime_end": "9999-12-31" },
    { "date": "2024-02-01", "value": "3.9", "realtime_start": "2024-03-08", "realtime_end": "9999-12-31" }
  ],
  "count": 3, "units": "lin"
}
```

Answer:

> The U.S. unemployment rate was **3.9%** in April 2024 (up from 3.8% in March), hovering in the high-3% range.
> *Source: FRED, series `UNRATE`, retrieved 2026-05-31, <https://fred.stlouisfed.org/series/UNRATE>. Seasonally adjusted; subject to revision.*

## Edge cases

- **Empty result** → widen the date range or re-verify the ID; never guess.
- **`value` is `"."`** → that period is missing; report the most recent non-missing value and say so.
- **Index-type series** (e.g. CPI) → don't report the raw index as a "rate"; use a YoY recipe instead.

## Production notes

- Cache the latest value briefly; most series update monthly.
- Skip the metadata call if you already know the series' units (saves a request).
