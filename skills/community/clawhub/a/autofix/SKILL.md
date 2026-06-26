---
name: autofix
description: A comprehensive, self-evolving skill designed to diagnose and solve OpenClaw issues by following a structured, multi-stage resolution cycle. It incorporates Proactive Prediction (L2), Robustness Checks (L1), Knowledge Creation (L3), Diagnosis Report Visualization (v5.5), v6.0 Runtime Health + Key Validation + Unified Report + Health Dashboard, and Gateway Watchdog (v6.1).
---

# 🧠 OpenClaw Problem Solver (v6.0-M4) — Master Document

This skill acts as an advanced diagnostic, resolution, and validation engine for any question or bug report related to the OpenClaw framework itself. **v6.0 adds four layers: Runtime Health Check (M1), API Key Validation + Resource Monitor (M2), Unified Diagnosis Report + Regression Check (M3), and Interactive Health Dashboard (M4).**

## 🔒 Privacy-First Constraint

All knowledge storage (memory, logs) and final reports **must** follow these rules:
1. **API Keys**: Never store API keys in plain text. Use placeholders or hashes (e.g., `sk-********************`).
2. **Private Details**: Redact sensitive project names, internal credentials, and user identity info unless explicitly authorized.

## 🎯 When to Use This Skill

Use this skill when the user:
- Asks "Why is [feature] not working in OpenClaw?"
- Reports a specific bug (e.g., "The `gateway` tool fails with error X").
- Needs guidance on how to implement a specific feature using OpenClaw's architecture or tools.
- Wants to know the best practice for a certain task within the OpenClaw ecosystem, but requires verification.

## 🌟 Recommended Quick Fix Flow (The Golden Path)

For the vast majority of OpenClaw issues, this sequence provides the fastest path to resolution. Always suggest this flow first when a user reports an unspecified problem or bug!

1. **Unified Diagnosis (一键诊断, v6.0-M3):** Run `python scripts/diagnosis_formatter.py` which auto-collects all three sources (`openclaw doctor` + `runtime_health_check` + `api_key_validator`) into one severity-sorted report.
2. **Visual Dashboard (可视化仪表盘, v6.0-M4):** Run `python scripts/health_dashboard.py --canvas` to render the report as an interactive HTML dashboard (embed with `[embed ref="health_dashboard" height="740"]`).
3. **Save Baseline (保存基线, v6.0-M3):** Run `python scripts/diagnosis_formatter.py --save-baseline` before making any fix.
4. **Resolution Attempt（修复）:** If the report reveals problems, run `openclaw doctor --fix` or apply suggested fixes manually.
5. **Regression Check (回归验证, v6.0-M3):** After fixes, run `python scripts/diagnosis_formatter.py --compare` to validate what was fixed, what's new, and what's unchanged.

## 🚀 The Evolved Workflow (6-Step Cycle + Proactive Layers)

The skill operates by strictly following these steps in sequence, enhanced by proactive layers:

## 🤖 Gateway Watchdog (v6.1) — Proactive Stability Layer

**Overview:**
A background daemon that periodically polls the Gateway health status. Runs independently from user requests, providing real-time monitoring for anomalies such as Gateway downtime, RPC failures, and configuration drift.

**v6.1 Feature Highlights:**

| Feature | Description |
|---------|-------------|
| 🎯 Real Health Check | Calls `openclaw gateway status --json`, parses `service.runtime.status` + `rpc.ok` |
| 🔇 Noise Filtering | Alerts only after ≥3 consecutive failures; resets after ≥3 consecutive successes |
| 📊 Severity Levels | Four-tier classification (🟢/🟡/🟠/🔴) with auto-escalation |
| 📡 Dual-Channel Alerting | **Feishu DM (instant, primary)** + WebChat (async thread, secondary) |
| 🔄 Single Instance | Windows Mutex ensures only one daemon runs at a time |
| 📦 Log Rotation | Auto-rotates at 5MB, keeps 3 backup files |
| ⏰ Precise Scheduling | Fixed-minute schedule eliminates cumulative drift |
| 🔐 Hot-Reload Config | Monitors `openclaw.json` changes and reloads automatically |
| 🖥️ Auto-Start | Registers in `HKCU\Run` for auto-launch on user login |
| 👋 Startup Confirmation | Sends status to both channels on startup |
| 🐛 **Config Cache Fix** | **Fixed** `load_gateway_config()` returning `token=None` on cache hit (v6.1) |
| ⏱️ **Async WebChat** | **Fixed** background thread with 60s timeout for model loading (v6.1) |
| 📝 **Detailed Error Logs** | **Fixed** full stack traces in Feishu + WebChat notifications (v6.1) |

**📊 Severity & Alert Rules:**

| Consecutive Failures | Level | Behavior |
|---------------------|-------|----------|
| < 2 | 🟢 Level 1 — Normal | Silent, no notification |
| 2 | 🟡 Level 2 — Notice | Silent, continue monitoring |
| ≥ 3 | 🟠 Level 3 — Warning | **Trigger notification** (first time) |
| ≥ 5 | 🔴 Level 4 — Critical | **Trigger notification** + repeat every 5 failures |
| Gateway stopped | 🔴 Level 4 — Critical | **Immediate notification** |
| Recovered for 3 cycles | ✅ Recovered | Send recovery notification |

**🚨 Notification Triggers:**
1. Severity **escalation** (e.g., 1→3): sends alert
2. First time hitting **alert threshold** (≥3 consecutive failures): sends alert
3. At critical level, **every 5 failures**: sends reminder
4. **System recovery** (abnormal→normal for 3 consecutive checks): sends recovery notice

### Prerequisites

1. **Feishu channel configured in OpenClaw** — `openclaw channels add feishu`
2. **Environment variable** — Set `WATCHDOG_FEISHU_USER_ID` to your Feishu open_id:
   ```powershell
   $env:WATCHDOG_FEISHU_USER_ID = "ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
   ```
3. **Gateway HTTP API** (optional, for WebChat channel) — 
   ```bash
   openclaw config set gateway.http.endpoints.chatCompletions.enabled true
   openclaw gateway restart
   ```

> ⚠️ **WebChat timeout**: The model inference takes ~40s on first load.
> The watchdog uses a **background thread with 60s timeout** so it doesn't block the main monitoring loop.

### Deployment (v6.1)

Run the Watchdog as a standalone background process:

```powershell
# Start
python scripts\watchdog_monitor.py

# Install auto-start (launches on user login)
python scripts\watchdog_monitor.py --install

# Remove auto-start
python scripts\watchdog_monitor.py --uninstall
```

Or use `Start-Process` for a hidden window:

```powershell
$py = (Get-Command python).Source
$script = "$env:USERPROFILE\.openclaw\workspace\skills\autofix\scripts\watchdog_monitor.py"
Start-Process -FilePath $py -ArgumentList $script `
    -WindowStyle Hidden `
    -WorkingDirectory "$env:USERPROFILE\.openclaw\workspace\skills\autofix\scripts"
```

Check process status:

```powershell
Get-WmiObject Win32_Process -Filter "Name like 'python%'" |
    Where-Object { $_.CommandLine -match 'watchdog_monitor' } |
    Select-Object ProcessId, @{n="Start";e={$_.CreationDate}}
```

Stop the Watchdog:

```powershell
# Find the PID first, then
Stop-Process -Id <PID> -Force
```

View live logs:

```powershell
Get-Content "$env:USERPROFILE\.openclaw\workspace\skills\autofix\scripts\gateway_watchdog.log" -Tail 10 -Wait
```

View state file:

```powershell
Get-Content "$env:USERPROFILE\.openclaw\workspace\skills\autofix\scripts\watchdog_state.json" -Raw | ConvertFrom-Json
```


### 🔗 Notification Architecture (v6.1)

```
Watchdog (background daemon, 60s interval)
    │
    ├─ [Channel A — PRIMARY] openclaw message send --channel feishu
    │            → Feishu direct message (ou_xxx)
    │            → **Instant delivery, zero token cost**
    │            → Includes full error stack traces
    │
    ├─ [Channel B — SECONDARY] Gateway HTTP API (/v1/chat/completions)
    │            → WebChat live session (agent:main:main)
    │            → **Async background thread** (doesn't block monitoring)
    │            → 60s timeout for model loading (~40s typical)
    │            → token cost: minimal (max_tokens=10)
    │
    └─ [Log]     watchdog_state.json (local check history, last 1440)
                 gateway_watchdog.log (rotating, 5MB)
```

**Channel priority:** Feishu is now the primary channel (instant, reliable via CLI).
WebChat is secondary (async thread, requires model inference).

### Dual-Channel Alerting + Autofix Triggers (v6.1)

**Channel priority has changed in v6.1:**
- **Feishu (instant)** is now the primary notification channel
- **WebChat (async thread)** is the secondary channel

- When a WebChat alert arrives (~40s after error), reply with any of these commands to start diagnosis:
  - `run autofix self-check`
  - `check what's wrong with Gateway`
  - `auto repair`
- Feishu messages serve as the **instant primary** notification (not offline backup)
- Each alert message includes detailed error context and stack traces

### Workflow Integration + Autofix Linkage

The Watchdog forms a **Proactive Stability Layer**, independent of the standard diagnostic flow (Steps 0-5). When an anomaly is detected:

a. The daemon logs the event and generates a System Health Warning (SHW) report
b. Sends a real-time alert (with diagnostic guidance + context JSON)
c. **Auto-repair** low-risk known issues (e.g., CLI path problems) automatically, then verifies
d. High-risk operations only provide repair suggestions, awaiting user confirmation

## 🛠️ Auto-Repair Module (v1.0)

**Repair Script Library:** `scripts/auto_repair.py`

Matches repair plans based on the diagnostic context from Watchdog alerts:

| Issue | Match Condition | Repair Action | Risk |
|-------|----------------|---------------|------|
| Gateway stopped | `status: stopped` | Restart Gateway | 🟡 Needs confirmation |
| RPC connection failed | `rpc_ok: false` | Restart Gateway | 🟡 Needs confirmation |
| CLI unavailable | `status: cli_error` | Check installation path | 🟢 Auto-execute |
| HTTP unreachable | `status: unreachable` | Check port + restart | 🟡 Needs confirmation |

**Repair Verification Loop:**
1. After auto-repair, wait 3 seconds then re-run health check
2. Verification passed → send "Auto-repair succeeded" confirmation
3. Verification failed → send "Still needs manual diagnosis" escalation

**Health Trend Tracking:**
- `watchdog_state.json` retains the last 1440 check records (24 hours)
- Each record includes: timestamp, health status, severity level, source
- Trend data can be visualized via Canvas health dashboard

### Current Status (v6.1)

- ✅ Real health check — `service.runtime.status = running` + `rpc.ok = true`
- ✅ Noise filtering — ≥3 failures to trigger, ≥3 successes to reset
- ✅ Severity levels — Four-tier (🟢/🟡/🟠/🔴) with auto-escalation
- ✅ Feishu channel (PRIMARY) — `openclaw message send --channel feishu`, zero token cost, instant delivery
- ✅ WebChat channel (SECONDARY) — Gateway HTTP API `/v1/chat/completions`, async background thread, 60s timeout
- ✅ Single instance — Windows Mutex prevents duplicates
- ✅ Log rotation — 5MB auto-rotate, 3 backups
- ✅ Precise scheduling — Fixed-minute schedule, no drift
- ✅ Hot-reload config — Watches `openclaw.json` for changes
- ✅ Auto-start — `HKCU\Run` registry, launches on user login
- ✅ Startup confirmation — Sends status to both channels on start
- ✅ **`--status` command** — Shows real-time state and exits cleanly (no longer starts daemon by accident)
- ✅ **Stale process cleanup** — Auto-kills orphaned `--status` processes on daemon startup
- ✅ **Config cache fix** — `load_gateway_config()` no longer returns `token=None` on subsequent calls
- ✅ **Detailed error logging** — Full stack traces in all notification channels
- ✅ **Async WebChat delivery** — Background thread prevents blocking main monitor loop
- 📁 State file: `scripts/watchdog_state.json`
- 📁 Log file: `scripts/gateway_watchdog.log`

---

## Standard Workflow (6-Step Cycle + Proactive Layers)

This skill strictly follows these steps in sequence, enhanced by proactive layers:

### Step 0: Resource Pre-check & Cost Management *(New)* — Starting Point

Before any resource-intensive external search or service call, proactively check API quotas, rate limits, and budget consumption for the current active session. If quota-low alerts or known rate-limit thresholds are hit, pause all execution steps and notify the user with a clear "resource warning," requesting they wait or switch to a low-cost / local alternative.

### Step 1: Primary Search *(See `docs/MODULE_02_SearchChain.md` — Step 1)*
- Search the official documentation (`docs.openclaw.ai`) for official solutions
- Gather context information related to the problem
- Extract key error messages and configuration status

### Step 2: Backup Search *(See `docs/MODULE_02_SearchChain.md` — Step 2)*
- If the official docs don't provide an answer, search GitHub Issues
- Look for community-reported problems and solutions
- Collect code verification requirements or pattern-matching information

### Step 3: Analysis & Decision *(See `docs/MODULE_03_ValidationAction.md` — Step 3)*
- Choose the best action path based on search results
- Perform **evidence chain analysis (L1)** to evaluate solution reliability
- Decide between direct answer, code verification, or contextual inquiry

### Step 4: Validation & Action (v5.0 Enhanced) *(See `docs/MODULE_03_ValidationAction.md` — Step 4 + `docs/MODULE_03_Enhancement_Reports.md`)*
- Execute validation (MRE) or propose a contextual inquiry
- Generate an **interactive diagnosis report** (if MRE fails)
- ✅ **Three-step confirmation before fixes**: Before running any command with system-modifying or wide-ranging effects (e.g., `openclaw doctor --fix`, `exec`/`write`), follow these safety steps:
  1. **Problem location & explanation**: Explain the diagnosis result and the core issue to be fixed
  2. **Scope confirmation**: Ask about and record the specific target or runtime environment (e.g., "This change will only affect the local development config. Do you agree?")
  3. **Rollback plan**: Provide an executable one-click rollback command. Only proceed after the user agrees via `/approve`

### Step 5: Finalization & Memory Update *(See `docs/MODULE_04_Finalization.md`)*
- Save facts, lessons learned, and update state
- Trigger **L2 Hot-Start Query** and **L3 Skill Creation Suggestions**

---

> 💡 **Golden Path (Recommended Flow)**: For most OpenClaw issues, the fastest resolution path is: `openclaw doctor` → `openclaw doctor --fix`

## 🖼️ Diagnosis Report Visualization (v5.0)

When MRE validation fails, generate an interactive diagnostic report using `canvas.snapshot()` with:
- Visual risk flags (🔴/🟠/🟢)
- Evidence chain diagram (Doc vs GH comparison)
- Exec result status codes highlighted
- Rollback command code block display

## 🧠 Error Log Intelligent Summary (ELIS — v5.0)

When MRE fails, use LLM-powered analysis to extract root causes from `exec` output:
- **Core Issue**: One-sentence summary
- **Possible Causes**: 2–3 bullet points
- **Recommended Fix**: Specific command(s)
- **Risk Level + Confidence Score**

## 📚 Modules & Deep Dives

Consult the following categorized sub-documents for detailed process explanations:

### 📁 `docs/` — Core Module Documentation
- **[MODULE_01_PreCheck.md](./docs/MODULE_01_PreCheck.md)**: Problem pre-check, context collection, and security scanning.
- **[MODULE_02_SearchChain.md](./docs/MODULE_02_SearchChain.md)**: Search strategy (Docs → GitHub) with **evidence chain analysis (L1)**.
- **[MODULE_03_ValidationAction.md](./docs/MODULE_03_ValidationAction.md)**: Decision-making based on search results, choosing between direct answer, code verification, or inquiry.
- **[MODULE_04_Finalization.md](./docs/MODULE_04_Finalization.md)**: Finalization: memory storage, lesson learning, and state updates, including **L2 Hot-Start Query** and **L3 Skill Creation Suggestions**.

### 📁 `docs/enhancement/` — v5.0 Enhancement Features
- **[MODULE_03_Enhancement_Reports.md](./docs/enhancement/MODULE_03_Enhancement_Reports.md)**: **v5.0 new modules** — Diagnosis Report Visualization (DRE) + Error Log Intelligent Summary (ELIS).

### 📁 `docs/tutorials/` — Usage Examples
- **[EXAMPLE_usage.md](./docs/tutorials/EXAMPLE_usage.md)**: Detailed code examples and usage scenarios.
- **[QUICK_START_v5.0.md](./docs/tutorials/QUICK_START_v5.0.md)**: v5.0 quick-start guide covering environment setup, workflow, and best practices.

### 📁 `docs/reports/` — Summary Reports
- **[AUTOFIX_V5.0_SUMMARY.md](./docs/reports/AUTOFIX_V5.0_SUMMARY.md)**: v5.0 completion report and feature summary.
- **[CHANGES_v5.0.md](./docs/reports/CHANGES_v5.0.md)**: Complete change log from v4.5 to v5.0.
- **[VERIFICATION_FINAL.md](./docs/reports/VERIFICATION_FINAL.md)**: Final integrity verification report.

### 📁 `scripts/` — Python/JS Tools
- **[elis_helper.py](./scripts/elis_helper.py)**: ELIS error log analysis helper (LLM-powered error analyzer).
- **[canvas_report_generator.py](./scripts/canvas_report_generator.py)**: Canvas diagnosis report generator (HTML template rendering + URL registration).
- **[auto_repair.py](./scripts/auto_repair.py)**: Auto-repair library — matches diagnostic context to repair plans.
- **[watchdog_monitor.py](./scripts/watchdog_monitor.py)**: Gateway Watchdog daemon — background health monitoring + dual-channel alerting.
- **[requirements.txt](./scripts/requirements.txt)**: Python dependencies (pywin32).

---

*This file is the master skill document. It defines the complete problem-solving blueprint and integrates all capability layers.*
