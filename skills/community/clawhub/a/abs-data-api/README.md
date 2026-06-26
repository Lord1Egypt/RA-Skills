# ABS Data API Skill

Query Australian Bureau of Statistics data through the ABS Data API with a workflow designed for OpenClaw agents and practical human use.

This skill translates natural-language data requests into ABS API queries, returns structured results with human-readable labels, adds analyst-grade citations, and supports polished outputs: readable tables, JSON with labels, charts, summary briefs, and macro reports.

---

## Overview

The ABS Data API exposes a large SDMX-based statistical service. That is powerful, but raw SDMX is not friendly. Dataset IDs, dimension keys, codelists, versions, and geography structures can turn a simple question into a small bureaucratic hostage situation.

This skill exists to reduce that pain.

It provides:
- dataset discovery via natural-language search with ambiguity detection
- metadata caching so repeated queries are faster and lighter
- structured metadata (no more markdown parsing at runtime)
- 20 validated preset queries for common economic indicators
- direct querying of ABS datasets with dimension keys
- readable text, table, CSV, and JSON output (with friendly labels)
- human-readable period rendering (January 2026, December quarter 2025)
- `--summary latest` mode: latest value + change context + short brief
- `--report macro-snapshot` mode: compact macro briefing from presets
- `--describe-preset` mode: full documentation for each preset
- analyst-style source footnotes for polished summaries
- chart output with improved titles and latest-point annotation
- validation test script for all presets

---

## What's included

```text
abs-data-api/
├── SKILL.md
├── README.md
├── presets.json
├── metadata.overrides.json
├── scripts/
│   ├── abs_cache.py
│   ├── abs_query.py
│   ├── abs_search.py
│   └── test_presets.py
└── references/
    ├── api-guide.md
    ├── dataset-catalog.md
    └── sdmx-patterns.md
```

---

## Quick start

```bash
# 1. Warm the cache (once; auto-refreshes after 24h)
python3 scripts/abs_cache.py refresh
python3 scripts/abs_cache.py gen-metadata

# 2. Search for a dataset
python3 scripts/abs_search.py "unemployment rate"
python3 scripts/abs_search.py "house prices"

# 3. List presets
python3 scripts/abs_query.py --list-presets

# 4. Query latest CPI inflation
python3 scripts/abs_query.py --preset cpi-annual-change --latest --format table

# 5. Summary brief with change context
python3 scripts/abs_query.py --preset cpi-annual-change --summary latest
python3 scripts/abs_query.py --preset unemployment-rate --summary latest

# 6. Macro snapshot report
python3 scripts/abs_query.py --report macro-snapshot

# 7. Describe a preset
python3 scripts/abs_query.py --describe-preset cpi-annual-change
```

---

## Preset queries (validated)

All 20 presets are validated live against the ABS API. Run `--list-presets` for the full list, `--describe-preset <name>` for detail.

| Preset | Dataflow | Description |
|---|---|---|
| `cpi-all-groups` | CPI | CPI All Groups Index (Monthly) |
| `cpi-annual-change` | CPI | CPI Annual % Change (Monthly) |
| `cpi-quarterly` | CPI | CPI All Groups Index (Quarterly) |
| `unemployment-rate` | LF | Unemployment Rate — Seasonally Adjusted |
| `unemployment-original` | LF | Unemployment Rate — Original |
| `participation-rate` | LF_UNDER | Participation Rate — Seasonally Adjusted |
| `employment-level` | LF | Employed Persons (thousands) — Seasonally Adjusted |
| `labour-force-size` | LF_UNDER | Total Labour Force (thousands) — Seasonally Adjusted |
| `underemployment-rate` | LF_UNDER | Underemployment Rate — Seasonally Adjusted |
| `gdp-chain-volume` | ANA_AGG | GDP Chain Volume Measures — Seasonally Adjusted |
| `gdp-annual-change` | ANA_AGG | GDP Annual % Change — Seasonally Adjusted |
| `wage-index` | WPI | Wage Price Index — All Industries |
| `wage-annual-change` | WPI | WPI Annual % Change — All Industries |
| `population-national` | ERP_Q | ERP Australia (Quarterly) |
| `dwelling-prices-mean` | RES_DWELL_ST | Mean Dwelling Price Australia ($000s) |
| `trade-balance` | ITGS | Goods Trade Balance — Seasonally Adjusted |
| `goods-exports` | ITGS | Total Goods Exports — Seasonally Adjusted |
| `goods-imports` | ITGS | Total Goods Imports — Seasonally Adjusted |
| `household-spending-change` | HSI_M | Household Spending Annual % Change |

---

## Usage examples

### Latest CPI inflation

```bash
python3 scripts/abs_query.py --preset cpi-annual-change --latest --format table
```

Output:
```
| MEASURE                               | INDEX  | TSEST    | REGION    | FREQ    | TIME_PERIOD   | VALUE |
| ------------------------------------- | ------ | -------- | --------- | ------- | ------------- | ----- |
| Percentage change from previous year  | 10001  | Original | Australia | Monthly | January 2026  | 3.800 |

Source: Australian Bureau of Statistics, *Consumer Price Index* (Cat. 6401.0; dataset `CPI`; v2.0.0). January 2026. ...
```

### GDP growth table

```bash
python3 scripts/abs_query.py --preset gdp-annual-change --start-period 2024-Q1 --format table --citation-style analyst
```

Output includes quarter labels like "March quarter 2024", "December quarter 2025".

### Summary brief (latest plus context)

```bash
python3 scripts/abs_query.py --preset unemployment-rate --summary latest
```

Output:
```
──────────────────────────────────────────────────
  Labour Force
  Preset: unemployment-rate
──────────────────────────────────────────────────
  Latest:   4.278  (February 2026)
  Previous: 4.095  (January 2026)
  Change:   +0.183  (+4.47%)

  Summary: Labour Force was 4.28 in February 2026, up from 4.10 in January 2026.

  Source: Australian Bureau of Statistics, ...
```

### Macro snapshot report

```bash
python3 scripts/abs_query.py --report macro-snapshot
```

Output:
```
==============================================================
  AUSTRALIAN MACRO SNAPSHOT
  Source: ABS Data API | Generated by abs-data-api skill
==============================================================

  Inflation (CPI)                       3.80  (January 2026)  → +0.00%
  GDP Growth                            0.80  (December quarter 2025)  ▲ +60.00%
  Unemployment Rate                     4.28  (February 2026)  ▲ +5.03%
  Wage Growth (WPI)                     3.50  (December quarter 2025)  ▼ -5.41%
  Participation Rate                   66.89  (February 2026)  ▲ +0.33%
  Population (ERP)                27,724,744  (September quarter 2025)  ▲ +0.40%
  ...
```

### Describe a preset

```bash
python3 scripts/abs_query.py --describe-preset cpi-annual-change
```

Output:
```
Preset: cpi-annual-change
──────────────────────────
Description:     CPI All Groups - Annual % Change (Original, Australia, Monthly)
Dataflow:        CPI
Key:             3.10001.10.50.M
What it measures: Inflation rate: how much consumer prices have risen compared to the same month last year
When to use:     Best single number for current inflation rate; use for media-style briefings
Technical note:  Year-on-year CPI percentage change for Australia. MEASURE=3. Source: ABS 6401.0
```

### Census-style geography lookup

```bash
python3 scripts/abs_search.py "Brisbane population SA2"
python3 scripts/abs_query.py ERP_ASGS2021 all --format table
python3 scripts/abs_cache.py structure ERP_ASGS2021 1.0.0
```

### Analyst citation mode

```bash
python3 scripts/abs_query.py --preset gdp-chain-volume --start-period 2025-Q1 --format table --citation-style analyst
```

Output:
```
Sources
- Australian Bureau of Statistics, *Australian National Accounts Key Aggregates* (Cat. 5206.0; dataset `ANA_AGG`; v1.0.0), March quarter 2025 to December quarter 2025, via ABS Data API
```

### JSON output with friendly labels

```bash
python3 scripts/abs_query.py --preset unemployment-rate --latest --format json
```

Each dimension gets a `*_label` field alongside its raw code:
```json
{
  "MEASURE": "M13",
  "MEASURE_label": "Unemployment rate",
  "SEX": "3",
  "SEX_label": "Persons",
  "TSEST": "20",
  "TSEST_label": "Seasonally Adjusted",
  "TIME_PERIOD": "2026-02",
  "TIME_PERIOD_rendered": "February 2026",
  "value": 4.277
}
```

### Search with ambiguity detection

```bash
python3 scripts/abs_search.py "inflation"
```

Output:
```
Found 3 dataset(s) for: 'inflation'

  ID: CPI  (Quarterly — official)
  ID: CPI_M  (Monthly — experimental)
  ID: PPI  (producer prices)

Ambiguity detected:

  [FREQUENCY] Multiple frequencies available (e.g. monthly vs quarterly)
  → Do you want monthly or quarterly data? (Monthly CPI Indicator is experimental; Quarterly CPI is the official series.)
```

### Chart with dataset name and annotated latest

```bash
python3 scripts/abs_query.py --preset gdp-chain-volume --start-period 2020-Q1 --chart
```

Chart saved to `/tmp/abs_ana_agg.png` with:
- Title: dataset name ("Australian National Accounts Key Aggregates")
- Subtitle: source and period range
- Latest point annotated with value

### Validate all presets

```bash
python3 scripts/test_presets.py
python3 scripts/test_presets.py --preset cpi-annual-change    # single preset
python3 scripts/test_presets.py --verbose                     # show timing
```

---

## Search-first workflow

```bash
# Find the right dataset
python3 scripts/abs_search.py "housing prices state"
python3 scripts/abs_search.py "GDP income approach"
python3 scripts/abs_search.py "population growth"

# Inspect structure
python3 scripts/abs_cache.py structure RES_DWELL_ST 1.0.0

# Query directly
python3 scripts/abs_query.py RES_DWELL_ST 5.AUS.Q --latest --format table
```

---

## Output modes

| Flag | Output |
|---|---|
| *(default)* | Human-readable text with friendly labels + citation |
| `--format table` | Markdown table with friendly labels and rendered periods |
| `--format csv` | CSV with dimension codes + citation comment |
| `--format json` | JSON with raw codes + `*_label` fields + `TIME_PERIOD_rendered` |
| `--chart` | PNG chart (requires matplotlib) with dataset title and latest annotation |
| `--summary latest` | Latest value + previous + change + short text brief |
| `--report macro-snapshot` | Compact multi-indicator macro briefing |
| `--citation-style analyst` | Analyst-style source footnote block |
| `--flat-view` | AllDimensions format (wider response; may return large datasets) |

---

## Metadata architecture

From v1.0.1, runtime metadata is structured rather than parsed from markdown:

- **`~/.cache/abs-data-api/metadata.generated.json`** — auto-generated from presets + catalog
- **`metadata.overrides.json`** — thin manual override file in skill dir for discontinued datasets, nicer labels, or corrections
- Catalog and generated metadata are merged at query time

The `dataset-catalog.md` reference file is for humans. Runtime code uses structured metadata.

To regenerate:
```bash
python3 scripts/abs_cache.py gen-metadata
```

---

## Cache management

| Command | Description |
|---|---|
| `abs_cache.py refresh` | Fetch all dataflows from ABS API |
| `abs_cache.py gen-metadata` | Build metadata.generated.json from presets + catalog |
| `abs_cache.py status` | Show cache age, counts, metadata status |
| `abs_cache.py search <term>` | Search across all cached dataflows |
| `abs_cache.py structure <ID>` | Fetch and cache DSD for a dataflow |

---

## Known caveats and deferred items

### 1. RPPI is stale in the API
`RPPI` (Residential Property Price Index) only has data to ~2021-Q4 via the API. Use `RES_DWELL_ST` for current mean dwelling prices (validated to 2025-Q4).

### 2. RT Retail Trade is discontinued
`RT` was discontinued after June 2025. Prefer `HSI_M` (Household Spending Indicator) for current household spending analysis.

`BUSINESS_TURNOVER` is also ceased and is intentionally **not** included as an active preset in v1.0.1, to avoid encouraging stale series in current analysis.

### 3. Population growth rate not available as direct preset
Population growth rate requires two observations and division. The `population-national` preset returns the level; compute growth manually or use `--summary latest` which shows the change.

### 4. Broad queries can explode
Using `all` without a narrow key may return huge result sets. The skill warns when a query exceeds 100 observations.

### 5. Some datasets require fiddly dimension keys
Census-style geographic queries, detailed industry breakdowns, and age-sex-region cross-tabulations may require inspecting structure first with `abs_cache.py structure <ID>`.

---

## Recommended workflow for analysts

1. `abs_search.py <topic>` — find the dataset
2. `--list-presets` or `--describe-preset <name>` — check for a shortcut
3. `abs_cache.py structure <ID>` if no preset and key is unclear
4. `--preset <name>` or direct `<ID> <KEY>` query
5. `--summary latest` for quick brief; `--format table --citation-style analyst` for polished output
6. `--report macro-snapshot` for a full economic snapshot

---

## Validated test results (v1.0.1)

All 20 presets pass live API validation. Run `python3 scripts/test_presets.py` to re-verify.

```
[PASS]  cpi-all-groups           101.33 (2026-01)
[PASS]  cpi-annual-change        3.8 (2026-01)
[PASS]  unemployment-rate        4.28 (2026-02)
[PASS]  participation-rate       66.89 (2026-02)
[PASS]  employment-level         10116.95 (2026-02)
[PASS]  underemployment-rate     5.85 (2026-02)
[PASS]  gdp-annual-change        0.8 (2025-Q4)
[PASS]  wage-annual-change       3.5 (2025-Q4)
[PASS]  population-national      27724744 (2025-Q3)
[PASS]  dwelling-prices-mean     1074.7 (2025-Q4)
[PASS]  trade-balance            2631 (2026-01)
[PASS]  household-spending-change 4.6 (2026-01)
... (20/20 passed)
```
