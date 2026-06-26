---
name: cyber-security-engineer
version: 0.1.9
description: Security engineering workflow for OpenClaw privilege governance and hardening. Use for least-privilege execution, approval-first privileged actions, idle timeout controls, port + egress monitoring, and ISO 27001/NIST-aligned compliance reporting with mitigations.
---

# Cyber Security Engineer

## Requirements

**Required tools:**
- `python3` (>= 3.8)
- `openclaw` CLI (installed via `npm` during bootstrap, or pre-installed)
- `npm` (only needed for bootstrap if `openclaw` is not already installed)
- One of `lsof`, `ss`, or `netstat` for port/egress checks
- `stat`, `readlink` (standard on macOS/Linux, used by the runtime hook installer)

**Env vars (all optional, documented for configuration):**
- `OPENCLAW_REQUIRE_POLICY_FILES` — set to `1` to block privileged execution when policy files are missing
- `OPENCLAW_REQUIRE_SESSION_ID` — set to `1` to require a task session id for each privileged action
- `OPENCLAW_TASK_SESSION_ID` — per-task session id (used when `OPENCLAW_REQUIRE_SESSION_ID=1`)
- `OPENCLAW_APPROVAL_TOKEN` — if set, requires this token during the approval step
- `OPENCLAW_UNTRUSTED_SOURCE` — set to `1` to flag the current content source as untrusted
- `OPENCLAW_VIOLATION_NOTIFY_CMD` — absolute path to a notifier binary (must also be allowlisted)
- `OPENCLAW_VIOLATION_NOTIFY_ALLOWLIST` — JSON array of allowed argv arrays, or comma-separated absolute paths
- `OPENCLAW_REAL_SUDO` — override path to the real sudo binary (used by the runtime hook shim)
- `OPENCLAW_PYTHON3` — override path to python3 (used by the runtime hook shim)
- `OPENCLAW_CYBER_SKILL_DIR` — override path to the skill directory (used by the runtime hook shim)
- `OPENCLAW_ALLOW_NONINTERACTIVE_SUDO` — set to `1` to allow non-interactive sudo through the shim (default: blocked)
- `OPENCLAW_PRIV_REASON` — human-readable reason passed to the guarded execution wrapper
- `OPENCLAW_VIOLATION_NOTIFY_STATE` — override path to the notification state file
- `OPENCLAW_SKIP_PLIST_CONFIRM` — set to `1` to skip the interactive confirmation before modifying the macOS LaunchAgent plist

**Policy files (admin reviewed):**
- `~/.openclaw/security/approved_ports.json`
- `~/.openclaw/security/command-policy.json`
- `~/.openclaw/security/egress_allowlist.json`
- `~/.openclaw/security/prompt-policy.json`

Implement these controls in every security-sensitive task:

1. Keep default execution in normal (non-root) mode.
2. Request explicit user approval before any elevated command.
3. Scope elevation to the minimum command set required for the active task.
4. Drop elevated state immediately after the privileged command completes.
5. Expire elevated state after 30 idle minutes and require re-approval.
6. Monitor listening network ports and flag insecure or unapproved exposure.
7. Monitor outbound connections and flag destinations not in the egress allowlist.
8. If no approved baseline exists, generate one with `python3 scripts/generate_approved_ports.py`, then review and prune.
9. Benchmark controls against ISO 27001 and NIST and report violations with mitigations.

## Runtime Hook (sudo shim)

The script `scripts/install-openclaw-runtime-hook.sh` installs an **opt-in** sudo
shim at `~/.openclaw/bin/sudo`. This shim **shadows** the system `sudo` binary by
prepending `~/.openclaw/bin` to `PATH` in the OpenClaw gateway process.

**What it does:**
- Intercepts `sudo` invocations and routes them through `guarded_privileged_exec.py`
- Requires explicit interactive user approval before running any privileged command
- Enforces command policy allow/deny rules, audit logging, and a 30-minute idle timeout
- Blocks non-interactive sudo by default (prevents automated abuse)
- Passes through harmless flags (`-h`, `--version`, `-k`, `-l`) directly to real sudo

**What it does NOT do:**
- It does not replace or modify the system sudo binary
- It does not grant itself any elevated permissions
- It only affects processes whose `PATH` includes `~/.openclaw/bin` before `/usr/bin`

**Opt-in:** The hook is **not installed by default**. To enable it, run bootstrap with
`ENFORCE_PRIVILEGED_EXEC=1`. On macOS, the installer will prompt for confirmation
before modifying the gateway LaunchAgent plist. The shim can be removed at any time
by deleting `~/.openclaw/bin/sudo`.

## File Writes

This skill writes only to `~/.openclaw/` and the `assessments/` directory inside the
skill folder. No files are written outside these two trees.

**Under `~/.openclaw/` (user config/state):**
- `~/.openclaw/security/approved_ports.json` — generated port baseline (by `generate_approved_ports.py`)
- `~/.openclaw/security/root-session-state.json` — elevated session state (by `root_session_guard.py`)
- `~/.openclaw/security/privileged-audit.jsonl` — append-only audit log (by `audit_logger.py`)
- `~/.openclaw/security/violation-notify-state.json` — notification diff state (by `notify_on_violation.py`)
- `~/.openclaw/bin/sudo` — opt-in sudo shim (by `install-openclaw-runtime-hook.sh`, see Runtime Hook section)
- `~/.openclaw/logs/cyber-security-engineer-auto.log` — auto-cycle run log (by `auto_invoke_cycle.sh`)

**Under `assessments/` (inside skill directory):**
- `assessments/openclaw-assessment.json` — compliance check results
- `assessments/compliance-summary.json` — structured summary for tools/integrations
- `assessments/compliance-dashboard.html` — human-readable report page
- `assessments/port-monitor-latest.json` — latest open-port scan output
- `assessments/egress-monitor-latest.json` — latest outbound connection scan output

**Temporary files:**
- A short-lived temp file via `tempfile.NamedTemporaryFile` (by `generate_approved_ports.py`) — auto-cleaned

No files are written to `/usr/`, `/etc/`, or any system directory.

## Non-Goals (Web Browsing)

- Do not use web browsing / web search as part of this skill. Keep assessments and recommendations based on local host/OpenClaw state and the bundled references in this skill.

## Files To Use

- `references/least-privilege-policy.md`
- `references/port-monitoring-policy.md`
- `references/compliance-controls-map.json`
- `references/approved_ports.template.json`
- `references/command-policy.template.json`
- `references/prompt-policy.template.json`
- `references/egress-allowlist.template.json`
- `scripts/preflight_check.py`
- `scripts/root_session_guard.py`
- `scripts/audit_logger.py`
- `scripts/command_policy.py`
- `scripts/prompt_policy.py`
- `scripts/guarded_privileged_exec.py`
- `scripts/install-openclaw-runtime-hook.sh`
- `scripts/port_monitor.py`
- `scripts/generate_approved_ports.py`
- `scripts/egress_monitor.py`
- `scripts/notify_on_violation.py`
- `scripts/compliance_dashboard.py`
- `scripts/live_assessment.py`

## Behavior

- Never keep root/elevated access open between unrelated tasks.
- Never execute root commands without an explicit approval step in the current flow.
- Enforce command allow/deny policy when configured.
- Require confirmation when untrusted content sources are detected (`OPENCLAW_UNTRUSTED_SOURCE=1` + prompt policy).
- Enforce task session id scoping when configured (`OPENCLAW_REQUIRE_SESSION_ID=1`).
- If timeout is exceeded, force session expiration and approval renewal.
- Log privileged actions to `~/.openclaw/security/privileged-audit.jsonl` (best-effort).
- Flag listening ports not present in the approved baseline and recommend secure alternatives for insecure ports.
- Flag outbound destinations not present in the egress allowlist.

## Output Contract

When reporting status, include:

- The specific `check_id`(s) affected, `status`, `risk`, and concise evidence.
- Concrete mitigations (what to change, where) and any owners/due dates if present.
- For network findings: port, bind address, process/service, and why it is flagged (unapproved/insecure/public).
