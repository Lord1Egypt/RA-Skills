# ABS Data API Skill — Install / Use Note

This is a quick practical note for installing, testing, and using the `abs-data-api` skill.

## Files

- **Source folder:** `~/.openclaw/workspace/skills/abs-data-api/`
- **Packaged bundle:** `~/.openclaw/workspace/skills/dist/abs-data-api.skill`

## What this skill does

This skill helps an OpenClaw agent query the Australian Bureau of Statistics Data API using natural language and structured preset queries.

It supports:
- ABS dataset discovery
- metadata caching
- querying time series and indicator data
- Census / CED lookups when available in the ABS API
- readable citations
- analyst-style source blocks
- friendly table labels instead of raw SDMX codes

## Install options

### Option 1: Use the source folder directly

If the skill directory already sits inside your skills path, you can use it in place.

Current path:
```bash
~/.openclaw/workspace/skills/abs-data-api/
```

### Option 2: Use the packaged `.skill` bundle

Packaged file:
```bash
~/.openclaw/workspace/skills/dist/abs-data-api.skill
```

If you need to inspect it manually:
```bash
mkdir -p /tmp/abs-data-api-test
unzip ~/.openclaw/workspace/skills/dist/abs-data-api.skill -d /tmp/abs-data-api-test
find /tmp/abs-data-api-test -maxdepth 3 -type f | sort
```

## Smoke test

From the source directory or extracted package root:

```bash
cd ~/.openclaw/workspace/skills/abs-data-api
python3 scripts/abs_query.py --list-presets
python3 scripts/abs_query.py --preset cpi-annual-change --latest --format table
python3 scripts/abs_query.py --preset gdp-chain-volume --start-period 2025-Q3 --format table --citation-style analyst
python3 scripts/abs_search.py "Brisbane population CED"
```

## Day to day usage

### List built-in presets
```bash
python3 scripts/abs_query.py --list-presets
```

### Query latest inflation
```bash
python3 scripts/abs_query.py --preset cpi-annual-change --latest --format table
```

### Query GDP time series
```bash
python3 scripts/abs_query.py --preset gdp-chain-volume --start-period 2024-Q1 --format table
```

### Query with analyst-style sources
```bash
python3 scripts/abs_query.py --preset gdp-chain-volume --start-period 2025-Q1 --format table --citation-style analyst
```

### Search for a dataset
```bash
python3 scripts/abs_search.py "unemployment rate"
python3 scripts/abs_search.py "GDP per capita"
python3 scripts/abs_search.py "Brisbane population CED"
```

### Refresh the ABS metadata cache
```bash
python3 scripts/abs_cache.py refresh
python3 scripts/abs_cache.py status
```

## Output behavior

### Friendly labels
Text and table outputs render readable values where possible.

Example:
- `Australia` instead of `50`
- `Monthly` instead of `M`
- `Percentage change from previous year` instead of `3`

### Citation styles

Default:
```text
Source: Australian Bureau of Statistics, *Consumer Price Index* (Cat. 6401.0; dataset `CPI`; v2.0.0). 2026-01. Retrieved via ABS Data API: ...
```

Analyst style:
```text
Sources
- Australian Bureau of Statistics, *Australian National Accounts Key Aggregates* (Cat. 5206.0; dataset `ANA_AGG`; v1.0.0), 2025-Q1 to 2025-Q4, via ABS Data API
```

## Common troubleshooting

### Too much data returned
Use a narrower key, or inspect the structure first:
```bash
python3 scripts/abs_cache.py structure CPI 2.0.0
```

### Dataset not obvious
Search the catalog first:
```bash
python3 scripts/abs_search.py "housing prices"
```

### Query times out or is too broad
Prefer:
- `--latest`
- `--start-period`
- a preset
- a more specific dimension key

### Census / geography queries are tricky
Census datasets often require exact multi-part dimension keys. Use the search script, inspect the structure, then narrow the query.

## Recommended workflow

1. Search the dataset
2. Try a preset if one exists
3. If needed, inspect structure
4. Run a narrow query with a date range or `--latest`
5. Use `--citation-style analyst` for polished outputs

## Notes

- ABS Data API structures and versions can change
- the skill already handles current verified patterns, but some datasets may need refreshed presets over time
- if a preset fails, the underlying dataset structure may have changed upstream
