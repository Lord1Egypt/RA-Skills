---
name: cpu
version: "2.0.0"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
license: MIT-0
tags: [cpu, tool, utility]
description: "Monitor CPU load, per-core usage, and rank top resource-consuming processes. Use when checking temperatures, ranking processes, tracking load."
---

# Cpu

Cpu v2.0.0 — a sysops toolkit for scanning, monitoring, reporting, alerting, benchmarking, and managing system operations. Each command logs timestamped records locally, providing a lightweight operations journal for tracking system events, fixes, backups, and performance comparisons.

## Commands

| Command | Description |
|---------|-------------|
| `cpu scan <input>` | Record a scan result (or view recent scans with no args) |
| `cpu monitor <input>` | Log a monitoring observation (or view recent monitors) |
| `cpu report <input>` | Record a report entry (or view recent reports) |
| `cpu alert <input>` | Log an alert event (or view recent alerts) |
| `cpu top <input>` | Record a top-process snapshot (or view recent tops) |
| `cpu usage <input>` | Log a usage measurement (or view recent usage records) |
| `cpu check <input>` | Record a health check (or view recent checks) |
| `cpu fix <input>` | Log a fix or remediation (or view recent fixes) |
| `cpu cleanup <input>` | Record a cleanup action (or view recent cleanups) |
| `cpu backup <input>` | Log a backup event (or view recent backups) |
| `cpu restore <input>` | Record a restore operation (or view recent restores) |
| `cpu log <input>` | Add a general log entry (or view recent log entries) |
| `cpu benchmark <input>` | Record a benchmark result (or view recent benchmarks) |
| `cpu compare <input>` | Log a comparison (or view recent comparisons) |
| `cpu stats` | Show summary statistics across all log files |
| `cpu search <term>` | Search all entries for a keyword (case-insensitive) |
| `cpu recent` | Show the 20 most recent activity entries |
| `cpu status` | Health check — version, entry count, disk usage, last activity |
| `cpu help` | Display all available commands |
| `cpu version` | Print version string |

Each operations command (scan, monitor, report, alert, top, usage, check, fix, cleanup, backup, restore, log, benchmark, compare) works identically:

- **With arguments:** saves a timestamped entry to `~/.local/share/cpu/<command>.log` and logs to `history.log`
- **Without arguments:** displays the 20 most recent entries from that command's log file

## Data Storage

All data is stored locally in `~/.local/share/cpu/`:

| File | Contents |
|------|----------|
| `scan.log` | System scan results |
| `monitor.log` | Monitoring observations |
| `report.log` | Report entries |
| `alert.log` | Alert events |
| `top.log` | Top-process snapshots |
| `usage.log` | Usage measurements |
| `check.log` | Health check records |
| `fix.log` | Fix/remediation records |
| `cleanup.log` | Cleanup action records |
| `backup.log` | Backup event records |
| `restore.log` | Restore operation records |
| `log.log` | General log entries |
| `benchmark.log` | Benchmark results |
| `compare.log` | Comparison records |
| `history.log` | Unified activity log for all commands |

The `stats` command reads all `.log` files and reports line counts per file, total entries, data directory size, and the timestamp of the first recorded activity.

The `export` utility function can produce **JSON**, **CSV**, or **TXT** output files under the data directory.

## Requirements

- **Bash** (4.0+)
- **coreutils** — `date`, `wc`, `du`, `head`, `tail`, `grep`, `basename`, `cat`
- No external dependencies, API keys, or network access required
- Works on Linux and macOS

## When to Use

1. **Tracking system operations** — use `scan`, `monitor`, `check`, and `alert` to maintain a timestamped journal of system health events and observations
2. **Recording fixes and remediations** — use `fix` and `cleanup` to document what was changed and when, creating an audit trail for incident response
3. **Benchmarking and comparing performance** — use `benchmark` and `compare` to log performance results over time and track improvements or regressions
4. **Managing backup and restore history** — use `backup` and `restore` to log when backups were taken and restores were performed, with searchable history
5. **Searching operational history** — use `search <term>` to find specific events across all log categories, or `recent` to view the latest 20 activities at a glance

## Examples

```bash
# Record a scan finding
cpu scan "port 8080 open on web-server-01"

# Log a monitoring observation
cpu monitor "memory usage at 78% on db-primary"

# Record an alert
cpu alert "disk /var/log at 92% capacity"

# Log a fix
cpu fix "rotated nginx logs, freed 2.3GB on web-01"

# Record a benchmark result
cpu benchmark "sysbench cpu run: 1847 events/sec"

# Compare two environments
cpu compare "prod latency 45ms vs staging 62ms"

# Log a backup
cpu backup "full backup of postgres completed 14.2GB"

# Search all logs for a keyword
cpu search "disk"

# View summary statistics
cpu stats

# Check system status
cpu status

# View recent activity
cpu recent
```

## How It Works

Cpu uses a simple append-only log architecture. Every command writes a pipe-delimited record (`timestamp|value`) to its dedicated log file. The `history.log` file captures a unified timeline of all operations with the format `MM-DD HH:MM command: value`.

This design makes Cpu:
- **Fast** — pure bash, no database overhead
- **Transparent** — all data is human-readable plain text
- **Portable** — works anywhere bash runs, no install needed
- **Auditable** — every action is timestamped and traceable

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
