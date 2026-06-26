# databricks-helper

A ClawHub skill that lets your AI agent query and control Databricks from plain text.

## Install

```bash
npx clawhub@latest install databricks-helper
```

## Setup

```bash
export DATABRICKS_HOST=https://adb-xxxx.azuredatabricks.net
export DATABRICKS_TOKEN=dapiXXXXXXXXXXXXXXXX
```

## What's new in 1.1.0

- Retry/cancel runs, inspect detailed logs, and monitor SLA breaches.
- Filter jobs by name/tags, list only running jobs, and see top failing pipelines.
- Unity Catalog discovery plus table previews and safe, read-only SQL queries.
- Daily/weekly success summaries and top failing jobs to spot regressions quickly.

## What it does

| You say | What happens |
|---------|-------------|
| "check my databricks jobs" | Lists last 10 runs with status, duration, and links |
| "what failed in databricks today" | Shows FAILED runs from last 24h with error messages |
| "run pipeline nightly_etl" | Triggers the job by name, returns run ID |
| "retry run 123" | Calls the Jobs Repair API to rerun failed tasks |
| "cancel run 456" | Sends a cancel request for the active run |
| "what's running now" | Shows currently running jobs with elapsed time |
| "list prod jobs" | Filters job list by name/tag combinations |
| "databricks summary" | Prints 24h/7d success/failure counts |
| "top failing jobs" | Aggregates failures and surfaces worst offenders |
| "list catalogs" / "list schemas" | Browses Unity Catalog objects |
| "preview table main.bronze.events" | Samples table rows via SQL with row limits |
| "run sql select * from ..." | Executes read-only SQL through a warehouse |

## Direct usage

```bash
# Core job operations
python scripts/databricks_helper.py list-runs
python scripts/databricks_helper.py failures --hours 24
python scripts/databricks_helper.py run-job "nightly_etl"
python scripts/databricks_helper.py job-status "nightly_etl"
python scripts/databricks_helper.py retry-run 123
python scripts/databricks_helper.py cancel-run 123
python scripts/databricks_helper.py run-details 123

# Analytics and monitoring
python scripts/databricks_helper.py running-jobs --pattern nightly
python scripts/databricks_helper.py jobs --pattern prod --tag env=prod
python scripts/databricks_helper.py sla-watch --minutes 90
python scripts/databricks_helper.py summary
python scripts/databricks_helper.py top-failures --hours 72

# Catalog + SQL
python scripts/databricks_helper.py list-catalogs
python scripts/databricks_helper.py list-schemas --catalog main
python scripts/databricks_helper.py list-tables --catalog main --schema bronze
python scripts/databricks_helper.py preview-table main.bronze.events --limit 10
python scripts/databricks_helper.py run-sql --query "SELECT * FROM main.bronze.events" --limit 50
```

## Requirements

- Python 3.8+
- No pip dependencies (uses only stdlib)
- Environment variables:
  - `DATABRICKS_HOST` and `DATABRICKS_TOKEN`
  - `DATABRICKS_SQL_WAREHOUSE_ID` for table preview & SQL
  - Optional safety overrides:
    - `DATABRICKS_MAX_ROWS` (default 200) controls SQL row limit
    - `DATABRICKS_SQL_TIMEOUT_SEC` (default 60) bounds SQL polling
    - `DATABRICKS_ALLOW_WRITE_SQL` only if you explicitly want to allow DDL/DML
    - `DATABRICKS_SLA_MINUTES` default SLA threshold for `sla-watch`

Read-only SQL is enforced by default—DDL/DML keywords are blocked unless you set `DATABRICKS_ALLOW_WRITE_SQL=true`. Even then, be cautious and prefer view-only queries.

## Verification

Run the lightweight tests before shipping updates:

```bash
python -m unittest scripts/test_databricks_helper.py
```

## License

MIT
