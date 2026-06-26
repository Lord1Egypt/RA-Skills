---
name: cron-doctor
version: 1.1.0
author: Polycat
tags: [cron, monitoring, diagnosis]
license: MIT
platform: universal
description: >
  Diagnose and triage cron job failures. Checks job states, identifies error
  patterns, prioritizes by criticality, generates health reports. Triggers on: cron
  failures, job health check, scheduled task errors, cron diagnosis, job not running,
  backup failed.
---

> **Compatible with Claude Code, Codex CLI, Cursor, Windsurf, and any SKILL.md-compatible agent.**

# Cron Doctor

Diagnose and triage cron job failures.

## Usage

When asked to check cron health or diagnose failures:

### 1. List All Jobs

```bash
# List user's crontab
crontab -l

# List system crontabs
sudo cat /etc/crontab
ls -la /etc/cron.d/
```

### 2. Check Recent Execution

```bash
# Check cron logs (location varies by system)
# Debian/Ubuntu:
grep CRON /var/log/syslog | tail -50

# RHEL/CentOS:
tail -50 /var/log/cron

# macOS:
log show --predicate 'process == "cron"' --last 1h

# Check for specific job output
grep "your_job_name" /var/log/syslog | tail -20
```

### 3. Identify Problems

**Error patterns to watch:**
- `"command not found"` — Missing executable or PATH issue
- `"Permission denied"` — File/directory permissions wrong
- `"No such file or directory"` — Script path incorrect
- `"timeout"` — Job took too long
- `"ECONNREFUSED"` — Network/service down
- `"rate limit"` — API throttling
- Missing output — Job may not be running at all

### 4. Triage Priority

| Priority | Criteria |
|----------|----------|
| 🔴 Critical | Trading, backup, security jobs |
| 🟠 High | User-facing deliveries |
| 🟡 Medium | Monitoring, research jobs |
| 🟢 Low | Nice-to-have, non-essential |

### 5. Generate Report

Write to `~/workspace/reports/cron-health-YYYY-MM-DD.md`:

```markdown
# Cron Health Report - [DATE]

## Summary
- ✅ Healthy: X jobs
- ⚠️ Warning: X jobs  
- ❌ Failed: X jobs

## Failed Jobs

### [Job Name]
- **Error:** [message]
- **Last Success:** [date]
- **Priority:** [level]
- **Fix:** [suggested action]

## Recommendations
1. [Action item]
2. [Action item]
```

### 6. Common Fixes

| Error | Fix |
|-------|-----|
| Command not found | Use full path to executable, or set PATH in crontab |
| Permission denied | Check file permissions, run `chmod +x script.sh` |
| No output | Add `>> /tmp/job.log 2>&1` to capture output |
| Wrong timezone | Set `TZ=` in crontab or use system timezone |
| Rate limit | Reduce frequency or add backoff |

### 7. Debugging Tips

```bash
# Test cron environment (cron has minimal PATH)
env -i /bin/sh -c 'echo $PATH'

# Verify script runs manually
/path/to/your/script.sh

# Check if cron daemon is running
systemctl status cron   # Linux
launchctl list | grep cron  # macOS
```

## Escalation

If 3+ critical jobs failed, alert the user immediately.

## Verification Gates

Before claiming diagnosis complete:
- [ ] **All failed jobs listed** — none skipped or ignored
- [ ] **Priority assigned** — based on impact, not just recency
- [ ] **Fix suggested** — actionable next step for each failure
- [ ] **Report written** — to `~/workspace/reports/cron-health-YYYY-MM-DD.md`
- [ ] **Critical failures escalated** — 3+ critical = alert user
