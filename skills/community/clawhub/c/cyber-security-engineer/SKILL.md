---
name: cyber-security-engineer
version: 0.2.1
homepage: https://github.com/FletcherFrimpong/OpenClaw-Cyber-Analyst
metadata:
  {
    "openclaw":
      {
        "homepage": "https://github.com/FletcherFrimpong/OpenClaw-Cyber-Analyst",
        "os": ["darwin", "linux"],
        "requires": { "bins": ["python3"], "anyBins": ["lsof", "ss", "netstat"] },
      },
  }
description: Security engineering workflow for OpenClaw privilege governance and hardening. Use for least-privilege execution, approval-first privileged actions, idle timeout controls, port + egress monitoring, and ISO 27001/NIST-aligned compliance reporting with mitigations.
---

# Cyber Security Engineer

## Requirements

**Required tools:**
- `python3` (>= 3.9)
- `openclaw` CLI (installed via `npm` during bootstrap, or pre-installed)
- `npm` (only needed for bootstrap if `openclaw` is not already installed)
- One of `lsof`, `ss`, or `netstat` for port/egress checks
- `stat`, `readlink` (standard on macOS/Linux, used by the runtime hook installer)

**Settings (all optional).** Set them in the process environment or, for the ones marked *file*, as
`NAME=value` lines in `~/.openclaw/env` (mode 600). A protection is on when either place sets it.
- `OPENCLAW_REQUIRE_POLICY_FILES` — *file* — set to `1` to block privileged execution when policy files are missing
- `OPENCLAW_REQUIRE_SESSION_ID` — *file* — set to `1` to require a task session id for each privileged action
- `OPENCLAW_TASK_SESSION_ID` — per-task session id (used when `OPENCLAW_REQUIRE_SESSION_ID=1`)
- `OPENCLAW_APPROVAL_TOKEN` — *file* — if set, this token must be typed at the terminal during approval
- `OPENCLAW_AUDIT_OPTIONAL` — *file* — set to `1` to let a privileged command run when the audit log cannot be written (default: refuse)
- `OPENCLAW_UNTRUSTED_SOURCE` — set to `1` to flag the current content source as untrusted
- `OPENCLAW_VIOLATION_NOTIFY_CMD` — absolute path to a notifier binary (must also be allowlisted)
- `OPENCLAW_VIOLATION_NOTIFY_ALLOWLIST` — JSON array of allowed argv arrays, or comma-separated absolute paths
- `OPENCLAW_PRIV_REASON` — human-readable reason passed to the guarded execution wrapper
- `OPENCLAW_VIOLATION_NOTIFY_STATE` — override path to the notification state file
- `OPENCLAW_HOOK_ASSUME_YES` — set to `1` to let the hook installer change OpenClaw's command PATH without asking (for unattended installs; without it and without a terminal, nothing is changed)

**Policy files (admin reviewed):**
- `~/.openclaw/security/approved_ports.json`
- `~/.openclaw/security/command-policy.json`
- `~/.openclaw/security/egress_allowlist.json`
- `~/.openclaw/security/prompt-policy.json`

Implement these controls in every security-sensitive task:

1. Keep default execution in normal (non-root) mode.
2. Request explicit user approval before any elevated command. Approval is given by a person at the terminal; never pipe an answer into the guard.
3. Scope elevation to the minimum command set required for the active task.
4. Drop elevated state immediately after the privileged command completes.
5. Expire elevated state after 30 idle minutes and require re-approval.
6. Monitor listening network ports and flag insecure or unapproved exposure.
7. Monitor OpenClaw's outbound connections and flag destinations not in the egress allowlist.
8. If no approved baseline exists, generate one with `python3 scripts/generate_approved_ports.py`, then review and prune.
9. Benchmark controls against ISO 27001 and NIST and report violations with mitigations.

## Runtime Hook (sudo shim)

The script `scripts/install-openclaw-runtime-hook.sh` installs an **opt-in** sudo
shim at `~/.openclaw/bin/sudo`. This shim **shadows** the system `sudo` binary by
putting `~/.openclaw/bin` first on the `PATH` of commands OpenClaw runs, through OpenClaw's
`tools.exec.pathPrepend` setting (or the gateway LaunchAgent's `PATH` on older releases).

**What it does:**
- Intercepts `sudo` invocations and routes them through `guarded_privileged_exec.py`
- Requires approval typed at the controlling terminal before running any privileged command
- Runs the command as `sudo -k -- <command>`, so sudo asks for the password every time
- Enforces command policy allow/deny rules, audit logging, and a 30-minute idle timeout
- Resolves bare command names (`sudo ls`) in the system directories only; sudo options such as `-u` are not supported
- Passes a flag straight to the real sudo only when it is the single argument and runs nothing:
  `-h`, `--help`, `-V`, `--version`, `-k`, `-K`. The same flag followed by a command goes through the guard.

**What it does NOT do:**
- It does not stop a caller that runs `/usr/bin/sudo` by its full path; that call still meets sudo's password prompt
- It does not replace or modify the system sudo binary
- It does not grant itself any elevated permissions
- It does not read its sudo, python or guard paths from the environment; they are fixed when the shim is installed

**Opt-in:** The hook is **not installed by default**. To enable it, run bootstrap with
`ENFORCE_PRIVILEGED_EXEC=1`. The installer asks for confirmation before changing OpenClaw's
command PATH, and changes nothing if it cannot ask. The shim can be removed at any time
by deleting `~/.openclaw/bin/sudo`.

## File Writes

This skill writes only to `~/.openclaw/` and the `assessments/` directory inside the
skill folder. No files are written outside these two trees.

**Under `~/.openclaw/` (user config/state):**
- `~/.openclaw/security/approved_ports.json` — generated port baseline (by `generate_approved_ports.py`)
- `~/.openclaw/security/root-session-state.json` — signed elevated session state (by `root_session_guard.py`)
- `~/.openclaw/security/session-state.key` — per-user key that signs the session state (by `root_session_guard.py`)
- `~/.openclaw/security/privileged-audit.jsonl` — hash-chained audit log, rotated to `privileged-audit.jsonl.1` at 5 MB (by `audit_logger.py`)
- `~/.openclaw/security/violation-notify-state.json` — notification diff state (by `notify_on_violation.py`)
- `~/.openclaw/security/egress-dns-cache.json` — DNS answers for allowlisted hostnames, kept 7 days (by `egress_monitor.py`)
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

## Network Use

- `scripts/egress_monitor.py` resolves the hostnames listed in `~/.openclaw/security/egress_allowlist.json`
  through the system DNS resolver, so they can be compared with the IP addresses the OS reports.
  Run it with `--no-resolve` to make no DNS queries.
- No other script in this skill makes network calls.

## Non-Goals (Web Browsing)

- Do not use web browsing / web search as part of this skill. Keep assessments and recommendations based on local host/OpenClaw state and the bundled references in this skill.

## Files To Use

- `references/threat-model.md`
- `references/least-privilege-policy.md`
- `references/port-monitoring-policy.md`
- `references/egress-monitoring-policy.md`
- `references/compliance-controls-map.json`
- `references/approved_ports.template.json`
- `references/command-policy.template.json`
- `references/prompt-policy.template.json`
- `references/egress-allowlist.template.json`
- `scripts/preflight_check.py`
- `scripts/security_config.py`
- `scripts/root_session_guard.py`
- `scripts/audit_logger.py`
- `scripts/command_policy.py`
- `scripts/prompt_policy.py`
- `scripts/guarded_privileged_exec.py`
- `scripts/install-openclaw-runtime-hook.sh`
- `scripts/sudo-shim.template.sh`
- `scripts/port_monitor.py`
- `scripts/generate_approved_ports.py`
- `scripts/egress_monitor.py`
- `scripts/notify_on_violation.py`
- `scripts/compliance_dashboard.py` (with `assets/dashboard.css` and `assets/dashboard.js`)
- `scripts/live_assessment.py`

## Behavior

- Never keep root/elevated access open between unrelated tasks.
- Never execute root commands without an explicit approval step in the current flow.
- Never answer the approval or password prompt on the user's behalf, and never call `/usr/bin/sudo` directly to avoid the guard.
- Refuse privileged execution when no terminal is attached, when the audit log cannot be written, or when the command policy file is broken.
- Enforce command allow/deny policy when configured.
- Require confirmation when untrusted content sources are detected (`OPENCLAW_UNTRUSTED_SOURCE=1` + prompt policy).
- Enforce task session id scoping when configured (`OPENCLAW_REQUIRE_SESSION_ID=1`).
- If timeout is exceeded, force session expiration and approval renewal.
- Log privileged actions to `~/.openclaw/security/privileged-audit.jsonl`; verify the log with `python3 scripts/audit_logger.py verify`.
- Flag listening ports not present in the approved baseline and recommend secure alternatives for insecure ports.
- Flag services listening on all interfaces unless their baseline rule sets `"allow_public": true`.
- State the limits in `references/threat-model.md` when asked what this skill protects against.
- Flag outbound destinations not present in the egress allowlist. Evaluate only OpenClaw's own processes,
  outbound direction, and destinations that leave the host (see `references/egress-monitoring-policy.md`).
- Treat an egress report with `summary.evaluated` of 0 as "nothing checked", not as proof of compliance.

## Output Contract

When reporting status, include:

- The specific `check_id`(s) affected, `status`, `risk`, and concise evidence.
- Concrete mitigations (what to change, where) and any owners/due dates if present.
- For network findings: port, bind address, process/service, and why it is flagged (unapproved/insecure/public).
- For egress findings: process, pid, remote address and port, any allowlisted hostname it resolves to, and the rule that would be needed.
