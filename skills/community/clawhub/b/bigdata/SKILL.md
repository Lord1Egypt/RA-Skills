---
name: bigdata
version: "2.0.0"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
license: MIT-0
tags: [bigdata, tool, utility]
description: "Split large files, run parallel processing, and stream batch analysis. Use when sampling datasets, aggregating logs, or transforming bulk data."
---

# BigData

A comprehensive data processing toolkit for ingesting, transforming, querying, filtering, aggregating, and managing data workflows — all from the command line with local timestamped log storage.

## Commands

| Command | Description |
|---------|-------------|
| `bigdata ingest <input>` | Ingest raw data into the system. Without args, shows recent ingest entries |
| `bigdata transform <input>` | Record a data transformation step. Without args, shows recent transforms |
| `bigdata query <input>` | Log and track data queries. Without args, shows recent queries |
| `bigdata filter <input>` | Apply and record data filters. Without args, shows recent filters |
| `bigdata aggregate <input>` | Record aggregation operations. Without args, shows recent aggregations |
| `bigdata visualize <input>` | Log visualization tasks. Without args, shows recent visualizations |
| `bigdata export <input>` | Log export operations. Without args, shows recent exports |
| `bigdata sample <input>` | Record data sampling operations. Without args, shows recent samples |
| `bigdata schema <input>` | Track schema definitions and changes. Without args, shows recent schemas |
| `bigdata validate <input>` | Log data validation checks. Without args, shows recent validations |
| `bigdata pipeline <input>` | Record pipeline configurations. Without args, shows recent pipelines |
| `bigdata profile <input>` | Log data profiling operations. Without args, shows recent profiles |
| `bigdata stats` | Show summary statistics across all entry types |
| `bigdata search <term>` | Search across all log entries for a keyword |
| `bigdata recent` | Show the 20 most recent activity entries from the history log |
| `bigdata status` | Health check — version, data dir, total entries, disk usage, last activity |
| `bigdata help` | Show all available commands |
| `bigdata version` | Print version (v2.0.0) |

Each data command (ingest, transform, query, etc.) works the same way:
- **With arguments**: saves the entry with a timestamp to its dedicated `.log` file and records it in the activity history
- **Without arguments**: displays the 20 most recent entries from that command's log

## Data Storage

All data is stored locally in plain-text log files:

```
~/.local/share/bigdata/
├── ingest.log          # Ingested data entries
├── transform.log       # Transformation records
├── query.log           # Query log
├── filter.log          # Filter operations
├── aggregate.log       # Aggregation records
├── visualize.log       # Visualization tasks
├── export.log          # Export operations
├── sample.log          # Sampling records
├── schema.log          # Schema definitions
├── validate.log        # Validation checks
├── pipeline.log        # Pipeline configurations
├── profile.log         # Profiling results
└── history.log         # Unified activity log with timestamps
```

Each entry is stored as `YYYY-MM-DD HH:MM|<value>` for easy parsing and export.

## Requirements

- **Bash** 4.0+ (uses `set -euo pipefail`)
- Standard UNIX utilities: `date`, `wc`, `du`, `grep`, `head`, `tail`, `cat`
- No external dependencies or API keys required
- Works offline — all data stays on your machine

## When to Use

1. **Data pipeline tracking** — Record each step of a multi-stage data workflow (ingest → transform → validate → export) with full timestamps for audit trails
2. **Quick data logging** — Capture observations, measurements, or notes about datasets directly from the terminal without opening a separate app
3. **Schema management** — Keep track of schema definitions, changes, and validation rules as your data evolves over time
4. **Data quality monitoring** — Log validation checks and profiling results to build a history of data quality metrics
5. **Workflow documentation** — Use search and recent commands to review what data operations were performed, when, and in what order

## Examples

### Log a complete data workflow

```bash
# Ingest raw data
bigdata ingest "customer_orders_2024.csv — 1.2M rows loaded"

# Transform it
bigdata transform "normalize dates to ISO-8601, trim whitespace, deduplicate"

# Validate the output
bigdata validate "all required fields present, no nulls in customer_id"

# Record the schema
bigdata schema "orders: id(int), customer_id(int), amount(decimal), date(date)"

# Export when ready
bigdata export "final dataset pushed to analytics warehouse"
```

### Search and review activity

```bash
# Search across all logs for a keyword
bigdata search "customer"

# Check overall statistics
bigdata stats

# View recent activity across all commands
bigdata recent

# Health check
bigdata status
```

### Pipeline and profiling

```bash
# Define a pipeline
bigdata pipeline "daily-etl: ingest → clean → validate → load — runs at 02:00 UTC"

# Profile a dataset
bigdata profile "users table: 500K rows, 12 columns, 0.3% nulls in email field"

# Sample data for testing
bigdata sample "random 10% sample from transactions for QA testing"

# Record an aggregation
bigdata aggregate "monthly revenue by region — Q1 totals computed"
```

### Filter and query tracking

```bash
# Log a filter operation
bigdata filter "removed records older than 2020-01-01, kept 850K of 1.2M rows"

# Track a query
bigdata query "SELECT region, SUM(revenue) FROM orders GROUP BY region"

# Log a visualization
bigdata visualize "bar chart: monthly revenue trend, exported as PNG"
```

## Output

All commands print confirmation to stdout. Data is persisted in `~/.local/share/bigdata/`. Use `bigdata stats` for a summary or `bigdata search <term>` to find specific entries across all logs.

---

*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*
