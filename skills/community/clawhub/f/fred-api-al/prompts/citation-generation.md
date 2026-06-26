# Prompt — Citation Generation

## Purpose

Produce a correct, consistent citation for every FRED value reported, so the answer is verifiable and honest about freshness/revisions.

## Reusable template

```
Write a citation for a value taken from FRED.

Inputs:
- series_id:        {{series_id}}
- series_title:     {{series_title}}
- observation_date: {{observation_date}}   (the period the value refers to)
- value:            {{value}}              (with its units / transform)
- units_transform:  {{units}}             (lin/pch/pc1/... ; omit if lin)
- seasonal_adj:     {{seasonal_adjustment}}
- retrieved_date:   {{today}}

Produce, inline after the figure:
"({{value}} — FRED, series {{series_id}}{{#units}} (units={{units}}){{/units}}, retrieved {{today}},
 https://fred.stlouisfed.org/series/{{series_id}}; {{seasonal_adjustment}}; subject to revision)."

Rules:
- ALWAYS include series_id, observation_date context, retrieved_date, and the URL.
- Note the transform if not lin (e.g. pc1 = year-over-year %).
- Note SA/NSA and "subject to revision".
- Never include or reference the API key.
```

## Variables

| Variable | Meaning |
|----------|---------|
| `{{series_id}}` | FRED series ID |
| `{{series_title}}` | Series name |
| `{{observation_date}}` | Date the value belongs to |
| `{{value}}` | The reported number |
| `{{units}}` | Transform applied (omit if `lin`) |
| `{{seasonal_adjustment}}` | SA / NSA |
| `{{today}}` | Retrieval date |

## Example (filled)

> "Headline CPI inflation was **3.4%** in April 2024 (FRED, series `CPIAUCSL` (units=pc1), retrieved 2026-05-31, <https://fred.stlouisfed.org/series/CPIAUCSL>; seasonally adjusted; subject to revision)."

## Bad

> "Inflation is 3.4%." — No source, no series ID, no date, no URL; unverifiable.

## Good

> "U.S. headline CPI inflation was **3.4% year-over-year** in **April 2024** (FRED, series `CPIAUCSL`, units=pc1, retrieved **2026-05-31**, <https://fred.stlouisfed.org/series/CPIAUCSL>; SA; subject to revision)."
