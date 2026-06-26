# Prompt — Series Discovery

## Purpose

Turn a vague economic concept into the **single best `series_id`** to use, by driving `fred_series_search` and picking correctly among results.

## Reusable template

```
You need the FRED series_id for: "{{concept}}".

Constraints:
- Geography/scope: {{scope}}            (e.g. "United States", "Euro area"; default United States)
- Seasonal adjustment: {{sa_pref}}      (prefer "Seasonally Adjusted" for trend reading)
- Frequency preference: {{freq_pref}}   (e.g. "Monthly"; or "any")
- Real vs nominal (if applicable): {{real_nominal}}

Steps:
1. Call fred_series_search with search_text="{{search_text}}", order_by="popularity", sort_order="desc", limit={{limit}}.
2. From the results, choose the series whose TITLE exactly matches "{{concept}}" and whose
   seasonal_adjustment/frequency/units fit the constraints. Prefer higher popularity.
3. Return: the chosen id, title, units, frequency, seasonal_adjustment, observation range — and a one-line reason.
4. If nothing fits, broaden or rephrase {{search_text}} and try once more.

Do NOT fetch observations yet. Do NOT invent an id.
```

## Variables

| Variable | Meaning | Example |
|----------|---------|---------|
| `{{concept}}` | Human concept | "U.S. inflation (CPI)" |
| `{{search_text}}` | Keywords for search | "consumer price index all items" |
| `{{scope}}` | Geography/scope | "United States" |
| `{{sa_pref}}` | SA preference | "Seasonally Adjusted" |
| `{{freq_pref}}` | Frequency | "Monthly" |
| `{{real_nominal}}` | Real or nominal | "n/a" |
| `{{limit}}` | Result count | 5 |

## Example (filled)

```
You need the FRED series_id for: "U.S. inflation (CPI)".
Constraints: scope United States; Seasonally Adjusted; Monthly; real_nominal n/a.
Steps: search_text="consumer price index all items", order_by="popularity", sort_order="desc", limit=5 ...
```

Expected pick: `CPIAUCSL` — "CPI for All Urban Consumers: All Items", Monthly, Seasonally Adjusted, Index 1982-84=100.

## Bad

> "The series is probably `INFLATION`." — Invented ID, no search, no confirmation.

## Good

> Searched, compared titles, chose `CPIAUCSL` (highest popularity, exact title, SA, Monthly), and noted it's an **index** (so inflation needs `units=pc1`).
