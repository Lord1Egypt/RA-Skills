# Recipe — Compare Two Series

## Goal

Compare two economic series over the same period — e.g. unemployment vs. inflation, or 10-year vs. 2-year Treasury yields.

## When

The user asks to relate two indicators ("compare X and Y", "how do rates and inflation move together", "what's the yield curve doing").

## Inputs

- Two concepts or known `series_id`s.
- A shared date range and a comparable view (same `units`/`frequency`).

## Steps

1. **Resolve both series** (`fred_series_search` as needed).
2. **Align the comparison**: pick the **same** `frequency` and a **comparable** `units` (often both `lin`, or both `pc1` for growth/inflation). Use the **same** `observation_start`/`observation_end`.
3. **Fetch each** with `fred_series_observations`.
4. **Compare** on matching dates; describe the relationship.
5. **Cite both** series separately.

> If the two series have different native frequencies (e.g. daily `DGS10` vs. daily `DGS2` is fine; daily vs. monthly is not), down-sample the finer one with `frequency` + `aggregation_method` so dates line up.

## Output

A side-by-side comparison and a short interpretation, each value cited.

## Example

User: *"Is the yield curve inverted? Compare the 10-year and 2-year Treasury yields."*

```json
{ "tool": "fred_series_observations",
  "arguments": { "series_id": "DGS10", "observation_start": "2024-04-01", "sort_order": "desc", "limit": 1 } }
```

```json
{ "tool": "fred_series_observations",
  "arguments": { "series_id": "DGS2", "observation_start": "2024-04-01", "sort_order": "desc", "limit": 1 } }
```

```json
{ "observations": [ { "date": "2024-04-30", "value": "4.69", "realtime_start": "2024-05-01", "realtime_end": "9999-12-31" } ], "count": 1, "units": "lin" }
```
```json
{ "observations": [ { "date": "2024-04-30", "value": "5.04", "realtime_start": "2024-05-01", "realtime_end": "9999-12-31" } ], "count": 1, "units": "lin" }
```

Answer:

> On 2024-04-30 the 10-year Treasury yield was **4.69%** and the 2-year was **5.04%** — the 2-year is higher, so the curve was **inverted** (a 10Y–2Y spread of about **-0.35 pp**).
> *Sources: FRED, series `DGS10` and `DGS2`, retrieved 2026-05-31, <https://fred.stlouisfed.org/series/DGS10> and <https://fred.stlouisfed.org/series/DGS2>. Subject to revision.*

> Tip: FRED also publishes the spread directly as `T10Y2Y` — one call instead of two.

## Edge cases

- **Mismatched dates** (different missing days) → compare only dates present in both; or use a single combined series like `T10Y2Y`.
- **Mismatched frequency** → down-sample the finer series.
- **Mismatched units** → convert both to a comparable transform (e.g. both `pc1`).

## Production notes

- Prefer a single pre-computed series (e.g. `T10Y2Y`) when one exists — fewer calls, fewer alignment bugs.
- Cache both pulls; reuse for follow-up questions.
