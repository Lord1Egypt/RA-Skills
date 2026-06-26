# databricks-helper

Query, inspect, and control your Databricks workspace from plain text. Check job status, rerun/cancel runs, inspect logs, explore Unity Catalog, and run read-only SQL without opening the UI.

## Triggers

Use this skill when the user says things like:
- "check my databricks jobs"
- "what failed in databricks today"
- "what failed this morning"
- "show me recent databricks runs"
- "run pipeline [name]"
- "trigger job [name]"
- "databricks job status"
- "what's running in databricks"
- "any failures in databricks"
- "retry databricks run 123"
- "cancel my stuck databricks job"
- "show detailed logs for run 123"
- "list only running jobs"
- "list jobs tagged env=prod"
- "did any runs breach SLA"
- "databricks success summary"
- "top failing jobs"
- "list catalogs/schemas/tables"
- "preview table main.bronze.events"
- "run SQL select ..." (read-only)

## Requirements

- Databricks REST API access (no CLI required)
- Environment variables set:
  - `DATABRICKS_HOST` — workspace URL, e.g. `https://adb-1234567890.12.azuredatabricks.net`
  - `DATABRICKS_TOKEN` — personal access token
  - `DATABRICKS_SQL_WAREHOUSE_ID` — required for catalog preview + SQL
- Optional safety tuning:
  - `DATABRICKS_SLA_MINUTES` for SLA alerts (default 60)
  - `DATABRICKS_MAX_ROWS` (default 200) row cap for SQL output
  - `DATABRICKS_SQL_TIMEOUT_SEC` (default 60) SQL wait timeout
  - `DATABRICKS_ALLOW_WRITE_SQL` — only set `true` if DDL/DML should be allowed

## Installation

```bash
npx clawhub@latest install databricks-helper
```

## Usage Examples

**Check recent jobs**
> "check my databricks jobs"

Lists the last 10 job runs with status, duration, and run URLs.

**Find failures**
> "what failed in databricks today"

Filters runs from the last 24 hours and prints failed ones with error snippets.

**Trigger or retry pipelines**
> "run pipeline customer_ingestion"
> "retry databricks run 123"

Starts a new run or reruns failed tasks via the Jobs Repair API.

**Cancel a run**
> "cancel databricks run 123"

Calls `jobs/runs/cancel` with safety checks and prints confirmation.

**Live monitoring + analytics**
> "what's running now"
> "databricks sla watch"
> "databricks success summary"

Shows active runs with elapsed time, highlights SLA breaches, and prints 24h/7d success/failure counts plus top failing jobs (with adjustable time ranges).

**Catalog + SQL exploration**
> "list catalogs"
> "list tables in main bronze"
> "preview table main.bronze.events"
> "run sql select * from main.bronze.events"

Uses the Unity Catalog API for discovery and runs read-only SQL through the configured warehouse with enforced row limits.

## Implementation

```bash
python scripts/databricks_helper.py list-runs
python scripts/databricks_helper.py failures --hours 24
python scripts/databricks_helper.py run-job "job name"
python scripts/databricks_helper.py retry-run 123
python scripts/databricks_helper.py cancel-run 123
python scripts/databricks_helper.py run-details 123
python scripts/databricks_helper.py running-jobs --pattern nightly
python scripts/databricks_helper.py jobs --tag env=prod
python scripts/databricks_helper.py sla-watch --minutes 90
python scripts/databricks_helper.py summary
python scripts/databricks_helper.py top-failures --hours 48
python scripts/databricks_helper.py list-catalogs
python scripts/databricks_helper.py list-schemas --catalog main
python scripts/databricks_helper.py list-tables --catalog main --schema bronze
python scripts/databricks_helper.py preview-table main.bronze.events --limit 20
python scripts/databricks_helper.py run-sql --query "SELECT * FROM main.bronze.events" --limit 50
```

## Output

Plain text. Each run: job name, status (SUCCESS/FAILED/RUNNING), start/end, duration, SLA status, error (if failed). Catalog + SQL commands return textual lists or tabular results.

## Notes

- Uses Databricks Jobs API v2.1, Unity Catalog API, and SQL Statement Execution API (read-only disposition by default).
- Requires CAN_VIEW for read operations, CAN_MANAGE_RUN to trigger/cancel/repair runs, and SQL warehouse access.
- SQL commands enforce read-only queries unless `DATABRICKS_ALLOW_WRITE_SQL=true`. Limits/timeouts are applied to avoid runaway scans.
- SLA alerts default to 60 minutes but may be overridden via `DATABRICKS_SLA_MINUTES` or per-command flags.

## CHANGELOG

- **1.1.0** — Adds run retry/cancel/details, running-job lists, job filtering by tags, SLA watch, success/failure summaries, top failing jobs, Unity Catalog discovery, table previews, and safe read-only SQL execution with row limits plus new docs/tests.
