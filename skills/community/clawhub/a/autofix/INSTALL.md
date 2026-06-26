# 🛡️ Autofix + Watchdog — Installation Guide

## Overview

This skill contains two main components:

| Component | Description | Usage |
|-----------|-------------|-------|
| **Autofix Diagnosis** | OpenClaw fault diagnosis and repair workflow | Works after install — try `python scripts/diagnosis_formatter.py --json` |
| **Watchdog Daemon** | Background Gateway health monitor with dual-channel alerting | Requires manual deployment (optional) |

---

## 1. Quick Start (Autofix Diagnosis)

After installing the skill:

```bash
# One-click unified diagnosis (v6.1)
python scripts/diagnosis_formatter.py --json

# Visual dashboard (v6.0-M4)
python scripts/health_dashboard.py --canvas
```

Or tell your agent:

> **`run autofix self-check`**
> **`check what's wrong with Gateway`**
> **`auto repair`**

> ⚠️ **v2026.5.20 note:** `openclaw doctor` may hang. The pipeline auto‑falls back to `gateway status --json` after 12 seconds.

---

## 2. Deploying the Watchdog Daemon (Optional)

### Prerequisites

| Dependency | Purpose | Install |
|-----------|---------|---------|
| Python 3.10+ | Run Python scripts | `winget install Python.Python` or python.org |
| pywin32 | Windows Mutex (single instance) | Included in `requirements.txt` |
| psutil | Process cleanup (optional, wmic fallback available) | Included in `requirements.txt` |
| openclaw CLI | Health check via CLI | Included with OpenClaw installation |
| Gateway HTTP API | Real-time WebChat notifications | Manual enable (see below) |

### Step 1: Enable the Gateway HTTP Endpoint

```bash
openclaw config set gateway.http.endpoints.chatCompletions.enabled true
openclaw gateway restart
```

### Step 2: Install Python Dependencies

```bash
pip install -r scripts/requirements.txt
```

### Step 3: Verify the CLI Works

```bash
python scripts/watchdog_monitor.py --status
```

If everything is configured correctly, you should see the current health state.

### Step 4: Start the Watchdog

**Windows (recommended):**
```powershell
cd scripts
python watchdog_monitor.py
```

**Run in background (hidden window):**
```powershell
$py = (Get-Command python).Source
$script = "scripts\watchdog_monitor.py"
Start-Process -FilePath $py -ArgumentList $script -WindowStyle Hidden -WorkingDirectory (Get-Location).Path
```

### Step 5: Install Auto-Start (Optional)

```powershell
python scripts\watchdog_monitor.py --install
```

This registers the daemon in `HKCU\Run` so it launches automatically when you log in.

---

## 3. Configuring Feishu Notifications (Optional)

By default the Watchdog sends alerts to the WebChat session. To enable the Feishu backup channel:

### Prerequisite
- Your OpenClaw instance must have Feishu bot configured (`channels.feishu` in `openclaw.json`)

### Set Your Feishu User ID (Environment Variable)

The watchdog now reads the Feishu user ID from the `WATCHDOG_FEISHU_USER_ID` environment variable.

**Permanent Setup (PowerShell profile):**
```powershell
[System.Environment]::SetEnvironmentVariable("WATCHDOG_FEISHU_USER_ID", "ou_your_feishu_open_id", "User")
```

**Ad-hoc (current session only):**
```powershell
$env:WATCHDOG_FEISHU_USER_ID = "ou_your_feishu_open_id"
python scripts\watchdog_monitor.py
```

To find your open_id:
```bash
openclaw message send --channel feishu --target "me" --message "test"
```
The delivery response will include your Feishu open_id.

---

## 4. Management Commands

```powershell
# Check status (v6.1 — safe, won't start a new daemon)
python scripts\watchdog_monitor.py --status

# View live logs
Get-Content scripts\gateway_watchdog.log -Tail 10 -Wait

# Stop Watchdog
Stop-Process -Id <PID> -Force

# Full diagnosis pipeline
python scripts\diagnosis_formatter.py --json

# Save baseline before making changes
python scripts\diagnosis_formatter.py --save-baseline

# Compare after fixes
python scripts\diagnosis_formatter.py --compare

# Check runtime health
python scripts\runtime_health_check.py --json

# Validate API keys
python scripts\api_key_validator.py
```

---

## 5. File Structure (v6.1)

```
autofix/
├── SKILL.md                         # Master document
├── INSTALL.md                       # This file
├── README.md / README_CN.md         # Overview
├── docs/
│   ├── MODULE_01_*.md ~ 04_*.md     # Core workflow docs
│   ├── enhancement/                 # v5.0 enhancements
│   ├── tutorials/                   # Usage examples
│   └── reports/
│       ├── CHANGES_v5.0.md
│       ├── CHANGES_v6.1.md          # NEW: v6.1 changelog
│       ├── AUTOFIX_V5.0_SUMMARY.md
│       └── VERIFICATION_FINAL.md
├── scripts/
│   ├── diagnosis_formatter.py       # Unified diagnosis (v6.0-M3)
│   ├── runtime_health_check.py      # Runtime health checks (v6.0-M1)
│   ├── api_key_validator.py         # API key validation (v6.0-M2)
│   ├── health_dashboard.py          # Interactive HTML dashboard (v6.0-M4)
│   ├── auto_repair.py               # Auto-repair library (v1.1)
│   ├── watchdog_monitor.py          # Watchdog daemon (v6.1)
│   ├── canvas_report_generator.py   # Canvas diagnosis report
│   ├── elis_helper.py               # Error log analysis
│   └── requirements.txt             # Python dependencies
```

---

## 6. Notes

- **Windows subprocess cleanup**: All scripts use `CREATE_NEW_PROCESS_GROUP` + `taskkill /T /F` to prevent zombie processes on timeout.
- **Diagnosis pipeline performance**: Completes in ~45-55 seconds on stock hardware (was ∞ in v6.0).
- **`openclaw doctor` hang**: v2026.5.20 has a known doctor hang issue. The pipeline handles it gracefully with a 12-second timeout + fallback.
- **Watchdog `--status`**: This is a safe command that reads the state file and exits. It will NOT start a new daemon.
- **Log rotation**: Log files auto-rotate at 5MB, keeping 3 backups.
