# bird.json schema

Version field: top-level `"version": 1`.

## Top level

| Field | Type | Description |
|-------|------|-------------|
| `version` | int | Schema version (1). |
| `location_query` | string | Place string from user. |
| `region` | object | Best match from ebird region-query. |
| `country_code` | string | eBird country for BirdID `-c`. |
| `observations` | array | Sightings, append-only. |

## `region`

| Field | Type | Description |
|-------|------|-------------|
| `code` | string | eBird code (country or subregion). |
| `name` | string | English label. |
| `name_cn` | string | Chinese label (may be empty). |
| `kind` | string | `country` or `region`. |
| `parent` | string | Parent country code for subregions; empty for countries. |
| `match_score` | number | Fuzzy score from region-query. |

## `observations[]`

| Field | Type | Description |
|-------|------|-------------|
| `time_utc` | string | ISO 8601 UTC (e.g. `2026-03-24T08:30:00+00:00`). |
| `species` | string | Species label (Latin, English, or user text). |
| `notes` | string | Free text. |
| `source` | string | `text` or `photo`. |
| `image_path` | string or null | Local path if photo. |
| `birdid_stdout` | string or null | Raw BirdID output if captured. |

## CSV export

Call **`export_csv.py`** with **absolute** paths for the script, **`--workspace`**, and any **`--output`** / **`--summary-output`** file targets (see skill `SKILL.md`).

**`export_csv.py`** produces:

1. **Observations CSV** — one row per record; columns include `time_utc`, `species`, `notes`, `source`, `image_path`, plus repeated session fields `location_query`, `ebird_region_*`, `ebird_country_code`.
2. **Summary CSV** (with `--summary`) — `species`, `count`, `first_time_utc`, `last_time_utc` (empty species grouped as `(empty)`).
