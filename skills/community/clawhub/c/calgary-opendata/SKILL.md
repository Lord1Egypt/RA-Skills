---
name: City of Calgary Open Data
description: "Access 988+ datasets from the City of Calgary open data portal. Search, fetch, and analyze city data on transit, environment, government, and more. The skills contain API information licensed under the Open Government Licence – City of Calgary"
permissions: Bash
triggers:
  - calgary open data
  - city of calgary data
  - calgary dataset
  - data.calgary.ca
  - calgary transit
  - calgary census
---

# City of Calgary Open Data

Access and analyze 988+ open datasets from the City of Calgary via the Socrata SODA API. Data covers transit, environment, government, demographics, health, business, and more.

**Portal:** https://data.calgary.ca
**Licence:** Open Government Licence – City of Calgary

## Quick Start

```bash
# Search for datasets
python3 scripts/calgary_data.py search "traffic"

# List datasets by category
python3 scripts/calgary_data.py list --category "Environment"

# View dataset info
python3 scripts/calgary_data.py info iric-4rrc

# Fetch data (default JSON, 10 rows)
python3 scripts/calgary_data.py fetch iric-4rrc --limit 5

# Fetch with filters
python3 scripts/calgary_data.py fetch iric-4rrc --where "period='2024-01'" --select "facility_name,solar_pv_production_kwh"

# Export to CSV
python3 scripts/calgary_data.py fetch iric-4rrc --limit 100 --csv > solar.csv

# List all categories
python3 scripts/calgary_data.py categories

# View popular datasets
python3 scripts/calgary_data.py popular

# GeoJSON export (if dataset has location columns)
python3 scripts/calgary_data.py geojson c9sh-grss --limit 50
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `search <query>` | Search datasets by keyword |
| `list [--category <cat>]` | List datasets, optionally filter by category |
| `info <dataset-id>` | Show dataset metadata (columns, types, row count) |
| `fetch <dataset-id>` | Download data rows (opts: `--limit`, `--where`, `--select`, `--order`, `--csv`, `--json`) |
| `categories` | List all categories with dataset counts |
| `popular` | Show most-viewed datasets |
| `geojson <dataset-id>` | Export geocoded data as GeoJSON |

## Query Parameters

The `fetch` command supports Socrata SODA query parameters:

- `--limit N` — Max rows to return (default: 10)
- `--where "condition"` — SQL-like filter (e.g., `"population > 5000"`)
- `--select "col1,col2"` — Choose specific columns
- `--order "col DESC"` — Sort results
- `--offset N` — Skip N rows (pagination)
- `--csv` — Output as CSV instead of JSON

## Dataset IDs

Dataset IDs are 9-character alphanumeric codes (e.g., `iric-4rrc`). Find them via `search` or `list`, or from the dataset URL: `data.calgary.ca/dataset/{id}`.

## Data Sources

All data sourced from the City of Calgary Open Data Portal (data.calgary.ca) under the Open Government Licence.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SOCRATA_APP_TOKEN` | No | Optional Socrata app token to reduce rate limits. Works without it. |
All data is sourced from the City of Calgary's Open Data Portal (data.calgary.ca) and is provided under the Open Government Licence – City of Calgary. See [references/datasets.md](references/datasets.md) for a curated list of popular datasets.
