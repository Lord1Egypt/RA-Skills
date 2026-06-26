---
name: cron-copilot-ops
description: "Install, configure, and operate CronCopilot — a Python-based scheduled task management system for cron jobs, scripts, monitoring, and alerts."
license: MIT
metadata:
  author: eden2f
  version: "1.0.0"
---

# CronCopilot Operations Skill

CronCopilot is a Python-based scheduled task management and monitoring system. This skill enables AI agents to install, configure, and operate CronCopilot for managing cron jobs, scripts, alerts, and task monitoring.

- **GitHub**: https://github.com/eden2f/cron-copilot
- **Gitee**: https://gitee.com/eden2f/cron-copilot

## When to Use This Skill

> **Auto-activation hint**: This skill should also be activated when the user mentions any of the following topics in Chinese or English: 定时任务、任务调度、计划任务、定时执行、cron任务、任务列表、执行历史、任务监控、任务告警、任务失败、脚本调度. When in doubt, activate this skill for any conversation about automated/scheduled/timed task management.

Activate this skill when the user needs to:

- **Set up scheduled tasks** — create, modify, or delete cron jobs
- **Manage scripts** — register, remove, or inspect scripts for task execution
- **Monitor task execution** — check task status, view execution history, diagnose failures
- **Configure alerting & notifications** — set up failure alerts, performance threshold alerts, email notifications
- **Troubleshoot scheduled tasks** — debug failing tasks, resolve dependency issues, handle stuck processes

## System Requirements

| Requirement | Detail |
|---|---|
| Python | 3.10+ |
| OS | Linux / macOS (Windows via WSL2) |
| Database | SQLite (built-in, no external DB needed) |

## Quick Start

```bash
# Clone the repository
git clone https://gitee.com/eden2f/cron-copilot.git
cd cron-copilot

# Production install (recommended for deployment)
pip install .

# Development install (editable mode, changes take effect immediately)
pip install -e .

# Development install with dev dependencies
pip install -e ".[dev]"

# Initialize CronCopilot (creates config and database)
croncopilot init
```

After initialization, start the scheduler:

```bash
croncopilot start          # foreground mode
croncopilot start --daemon # background daemon mode
```

## Upgrade CronCopilot

```bash
# Production upgrade
pip install --upgrade .
croncopilot stop && croncopilot start --daemon

# Development mode (editable install): just pull latest code and restart
git pull
croncopilot stop && croncopilot start --daemon

# Update Chinese holiday data
pip install -U chinesecalendar
```

## Core CLI Commands

### Initialization & Lifecycle

```bash
croncopilot init              # Initialize config and database
croncopilot start             # Start scheduler (foreground)
croncopilot start --foreground # Explicitly start in foreground mode
croncopilot start --daemon    # Start scheduler (daemon mode)
croncopilot stop              # Stop the scheduler
croncopilot status            # Show scheduler status
croncopilot health            # Perform system health check
```

### Global Options

| Option | Short | Description |
|---|---|---|
| `--config <path>` | `-c` | Specify a custom configuration file path (default: `~/.croncopilot/config.yaml`) |
| `--verbose` | `-v` | Enable verbose output for debugging |

### Task Management

```bash
croncopilot task add [OPTIONS]      # Add a new scheduled task
croncopilot task remove <name>      # Remove a task by name
croncopilot task remove <name> -f   # Force remove (skip confirmation)
croncopilot task list               # List all tasks
croncopilot task list -c <category> # Filter by category
croncopilot task list -s <status>   # Filter by status (enabled/disabled)
croncopilot task run <name>         # Manually trigger a task
croncopilot task history <name>           # View execution history of a task
croncopilot task history <name> -d 7      # View last 7 days
croncopilot task history <name> -l 50     # Show latest 50 records
croncopilot task history <name> --stats-only  # Show statistics summary only
```

**Key options for `task add`:**

> For the complete list of all available options, see the [`croncopilot task add`](REFERENCE.md#croncopilot-task-add-options) section in REFERENCE.md.

| Option | Description | Example |
|---|---|---|
| `--name` | Task name (unique identifier) | `--name daily-backup` |
| `--schedule` | Schedule expression | `--schedule "0 2 * * *"` |
| `--schedule-type` | Type (required): `cron`, `interval`, `daily`, `weekly`, `monthly` | `--schedule-type cron` |
| `--script` | Script path to execute (required) | `--script /opt/scripts/backup.py` |
| `--priority` | Priority 1-10 (higher = more important) | `--priority 8` |
| `--max-instances` | Max concurrent instances | `--max-instances 1` |
| `--depends-on` | Dependency task name(s) | `--depends-on pre-check` |
| `--holiday-mode` | Holiday handling mode | `--holiday-mode workday_only` |
| `--timeout` | Execution timeout in seconds | `--timeout 3600` |
| `--max-retries` | Max retry attempts on failure (default: 0) | `--max-retries 3` |
| `--description` | Human-readable description of the task | `--description "Daily backup job"` |
| `--category` | Task category for organization | `--category data-pipeline` |

### Script Management

```bash
croncopilot script add [OPTIONS]    # Register a new script
croncopilot script remove <name>              # Remove a registered script
croncopilot script remove <name> --delete-file  # Also delete the script file
croncopilot script list               # List all registered scripts
croncopilot script list -c <category> # Filter by category
croncopilot script info <name>      # Show script details
```

**Key options for `script add`:**

| Option | Description | Example |
|---|---|---|
| `--name` | Script name | `--name my-backup` |
| `--path` | Path to the script file | `--path /opt/scripts/backup.py` |
| `--venv` | Python virtual environment path | `--venv /opt/venvs/backup` |
| `--author` | Script author | `--author "eden2f"` |
| `--description` | Script description | `--description "ETL pipeline script"` |
| `--category` | Script category | `--category etl` |

## Schedule Types

### Cron Expression (5-field standard format)

Format: `minute hour day month weekday`

```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-6, 0=Sunday)
│ │ │ │ │
* * * * *
```

Examples: `0 2 * * *` (daily 2 AM), `*/5 * * * *` (every 5 min), `0 9 * * 1-5` (weekdays 9 AM)

### Interval

Use shorthand: `5m` (5 minutes), `1h` (1 hour), `1d` (1 day), `1w` (1 week)

### Preset Types

- `daily` — once per day (default midnight)
- `weekly` — once per week
- `monthly` — once per month

## Holiday Awareness

CronCopilot supports Chinese statutory holiday recognition. Configure via `--holiday-mode`:

| Mode | Behavior |
|---|---|
| `none` | Execute regardless of holidays (default) |
| `workday_only` | Execute only on working days (skip weekends & holidays) |
| `holiday_only` | Execute only on holidays |
| `skip_holiday` | Skip statutory holidays but run on weekends |
| `skip_workday` | Execute only on non-workdays (skip regular workdays, run on weekends & holidays) |

Example:

```bash
croncopilot task add --name daily-report \
  --schedule "0 9 * * *" \
  --schedule-type cron \
  --script /opt/scripts/report.py \
  --holiday-mode workday_only
```

## Task Dependencies & Priority

### Priority

Tasks have priority levels 1–10 (higher number = higher priority). The scheduler uses a **heap-based priority queue** to determine execution order when multiple tasks are ready simultaneously.

### Dependencies

Tasks can declare dependencies on other tasks. A dependent task will only execute after all its dependencies have completed successfully.

```bash
croncopilot task add --name data-export \
  --schedule "0 3 * * *" \
  --script export.py \
  --depends-on data-cleanup \
  --priority 5
```

### Concurrency Control

Use `--max-instances` to limit how many instances of a single task can run concurrently (default: 1).

## Alerting & Self-Healing

### Alert Types

- **Immediate failure alert** — triggered on any task failure
- **Consecutive failure alert** — triggered after N consecutive failures
- **Performance threshold alert** — triggered when execution time exceeds threshold

### Email Notification

Configure email alerts in the CronCopilot config file (`~/.croncopilot/config.yaml`):

```yaml
alerting:
  email:
    enabled: true
    smtp_host: smtp.example.com
    smtp_port: 587
    username: alerts@example.com
    password: "your-password"
    recipients:
      - admin@example.com
```

### Self-Healing

- **Auto-retry** with exponential backoff (`--max-retries 3`)
- **Health check** — periodic scheduler self-diagnosis
- **Deadlock detection** — identifies and terminates stuck tasks automatically
- **Timeout enforcement** — kills tasks exceeding `--timeout` threshold

## Hot Reload

After modifying the configuration file, apply changes without restarting:

```bash
kill -SIGHUP $(cat ~/.croncopilot/run/croncopilot.pid)
```

The scheduler reloads configuration and applies changes immediately.

## System Service Deployment

CronCopilot can auto-generate service configurations for production deployment:

```bash
croncopilot service install    # Generate and install system service
croncopilot service uninstall  # Remove system service
```

> **Note**: The `service` subcommand may not be available in all versions (e.g., not present in v0.1.0). If unavailable, refer to the [Daemon Process Management](REFERENCE.md#7-daemon-process-management) section in REFERENCE.md for manual systemd/launchd configuration.

Supported platforms:

| Platform | Service Manager |
|---|---|
| Linux | systemd |
| macOS | launchd |
| Windows (WSL2) | Windows Service wrapper |

## Common Usage Examples

### 1. Add a Daily Backup Task at 2 AM

```bash
croncopilot task add \
  --name daily-backup \
  --schedule "0 2 * * *" \
  --schedule-type cron \
  --script /opt/scripts/backup.sh \
  --priority 8 \
  --max-retries 3 \
  --timeout 7200
```

### 2. Add a Workday-Only Report Task

```bash
croncopilot task add \
  --name morning-report \
  --schedule "0 9 * * *" \
  --schedule-type cron \
  --script /opt/scripts/gen_report.py \
  --holiday-mode workday_only \
  --priority 6
```

### 3. Register a Script with Virtual Environment

```bash
croncopilot script add \
  --name etl-pipeline \
  --path /opt/scripts/etl.py \
  --venv /opt/venvs/etl-env

croncopilot task add \
  --name nightly-etl \
  --schedule "0 1 * * *" \
  --schedule-type cron \
  --script etl-pipeline
```

### 4. Configure Task Dependencies

```bash
# Step 1: cleanup task runs first
croncopilot task add \
  --name data-cleanup \
  --schedule "0 0 * * *" \
  --script cleanup.py \
  --priority 9

# Step 2: export task depends on cleanup
croncopilot task add \
  --name data-export \
  --schedule "0 1 * * *" \
  --script export.py \
  --depends-on data-cleanup \
  --priority 7
```

### 5. Start as Daemon and Check Status

```bash
croncopilot start --daemon
croncopilot status
croncopilot task list
```
