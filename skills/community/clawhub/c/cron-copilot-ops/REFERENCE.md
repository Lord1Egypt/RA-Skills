# CronCopilot Detailed Reference

> **Source**: [GitHub](https://github.com/eden2f/cron-copilot) | [Gitee](https://gitee.com/eden2f/cron-copilot)
>
> CronCopilot is a Python-based cron job management and monitoring system providing task scheduling, script management, execution monitoring, alert notifications, and self-healing capabilities.

> **Compatibility**: This reference is based on CronCopilot v0.1.0. Some features (e.g., the `service` subcommand) may be added in later versions.

---

## Table of Contents

1. [Complete CLI Command Reference](#1-complete-cli-command-reference)
2. [Configuration File Reference](#2-configuration-file-reference)
3. [Schedule Expression Syntax](#3-schedule-expression-syntax)
4. [Holiday Configuration](#4-holiday-configuration)
5. [Alert & Notification Configuration](#5-alert--notification-configuration)
6. [Virtual Environment Isolation](#6-virtual-environment-isolation)
7. [Daemon Process Management](#7-daemon-process-management)
8. [Monitoring & Metrics](#8-monitoring--metrics)
9. [Troubleshooting Guide](#9-troubleshooting-guide)
10. [Complete Usage Examples](#10-complete-usage-examples)

---

## 1. Complete CLI Command Reference

### Global Options

All commands accept the following global options:

| Option | Short | Description |
|--------|-------|-------------|
| `--config <path>` | `-c` | Specify a custom configuration file path (default: `~/.croncopilot/config.yaml`). |
| `--verbose` | `-v` | Enable verbose/debug output. |

---

### `croncopilot init`

Initialize CronCopilot configuration and directory structure.

```bash
croncopilot init
```

**Behavior:**
- Creates the default configuration file at `~/.croncopilot/config.yaml`
- Initializes the SQLite database at `~/.croncopilot/croncopilot.db`
- Creates the log directory at `~/.croncopilot/logs/`
- Creates the scripts directory at `~/.croncopilot/scripts/`
- Creates the PID file directory at `~/.croncopilot/run/`

If the configuration already exists, a prompt will ask whether to overwrite.

---

### `croncopilot start [OPTIONS]`

Start the CronCopilot scheduler.

```bash
# Foreground mode (default)
croncopilot start

# Daemon (background) mode
croncopilot start --daemon
croncopilot start -d
```

| Option | Short | Description |
|--------|-------|-------------|
| `--daemon` | `-d` | Run as a background daemon process. PID is written to `~/.croncopilot/run/croncopilot.pid`. |
| `--foreground` | `-f` | Run in foreground mode (default behavior). Logs are printed to stdout/stderr. |

**Foreground mode**: The scheduler runs in the current terminal session. Logs are printed to stdout/stderr. Press `Ctrl+C` to stop gracefully.

**Daemon mode**: The process detaches from the terminal, writes its PID to the PID file, and redirects output to the configured log file.

---

### `croncopilot stop`

Stop a running CronCopilot daemon process.

```bash
croncopilot stop
```

**Behavior:**
- Reads the PID from `~/.croncopilot/run/croncopilot.pid`
- Sends `SIGTERM` to the process for graceful shutdown
- Waits for the process to finish current task executions
- Removes the PID file after successful shutdown
- If the process does not respond within the timeout, sends `SIGKILL`

---

### `croncopilot status`

Display the current running status of CronCopilot.

```bash
croncopilot status
```

**Output includes:**
- Daemon running state (running / stopped)
- PID (if running)
- Uptime
- Number of registered tasks
- Number of active tasks
- Next scheduled execution time
- System resource usage (CPU%, Memory%, Disk%)

---

### `croncopilot health`

Perform a system health check on CronCopilot.

```bash
croncopilot health
```

**Output includes:**
- Scheduler process status
- Database connectivity and integrity
- Disk space availability
- Configuration file validity
- Pending task queue status
- Recent error summary

---

### `croncopilot task add [OPTIONS]`

Register a new scheduled task.

```bash
croncopilot task add --name <NAME> --script <SCRIPT> [OPTIONS]
```

| Option | Short | Required | Default | Description |
|--------|-------|----------|---------|-------------|
| `--name` | `-n` | **Yes** | — | Unique task name identifier. |
| `--script` | `-s` | **Yes** | — | Script path to execute. |
| `--schedule-type` | `-t` | **Yes** | — | Scheduling type: `cron`, `interval`, `daily`, `weekly`, `monthly`. |
| `--schedule` | `-S` | No | `* * * * *` | Schedule expression (format depends on `--schedule-type`). |
| `--priority` | `-p` | No | `5` | Task priority from 1 (lowest) to 10 (highest). Higher priority tasks execute first when multiple tasks are scheduled simultaneously. |
| `--holiday-mode` | `-H` | No | `none` | Holiday handling mode: `none`, `workday_only`, `holiday_only`, `skip_holiday`. |
| `--max-instances` | `-m` | No | `1` | Maximum number of concurrent running instances of this task. Set to `0` for unlimited. |
| `--depends-on` | `-D` | No | — | Comma-separated list of task names this task depends on. The task will only execute after all dependencies complete successfully. |
| `--timeout` | `-T` | No | `3600` | Maximum execution time in seconds. The task is killed if it exceeds this limit. Set to `0` for no timeout. |
| `--max-retries` | `-r` | No | `0` | Number of retry attempts on failure. |
| `--description` | | No | — | Human-readable description of the task. |
| `--category` | | No | — | Task category for organization. |

**Example:**

```bash
croncopilot task add \
  --name daily-report \
  --script generate_report.py \
  --schedule-type cron \
  --schedule "30 9 * * 1-5" \
  --priority 8 \
  --holiday-mode workday_only \
  --timeout 1800 \
  --max-retries 3
```

---

### `croncopilot task remove <name>`

Remove a registered task by name.

```bash
croncopilot task remove daily-report
```

| Option | Short | Description |
|--------|-------|-------------|
| `--force` | `-f` | Skip confirmation prompt and force remove the task. |

**Behavior:**
- Removes the task from the scheduler
- Execution history is preserved in the database
- If the task is currently running, it will be stopped before removal

---

### `croncopilot task list`

List all registered tasks.

```bash
croncopilot task list
```

| Option | Short | Description |
|--------|-------|-------------|
| `--category <name>` | `-c` | Filter tasks by category. |
| `--status <state>` | `-s` | Filter tasks by status (`enabled` / `disabled`). |

**Output columns:** Name, Script, Schedule, Status (enabled/disabled), Last Run, Next Run, Last Result (success/failure).

---

### `croncopilot task run <name>`

Manually trigger an immediate execution of a task.

```bash
croncopilot task run daily-report
```

**Behavior:**
- Executes the task once immediately, regardless of schedule
- Respects `--max-instances` limits
- Execution is recorded in history
- Does not affect the next scheduled execution time

---

### `croncopilot task history <name>`

View the execution history of a task.

```bash
croncopilot task history daily-report
```

| Option | Short | Description |
|--------|-------|-------------|
| `--days <N>` | `-d` | View execution history for the last N days (default: 30). |
| `--limit <N>` | `-l` | Show the latest N records (default: 20). |
| `--stats-only` | — | Show statistics summary only (total runs, success/failure counts, average duration). |

**Output columns:** Execution ID, Start Time, End Time, Duration, Exit Code, Status (success/failure/timeout/killed), Retry Attempt.

---

### `croncopilot script add [OPTIONS]`

Register a script for use with tasks.

```bash
croncopilot script add --path <PATH> [OPTIONS]
```

| Option | Short | Required | Default | Description |
|--------|-------|----------|---------|-------------|
| `--path` | `-p` | **Yes** | — | Absolute or relative path to the script file. |
| `--name` | `-n` | No | filename stem | Registered name for the script. Defaults to the filename without extension. |
| `--venv` | `-v` | No | — | Path to a Python virtual environment to use for execution. |
| `--author` | `-a` | No | — | Script author. |
| `--description` | `-d` | No | — | Script description. |
| `--category` | `-c` | No | — | Script category for organization. |

**Behavior:**
- Performs syntax validation (for Python scripts: `py_compile`)
- Creates an automatic backup copy in `~/.croncopilot/scripts/`
- Records script metadata (hash, size, registration time)

---

### `croncopilot script remove <name>`

Remove a registered script.

```bash
croncopilot script remove generate_report
```

| Option | Description |
|--------|-------------|
| `--delete-file` | Also delete the actual script file from disk (by default, only the registration is removed). |

**Note:** Tasks using this script will be disabled automatically.

---

### `croncopilot script list`

List all registered scripts.

```bash
croncopilot script list
```

| Option | Short | Description |
|--------|-------|-------------|
| `--category <name>` | `-c` | Filter scripts by category. |

**Output columns:** Name, Path, Interpreter, Virtual Env, Registered At, Used By (task count).

---

### `croncopilot script info <name>`

Show detailed information about a registered script.

```bash
croncopilot script info generate_report
```

**Output includes:** Name, file path, interpreter, virtual environment, file size, file hash, registration time, last modified time, associated tasks.

---

## 2. Configuration File Reference

The default configuration file is located at `~/.croncopilot/config.yaml`.

```yaml
# ============================================================
# CronCopilot Configuration
# ============================================================

# --- Scheduler Configuration ---
scheduler:
  # Maximum number of tasks to run concurrently
  max_workers: 10
  # How often the scheduler checks for due tasks (seconds)
  tick_interval: 30
  # Timezone for schedule evaluation
  timezone: "Asia/Shanghai"
  # Graceful shutdown timeout in seconds
  shutdown_timeout: 60
  # Enable task dependency resolution
  enable_dependencies: true
  # Misfire grace time: max seconds a task can be late and still run
  misfire_grace_time: 300

# --- Logging Configuration ---
logging:
  # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
  level: "INFO"
  # Log file path
  file: "~/.croncopilot/logs/croncopilot.log"
  # Max size per log file (bytes), 0 for unlimited
  max_size: 10485760  # 10 MB
  # Number of rotated log files to keep
  backup_count: 5
  # Log format string
  format: "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
  # Also log task stdout/stderr to separate files
  task_log_dir: "~/.croncopilot/logs/tasks/"

# --- Database Configuration ---
database:
  # SQLite database file path
  path: "~/.croncopilot/croncopilot.db"
  # Enable WAL mode for better concurrent read performance
  wal_mode: true
  # Database connection timeout (seconds)
  timeout: 30
  # Max execution history records to keep per task (0 = unlimited)
  max_history_per_task: 1000

# --- Alert Configuration ---
alert:
  # Enable alert system
  enabled: true
  # Alert on immediate failure
  on_failure: true
  # Alert after N consecutive failures (0 = disabled)
  consecutive_failure_threshold: 3
  # Alert when execution time exceeds this ratio of timeout (0.0-1.0)
  performance_threshold_ratio: 0.8
  # Cooldown period between repeated alerts for the same task (seconds)
  alert_cooldown: 1800
  # Notification channels (see Alert & Notification section)
  channels:
    email:
      enabled: false
      smtp_host: "smtp.example.com"
      smtp_port: 587
      smtp_tls: true
      smtp_user: ""
      smtp_password: ""
      from_address: ""
      to_addresses: []

# --- System Resource Monitoring ---
monitor:
  # Enable system resource monitoring
  enabled: true
  # Monitoring check interval (seconds)
  interval: 60
  # CPU usage alert threshold (percentage)
  cpu_threshold: 90
  # Memory usage alert threshold (percentage)
  memory_threshold: 85
  # Disk usage alert threshold (percentage)
  disk_threshold: 90
  # Monitored disk paths
  disk_paths:
    - "/"

# --- Self-Healing Configuration ---
self_healing:
  # Enable self-healing strategies
  enabled: true
  # Auto-restart tasks that failed due to transient errors
  auto_restart: true
  # Max auto-restart attempts per task per day
  max_restart_per_day: 5
  # Auto-restart delay (seconds)
  restart_delay: 30
  # Auto-clear stale PID files
  clear_stale_pid: true
  # Detect and resolve deadlocks
  deadlock_detection: true
  # Deadlock detection interval (seconds)
  deadlock_check_interval: 300
  # Auto-recover database from WAL corruption
  db_auto_recover: true
```

### Configuration Field Details

| Section | Field | Type | Description |
|---------|-------|------|-------------|
| `scheduler.max_workers` | int | Maximum concurrent task processes. Increase for I/O-heavy workloads. |
| `scheduler.tick_interval` | int | Scheduler polling interval in seconds. Lower values = more precise scheduling but higher CPU usage. |
| `scheduler.timezone` | string | IANA timezone string for interpreting cron expressions. |
| `scheduler.shutdown_timeout` | int | Seconds to wait for running tasks before force-killing on shutdown. |
| `scheduler.enable_dependencies` | bool | When `true`, tasks with `depends_on` will wait for dependencies. |
| `scheduler.misfire_grace_time` | int | If the scheduler is behind, tasks within this window (seconds) will still fire. |
| `logging.level` | string | Minimum log level. One of: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. |
| `logging.file` | string | Log file path, supports ~ expansion. |
| `logging.format` | string | Python logging format string. |
| `logging.max_size` | int | Log file rotation threshold in bytes. |
| `logging.backup_count` | int | Number of rotated log files to retain. |
| `logging.task_log_dir` | string | Directory for individual task log files. |
| `database.wal_mode` | bool | SQLite WAL mode improves concurrent read access. Recommended `true`. |
| `database.max_history_per_task` | int | Prunes old execution history records. Set `0` to keep all. |
| `alert.consecutive_failure_threshold` | int | Triggers alert after this many consecutive failures. `0` disables. |
| `alert.performance_threshold_ratio` | float | Ratio of timeout. E.g., `0.8` alerts when execution takes ≥80% of timeout. |
| `alert.alert_cooldown` | int | Prevents alert spam by enforcing minimum seconds between alerts per task. |
| `monitor.cpu_threshold` | int | System CPU percentage that triggers an alert. |
| `monitor.memory_threshold` | int | System memory percentage that triggers an alert. |
| `self_healing.max_restart_per_day` | int | Safety cap on automatic restarts to prevent infinite restart loops. |
| `self_healing.deadlock_detection` | bool | Periodically checks for tasks stuck beyond their timeout. |

---

## 3. Schedule Expression Syntax

### Standard Cron Expression (5-field)

```
┌───────── minute (0-59)
│ ┌─────── hour (0-23)
│ │ ┌───── day of month (1-31)
│ │ │ ┌─── month (1-12)
│ │ │ │ ┌─ day of week (0-6, 0=Sunday)
│ │ │ │ │
* * * * *
```

**Special Characters:**

| Character | Description | Example |
|-----------|-------------|---------|
| `*` | Any value | `* * * * *` — every minute |
| `,` | Value list separator | `1,15,30 * * * *` — at minute 1, 15, and 30 |
| `-` | Range of values | `1-5` — Monday through Friday (in day-of-week) |
| `/` | Step values | `*/15 * * * *` — every 15 minutes |

**Common Cron Expressions:**

| Expression | Description |
|------------|-------------|
| `* * * * *` | Every minute |
| `*/5 * * * *` | Every 5 minutes |
| `0 * * * *` | Every hour at minute 0 |
| `0 9 * * *` | Every day at 09:00 |
| `30 9 * * 1-5` | Weekdays at 09:30 |
| `0 0 * * *` | Every day at midnight |
| `0 9,18 * * *` | Every day at 09:00 and 18:00 |
| `0 0 1 * *` | First day of every month at midnight |
| `0 0 * * 0` | Every Sunday at midnight |
| `0 0 1 1 *` | January 1st at midnight (yearly) |
| `0 */2 * * *` | Every 2 hours |
| `0 9 * * 1` | Every Monday at 09:00 |
| `15 10 1,15 * *` | 1st and 15th of each month at 10:15 |

### Interval Expression

Format: `<number><unit>`

| Unit | Description | Example |
|------|-------------|---------|
| `s` | Seconds | `30s` — every 30 seconds |
| `m` | Minutes | `5m` — every 5 minutes |
| `h` | Hours | `2h` — every 2 hours |
| `d` | Days | `1d` — every day |
| `w` | Weeks | `1w` — every week |

Use with `--schedule-type interval`:

```bash
croncopilot task add --name heartbeat --script ping.py \
  --schedule-type interval --schedule "30s"
```

### Preset Schedule Types

**daily**: Runs once per day. The `--schedule` value specifies the time in `HH:MM` format.

```bash
croncopilot task add --name daily-cleanup --script cleanup.py \
  --schedule-type daily --schedule "03:00"
```

**weekly**: Runs once per week. The `--schedule` value specifies `<DAY> <HH:MM>` where DAY is `mon`, `tue`, `wed`, `thu`, `fri`, `sat`, `sun`.

```bash
croncopilot task add --name weekly-report --script report.py \
  --schedule-type weekly --schedule "mon 09:00"
```

**monthly**: Runs once per month. The `--schedule` value specifies `<DAY_NUMBER> <HH:MM>`.

```bash
croncopilot task add --name monthly-billing --script billing.py \
  --schedule-type monthly --schedule "1 00:00"
```

---

## 4. Holiday Configuration

CronCopilot includes built-in support for Chinese statutory holidays (中国法定节假日), enabling intelligent scheduling that accounts for holidays and adjusted workdays (调休).

### Holiday Data Source

Holiday data is bundled with the package and updated annually. It includes:
- All Chinese statutory holidays (Spring Festival, National Day, etc.)
- Adjusted workdays (调休/补班 — weekend days that become workdays)
- Regular weekends (Saturday and Sunday)

### Holiday Modes

Set via `--holiday-mode` when adding a task:

#### `none` (default)

The task runs according to its schedule with **no holiday awareness**. Weekends and holidays are treated as regular days.

```bash
croncopilot task add --name always-run --script job.py \
  --schedule "0 9 * * *" --holiday-mode none
```

#### `workday_only`

The task runs **only on workdays**:
- Skips Saturdays and Sundays (unless they are adjusted workdays / 调休)
- Skips Chinese statutory holidays
- **Executes** on adjusted workdays (调休日 that fall on weekends)

```bash
croncopilot task add --name weekday-report --script report.py \
  --schedule "0 9 * * *" --holiday-mode workday_only
```

**Example behavior for Spring Festival week:**
- Adjusted workday (Sat before Spring Festival): **Executes** ✓
- Spring Festival holidays (Mon-Fri): **Skipped** ✗
- Regular Saturday/Sunday: **Skipped** ✗

#### `holiday_only`

The task runs **only on holidays** (statutory holidays and regular weekends). It does **not** run on adjusted workdays.

```bash
croncopilot task add --name holiday-backup --script backup.py \
  --schedule "0 2 * * *" --holiday-mode holiday_only
```

#### `skip_holiday`

The task runs on **all days except Chinese statutory holidays**. Regular weekends are treated normally (task executes if schedule matches).

```bash
croncopilot task add --name skip-holiday-job --script job.py \
  --schedule "0 9 * * *" --holiday-mode skip_holiday
```

#### `skip_workday`

The task runs **only on non-workdays** — it skips regular workdays (Monday–Friday, excluding holidays) and adjusted workdays (调休), but executes on weekends and statutory holidays.

```bash
croncopilot task add --name weekend-maintenance --script maintenance.py \
  --schedule "0 3 * * *" --holiday-mode skip_workday
```

**Comparison:**

| Day Type | `none` | `workday_only` | `holiday_only` | `skip_holiday` | `skip_workday` |
|----------|----------|----------------|-----------------|----------------|----------------|
| Regular weekday | ✓ Run | ✓ Run | ✗ Skip | ✓ Run | ✗ Skip |
| Regular weekend | ✓ Run | ✗ Skip | ✓ Run | ✓ Run | ✓ Run |
| Statutory holiday | ✓ Run | ✗ Skip | ✓ Run | ✗ Skip | ✓ Run |
| Adjusted workday (调休) | ✓ Run | ✓ Run | ✗ Skip | ✓ Run | ✗ Skip |

---

## 5. Alert & Notification Configuration

### Email Notification (SMTP)

Configure in `config.yaml` under `alert.channels.email`:

```yaml
alert:
  enabled: true
  channels:
    email:
      enabled: true
      smtp_host: "smtp.gmail.com"
      smtp_port: 587
      smtp_tls: true
      smtp_user: "your-email@gmail.com"
      smtp_password: "your-app-password"
      from_address: "croncopilot@your-domain.com"
      to_addresses:
        - "admin@your-domain.com"
        - "oncall@your-domain.com"
```

### Alert Trigger Conditions

#### Immediate Failure Alert

Triggered when **any** task execution fails (non-zero exit code, exception, or timeout).

```yaml
alert:
  on_failure: true
```

#### Consecutive Failure Alert

Triggered when a task fails **N times in a row**. Useful for distinguishing transient errors from persistent issues.

```yaml
alert:
  consecutive_failure_threshold: 3  # alert after 3 consecutive failures
```

Set to `0` to disable.

#### Performance Threshold Alert

Triggered when a task's execution time exceeds a specified ratio of its configured timeout. For example, if timeout is 3600s and ratio is 0.8, an alert fires when execution exceeds 2880s.

```yaml
alert:
  performance_threshold_ratio: 0.8
```

#### System Resource Alert

Triggered when system resource usage exceeds configured thresholds.

```yaml
monitor:
  enabled: true
  cpu_threshold: 90       # Alert when CPU usage > 90%
  memory_threshold: 85    # Alert when memory usage > 85%
  disk_threshold: 90      # Alert when disk usage > 90%
```

### Alert Cooldown

To prevent alert flooding, a cooldown period can be set per task:

```yaml
alert:
  alert_cooldown: 1800  # 30 minutes between repeated alerts for the same task
```

---

## 6. Virtual Environment Isolation

CronCopilot supports running each script in its own isolated Python virtual environment, preventing dependency conflicts between tasks.

### Specifying a Virtual Environment

When registering a script:

```bash
# Create a venv for the script
python3 -m venv /opt/venvs/report-env
/opt/venvs/report-env/bin/pip install pandas openpyxl

# Register the script with its venv
croncopilot script add \
  --path /opt/scripts/generate_report.py \
  --name generate_report \
  --venv /opt/venvs/report-env
```

### How It Works

When a task associated with a venv-configured script executes:
1. CronCopilot activates the specified virtual environment
2. The script runs using the venv's Python interpreter (`<venv>/bin/python`)
3. Only packages installed in that venv are available to the script
4. The system Python environment is unaffected

### Best Practices

1. **One venv per project group**: Scripts with shared dependencies can share a venv.

   ```bash
   # Shared venv for all reporting scripts
   python3 -m venv /opt/venvs/reporting
   /opt/venvs/reporting/bin/pip install -r /opt/scripts/reporting/requirements.txt
   ```

2. **Pin dependency versions**: Use `requirements.txt` with pinned versions.

   ```
   pandas==2.1.0
   openpyxl==3.1.2
   ```

3. **Separate conflicting dependencies**: If two scripts need different versions of the same library, use separate venvs.

   ```bash
   croncopilot script add --path script_a.py --name script-a --venv /opt/venvs/env-a
   croncopilot script add --path script_b.py --name script-b --venv /opt/venvs/env-b
   ```

4. **Document venv contents**: Keep a `requirements.txt` alongside each venv for reproducibility.

---

## 7. Daemon Process Management

### Foreground vs. Daemon Mode

| Aspect | Foreground (`croncopilot start`) | Daemon (`croncopilot start -d`) |
|--------|------|--------|
| Terminal attachment | Attached, logs to stdout | Detached, logs to file |
| Stop method | `Ctrl+C` | `croncopilot stop` |
| Survives terminal close | No | Yes |
| PID file | Not created | Written to `~/.croncopilot/run/croncopilot.pid` |
| Recommended for | Development, debugging | Production deployment |

### PID File Management

- Location: `~/.croncopilot/run/croncopilot.pid`
- Created on daemon start, removed on clean shutdown
- Stale PID files (process no longer running) are automatically detected and cleaned if `self_healing.clear_stale_pid` is enabled

### Graceful Shutdown

When `croncopilot stop` is issued:
1. `SIGTERM` is sent to the daemon process
2. The scheduler stops accepting new task executions
3. Currently running tasks are allowed to finish (up to `scheduler.shutdown_timeout` seconds)
4. After timeout, remaining tasks receive `SIGKILL`
5. PID file is removed

### Configuration Hot Reload (SIGHUP)

Send `SIGHUP` to the daemon to reload configuration without restarting:

```bash
kill -HUP $(cat ~/.croncopilot/run/croncopilot.pid)
```

**What is reloaded:**
- Task schedules and parameters
- Alert configuration
- Monitoring thresholds
- Logging level

**What is NOT reloaded (requires restart):**
- Database path
- Scheduler `max_workers`
- PID file path

### systemd Service (Linux)

Generate and install a systemd service file:

```bash
# Generate the service file
croncopilot service install --type systemd
```

> **Note**: The `service` subcommand may not be available in all CronCopilot versions (e.g., it is not present in v0.1.0 CLI). If the command is unavailable, you can manually create the service configuration files as shown below.

This creates `/etc/systemd/system/croncopilot.service`:

```ini
[Unit]
Description=CronCopilot - Python Cron Job Manager
After=network.target

[Service]
Type=forking
User=croncopilot
Group=croncopilot
PIDFile=/home/croncopilot/.croncopilot/run/croncopilot.pid
ExecStart=/usr/local/bin/croncopilot start --daemon
ExecStop=/usr/local/bin/croncopilot stop
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable croncopilot
sudo systemctl start croncopilot

# Check status
sudo systemctl status croncopilot
```

### launchd Service (macOS)

Generate and install a launchd plist:

```bash
croncopilot service install --type launchd
```

This creates `~/Library/LaunchAgents/com.croncopilot.agent.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.croncopilot.agent</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/croncopilot</string>
        <string>start</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/you/.croncopilot/logs/croncopilot.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/you/.croncopilot/logs/croncopilot.err</string>
</dict>
</plist>
```

```bash
# Load the service
launchctl load ~/Library/LaunchAgents/com.croncopilot.agent.plist

# Unload the service
launchctl unload ~/Library/LaunchAgents/com.croncopilot.agent.plist
```

### Windows Service (via WSL2)

CronCopilot can run inside WSL2 on Windows:

```bash
# Inside WSL2
croncopilot start --daemon

# To auto-start with WSL, add to ~/.bashrc or ~/.profile:
croncopilot start --daemon 2>/dev/null || true
```

For a more robust setup, configure a Windows Task Scheduler entry to launch WSL and start CronCopilot on boot.

---

## 8. Monitoring & Metrics

### Task Execution Tracking

Every task execution is recorded with:
- Execution ID (unique identifier)
- Start and end timestamps
- Duration in seconds
- Exit code
- Status: `success`, `failure`, `timeout`, `killed`, `skipped`
- stdout/stderr output (stored in task-specific log files)
- Retry attempt number

### System Resource Metrics

When `monitor.enabled` is `true`, CronCopilot periodically collects:

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| CPU Usage (%) | System-wide CPU utilization | `monitor.cpu_threshold` |
| Memory Usage (%) | System RAM utilization | `monitor.memory_threshold` |
| Disk Usage (%) | Disk space utilization per configured path | `monitor.disk_threshold` |

### Execution History & Statistics

View task execution history:

```bash
# Full history for a specific task
croncopilot task history daily-report

# Summary statistics
croncopilot status
```

**Available statistics:**
- Total executions (all-time and recent)
- Success / failure counts
- Average execution duration
- Min / max execution duration
- Last execution result and timestamp

### Failure Rate Analysis

CronCopilot tracks per-task failure rates:
- **Recent failure rate**: Failures in the last N executions
- **Consecutive failure count**: Current streak of failures (resets on success)
- **Failure trend**: Increasing or decreasing failure rate over time

These metrics feed into the alert system and self-healing decisions.

---

## 9. Troubleshooting Guide

### Task Not Executing on Schedule

**Symptoms:** Task is registered but does not run at the expected time.

**Solutions:**
1. Verify the scheduler is running: `croncopilot status`
2. Check the task is enabled: `croncopilot task list`
3. Verify the cron expression: double-check field order (min hour day month weekday)
4. Check timezone configuration in `config.yaml` (`scheduler.timezone`)
5. Check holiday mode — task may be skipped due to holiday settings
6. Check misfire grace time — if the scheduler was down, the task may have been missed
7. Review logs: `tail -f ~/.croncopilot/logs/croncopilot.log`

### Script Execution Failure

**Symptoms:** Task runs but reports failure status.

**Solutions:**
1. Check task execution logs in `~/.croncopilot/logs/tasks/<task-name>/`
2. Test the script manually: `python3 /path/to/script.py`
3. If using a venv, verify the venv is valid: `<venv>/bin/python --version`
4. Check file permissions: `ls -la /path/to/script.py`

### Daemon Unexpectedly Exits

**Symptoms:** The daemon process stops without `croncopilot stop` being called.

**Solutions:**
1. Check system logs: `journalctl -u croncopilot` (systemd) or `/var/log/syslog`
2. Check CronCopilot logs for errors before the crash
3. Verify available memory — OOM killer may have terminated the process
4. Check PID file status: `cat ~/.croncopilot/run/croncopilot.pid`
5. Enable `self_healing.auto_restart` and use systemd `Restart=on-failure`
6. Check disk space — full disks can cause database write failures

### Deadlock Detection and Resolution

**Symptoms:** Tasks appear stuck in "running" state indefinitely.

**Solutions:**
1. Enable `self_healing.deadlock_detection: true`
2. Set appropriate `--timeout` values for all tasks
3. Check for tasks waiting on dependencies that will never complete
4. Manually kill stuck tasks: `croncopilot task run <name>` (will detect and reset stuck state)
5. Review `self_healing.deadlock_check_interval` — default is 300 seconds

### Configuration Hot Reload Not Working

**Symptoms:** Changes to `config.yaml` are not reflected after sending SIGHUP.

**Solutions:**
1. Verify the SIGHUP was sent to the correct PID: `kill -HUP $(cat ~/.croncopilot/run/croncopilot.pid)`
2. Check logs for reload confirmation or errors
3. Some settings require a full restart (see [Daemon Process Management](#7-daemon-process-management))
4. Validate YAML syntax: `python3 -c "import yaml; yaml.safe_load(open('config.yaml'))"`

### Database Locking Issues

**Symptoms:** "database is locked" errors in logs.

**Solutions:**
1. Enable WAL mode: set `database.wal_mode: true` in config (requires restart)
2. Increase database timeout: `database.timeout: 60`
3. Check for external processes accessing the database file
4. Enable `self_healing.db_auto_recover: true`
5. If corruption is suspected, stop the daemon and run: `sqlite3 croncopilot.db "PRAGMA integrity_check;"`

### Permission Issues

**Symptoms:** "Permission denied" errors when executing scripts or writing logs.

**Solutions:**
1. Verify the CronCopilot process user has read access to script files
2. Verify write access to log directories: `ls -la ~/.croncopilot/logs/`
3. Verify write access to the database file
4. If running as a systemd service, check the `User` and `Group` settings
5. For venv scripts, ensure the venv Python binary is executable

---

## 10. Complete Usage Examples

### Example 1: Getting Started — First Cron Task

Install CronCopilot, initialize, and create your first scheduled task.

```bash
# Install CronCopilot
pip install cron-copilot

# Initialize configuration and directories
croncopilot init

# Create a simple script
cat > ~/scripts/hello.py << 'EOF'
import datetime
print(f"Hello from CronCopilot! Current time: {datetime.datetime.now()}")
EOF

# Register the script
croncopilot script add --path ~/scripts/hello.py --name hello

# Create a task that runs every 5 minutes
croncopilot task add \
  --name hello-world \
  --script hello \
  --schedule-type interval \
  --schedule "5m"

# Start CronCopilot in foreground to verify
croncopilot start

# (In another terminal) Check status
croncopilot status
```

### Example 2: Holiday-Aware Workday Report

Configure a report task that runs only on Chinese workdays.

```bash
# Register the report script
croncopilot script add --path /opt/scripts/daily_report.py --name daily-report

# Create task: runs at 09:30 on workdays only (skips weekends & holidays)
croncopilot task add \
  --name workday-report \
  --script daily-report \
  --schedule-type cron \
  --schedule "30 9 * * *" \
  --holiday-mode workday_only \
  --priority 8 \
  --timeout 1800 \
  --max-retries 2 \
  --description "Generate daily business report on workdays"
```

### Example 3: Script with Virtual Environment Isolation

Register a script with its own isolated Python environment.

```bash
# Create a dedicated virtual environment
python3 -m venv /opt/venvs/data-pipeline
/opt/venvs/data-pipeline/bin/pip install pandas==2.1.0 sqlalchemy==2.0.20 requests==2.31.0

# Register the script with venv
croncopilot script add \
  --path /opt/scripts/data_pipeline.py \
  --name data-pipeline \
  --venv /opt/venvs/data-pipeline

# Create task
croncopilot task add \
  --name etl-pipeline \
  --script data-pipeline \
  --schedule-type cron \
  --schedule "0 2 * * *" \
  --timeout 7200 \
  --description "Nightly ETL data pipeline"
```

### Example 4: Task Dependency Chain (A → B → C)

Set up three tasks where B depends on A, and C depends on B.

```bash
# Register scripts
croncopilot script add --path /opt/scripts/extract.py --name extract
croncopilot script add --path /opt/scripts/transform.py --name transform
croncopilot script add --path /opt/scripts/load.py --name load

# Task A: Extract data (no dependencies)
croncopilot task add \
  --name etl-extract \
  --script extract \
  --schedule-type cron \
  --schedule "0 1 * * *" \
  --priority 10 \
  --timeout 3600

# Task B: Transform data (depends on A)
croncopilot task add \
  --name etl-transform \
  --script transform \
  --schedule-type cron \
  --schedule "0 1 * * *" \
  --depends-on etl-extract \
  --priority 8 \
  --timeout 3600

# Task C: Load data (depends on B)
croncopilot task add \
  --name etl-load \
  --script load \
  --schedule-type cron \
  --schedule "0 1 * * *" \
  --depends-on etl-transform \
  --priority 6 \
  --timeout 1800
```

When triggered, `etl-extract` runs first. Upon success, `etl-transform` starts. Upon its success, `etl-load` runs.

### Example 5: Email Alert Notification

Configure CronCopilot to send email alerts on task failures.

```bash
# Edit config.yaml to enable email alerts
cat >> ~/.croncopilot/config.yaml << 'EOF'

# Override alert settings
alert:
  enabled: true
  on_failure: true
  consecutive_failure_threshold: 3
  performance_threshold_ratio: 0.8
  alert_cooldown: 1800
  channels:
    email:
      enabled: true
      smtp_host: "smtp.gmail.com"
      smtp_port: 587
      smtp_tls: true
      smtp_user: "your-email@gmail.com"
      smtp_password: "your-app-specific-password"
      from_address: "croncopilot@your-domain.com"
      to_addresses:
        - "admin@your-domain.com"
        - "oncall@your-domain.com"
EOF

# Reload configuration if daemon is running
kill -HUP $(cat ~/.croncopilot/run/croncopilot.pid)
```

### Example 6: Daemon Deployment with systemd

Deploy CronCopilot as a production systemd service.

```bash
# Create a dedicated user
sudo useradd -r -s /bin/bash -m -d /home/croncopilot croncopilot

# Install as croncopilot user
sudo -u croncopilot pip install --user cron-copilot
sudo -u croncopilot croncopilot init

# Generate and install systemd service
sudo croncopilot service install --type systemd

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable croncopilot
sudo systemctl start croncopilot

# Verify
sudo systemctl status croncopilot
sudo -u croncopilot croncopilot status
```

### Example 7: Monitoring and Analyzing Task Execution

Monitor task performance and review execution history.

```bash
# Check overall system status
croncopilot status

# View execution history of a specific task
croncopilot task history etl-pipeline

# List all tasks with their current state
croncopilot task list

# Check logs for a specific task
tail -100 ~/.croncopilot/logs/tasks/etl-pipeline/latest.log

# Monitor real-time logs
tail -f ~/.croncopilot/logs/croncopilot.log
```

### Example 8: Auto-Retry and Self-Healing

Configure a task with automatic retry and self-healing on failure.

```bash
# Create a task with retry and self-healing
croncopilot task add \
  --name resilient-sync \
  --script data_sync.py \
  --schedule-type cron \
  --schedule "*/30 * * * *" \
  --timeout 900 \
  --max-retries 3 \
  --description "Data sync with auto-retry and self-healing"

# Ensure self-healing is enabled in config.yaml
# self_healing:
#   enabled: true
#   auto_restart: true
#   max_restart_per_day: 5
#   restart_delay: 30
```

When `resilient-sync` fails:
1. Retries up to 3 times with 60-second delays
2. If all retries fail, sends an alert notification

### Example 9: Hot Reload Configuration Changes

Modify task scheduling without restarting the daemon.

```bash
# Start daemon
croncopilot start -d

# Add a task running every hour
croncopilot task add \
  --name hourly-check \
  --script health_check.py \
  --schedule-type interval \
  --schedule "1h"

# Later, decide to change the schedule to every 30 minutes
# Edit config or re-add the task
croncopilot task remove hourly-check
croncopilot task add \
  --name hourly-check \
  --script health_check.py \
  --schedule-type interval \
  --schedule "30m"

# Or, modify config.yaml directly and reload
# (for changes to scheduler/alert/monitor settings)
kill -HUP $(cat ~/.croncopilot/run/croncopilot.pid)

# Verify the reload was successful
croncopilot status
croncopilot task list
```

### Example 10: Batch Managing Multiple Tasks

Set up and manage a suite of related cron tasks.

```bash
# Register all scripts at once
for script in backup.py cleanup.py report.py sync.py monitor.py; do
  croncopilot script add --path /opt/scripts/$script --name ${script%.py}
done

# Create a batch of tasks
croncopilot task add --name nightly-backup \
  --script backup --schedule "0 2 * * *" --priority 10 --timeout 7200

croncopilot task add --name log-cleanup \
  --script cleanup --schedule "0 3 * * *" --priority 5 --timeout 600 \
  --depends-on nightly-backup

croncopilot task add --name daily-report \
  --script report --schedule "0 9 * * 1-5" --priority 8 --timeout 1800 \
  --holiday-mode workday_only

croncopilot task add --name data-sync \
  --script sync --schedule-type interval --schedule "15m" --priority 7 \
  --max-instances 1 --max-retries 2

croncopilot task add --name system-monitor \
  --script monitor --schedule-type interval --schedule "5m" --priority 9

# List all tasks to verify
croncopilot task list

# Manually test one task
croncopilot task run daily-report

# Check its execution
croncopilot task history daily-report
```
