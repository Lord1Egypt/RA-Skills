# 🛡️ Autofix + Watchdog

**OpenClaw diagnostic repair skill + Gateway health monitoring daemon.**

When something breaks — Gateway won't start, tools return errors, configs go wrong — this skill walks through a structured cycle to diagnose, fix, and validate. The optional Watchdog daemon monitors Gateway health in the background and alerts you in real time.

---

## ✨ Features

### Autofix Diagnosis (v6.1)
- **Unified diagnosis pipeline** — 3 data sources in one pass (`gateway status` + runtime checks + key validation)
- **`openclaw doctor` fallback** — 12s timeout, auto‑falls back to `gateway status --json` (fixes doctor hang in v2026.5.20)
- **Safe subprocess cleanup** — All commands use `taskkill /T /F` to prevent zombie processes on Windows
- **Interactive Health Dashboard** — HTML dashboard with Canvas embed (`health_dashboard.py --canvas`)
- **Regression comparison** — `--save-baseline` / `--compare` to track fixes over time

### Auto-Repair (v1.1)
- **Gateway restart without hangs** — Uses `taskkill + start` instead of `openclaw gateway restart` (which hangs in v2026.5.20)
- **Session archiving** — >7-day-old session files automatically archived to `archive/` when backlog >100
- **Gateway memory alert** — Recommends restart when memory exceeds 800 MB
- **Verification polling** — After repair, polls Gateway status every 5 seconds (up to 30s)

### Gateway Watchdog *(optional)*
- **Real-time health monitoring** — Polls Gateway every 60 seconds
- **Dual-channel alerting** — WebChat session (async, ~40s) + Feishu DM (instant)
- **Severity escalation** — Four-tier alerting (🟢/🟡/🟠/🔴) with noise filtering
- **Auto-repair** — Low-risk issues (CLI path, session archive) are fixed automatically
- **Stale process cleanup** — Auto-kills orphaned daemon processes on startup
- **`--status` command** — Quick state check without starting a new daemon
- **Single-instance protection** — Windows Mutex prevents duplicate daemons
- **Auto-start on login** — Registers in `HKCU\Run`

---

## 🚀 Quick Start

### Just tell your agent:

```
run autofix self-check
check what's wrong with Gateway
auto repair
```

### Recommended first step for any issue:

```bash
python scripts/diagnosis_formatter.py --json       # Unified diagnosis
python scripts/health_dashboard.py --canvas         # Visual dashboard
```

> ⚠️ **v2026.5.20 note:** `openclaw doctor` may hang. The pipeline auto‑falls back to `gateway status --json` after 12 seconds.

---

## 📦 Installation

```bash
clawhub install autofix
```

Then restart OpenClaw to load the skill.

### Watchdog daemon *(optional)*

```bash
pip install -r scripts/requirements.txt
python scripts/watchdog_monitor.py                  # Start daemon
python scripts/watchdog_monitor.py --status         # Check status
python scripts/watchdog_monitor.py --install        # Auto-start on login
```

See [`INSTALL.md`](./INSTALL.md) for full setup.

---

## 🔔 Feishu Error Notification Setup

When the Watchdog detects anomalies (Gateway crash, RPC failure, etc.), it sends detailed error information to **Feishu** instantly.

### 1. Connect OpenClaw to Feishu

First, configure your Feishu channel in OpenClaw:

```bash
# Add Feishu channel
openclaw channels add feishu
```
Follow the interactive prompts to authenticate.

Verify the channel works:
```bash
openclaw message send --channel feishu --target "me" --message "Hello from Watchdog"
```

### 2. Set Your Feishu User ID

The Watchdog needs your Feishu **open_id** to send you direct messages.

**Find your open_id:**
```bash
openclaw message send --channel feishu --target "me" --message "test"
# The response includes your open_id (e.g., "ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
```

**Configure via environment variable:**

PowerShell (current session):
```powershell
$env:WATCHDOG_FEISHU_USER_ID = "ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
python scripts\watchdog_monitor.py
```

PowerShell (permanent, in profile):
```powershell
[System.Environment]::SetEnvironmentVariable("WATCHDOG_FEISHU_USER_ID", "ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx", "User")
```

Command Prompt:
```cmd
set WATCHDOG_FEISHU_USER_ID=ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
python scripts\watchdog_monitor.py
```

### 3. Notification Flow

```
Gateway Crash / Error Detected
        │
        ├─► Feishu DM (instant, 0 delay)
        │    └─ Message: "Watchdog: Gateway has been down for 3 checks..."
        │       includes: severity level, error detail, timestamp
        │
        ├─► WebChat session (async, ~40s for model inference)
        │    └─ Background thread, won't block monitoring
        │
        └─► watchdog_state.json (local log)
             └─ Full check history (last 1440 records)
```

### 4. What You'll Receive

When an error occurs, your Feishu will receive alerts like:

```
Watchdog

Gateway 不可达 (连续失败 3/5 次)
状态: cli_err

严重级别: 🟠 警告
错误详情: Gateway 无输出或返回异常

---
2026-01-15 14:30:00
```

With the v6.1 improvements, errors now include **detailed stack traces** and **full diagnostic context** (not just a simple "Watchdog" header).

---

## 📚 Documentation

| Document | What it covers |
|----------|----------------|
| [`INSTALL.md`](./INSTALL.md) | Full installation with prerequisites |
| [`SKILL.md`](./SKILL.md) | Master document with all workflows |
| [`docs/CHANGES_v6.1.md`](./docs/reports/CHANGES_v6.1.md) | Complete v6.1 changelog |
| [`docs/MODULE_01_PreCheck.md`](./docs/MODULE_01_PreCheck.md) | Problem pre-check and context collection |
| [`docs/MODULE_02_SearchChain.md`](./docs/MODULE_02_SearchChain.md) | Search strategy: docs → GitHub |
| [`docs/MODULE_03_ValidationAction.md`](./docs/MODULE_03_ValidationAction.md) | Decision-making and validation |
| [`docs/MODULE_04_Finalization.md`](./docs/MODULE_04_Finalization.md) | Memory updates and lesson learning |

---

## 🗺️ Diagnosis Pipeline

```
┌─ gateway status --json ────────┐
│  (8s, fast)                    │
└────────┬───────────────────────┘
         ▼
┌─ runtime_health_check.py ──────┐
│  (25-30s)                      │
│  gateway · disk · sessions     │
│  logs · models (max 3)         │
└────────┬───────────────────────┘
         ▼
┌─ api_key_validator.py ─────────┐
│  (10-20s)                      │
│  OpenAI · Tavily · GitHub etc  │
└────────┬───────────────────────┘
         ▼
┌─ diagnosis_formatter.py ───────┤
│  severity-sorted report        │
│  --save-baseline / --compare   │
└────────────────────────────────┘
   Total: ~45-55s (was ∞)
```

---

## ⚙️ Requirements

- **OpenClaw** 2025.x or later (v2026.5.20 fully supported)
- **Python 3.10+** *(for diagnostic scripts and Watchdog daemon)*
- **pywin32** *(for Watchdog single-instance protection)*
- **psutil** *(optional, for Watchdog process cleanup)*

---

## 📄 License

Open source. Feel free to fork, modify, and share.
