---
name: etl
version: "2.0.0"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
license: MIT-0
tags: [etl, tool, utility]
description: "Build ETL pipelines with data ingestion, cleaning, and validation steps. Use when ingesting sources, transforming formats, validating data, or scheduling loads."
---

# ETL

Extract-Transform-Load data toolkit (v2.0.0). Record and manage data pipeline activities across the full ETL lifecycle — ingest, transform, query, filter, aggregate, visualize, export, sample, schema definition, validation, pipeline orchestration, and data profiling. Each command logs timestamped entries to its own log file, giving you a structured record of all data operations.

## Commands

| Command | Description |
|---------|-------------|
| `etl ingest <input>` | Record a data ingestion event (source, format, row count, etc.). Without args, shows recent ingest entries. |
| `etl transform <input>` | Log a transformation step (column rename, type cast, normalization, etc.). Without args, shows recent transforms. |
| `etl query <input>` | Record a query operation or SQL statement. Without args, shows recent queries. |
| `etl filter <input>` | Log a filtering rule or condition applied to data. Without args, shows recent filters. |
| `etl aggregate <input>` | Record an aggregation step (GROUP BY, SUM, AVG, etc.). Without args, shows recent aggregations. |
| `etl visualize <input>` | Log a visualization request or chart configuration. Without args, shows recent visualizations. |
| `etl export <input>` | Record an export operation (destination, format, row count). Without args, shows recent exports. |
| `etl sample <input>` | Log a data sampling step (sample size, method, seed). Without args, shows recent samples. |
| `etl schema <input>` | Record a schema definition or schema change. Without args, shows recent schema entries. |
| `etl validate <input>` | Log a data validation rule or result. Without args, shows recent validations. |
| `etl pipeline <input>` | Record a pipeline configuration or execution step. Without args, shows recent pipeline entries. |
| `etl profile <input>` | Log a data profiling result (null counts, distributions, anomalies). Without args, shows recent profiles. |
| `etl stats` | Show summary statistics: entry counts per category, total entries, data size, and earliest record date. |
| `etl export <fmt>` | Export all logged data to a file. Supported formats: `json`, `csv`, `txt`. (Note: this is a different code path from the `export` log command — it exports the tool's own data.) |
| `etl search <term>` | Search across all log files for a keyword (case-insensitive). |
| `etl recent` | Show the 20 most recent entries from the activity history log. |
| `etl status` | Health check: version, data directory, total entries, disk usage, last activity. |
| `etl help` | Show the built-in help with all available commands. |
| `etl version` | Print the current version (v2.0.0). |

## Data Storage

All data is stored as plain-text log files in `~/.local/share/etl/`:

- **Per-command logs** — Each command (ingest, transform, query, etc.) writes to its own `.log` file (e.g., `ingest.log`, `transform.log`).
- **History log** — Every operation is also appended to `history.log` with a timestamp and command name.
- **Export files** — Generated in the same directory as `export.json`, `export.csv`, or `export.txt`.

Entries are stored in `timestamp|value` format, making them easy to grep, parse, or pipe into downstream tools.

## Requirements

- **Bash** 4.0+ (uses `set -euo pipefail`)
- **coreutils** — `date`, `wc`, `du`, `head`, `tail`, `grep`, `basename`, `cut`
- No external dependencies, API keys, or network access required
- Works fully offline on any POSIX-compatible system

## When to Use

1. **Logging data pipeline steps** — Record each stage of your ETL process (ingest → transform → validate → export) with timestamps, creating a complete audit trail of data movements.
2. **Schema management and validation** — Use `schema` to document table structures and `validate` to log data quality rules and their pass/fail results.
3. **Data profiling and exploration** — Use `profile` to record column statistics, null rates, and distribution anomalies; use `sample` to log sampling parameters for reproducibility.
4. **Pipeline orchestration tracking** — Use `pipeline` to record multi-step workflow configurations, execution order, and dependencies between ETL stages.
5. **Cross-team data operations review** — Run `stats` for aggregate counts, `search` to find specific operations by keyword, and `export json` to share pipeline logs with team members or load into dashboards.

## Examples

```bash
# Log a data ingestion from S3
etl ingest "s3://data-lake/raw/users_2024.csv — 1.2M rows, CSV format"

# Record a transformation step
etl transform "Normalize email to lowercase, cast created_at to UTC timestamp"

# Log a validation rule
etl validate "NOT NULL check on user_id: 0 violations out of 1,200,000 rows"

# Record schema for a new table
etl schema "users_dim: id INT PK, email VARCHAR(255), created_at TIMESTAMP, country CHAR(2)"

# Define a pipeline
etl pipeline "daily_user_load: ingest(s3) -> dedupe -> validate -> load(postgres)"

# Search for anything related to 'users'
etl search users

# Export all ETL logs to CSV for analysis
etl export csv

# View summary statistics
etl stats

# Check system health
etl status
```

## Tips

- Run any data command without arguments to see recent entries (e.g., `etl ingest` shows the last 20 ingest entries).
- Use `etl recent` for a quick overview of all activity across all categories.
- Combine with cron to auto-log pipeline runs: `0 2 * * * etl pipeline "nightly_load completed at $(date)"`
- Back up your data by copying `~/.local/share/etl/` to your preferred backup location.

---
*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*
