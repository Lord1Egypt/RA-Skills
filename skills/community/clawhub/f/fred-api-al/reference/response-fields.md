# Reference — Response Fields

What the FRED MCP tools return, what each field means, and how to cite it.

---

## Observations (`fred_series_observations`)

```json
{
  "observations": [
    { "date": "2024-04-01", "value": "3.9", "realtime_start": "2024-05-03", "realtime_end": "9999-12-31" }
  ],
  "count": 1,
  "units": "lin"
}
```

| Field | Type | Meaning |
|-------|------|---------|
| `observations` | array | The data points. |
| `observations[].date` | string `YYYY-MM-DD` | The period the value belongs to (start of period for monthly/quarterly). |
| `observations[].value` | **string** | The number — as a string. Parse before computing. **`"."` means missing.** |
| `observations[].realtime_start` | string | First date this value was the current vintage. |
| `observations[].realtime_end` | string | Last date this value was current; `9999-12-31` = still current. |
| `count` | number | Total observations matching the request. |
| `units` | string | The transform applied (`lin`, `pch`, `pc1`, …). |

### Handling values

- **Always parse** `value` from string to number.
- **`"."` = missing** — skip it, report "not available" for that period; **never** substitute a guess or zero.
- Keep the original precision FRED returns; round only for display and say so if it matters.

---

## Series metadata (`fred_series`, also returned by search/category/release)

```json
{
  "seriess": [
    { "id": "UNRATE", "title": "Unemployment Rate", "frequency": "Monthly", "units": "Percent",
      "seasonal_adjustment": "Seasonally Adjusted", "observation_start": "1948-01-01",
      "observation_end": "2024-04-01", "last_updated": "2024-05-03 07:43:01-05",
      "popularity": 92, "notes": "..." }
  ]
}
```

| Field | Meaning |
|-------|---------|
| `id` | The `series_id` (use this in calls and citations). |
| `title` | Human-readable name. |
| `frequency` | Native frequency (Daily/Weekly/Monthly/Quarterly/Annual). |
| `units` | Native units (Percent, Index, Billions of $, …). |
| `seasonal_adjustment` | SA / NSA — affects interpretation. |
| `observation_start` / `observation_end` | Available date range. |
| `last_updated` | When FRED last refreshed it — use for **freshness**. |
| `popularity` | Usage score (0–100) — helps pick among search results. |
| `notes` | Source, definition, methodology caveats. |

> The plural key is `seriess` (FRED's spelling), even for a single series.

---

## Realtime / vintages explained

FRED stores the **history of revisions**. `realtime_start`/`realtime_end` mark which time window a given value was the "as-known" figure.

- **Default**: you get the **latest** vintage (`realtime_end = 9999-12-31`).
- **As-of a past date**: pass `realtime_start`/`realtime_end` (via `fred_request` on `series/observations`) to see data as it was known then.
- **List vintage dates**: `fred_request` `endpoint: "series/vintagedates"`, `params: { "series_id": "<ID>" }`.

Always state that figures are **as of retrieval** and **subject to revision**.

---

## How to cite

Combine fields into a citation:

> FRED, series `<id>`, retrieved `<today>` — <https://fred.stlouisfed.org/series/<id>>

Include the **observation date** the value refers to. Example:

> "Unemployment was 3.9% in April 2024 (FRED, series `UNRATE`, retrieved 2026-05-31, <https://fred.stlouisfed.org/series/UNRATE>; seasonally adjusted, subject to revision)."

> Verification needed: confirm field names and vintage behavior at <https://fred.stlouisfed.org/docs/api/fred/>.
