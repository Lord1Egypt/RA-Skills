---
name: bird-watching-mode
description: >-
  Bird-watching log workflow: ask for place on enable, resolve eBird region via
  superpicky-cli region-query, persist to workspace/bird.json; record sightings
  (time, species) from user text or BirdID photo identify; export CSV summary
  for the user. Invocation requires absolute paths for script, --workspace, and
  image files. Use when the user enables 观鸟模式, bird watching mode, wants
  to log birds, export sightings to CSV, or record species from photos to
  bird.json.
---

# Bird watching mode (观鸟模式)

## Purpose

1. **On enable**: Ask the user for **地点** (place name). Resolve **eBird region** with **superpicky-cli** `region-query`, then write **`workspace/bird.json`**.
2. **During use**: Either **identify a photo** (BirdID via scripts) or **record plain text** (species name). Always append **time** + **species** (and optional fields) to **`workspace/bird.json`**.
3. **Summary / export**: On request, run **`export_csv.py`** to produce CSV (and optional per-species counts), then **send the file or paste** to the user (chat attachment, email, etc.).

**`$SKILL`** = directory containing this `SKILL.md` (usually `~/.myagent/skills/bird-watching-mode`). Before invoking anything, resolve it to an **absolute** path (e.g. `SKILL="$(cd ~/.myagent/skills/bird-watching-mode && pwd)"`).

## Paths

- **Bird log file**: `{project}/workspace/bird.json` (create `workspace/` if missing).
- **SuperPicky skill**: default sibling `../superpicky-cli`. Override with env **`SUPERPICKY_CLI_SKILL`** (absolute path to superpicky-cli skill root).

### Absolute paths (required for invocation)

When calling these scripts from the agent or shell, **all filesystem arguments must be absolute paths** — do not rely on cwd or `~` inside subprocesses unless the shell expands them before the call.

| Argument | Rule |
|----------|------|
| **Python script path** | Must be absolute, e.g. `/Users/you/.myagent/skills/bird-watching-mode/scripts/set_region.py`. |
| **`--workspace`** | Must be the **absolute** project root (directory that will contain `workspace/bird.json`). |
| **Image path** (`identify_photo.py` positional, **`--image`** on `append_sighting.py`) | Must be **absolute** path to the file on disk. |
| **`--output` / `--summary-output`** (`export_csv.py`) | If not `-`, use an **absolute** path for the CSV file (avoids ambiguity vs cwd). |

Relative paths inside **stored JSON** (e.g. past `image_path` values) are legacy data only; **new invocations should still use absolute paths**.

## Scripts (run from any cwd)

| Script | Role |
|--------|------|
| **`scripts/set_region.py`** | After user gives a place: call region-query `--json`, pick match, merge into `bird.json` (`region`, `location_query`, `country_code`). |
| **`scripts/append_sighting.py`** | Append one observation: `--species`, optional `--notes`, `--source text\|photo`, `--image`, `--time` (ISO UTC). |
| **`scripts/identify_photo.py`** | Run BirdID `identify` using `-c`/`-r` from `bird.json`; print CLI stdout (agent reads top species); optional `--append` to log raw output + image path. |
| **`scripts/export_csv.py`** | Export all observations to CSV; optional **`--summary`** for per-species counts. Deliver CSV to the user (file path or `-` stdout for inline paste). |

```bash
# $SKILL and PROJECT must already be absolute (example values):
# SKILL=/Users/you/.myagent/skills/bird-watching-mode
# PROJECT=/Users/you/Workspace/myproject
# PHOTO=/Users/you/.myagent/workspace/media/abc123.jpg

# Resolve region (agent: ask user to confirm if multiple lines printed)
python3 "${SKILL}/scripts/set_region.py" --workspace "${PROJECT}" --location "上海"

# Manual / AI-confirmed text record
python3 "${SKILL}/scripts/append_sighting.py" --workspace "${PROJECT}" \
  --species "Eurasian Tree Sparrow" --source text --notes "flock of 5"

# Photo: run BirdID (requires superpicky install + models)
python3 "${SKILL}/scripts/identify_photo.py" --workspace "${PROJECT}" "${PHOTO}"
# Optional: append a sighting row with species left empty for later edit, or use --append-species "Latin name"
python3 "${SKILL}/scripts/identify_photo.py" --workspace "${PROJECT}" --append "${PHOTO}"

# Export CSV (default: workspace/bird_sightings_export.csv under PROJECT); paths printed on stderr
python3 "${SKILL}/scripts/export_csv.py" --workspace "${PROJECT}"
python3 "${SKILL}/scripts/export_csv.py" --workspace "${PROJECT}" --summary
python3 "${SKILL}/scripts/export_csv.py" --workspace "${PROJECT}" --output -   # stdout for paste only; no second file
```

## Agent workflow

### A. User turns on 观鸟模式

1. Ask: **Where are you birding?** (地点 — city, province, park, etc.)
2. Run **`set_region.py`** using **absolute** paths for the script and **`--workspace`**. If exit code **3**, several matches were printed — ask the user which **code** (or re-run with `--pick N`).
3. Confirm **`workspace/bird.json`** exists and contains **`region.code`** (and `country_code`).

### B. User sends a **photo**

1. Ensure SuperPicky is installed (see **Prerequisites** below).
2. Run **`identify_photo.py`** with **absolute** script path, **absolute** **`--workspace`**, and **absolute** image file path.
3. Read stdout; treat top BirdID lines as primary candidates. **Confirm species** with the user if uncertain.
4. Run **`append_sighting.py`** with **absolute** script path and **`--workspace`**, final **`--species`**, **`--source photo`**, and **absolute** **`--image`** path.

**Prerequisites:** SuperPicky venv under **`$SUPERPICKY_CLI_SKILL`** (default sibling `superpicky-cli`). If missing: **`$SUPERPICKY_CLI_SKILL/scripts/install.sh`** (see superpicky-cli skill).

### C. User sends **text** (species / field note)

1. Parse species (and optional notes) from the message.
2. Run **`append_sighting.py`** with **absolute** script path, **absolute** **`--workspace`**, and **`--source text`**.

### D. User asks for **汇总** / **导出** / **CSV**

1. Run **`export_csv.py`** with **absolute** script path and **absolute** **`--workspace`** (add **`--summary`** if they want counts by species; use **absolute** paths for **`--output`** / **`--summary-output`** when writing files).
2. Read the path(s) printed on **stderr**; attach the CSV file(s) in the channel or paste **`--output -`** stdout if the UI supports it.
3. Optional **`--excel`**: UTF-8 BOM for Excel on Windows.

## `bird.json` shape (summary)

- **`location_query`**: user’s place string.
- **`region`**: `{ code, name, name_cn, kind, parent, match_score }` from region-query JSON (first line unless `--pick`).
- **`country_code`**: eBird country (`CN`, …) — region’s `parent` if subnational, else `region.code`.
- **`observations[]`**: `{ time_utc, species, notes, source, image_path?, birdid_stdout? }`.

For full fields, run **`append_sighting.py --help`** or read **`scripts/bird_log_schema.md`**.

## Tests

From **`$SKILL/scripts/`**:

```bash
./run_tests.sh
# or: python3 bird_json_util_test.py && python3 set_region_test.py && …
```

## Related

- Region lookup CLI: [superpicky-cli/SKILL.md](../superpicky-cli/SKILL.md) — `./scripts/run.sh --region-query … --json`.
