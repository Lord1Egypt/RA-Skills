---
name: dial-a-cron
description: Stateful cron system for OpenClaw with persistent memory, change detection, smart routing, token budget tracking, and self-healing. Requires 'openclaw' and 'gog' CLIs. Broad I/O capabilities (file reads, HTTP requests, shell execution). Must be reviewed carefully before use. See security notes below.
---

# dial-a-cron

**Stateful cron system with memory, change detection, smart delivery, token budget tracking, and self-healing.**

## Security & Review Requirements (per OpenClaw scanner)

This skill has **broad I/O capabilities** and is marked **Suspicious (high confidence)** by the OpenClaw scanner.

**Before installing or using:**

- Audit **all job configs** (especially `diffs` for file/command/HTTP reads and `routes` for webhook URLs, target_id).
- Run in an **isolated environment** with limited network access (consider denying outbound webhooks if you do not want potential exfiltration).
- Ensure `openclaw` and `gog` CLIs exist and run with least privilege.
- Whitelist HTTP targets and restrict diff file paths to specific safe directories. Avoid diffs on secrets or system files.
- The code uses `subprocess.run(..., shell=True)` with values from job configs and outputs — unsanitized fields could allow shell injection.
- The skill can read arbitrary local files, make HTTP requests (including to internal IPs), and post outputs to external endpoints.
- Persisted state/logs may contain sensitive data from jobs — review storage permissions.

Full scanner report is in `references/security-review.md`.

**Only use if you have reviewed the code and trust the job configs.**

## Basic Usage

```bash
openclaw cron create --name my-job --command "your-command" --dial "state:yes,change-detection:yes,routing:telegram:error,slack:warning,budget:50000,self-heal:yes"
```

## What it contains

- Persistent state and change detection
- Smart delivery routing (webhook, message, email, etc.)
- Token budget tracking
- Self-healing (retries, backoff, auto-pause)
- Preflight, diff, router, and state scripts
- Requires `openclaw` and `gog` CLIs (not declared in older versions — now explicit)

**No credentials are requested**, but the code can contact arbitrary endpoints if job configs allow it.

## Installation

`openclaw skills install dial-a-cron`

Then review the scripts in `scripts/` and all job configs before creating any scheduled jobs.

## Security Notes (from scanner)

- The skill implements the advertised features but has disproportionate I/O for a simple cron wrapper.
- Missing declared dependencies (openclaw, gog) in older metadata.
- Potential for exfiltration of local file contents or command output via routes/webhooks.
- Shell command injection risk if job configs or outputs are not sanitized.
- Persistence of state/logs that may contain sensitive job output.

Review the code, restrict job configs, and run in an isolated environment with network controls.

Full details and the exact scanner report are in `references/security-review.md`.

**Version**: 1.0.1 (security audit and full disclosure)
**License**: MIT-0

Clean, honest, and auditable. Review before use.
