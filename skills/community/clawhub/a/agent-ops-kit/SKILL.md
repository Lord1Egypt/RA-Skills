---
name: Agent Ops Kit
description: Production-grade health monitoring, alerting, and service management for OpenClaw agents. Monitor URLs, auto-restart services, get Telegram alerts, track uptime.
version: 1.0.0
author: OpenClaw Systems
tags: [monitoring, health, alerting, telegram, devops, production]
price: 39
---

# Agent Ops Kit

A complete operational toolkit for running production services with autonomous health monitoring, intelligent alerting, service auto-recovery, task board management, and uptime tracking. Built from real production infrastructure running 24/7 across multiple sites.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Health Monitoring System](#health-monitoring-system)
3. [Telegram Alerting](#telegram-alerting)
4. [Service Auto-Recovery](#service-auto-recovery)
5. [Task Board System](#task-board-system)
6. [Uptime Metrics Tracking](#uptime-metrics-tracking)
7. [Orchestrator Loop](#orchestrator-loop)
8. [Configuration Reference](#configuration-reference)
9. [Recipes](#recipes)

---

## Quick Start

### Prerequisites

- Python 3.9+
- bash / zsh
- curl
- A Telegram bot token (see [Telegram Alerting](#telegram-alerting) for setup)

### 1. Create the directory structure

```bash
mkdir -p ~/.agent-ops/{config,logs,metrics,scripts,state}
```

### 2. Create your configuration file

```bash
cat > ~/.agent-ops/config/services.json << 'CONF'
{
  "services": [
    {
      "name": "My Web App",
      "type": "url",
      "target": "https://example.com",
      "expected_status": 200,
      "timeout_seconds": 10
    },
    {
      "name": "API Server",
      "type": "url",
      "target": "https://api.example.com/health",
      "expected_status": 200,
      "timeout_seconds": 5
    },
    {
      "name": "Local Dev Server",
      "type": "port",
      "host": "127.0.0.1",
      "port": 3000
    },
    {
      "name": "Background Worker",
      "type": "process",
      "process_name": "celery",
      "restart_command": "systemctl restart celery"
    }
  ],
  "alerting": {
    "telegram_bot_token": "YOUR_BOT_TOKEN",
    "telegram_chat_id": "YOUR_CHAT_ID",
    "rate_limit_seconds": 300,
    "alert_on_recovery": true
  },
  "check_interval_seconds": 300,
  "disk_warning_gb": 5,
  "stalled_task_hours": 24,
  "metrics_retention_days": 90
}
CONF
```

### 3. Deploy the health check script

Copy the `health-check.sh` from this skill's `scripts/` directory to `~/.agent-ops/scripts/` and make it executable:

```bash
chmod +x ~/.agent-ops/scripts/health-check.sh
```

### 4. Run your first check

```bash
~/.agent-ops/scripts/health-check.sh
```

### 5. Schedule it

```bash
# crontab: run every 5 minutes
(crontab -l 2>/dev/null; echo "*/5 * * * * ~/.agent-ops/scripts/health-check.sh >> ~/.agent-ops/logs/cron.log 2>&1") | crontab -

# Or on macOS, create a launchd plist (see Orchestrator Loop section)
```

---

## Health Monitoring System

The health monitoring system supports four types of checks, all configurable via `services.json`.

### Check Types

#### 1. URL Checks

Monitor any HTTP/HTTPS endpoint. Verifies status code and optionally response time.

```bash
# Simple URL check — returns 0 on success, 1 on failure
check_url() {
  local name="$1" url="$2" expected="${3:-200}" timeout="${4:-10}"
  local start_ms=$(python3 -c "import time; print(int(time.time()*1000))")

  status=$(curl -s -o /dev/null -w "%{http_code}" --max-time "$timeout" "$url" 2>/dev/null || echo "000")
  local end_ms=$(python3 -c "import time; print(int(time.time()*1000))")
  local latency_ms=$(( end_ms - start_ms ))

  if [ "$status" = "$expected" ]; then
    record_metric "$name" "up" "$latency_ms"
    return 0
  else
    record_metric "$name" "down" "$latency_ms"
    return 1
  fi
}
```

#### 2. Port Checks

Verify a TCP port is accepting connections (useful for databases, local services).

```bash
check_port() {
  local name="$1" host="$2" port="$3" timeout="${4:-3}"
  if python3 -c "
import socket, sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout($timeout)
try:
    s.connect(('$host', $port))
    s.close()
    sys.exit(0)
except:
    sys.exit(1)
" 2>/dev/null; then
    record_metric "$name" "up" "0"
    return 0
  else
    record_metric "$name" "down" "0"
    return 1
  fi
}
```

#### 3. Process Checks

Verify a named process is running. Optionally auto-restart it.

```bash
check_process() {
  local name="$1" process_name="$2" restart_cmd="$3"
  if pgrep -f "$process_name" > /dev/null 2>&1; then
    record_metric "$name" "up" "0"
    return 0
  else
    record_metric "$name" "down" "0"
    if [ -n "$restart_cmd" ]; then
      log "RESTART: Attempting to restart $name via: $restart_cmd"
      eval "$restart_cmd" 2>/dev/null || true
      sleep 3
      if pgrep -f "$process_name" > /dev/null 2>&1; then
        log "RESTART: $name recovered successfully"
        record_metric "$name" "recovered" "0"
      else
        log "RESTART: $name failed to recover"
      fi
    fi
    return 1
  fi
}
```

#### 4. Disk Space Check

```bash
check_disk() {
  local warning_gb="${1:-5}"
  local free_gb

  if [[ "$(uname)" == "Darwin" ]]; then
    free_gb=$(df -g / | awk 'NR==2 {print $4}')
  else
    free_gb=$(df -BG / | awk 'NR==2 {print $4}' | tr -d 'G')
  fi

  record_metric "disk_free_gb" "$free_gb" "0"

  if [ "$free_gb" -lt "$warning_gb" ]; then
    return 1
  fi
  return 0
}
```

### Python Health Check Class

For more sophisticated checks, use this Python class that reads your config and runs all checks:

```python
#!/usr/bin/env python3
"""
agent_ops_health.py — Configurable health checker with metrics and alerting.
Drop this into ~/.agent-ops/scripts/ and run it directly or import it.
"""

import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime

CONFIG_DIR = os.path.expanduser("~/.agent-ops/config")
METRICS_DIR = os.path.expanduser("~/.agent-ops/metrics")
STATE_DIR = os.path.expanduser("~/.agent-ops/state")
LOG_FILE = os.path.expanduser("~/.agent-ops/logs/health.log")

class HealthResult:
    """Result of a single health check."""
    def __init__(self, name, ok, detail="", latency_ms=0):
        self.name = name
        self.ok = ok
        self.detail = detail
        self.latency_ms = latency_ms
        self.timestamp = datetime.utcnow().isoformat() + "Z"

    def to_dict(self):
        return {
            "name": self.name,
            "status": "up" if self.ok else "down",
            "detail": self.detail,
            "latency_ms": self.latency_ms,
            "timestamp": self.timestamp,
        }

    def __str__(self):
        icon = "OK" if self.ok else "FAIL"
        d = f" - {self.detail}" if self.detail else ""
        lat = f" ({self.latency_ms}ms)" if self.latency_ms else ""
        return f"[{icon}] {self.name}{d}{lat}"


class HealthChecker:
    """Run health checks against configured services."""

    def __init__(self, config_path=None):
        self.config_path = config_path or os.path.join(CONFIG_DIR, "services.json")
        self.config = self._load_config()
        self.results = []
        os.makedirs(METRICS_DIR, exist_ok=True)
        os.makedirs(STATE_DIR, exist_ok=True)
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    def _load_config(self):
        with open(self.config_path, "r") as f:
            return json.load(f)

    def check_url(self, service):
        """Check an HTTP(S) endpoint."""
        name = service["name"]
        url = service["target"]
        expected = service.get("expected_status", 200)
        timeout = service.get("timeout_seconds", 10)

        start = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AgentOpsKit/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status = resp.status
                latency = int((time.time() - start) * 1000)
                ok = (status == expected)
                detail = f"HTTP {status}" + ("" if ok else f" (expected {expected})")
                return HealthResult(name, ok, detail, latency)
        except urllib.error.HTTPError as e:
            latency = int((time.time() - start) * 1000)
            return HealthResult(name, False, f"HTTP {e.code}", latency)
        except Exception as e:
            latency = int((time.time() - start) * 1000)
            return HealthResult(name, False, str(e)[:100], latency)

    def check_port(self, service):
        """Check a TCP port is open."""
        name = service["name"]
        host = service.get("host", "127.0.0.1")
        port = service["port"]
        timeout = service.get("timeout_seconds", 3)

        start = time.time()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            s.connect((host, port))
            s.close()
            latency = int((time.time() - start) * 1000)
            return HealthResult(name, True, f"port {port} open", latency)
        except Exception as e:
            latency = int((time.time() - start) * 1000)
            return HealthResult(name, False, f"port {port}: {e}", latency)

    def check_process(self, service):
        """Check a process is running."""
        name = service["name"]
        proc_name = service["process_name"]

        try:
            r = subprocess.run(
                ["pgrep", "-f", proc_name],
                capture_output=True, text=True, timeout=5
            )
            if r.returncode == 0:
                pids = r.stdout.strip().split("\n")
                return HealthResult(name, True, f"{len(pids)} process(es) running")
            else:
                return HealthResult(name, False, "not running")
        except Exception as e:
            return HealthResult(name, False, str(e)[:100])

    def check_disk(self):
        """Check disk space."""
        warning_gb = self.config.get("disk_warning_gb", 5)
        try:
            st = os.statvfs("/")
            free_gb = (st.f_bavail * st.f_frsize) / (1024 ** 3)
            ok = free_gb > warning_gb
            return HealthResult("Disk Space", ok, f"{free_gb:.1f} GB free")
        except Exception as e:
            return HealthResult("Disk Space", False, str(e))

    def run_all(self):
        """Run all configured checks and return results."""
        self.results = []

        for svc in self.config.get("services", []):
            svc_type = svc.get("type", "url")
            if svc_type == "url":
                self.results.append(self.check_url(svc))
            elif svc_type == "port":
                self.results.append(self.check_port(svc))
            elif svc_type == "process":
                self.results.append(self.check_process(svc))

        # Always check disk
        self.results.append(self.check_disk())

        # Save metrics
        self._save_metrics()

        return self.results

    def _save_metrics(self):
        """Append results to daily metrics file (JSONL)."""
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        metrics_file = os.path.join(METRICS_DIR, f"{date_str}.jsonl")
        with open(metrics_file, "a") as f:
            for r in self.results:
                f.write(json.dumps(r.to_dict()) + "\n")

    def get_failures(self):
        return [r for r in self.results if not r.ok]

    def summary(self):
        total = len(self.results)
        passed = sum(1 for r in self.results if r.ok)
        failed = total - passed
        return f"{passed}/{total} checks passed, {failed} failed"


def main():
    checker = HealthChecker()
    results = checker.run_all()

    for r in results:
        print(r)

    failures = checker.get_failures()
    if failures:
        print(f"\n{len(failures)} failure(s) detected.")
        sys.exit(1)
    else:
        print(f"\nAll {len(results)} checks passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
```

---

## Telegram Alerting

### Setting Up a Telegram Bot

1. Open Telegram and message `@BotFather`
2. Send `/newbot` and follow the prompts
3. Copy the bot token (looks like `110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw`)
4. Start a conversation with your new bot (send it any message)
5. Get your chat ID:

```bash
# Replace YOUR_BOT_TOKEN with your actual token
curl -s "https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for r in data.get('result', []):
    chat = r.get('message', {}).get('chat', {})
    if chat:
        print(f\"Chat ID: {chat['id']}  ({chat.get('first_name', '')} {chat.get('last_name', '')})\")
        break
"
```

6. Add your token and chat ID to `~/.agent-ops/config/services.json` in the `alerting` section.

### Alert System with Rate Limiting

The alert system includes built-in rate limiting to prevent alert storms. Each unique topic is limited to one alert per 5 minutes (configurable).

```python
#!/usr/bin/env python3
"""
agent_ops_alert.py — Telegram alerting with rate limiting and topic deduplication.

Usage:
  python3 agent_ops_alert.py send "Something broke"
  python3 agent_ops_alert.py send "Disk low" --level warning
  python3 agent_ops_alert.py send "API down" --topic api-health --level error
  python3 agent_ops_alert.py send "Recovered" --level info
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error

CONFIG_FILE = os.path.expanduser("~/.agent-ops/config/services.json")
RATE_STATE_FILE = os.path.expanduser("~/.agent-ops/state/alert-rate.json")

LEVEL_PREFIX = {
    "info": "[INFO]",
    "warning": "[WARNING]",
    "error": "[ERROR]",
    "recovery": "[RECOVERED]",
}

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def load_rate_state():
    if os.path.exists(RATE_STATE_FILE):
        try:
            with open(RATE_STATE_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_rate_state(state):
    os.makedirs(os.path.dirname(RATE_STATE_FILE), exist_ok=True)
    now = time.time()
    pruned = {k: v for k, v in state.items() if now - v < 3600}
    with open(RATE_STATE_FILE, "w") as f:
        json.dump(pruned, f, indent=2)

def is_rate_limited(topic, rate_limit_seconds):
    if not topic:
        return False
    state = load_rate_state()
    last_sent = state.get(topic, 0)
    return (time.time() - last_sent) < rate_limit_seconds

def record_sent(topic):
    if not topic:
        return
    state = load_rate_state()
    state[topic] = time.time()
    save_rate_state(state)

def send_telegram(bot_token, chat_id, text):
    """Send a message via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = json.dumps({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, headers={
        "Content-Type": "application/json",
    })

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if result.get("ok"):
                return True
            else:
                print(f"Telegram API error: {result}", file=sys.stderr)
                return False
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"Telegram HTTP {e.code}: {body}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Network error: {e}", file=sys.stderr)
        return False

def send_alert(message, level="info", topic=None):
    """High-level: send an alert with rate limiting."""
    config = load_config()
    alerting = config.get("alerting", {})

    bot_token = alerting.get("telegram_bot_token")
    chat_id = alerting.get("telegram_chat_id")
    rate_limit = alerting.get("rate_limit_seconds", 300)

    if not bot_token or not chat_id:
        print("ERROR: telegram_bot_token and telegram_chat_id required in config", file=sys.stderr)
        return False

    if is_rate_limited(topic, rate_limit):
        print(f"Rate limited: topic '{topic}' sent within last {rate_limit}s. Skipping.")
        return True  # Not an error, just throttled

    prefix = LEVEL_PREFIX.get(level, "")
    text = f"{prefix} *Agent Ops Alert*\n\n{message}"

    success = send_telegram(bot_token, chat_id, text)
    if success:
        record_sent(topic)
    return success

def main():
    if len(sys.argv) < 3 or sys.argv[1] != "send":
        print(__doc__.strip())
        sys.exit(0)

    message = sys.argv[2]
    level = "info"
    topic = None

    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == "--level" and i + 1 < len(sys.argv):
            level = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--topic" and i + 1 < len(sys.argv):
            topic = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    success = send_alert(message, level=level, topic=topic)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
```

### Integration with Health Checks

Wire alerting into your health checker by adding this to your check loop:

```python
from agent_ops_alert import send_alert

def check_and_alert(checker):
    """Run checks, alert on failures, and optionally alert on recovery."""
    # Load previous state for recovery detection
    state_file = os.path.expanduser("~/.agent-ops/state/last-status.json")
    prev_status = {}
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            prev_status = json.load(f)

    results = checker.run_all()
    failures = checker.get_failures()
    current_status = {r.name: r.ok for r in results}

    # Alert on new failures
    if failures:
        lines = ["Health check failures:"]
        for f in failures:
            lines.append(f"  - {f.name}: {f.detail}")
        send_alert("\n".join(lines), level="error", topic="health-check")

    # Alert on recoveries (was down, now up)
    if checker.config.get("alerting", {}).get("alert_on_recovery", False):
        for name, ok in current_status.items():
            if ok and prev_status.get(name) is False:
                send_alert(f"{name} has recovered.", level="recovery", topic=f"recovery-{name}")

    # Save current state
    os.makedirs(os.path.dirname(state_file), exist_ok=True)
    with open(state_file, "w") as f:
        json.dump(current_status, f, indent=2)

    return results
```

---

## Service Auto-Recovery

The auto-recovery system attempts to restart failed services using configurable restart commands.

### Configuration

Add `restart_command` to any service in your config:

```json
{
  "name": "Web Server",
  "type": "process",
  "process_name": "nginx",
  "restart_command": "sudo systemctl restart nginx",
  "restart_cooldown_seconds": 300,
  "max_restart_attempts": 3
}
```

For URL-based services, you can also define a restart:

```json
{
  "name": "My App",
  "type": "url",
  "target": "https://myapp.example.com/health",
  "expected_status": 200,
  "restart_command": "cd /opt/myapp && docker compose restart web",
  "restart_cooldown_seconds": 600
}
```

### Auto-Recovery Engine

```python
#!/usr/bin/env python3
"""
agent_ops_recovery.py — Automatic service recovery with cooldowns and attempt tracking.
"""

import json
import os
import subprocess
import time
from datetime import datetime

STATE_FILE = os.path.expanduser("~/.agent-ops/state/recovery.json")
LOG_FILE = os.path.expanduser("~/.agent-ops/logs/recovery.log")

def log(msg):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{ts}] {msg}\n")

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def attempt_recovery(service_name, restart_command, cooldown=300, max_attempts=3):
    """
    Attempt to recover a failed service.

    Returns: "recovered", "cooldown", "max_attempts", or "failed"
    """
    state = load_state()
    svc_state = state.get(service_name, {"attempts": 0, "last_attempt": 0})

    now = time.time()

    # Check cooldown
    if now - svc_state.get("last_attempt", 0) < cooldown:
        remaining = int(cooldown - (now - svc_state["last_attempt"]))
        log(f"COOLDOWN: {service_name} — {remaining}s remaining")
        return "cooldown"

    # Check max attempts (reset after 1 hour of no attempts)
    if now - svc_state.get("last_attempt", 0) > 3600:
        svc_state["attempts"] = 0

    if svc_state["attempts"] >= max_attempts:
        log(f"MAX_ATTEMPTS: {service_name} — {svc_state['attempts']} attempts exhausted")
        return "max_attempts"

    # Attempt restart
    log(f"RESTART: {service_name} — attempt {svc_state['attempts'] + 1}/{max_attempts}")
    try:
        result = subprocess.run(
            restart_command, shell=True,
            capture_output=True, text=True, timeout=30,
            env={**os.environ, "PATH": "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/sbin:/usr/sbin"}
        )
        svc_state["attempts"] += 1
        svc_state["last_attempt"] = now

        if result.returncode == 0:
            log(f"RESTART OK: {service_name}")
            svc_state["last_success"] = now
            state[service_name] = svc_state
            save_state(state)
            return "recovered"
        else:
            log(f"RESTART FAIL: {service_name} — {result.stderr[:200]}")
            state[service_name] = svc_state
            save_state(state)
            return "failed"

    except subprocess.TimeoutExpired:
        log(f"RESTART TIMEOUT: {service_name}")
        svc_state["attempts"] += 1
        svc_state["last_attempt"] = now
        state[service_name] = svc_state
        save_state(state)
        return "failed"
    except Exception as e:
        log(f"RESTART ERROR: {service_name} — {e}")
        return "failed"


def recover_failed_services(health_results, services_config):
    """
    Given health check results and service configs, attempt recovery for
    any failed services that have a restart_command.
    """
    from agent_ops_alert import send_alert

    services_by_name = {s["name"]: s for s in services_config}
    actions = []

    for result in health_results:
        if result.ok:
            continue

        svc = services_by_name.get(result.name, {})
        restart_cmd = svc.get("restart_command")
        if not restart_cmd:
            continue

        cooldown = svc.get("restart_cooldown_seconds", 300)
        max_attempts = svc.get("max_restart_attempts", 3)

        outcome = attempt_recovery(result.name, restart_cmd, cooldown, max_attempts)
        actions.append((result.name, outcome))

        if outcome == "recovered":
            send_alert(
                f"Auto-recovered: {result.name}\nRestart command: `{restart_cmd}`",
                level="info", topic=f"recovery-{result.name}"
            )
        elif outcome == "max_attempts":
            send_alert(
                f"CRITICAL: {result.name} failed after max restart attempts.\nManual intervention required.",
                level="error", topic=f"critical-{result.name}"
            )

    return actions
```

### macOS launchd Auto-Recovery

For macOS services managed by launchd:

```bash
# Restart a launchd service
restart_launchd_service() {
  local service_label="$1"
  local uid=$(id -u)
  launchctl kickstart -k "gui/${uid}/${service_label}" 2>/dev/null
  return $?
}

# Example: restart a tunnel
restart_launchd_service "com.myapp.cloudflared"
```

### systemd Auto-Recovery (Linux)

```bash
restart_systemd_service() {
  local service_name="$1"
  sudo systemctl restart "$service_name"
  sleep 2
  if systemctl is-active --quiet "$service_name"; then
    return 0
  else
    return 1
  fi
}
```

---

## Task Board System

A lightweight JSON-based task board for tracking operational work. Uses atomic writes and file locking to prevent data corruption.

### Board Structure

```json
{
  "columns": ["open", "in-progress", "in-review", "done"],
  "tasks": [
    {
      "id": "task-abc123",
      "title": "Investigate high latency on API",
      "column": "open",
      "owner": "agent-1",
      "priority": "high",
      "description": "API response times spiked to 2s+",
      "createdAt": "2025-01-15T10:30:00Z",
      "updatedAt": "2025-01-15T10:30:00Z",
      "tags": ["ops", "performance"]
    }
  ]
}
```

### Board I/O Module (Atomic, Locked)

This is critical for production use. Never read/write the board file directly; always go through this module to prevent data corruption.

```python
#!/usr/bin/env python3
"""
agent_ops_board.py — Atomic, locked task board I/O.

Guarantees:
- Atomic writes (write to .tmp, then os.replace)
- Exclusive file locking (prevents concurrent corruption)
- Read-modify-write under one lock
- Auto-backup before every write
- JSON validation with fallback to backup
"""

import json
import os
import fcntl
import shutil
import time
import hashlib
from contextlib import contextmanager
from datetime import datetime

BOARD_DIR = os.path.expanduser("~/.agent-ops/state")
BOARD_FILE = os.path.join(BOARD_DIR, "board.json")
BOARD_LOCK = os.path.join(BOARD_DIR, "board.lock")
BOARD_BACKUP = os.path.join(BOARD_DIR, "board.json.bak")

DEFAULT_COLUMNS = ["open", "in-progress", "in-review", "done"]
MAX_LOCK_WAIT = 30
LOCK_RETRY = 0.1

def _ensure_dir():
    os.makedirs(BOARD_DIR, exist_ok=True)

@contextmanager
def _file_lock():
    """Exclusive file lock with timeout."""
    _ensure_dir()
    deadline = time.time() + MAX_LOCK_WAIT
    lock_fd = open(BOARD_LOCK, "w")
    while True:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            break
        except BlockingIOError:
            if time.time() > deadline:
                lock_fd.close()
                raise TimeoutError(f"Could not acquire board lock within {MAX_LOCK_WAIT}s")
            time.sleep(LOCK_RETRY)
    try:
        yield lock_fd
    finally:
        fcntl.flock(lock_fd, fcntl.LOCK_UN)
        lock_fd.close()

def board_read():
    """Read board.json under lock. Returns dict."""
    _ensure_dir()
    with _file_lock():
        if not os.path.exists(BOARD_FILE):
            return {"columns": list(DEFAULT_COLUMNS), "tasks": []}
        try:
            with open(BOARD_FILE, "r") as f:
                data = json.load(f)
            if "columns" not in data:
                data["columns"] = list(DEFAULT_COLUMNS)
            if "tasks" not in data:
                data["tasks"] = []
            return data
        except json.JSONDecodeError:
            # Try backup
            if os.path.exists(BOARD_BACKUP):
                with open(BOARD_BACKUP, "r") as f:
                    return json.load(f)
            return {"columns": list(DEFAULT_COLUMNS), "tasks": []}

def board_write(data):
    """Write board.json atomically under lock."""
    _ensure_dir()
    with _file_lock():
        # Backup current
        if os.path.exists(BOARD_FILE):
            shutil.copy2(BOARD_FILE, BOARD_BACKUP)
        # Atomic write
        tmp = BOARD_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, BOARD_FILE)

def board_update(fn):
    """Read-modify-write under one lock. fn receives the board dict and must return it."""
    _ensure_dir()
    with _file_lock():
        if os.path.exists(BOARD_FILE):
            with open(BOARD_FILE, "r") as f:
                data = json.load(f)
        else:
            data = {"columns": list(DEFAULT_COLUMNS), "tasks": []}
        data = fn(data)
        if os.path.exists(BOARD_FILE):
            shutil.copy2(BOARD_FILE, BOARD_BACKUP)
        tmp = BOARD_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, BOARD_FILE)
        return data

def add_task(title, owner="", priority="medium", description="", tags=None):
    """Add a new task to the board."""
    now = datetime.utcnow().isoformat() + "Z"
    task_id = "task-" + hashlib.md5(f"{title}{now}".encode()).hexdigest()[:8]
    task = {
        "id": task_id,
        "title": title,
        "column": "open",
        "owner": owner,
        "priority": priority,
        "description": description,
        "tags": tags or [],
        "createdAt": now,
        "updatedAt": now,
    }

    def _add(board):
        board["tasks"].append(task)
        return board

    board_update(_add)
    return task

def move_task(task_id, new_column):
    """Move a task to a new column."""
    now = datetime.utcnow().isoformat() + "Z"

    def _move(board):
        for t in board["tasks"]:
            if t["id"] == task_id:
                t["column"] = new_column
                t["updatedAt"] = now
                break
        return board

    board_update(_move)

def get_stalled_tasks(hours=24):
    """Find tasks stuck in 'in-progress' longer than the given hours."""
    board = board_read()
    stalled = []
    now = datetime.utcnow()
    for t in board["tasks"]:
        if t["column"] == "in-progress":
            updated = t.get("updatedAt", t.get("createdAt", ""))
            if updated:
                try:
                    ts = datetime.fromisoformat(updated.replace("Z", ""))
                    if (now - ts).total_seconds() > hours * 3600:
                        stalled.append(t)
                except ValueError:
                    pass
    return stalled
```

### CLI Usage

```bash
# Add a task
python3 -c "
from agent_ops_board import add_task
t = add_task('Fix API timeout issue', owner='ops-agent', priority='high', tags=['ops', 'urgent'])
print(f'Created: {t[\"id\"]} — {t[\"title\"]}')
"

# Move a task
python3 -c "
from agent_ops_board import move_task
move_task('task-abc123', 'in-progress')
print('Moved to in-progress')
"

# Find stalled tasks
python3 -c "
from agent_ops_board import get_stalled_tasks
for t in get_stalled_tasks(hours=4):
    print(f'STALLED: {t[\"owner\"]}: {t[\"title\"]} (since {t[\"updatedAt\"]})')
"
```

---

## Uptime Metrics Tracking

### Metrics Storage

Metrics are stored as daily JSONL files in `~/.agent-ops/metrics/`:

```
~/.agent-ops/metrics/
  2025-01-15.jsonl
  2025-01-16.jsonl
  ...
```

Each line is a JSON object:

```json
{"name": "My App", "status": "up", "latency_ms": 145, "timestamp": "2025-01-15T10:30:00Z"}
```

### Uptime Calculator

```python
#!/usr/bin/env python3
"""
agent_ops_metrics.py — Calculate uptime percentages and generate reports.
"""

import json
import os
import glob
from datetime import datetime, timedelta
from collections import defaultdict

METRICS_DIR = os.path.expanduser("~/.agent-ops/metrics")

def load_metrics(days=7):
    """Load metrics for the last N days."""
    entries = []
    now = datetime.utcnow()
    for i in range(days):
        date_str = (now - timedelta(days=i)).strftime("%Y-%m-%d")
        path = os.path.join(METRICS_DIR, f"{date_str}.jsonl")
        if os.path.exists(path):
            with open(path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            entries.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass
    return entries

def calculate_uptime(days=7):
    """Calculate uptime percentage per service over the last N days."""
    entries = load_metrics(days)

    # Group by service
    checks = defaultdict(lambda: {"up": 0, "down": 0, "total_latency": 0, "count": 0})

    for e in entries:
        name = e.get("name", "unknown")
        status = e.get("status", "unknown")
        latency = e.get("latency_ms", 0)

        if status == "up":
            checks[name]["up"] += 1
        elif status == "down":
            checks[name]["down"] += 1

        checks[name]["total_latency"] += latency
        checks[name]["count"] += 1

    results = {}
    for name, data in checks.items():
        total = data["up"] + data["down"]
        if total > 0:
            uptime_pct = (data["up"] / total) * 100
            avg_latency = data["total_latency"] / data["count"] if data["count"] else 0
        else:
            uptime_pct = 0
            avg_latency = 0

        results[name] = {
            "uptime_percent": round(uptime_pct, 2),
            "total_checks": total,
            "failures": data["down"],
            "avg_latency_ms": round(avg_latency, 1),
        }

    return results

def uptime_report(days=7):
    """Generate a human-readable uptime report."""
    results = calculate_uptime(days)
    lines = [f"=== Uptime Report (last {days} days) ===\n"]

    for name, data in sorted(results.items()):
        pct = data["uptime_percent"]
        indicator = "OK" if pct >= 99.5 else ("WARN" if pct >= 95 else "CRITICAL")
        lines.append(
            f"[{indicator}] {name}: {pct}% uptime "
            f"({data['failures']} failures in {data['total_checks']} checks, "
            f"avg {data['avg_latency_ms']}ms)"
        )

    return "\n".join(lines)

def cleanup_old_metrics(retention_days=90):
    """Delete metrics files older than retention period."""
    cutoff = datetime.utcnow() - timedelta(days=retention_days)
    removed = 0
    for path in glob.glob(os.path.join(METRICS_DIR, "*.jsonl")):
        basename = os.path.basename(path).replace(".jsonl", "")
        try:
            file_date = datetime.strptime(basename, "%Y-%m-%d")
            if file_date < cutoff:
                os.remove(path)
                removed += 1
        except ValueError:
            pass
    return removed

if __name__ == "__main__":
    print(uptime_report())
```

### Telegram Uptime Reports

Send a daily uptime summary to Telegram:

```bash
#!/bin/bash
# daily-uptime-report.sh — Send uptime summary to Telegram
# Schedule: 0 9 * * * (daily at 9 AM)

cd ~/.agent-ops

report=$(python3 -c "
from scripts.agent_ops_metrics import uptime_report
print(uptime_report(days=1))
")

python3 scripts/agent_ops_alert.py send "$report" --level info --topic daily-uptime
```

---

## Orchestrator Loop

The orchestrator ties everything together into a single periodic loop.

### Full Orchestrator Script

```bash
#!/bin/bash
# agent-ops-orchestrator.sh — Main loop: check, recover, alert, track.
# Run every 5-10 minutes via cron or launchd.

set -euo pipefail

OPS_DIR="$HOME/.agent-ops"
LOG="$OPS_DIR/logs/orchestrator.log"
SCRIPTS="$OPS_DIR/scripts"

mkdir -p "$OPS_DIR/logs"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG"; }

log "=== Orchestrator run starting ==="

# Phase 1: Health checks
log "Phase 1: Health checks"
python3 "$SCRIPTS/agent_ops_health.py" > "$OPS_DIR/logs/last-health.txt" 2>&1
health_exit=$?

if [ $health_exit -ne 0 ]; then
  log "Health check found failures"

  # Phase 2: Auto-recovery
  log "Phase 2: Auto-recovery"
  python3 -c "
from scripts.agent_ops_health import HealthChecker
from scripts.agent_ops_recovery import recover_failed_services

checker = HealthChecker()
results = checker.run_all()
failures = checker.get_failures()

if failures:
    actions = recover_failed_services(failures, checker.config.get('services', []))
    for name, outcome in actions:
        print(f'  {name}: {outcome}')
" 2>&1 | tee -a "$LOG"

  # Phase 3: Alert
  log "Phase 3: Alerting"
  python3 -c "
from scripts.agent_ops_health import HealthChecker
from scripts.agent_ops_alert import send_alert

checker = HealthChecker()
results = checker.run_all()
failures = checker.get_failures()

if failures:
    lines = ['Health check failures after recovery attempt:']
    for f in failures:
        lines.append(f'  - {f.name}: {f.detail}')
    send_alert(chr(10).join(lines), level='error', topic='health-check')
" 2>&1 | tee -a "$LOG"

else
  log "All checks passed"
fi

# Phase 4: Stalled task detection
log "Phase 4: Stalled task check"
python3 -c "
from scripts.agent_ops_board import get_stalled_tasks
from scripts.agent_ops_alert import send_alert

stalled = get_stalled_tasks(hours=24)
if stalled:
    lines = ['Stalled tasks (>24h in progress):']
    for t in stalled:
        lines.append(f\"  - {t.get('owner', '?')}: {t['title'][:60]}\")
    send_alert(chr(10).join(lines), level='warning', topic='stalled-tasks')
    print(f'{len(stalled)} stalled task(s) found')
else:
    print('No stalled tasks')
" 2>&1 | tee -a "$LOG"

# Phase 5: Metrics cleanup
log "Phase 5: Metrics maintenance"
python3 -c "
from scripts.agent_ops_metrics import cleanup_old_metrics
removed = cleanup_old_metrics(retention_days=90)
if removed:
    print(f'Cleaned up {removed} old metrics file(s)')
" 2>&1 | tee -a "$LOG"

# Phase 6: Log rotation (rotate if > 50MB)
for logfile in "$OPS_DIR"/logs/*.log; do
  if [ -f "$logfile" ]; then
    size=$(stat -f%z "$logfile" 2>/dev/null || stat --format=%s "$logfile" 2>/dev/null || echo 0)
    if [ "$size" -gt 52428800 ]; then
      mv "$logfile" "${logfile}.$(date +%Y%m%d)"
      gzip "${logfile}.$(date +%Y%m%d)" 2>/dev/null || true
      log "Rotated $(basename "$logfile")"
    fi
  fi
done

log "=== Orchestrator run complete ==="
```

### macOS launchd Setup

Create `~/Library/LaunchAgents/com.agent-ops.orchestrator.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.agent-ops.orchestrator</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>~/.agent-ops/scripts/agent-ops-orchestrator.sh</string>
    </array>
    <key>StartInterval</key>
    <integer>300</integer>
    <key>StandardOutPath</key>
    <string>~/.agent-ops/logs/launchd-stdout.log</string>
    <key>StandardErrorPath</key>
    <string>~/.agent-ops/logs/launchd-stderr.log</string>
    <key>RunAtLoad</key>
    <true/>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
    </dict>
</dict>
</plist>
```

Load it:

```bash
launchctl load ~/Library/LaunchAgents/com.agent-ops.orchestrator.plist
```

### Linux systemd Setup

Create `/etc/systemd/system/agent-ops.service`:

```ini
[Unit]
Description=Agent Ops Kit Orchestrator
After=network.target

[Service]
Type=oneshot
User=your-username
ExecStart=/bin/bash /home/your-username/.agent-ops/scripts/agent-ops-orchestrator.sh
Environment=PATH=/usr/local/bin:/usr/bin:/bin

[Install]
WantedBy=multi-user.target
```

And a timer `/etc/systemd/system/agent-ops.timer`:

```ini
[Unit]
Description=Run Agent Ops every 5 minutes

[Timer]
OnBootSec=60
OnUnitActiveSec=300

[Install]
WantedBy=timers.target
```

```bash
sudo systemctl enable agent-ops.timer
sudo systemctl start agent-ops.timer
```

---

## Configuration Reference

### Full services.json Schema

```json
{
  "services": [
    {
      "name": "string (required) — Human-readable service name",
      "type": "url | port | process (required)",
      "target": "string — URL for type=url",
      "host": "string — Host for type=port (default: 127.0.0.1)",
      "port": "number — Port for type=port",
      "process_name": "string — Process name for type=process (used with pgrep -f)",
      "expected_status": "number — Expected HTTP status (default: 200)",
      "timeout_seconds": "number — Request timeout (default: 10)",
      "restart_command": "string — Shell command to restart the service",
      "restart_cooldown_seconds": "number — Min seconds between restart attempts (default: 300)",
      "max_restart_attempts": "number — Max restarts before giving up (default: 3)"
    }
  ],
  "alerting": {
    "telegram_bot_token": "string — Telegram bot API token",
    "telegram_chat_id": "string — Telegram chat ID for alerts",
    "rate_limit_seconds": "number — Min seconds between same-topic alerts (default: 300)",
    "alert_on_recovery": "boolean — Send alert when a service recovers (default: true)"
  },
  "check_interval_seconds": "number — How often to run checks (for reference, actual scheduling is external)",
  "disk_warning_gb": "number — Alert when free disk space drops below this (default: 5)",
  "stalled_task_hours": "number — Hours before a task is considered stalled (default: 24)",
  "metrics_retention_days": "number — Days to keep metrics files (default: 90)"
}
```

### Environment Variables (Optional Overrides)

| Variable | Description | Default |
|----------|-------------|---------|
| `AGENT_OPS_CONFIG` | Path to services.json | `~/.agent-ops/config/services.json` |
| `AGENT_OPS_LOG_DIR` | Log directory | `~/.agent-ops/logs` |
| `AGENT_OPS_METRICS_DIR` | Metrics directory | `~/.agent-ops/metrics` |
| `TELEGRAM_BOT_TOKEN` | Override bot token from config | (from config) |
| `TELEGRAM_CHAT_ID` | Override chat ID from config | (from config) |

---

## Recipes

### Recipe 1: Monitor a Cloudflare Pages Site

```json
{
  "name": "My Blog",
  "type": "url",
  "target": "https://myblog.pages.dev",
  "expected_status": 200,
  "timeout_seconds": 15
}
```

### Recipe 2: Monitor a Docker Compose Stack

```json
[
  {
    "name": "Web Frontend",
    "type": "url",
    "target": "http://localhost:3000/health",
    "restart_command": "cd /opt/myapp && docker compose restart web"
  },
  {
    "name": "API Backend",
    "type": "url",
    "target": "http://localhost:8080/api/health",
    "restart_command": "cd /opt/myapp && docker compose restart api"
  },
  {
    "name": "Redis",
    "type": "port",
    "host": "127.0.0.1",
    "port": 6379,
    "restart_command": "cd /opt/myapp && docker compose restart redis"
  },
  {
    "name": "PostgreSQL",
    "type": "port",
    "host": "127.0.0.1",
    "port": 5432,
    "restart_command": "cd /opt/myapp && docker compose restart db"
  }
]
```

### Recipe 3: Monitor Multiple Domains with SSL Check

```bash
# Add this to your health check loop for SSL expiry monitoring
check_ssl_expiry() {
  local domain="$1" warning_days="${2:-14}"
  local expiry_date
  expiry_date=$(echo | openssl s_client -servername "$domain" -connect "$domain:443" 2>/dev/null | \
    openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)

  if [ -z "$expiry_date" ]; then
    echo "FAIL: Could not check SSL for $domain"
    return 1
  fi

  local expiry_epoch
  if [[ "$(uname)" == "Darwin" ]]; then
    expiry_epoch=$(date -j -f "%b %d %H:%M:%S %Y %Z" "$expiry_date" +%s 2>/dev/null || echo 0)
  else
    expiry_epoch=$(date -d "$expiry_date" +%s 2>/dev/null || echo 0)
  fi

  local now_epoch=$(date +%s)
  local days_left=$(( (expiry_epoch - now_epoch) / 86400 ))

  if [ "$days_left" -lt "$warning_days" ]; then
    echo "WARNING: $domain SSL expires in $days_left days"
    return 1
  fi
  echo "OK: $domain SSL valid for $days_left days"
  return 0
}
```

### Recipe 4: Weekly Uptime Digest

```bash
#!/bin/bash
# weekly-digest.sh — Send weekly uptime digest every Monday at 9 AM
# Cron: 0 9 * * 1 ~/.agent-ops/scripts/weekly-digest.sh

report=$(python3 -c "
from agent_ops_metrics import uptime_report, calculate_uptime

# 7-day report
print(uptime_report(days=7))
print()

# Highlight any service below 99.9%
results = calculate_uptime(days=7)
concerns = [(n, d) for n, d in results.items() if d['uptime_percent'] < 99.9]
if concerns:
    print('Services below 99.9% SLA:')
    for name, data in concerns:
        print(f'  {name}: {data[\"uptime_percent\"]}% ({data[\"failures\"]} failures)')
else:
    print('All services above 99.9% SLA target.')
")

python3 ~/.agent-ops/scripts/agent_ops_alert.py send "$report" --level info --topic weekly-digest
```

### Recipe 5: Create Ops Tasks from Health Failures

```python
# Auto-create task board entries when services fail repeatedly

from agent_ops_board import add_task, board_read
from agent_ops_metrics import calculate_uptime

def create_ops_tasks_from_failures():
    """Create investigation tasks for services with poor uptime."""
    results = calculate_uptime(days=1)
    board = board_read()
    existing_titles = {t["title"] for t in board["tasks"] if t["column"] != "done"}

    for name, data in results.items():
        if data["uptime_percent"] < 95:
            title = f"Investigate: {name} at {data['uptime_percent']}% uptime"
            if title not in existing_titles:
                add_task(
                    title=title,
                    owner="ops-agent",
                    priority="high",
                    description=f"{data['failures']} failures in {data['total_checks']} checks. "
                                f"Avg latency: {data['avg_latency_ms']}ms",
                    tags=["auto-generated", "ops", "uptime"],
                )
                print(f"Created task: {title}")
```

---

## Troubleshooting

### Alert not sending

1. Verify bot token: `curl https://api.telegram.org/botYOUR_TOKEN/getMe`
2. Verify chat ID: Send a message to the bot, then check `/getUpdates`
3. Check rate limiting: Look at `~/.agent-ops/state/alert-rate.json`

### Health checks timing out

1. Increase `timeout_seconds` in the service config
2. Check if the service is behind a firewall or VPN
3. Test manually: `curl -v --max-time 10 <URL>`

### Board file locked

If the board file appears locked (stale lock):

```bash
# Check if any process holds the lock
lsof ~/.agent-ops/state/board.lock

# If no process holds it, remove the stale lock
rm ~/.agent-ops/state/board.lock
```

### Metrics disk usage

```bash
# Check metrics directory size
du -sh ~/.agent-ops/metrics/

# Manual cleanup (keep last 30 days)
python3 -c "
from agent_ops_metrics import cleanup_old_metrics
removed = cleanup_old_metrics(retention_days=30)
print(f'Removed {removed} files')
"
```

---

## License

MIT License. Built by OpenClaw Systems.
