---
name: abs-data-api
description: "Query Australian Bureau of Statistics (ABS) datasets via natural language and return data with citations. Use when: (1) the user asks about Australian economic indicators (CPI, inflation, GDP, wages, unemployment, retail trade, housing prices, job vacancies, population, births, deaths, migration, trade); (2) the user wants live ABS data or time series; (3) the user asks to compare ABS statistics across states, periods, or industries; (4) the user wants to visualise or export ABS data (chart, CSV, table); (5) any request referencing ABS catalogue numbers (e.g. 6401.0, 6202.0) or ABS dataset names. NOT for: Census DataPacks (use the census-database skill instead)."
---

# ABS Data API Skill

Query live ABS datasets, return data + citations, optional tables/charts/reports.

## Bundled Resources

| File | Purpose |
|---|---|
| `scripts/abs_cache.py` | Metadata cache manager — refresh catalog, search all 1,200+ dataflows, generate structured metadata |
| `scripts/abs_search.py` | NL → dataset mapper — curated lookup + fuzzy fallback + ambiguity detection |
| `scripts/abs_query.py` | Query engine — fetches data, formats output, summary/report/describe modes |
| `scripts/test_presets.py` | Preset validation — tests all presets against live API, pass/fail summary |
| `presets.json` | 20 validated preset queries for common indicators |
| `metadata.overrides.json` | Manual overrides for discontinued datasets and nicer labels |
| `references/dataset-catalog.md` | ~55 curated datasets with IDs, versions, notes (human reference) |
| `references/api-guide.md` | ABS API URL patterns, response structure, example queries |
| `references/sdmx-patterns.md` | Dimension codes (REGION, TSEST, FREQ, MEASURE) per dataset |

---

## Quick Start

```bash
# 1. Warm the cache (do once; auto-refreshes after 24h)
python3 scripts/abs_cache.py refresh
python3 scripts/abs_cache.py gen-metadata

# 2. Search for a dataset (with ambiguity hints)
python3 scripts/abs_search.py "unemployment rate"

# 3. List presets
python3 scripts/abs_query.py --list-presets

# 4. Describe a preset
python3 scripts/abs_query.py --describe-preset cpi-annual-change

# 5. Query latest
python3 scripts/abs_query.py --preset cpi-annual-change --latest --format table

# 6. Summary brief (latest + change context)
python3 scripts/abs_query.py --preset cpi-annual-change --summary latest

# 7. Macro snapshot
python3 scripts/abs_query.py --report macro-snapshot

# 8. Chart
python3 scripts/abs_query.py --preset gdp-chain-volume --start-period 2020-Q1 --chart
```

---

## Workflow

### Step 1 — Identify the dataset
1. Check `references/dataset-catalog.md` for the dataflow ID and version
2. If not found, run `python3 scripts/abs_search.py "<user query>"` for fuzzy match + ambiguity hints
3. If still not found, run `python3 scripts/abs_cache.py search "<term>"` (searches all 1,200+ dataflows)

### Step 2 — Determine dimension key
1. Check `presets.json` — if a preset exists, use it directly
2. Read `references/sdmx-patterns.md` for common dimension codes
3. For an unfamiliar dataset, fetch its structure:
   ```bash
   python3 scripts/abs_cache.py structure <ID> <VERSION>
   ```

### Step 3 — Query the data
```bash
python3 scripts/abs_query.py <ID> [KEY] [--version V] [--start-period P] [--end-period P] [--latest] [--format text|csv|json|table] [--chart] [--out FILE]
```

### Step 4 — Format and deliver
- Default text format includes citation. Use `--format table` for markdown tables.
- For charts, requires `matplotlib`; gracefully falls back if not installed.
- Use `--summary latest` for quick briefs with change context.
- Use `--report macro-snapshot` for a full multi-indicator briefing.
- Always include the citation line in any response to the user.

---

## Presets (20 validated)

Common indicator queries are bundled in `presets.json`. All validated live March 2026.

```bash
# List all available presets
python3 scripts/abs_query.py --list-presets

# Describe a preset (shows what it measures and when to use it)
python3 scripts/abs_query.py --describe-preset unemployment-rate

# Run a preset
python3 scripts/abs_query.py --preset cpi-annual-change --latest --format table
python3 scripts/abs_query.py --preset unemployment-rate --latest
python3 scripts/abs_query.py --preset gdp-annual-change --chart
python3 scripts/abs_query.py --preset wage-annual-change --start-period 2020-Q1
python3 scripts/abs_query.py --preset population-national --format csv
python3 scripts/abs_query.py --preset dwelling-prices-mean --format table
python3 scripts/abs_query.py --preset trade-balance --start-period 2024-01
python3 scripts/abs_query.py --preset household-spending-change --summary latest
```

Key presets: `cpi-annual-change`, `unemployment-rate`, `participation-rate`, `employment-level`,
`underemployment-rate`, `labour-force-size`, `gdp-annual-change`, `wage-annual-change`,
`population-national`, `dwelling-prices-mean`, `trade-balance`, `goods-exports`, `goods-imports`,
`household-spending-change`.

---

## Output Formats

| Flag | Output |
|---|---|
| *(default)* | Human-readable text with friendly labels + citation |
| `--format table` | Markdown table with friendly labels and rendered periods |
| `--format csv` | CSV with raw codes + citation comment |
| `--format json` | JSON with raw codes + `*_label` fields + `TIME_PERIOD_rendered` |
| `--chart` | PNG chart with dataset title, subtitle, latest-point annotation |
| `--summary latest` | Latest value + previous + absolute/percentage-point deltas + textual summary |
| `--report macro-snapshot` | Compact multi-indicator macro briefing (7 key economic indicators) |
| `--citation-style analyst` | Analyst-style source footnote block |
| `--flat-view` | AllDimensions format (wider; may be large) |

---

## Period Rendering

All output modes now render periods in human-readable format:
- `2026-01` → January 2026
- `2025-Q4` → December quarter 2025
- `2025-Q1` → March quarter 2025
- Ranges: `March quarter 2024 to December quarter 2025`

This applies to table headers, text output, citations, chart labels, and summary/report output.

---

## JSON Output with Labels

`--format json` returns both raw dimension codes and friendly `*_label` fields:

```json
{
  "TSEST": "20",
  "TSEST_label": "Seasonally Adjusted",
  "TIME_PERIOD": "2026-02",
  "TIME_PERIOD_rendered": "February 2026",
  "value": 4.277
}
```

Backward compatible — raw codes are preserved.

---

## Ambiguity Detection

`abs_search.py` classifies ambiguity when multiple datasets match:
- **frequency** — monthly vs quarterly
- **geography** — national vs state vs SA2/LGA
- **measure** — index vs % change vs level
- **series** — original vs seasonally adjusted
- **dataset** — distinct series cover the same topic

Prints clarifying questions to help the user or agent narrow the query.

---

## Cache and Metadata

| Command | Description |
|---|---|
| `abs_cache.py refresh` | Fetch all dataflows from ABS, save to `~/.cache/abs-data-api/catalog.json` |
| `abs_cache.py gen-metadata` | Generate `metadata.generated.json` from presets + catalog + overrides |
| `abs_cache.py status` | Show cache age, dataflow count, structure count, metadata status |
| `abs_cache.py search <term>` | Search across all cached dataflows |
| `abs_cache.py structure <ID> [VER]` | Fetch and cache DSD for a specific dataflow |

Runtime metadata priority: `metadata.generated.json` > `catalog.json` > `dataset-catalog.md`.
Override quirks (discontinued datasets, nicer labels) in `metadata.overrides.json`.

---

## Validation

```bash
python3 scripts/test_presets.py             # test all presets
python3 scripts/test_presets.py --verbose   # with timing
python3 scripts/test_presets.py --preset unemployment-rate  # single
```

---

## Ambiguity Rules

- **Multiple matching datasets**: prefer the most specific. E.g. for "inflation", `CPI` beats `CPI_M` beats `PPI`.
- **No dimension key provided**: use `all` — the API will return everything; then filter. If the response is large (>100 observations), the tool warns you.
- **Version unknown**: look up from generated metadata, then catalog; try `1.0.0` as last resort.
- **User asks for "latest"**: always add `--latest` flag (uses `lastNObservations=1`).
- **Census data requested**: redirect to the `census-database` skill; this skill handles ABS time-series only.
- **Chart requested but matplotlib missing**: output text/table format and note how to install matplotlib.
- **Retail Trade (RT) requested**: DISCONTINUED after June 2025. Use `HSI_M` or `BUSINESS_TURNOVER` instead.
- **RPPI requested**: note the API only has data to ~2021-Q4. Use `RES_DWELL_ST` for current dwelling prices.

---

## Citation Format

All responses include a citation:

> Source: Australian Bureau of Statistics, *`<Full Dataset Name>`* (Cat. `<catalogue-number>`; dataset `<ID>`; v`<version>`). `<human-readable-period>`. Retrieved via ABS Data API: `<url>`.

Example:

> Source: Australian Bureau of Statistics, *Consumer Price Index* (Cat. 6401.0; dataset `CPI`; v2.0.0). January 2026. Retrieved via ABS Data API: `https://data.api.abs.gov.au/rest/data/ABS,CPI,2.0.0/`.

---

## What's New in v1.0.2

### 1. Metadata Generation
- **`gen-metadata` command**: Builds unified metadata from presets + live catalog + manual overrides
- **Auto-refresh**: Generated metadata automatically updates when older than 24 hours
- Ensures all datasets are findable and correctly labeled, even as ABS API evolves

```bash
python3 scripts/abs_cache.py gen-metadata
```

### 2. Smart Ambiguity Detection
- **Classifies ambiguity** when multiple datasets match a user query (frequency, geography, measure, series, dataset)
- **Provides clarifying questions** grouped by intent (prices, wages, employment, housing, etc.)
- **Flags discontinued datasets** with replacement suggestions (e.g., RT → HSI_M)
- Uses curated intent groups + ambiguity tags to guide disambiguation

```bash
python3 scripts/abs_search.py "inflation"  # May suggest CPI, CPI_M, PPI with clarifying Qs
```

### 3. Summary Mode with Change Context
- **`--summary latest`**: Shows latest value + previous + **absolute deltas** + brief summary
- Automatically detects rates/growth measures and uses **percentage-point notation** instead of misleading relative % changes
  - Example: Unemployment rate rises from 4.0% to 4.3% → "change of +0.3 percentage points" (NOT "+7.5% relative change")
  - Applies to: unemployment, participation, inflation rates, growth measures
- Ideal for quick briefings and executive summaries

```bash
python3 scripts/abs_query.py --preset unemployment-rate --summary latest
# Output: Current: 4.3% | Previous: 4.0% (Feb) | Change: +0.3pp | [Brief context]
```

### 4. Macro-Snapshot Report
- **`--report macro-snapshot`**: Single-command economic briefing covering 7 key indicators
- Fetches CPI, unemployment, participation, employment, GDP growth, wage growth, household spending
- All with change context and period rendering
- Perfect for media snippets or executive briefings

```bash
python3 scripts/abs_query.py --report macro-snapshot
```

### 5. Percentage-Point Delta Fix
- **Smart detection**: Automatically recognizes rates and growth measures via keyword matching
- **Applies percentage-point notation** to avoid confusion with relative % changes
- **Examples**:
  - Unemployment: 4.0% → 4.3% = **+0.3 percentage points** (not +7.5%)
  - CPI: 3.5% → 3.2% = **-0.3 percentage points**
  - Wage growth: 4.1% → 4.0% = **-0.1 percentage points**
- Applies to all output modes: text, table, JSON, summary

### 6. Metadata Overrides (metadata.overrides.json)
- **Discontinued datasets** (RT → HSI_M, RPPI stale warning)
- **Friendly names** for complex dataset IDs
- **Replacement hints** with explanations
- Easy to extend for future dataset changes

The query engine appends this automatically. Do not strip it from tool output.

---

## Changelog

### v1.0.2 (March 2026)

**New Features:**
- ✨ Metadata generation (`gen-metadata` command) — builds unified metadata from presets + catalog + overrides with auto-refresh
- ✨ Smart ambiguity detection — classifies multiple matches by type (frequency, geography, measure, series, dataset) and provides grouped clarifying questions
- ✨ Summary mode with change context (`--summary latest`) — shows latest + previous + absolute deltas + brief summary
- ✨ Macro-snapshot report (`--report macro-snapshot`) — single-command economic briefing covering 7 key indicators
- ✨ Percentage-point delta fix — rates/growth measures automatically use pp notation instead of misleading relative % changes
- ✨ Intent grouping — curated entries now include `intent_group` and `ambiguity_tags` for smarter disambiguation

**Improvements:**
- Discontinued dataset detection (RT → HSI_M, RPPI stale warning)
- Better metadata overrides system for dataset quirks
- Enhanced search with ambiguity classification
- All output modes now respect percentage-point notation where applicable

**Affected Scripts:**
- `abs_cache.py` — added `gen-metadata` command and `generate_metadata()` function
- `abs_search.py` — added ambiguity detection, intent grouping, and clarifying questions
- `abs_query.py` — added `--summary latest`, `--report macro-snapshot`, percentage-point delta detection
- `metadata.overrides.json` — new file for manual dataset overrides

### v1.0.1 (Previous)
- Base preset system with 20 validated queries
- Curated dataset catalog and SDMX dimension references
- Cache refresh and fuzzy search capabilities
