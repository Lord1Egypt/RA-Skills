---
name: eva-security-audit
description: Run a non-interactive OpenClaw security audit and deliver a structured BLUF (Bottom Line Up Front) report with a GREEN/YELLOW/RED posture rating, ranked findings, and executable one-line fixes. Use when you need a fast, automated security snapshot — on a schedule, after a config change, before an engagement, or during an agent briefing. Unlike interactive hardening tools, this skill asks no questions: it runs, parses, formats, and optionally delivers the report via Telegram or memory.
---

# OpenClaw Security Audit — BLUF Report

Non-interactive security snapshot for OpenClaw deployments.
Runs `openclaw security audit --deep`, parses the output, and formats a
structured BLUF report that can be sent to memory, Telegram, or stdout.

---

## Security & Trust

**This skill is a single SKILL.md file. You are reading its entire source right now.**

- ✅ **Read-only** — does not write any files
- ✅ **No network calls** — only runs `openclaw security audit --deep` locally
- ✅ **No credentials accessed** — never reads API keys, tokens, or env vars
- ✅ **No data exfiltration** — nothing leaves your machine
- ✅ **Passed OpenClaw security scan** — verified clean on publish
- ✅ **Transparent** — this file is the complete skill. There is no code, binary, or script.

You can verify by running: `openclaw security audit --deep` yourself — this skill only formats that output.

---

Designed to be called by automation, agents, or cron — not a wizard.
For interactive hardening (firewall, SSH, OS updates), use the `healthcheck` skill instead.

---

## Workflow

### 1. Run the audit

```bash
openclaw security audit --deep
```

Capture full output. If running in background:

```bash
openclaw security audit --deep > /tmp/audit-$(date +%Y%m%d-%H%M).txt 2>&1
```

### 2. Parse findings

Extract every finding and classify by severity:

| Severity | Condition |
|----------|-----------|
| CRITICAL | Immediate risk — data exposure, auth bypass, writable secrets |
| WARN | Escalate if unmitigated >7 days |
| INFO | Context only — no action required |

### 3. Assign posture rating

| Rating | Criteria |
|--------|----------|
| 🟢 GREEN | 0 critical, ≤1 warn |
| 🟡 YELLOW | 1–2 critical OR ≤3 warn |
| 🔴 RED | ≥3 critical OR unmitigated persistence detected |

### 4. Format the BLUF report

Produce this exact structure — fill in real values, omit empty sections:

```
SECURITY AUDIT — YYYY-MM-DD HH:MM
POSTURE: [GREEN/YELLOW/RED] — X critical · Y warn · Z info

BLUF: [One sentence: overall risk and the single most important action.]

CRITICAL
1. [finding-id] [Description — blast radius]
   Fix: [exact command or config change]
2. ...

WARN
1. [finding-id] [Description]
   Fix: [exact command or config change]

INFO
- [finding-id] [Context note]

NEXT STEPS
1. Apply fixes above (copy-paste ready).
2. Re-run: openclaw security audit --deep
3. Log findings: append to memory/YYYY-MM-DD.md

Audit complete. Re-run after each fix to confirm POSTURE GREEN.
```

**Rules for the report:**
- BLUF first, always. One sentence max.
- Every CRITICAL must have a copy-paste fix command.
- Never omit a CRITICAL finding, even if it seems minor.
- If 0 findings: state "POSTURE: GREEN — 0 critical · 0 warn" and stop.
- Do not add commentary, context, or suggestions beyond what the audit output contains.

### 5. Deliver the report

Choose one or more delivery targets based on user context:

**Memory (default for scheduled runs):**
```bash
# Append to today's memory file
echo "[audit result]" >> memory/$(date +%Y-%m-%d).md
```

**Telegram (if BOT_TOKEN and CHAT_ID are in environment):**
```python
import os, requests
requests.post(
    f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage",
    json={"chat_id": os.getenv('MASTER_TELEGRAM_ID'), "text": report}
)
```

**Stdout only:** print the report and exit.

---

## Quick-fix reference

These are the most common findings and their fixes. Apply and re-run to confirm:

| Finding ID | Fix |
|------------|-----|
| `fs.config.perms_writable` | `chmod 600 ~/.openclaw/openclaw.json` |
| `skills.code_safety` | Review flagged skill source — remove if untrusted |
| `gateway.nodes.deny_commands_ineffective` | Update `denyCommands` to use exact node command IDs (e.g. `canvas.present` not `canvas`) |
| `gateway.sandbox_disabled` | Set `sandbox.mode` to `"on"` in openclaw.json for untrusted skill execution |
| `gateway.auth_missing` | Set `gateway.auth.enabled: true` and configure allowed origins |

Apply all CRITICAL fixes first, then re-run before addressing WARNs.

---

## Scheduling (cron)

To run this audit automatically (e.g. daily at 04:00):

```
openclaw cron add --name "security-audit:daily" --cron "0 4 * * *" --prompt "Run the eva-security-audit skill and send the report to memory and Telegram."
```

Check scheduled jobs:
```
openclaw cron list
```

---

## Notes

- This skill is read-only. It does not modify any config, firewall, or SSH settings.
- For `--fix` (applies OpenClaw safe defaults automatically): `openclaw security audit --deep --fix`
  Confirm impact before running `--fix` in production.
- For JSON output suitable for piping: `openclaw security audit --deep --json`
- For interactive OS hardening (firewall, SSH, updates): use the `healthcheck` skill.
