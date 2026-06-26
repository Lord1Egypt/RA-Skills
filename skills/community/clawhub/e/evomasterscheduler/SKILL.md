# EvoMasterScheduler Skill

The EvoMasterScheduler is a self-evolving system of daily maintenance tasks designed to ensure the health, security, and continuous improvement of the OpenClaw environment.

## Daily Schedule

| Time | Script | Purpose |
|------|--------|---------|
| 03:00 | `cron-diagnose.sh` | System health check and error detection |
| 03:00 | `cron-fix.sh` | Automated remediation of detected issues |
| 03:00 | `cron-memory.sh` | Memory optimization and debris cleanup |
| 03:05 | `cron-backup.sh` | Critical configuration and state backup |
| 03:10 | `cron-improve.sh` | Analysis of logs to suggest/apply improvements |
| 03:15 | `cron-upgrade.sh` | Check for and apply stable component updates |
| 03:20 | `cron-security.sh` | Security audit and permission validation |

## Logging
All scripts log to `~/.openclaw/logs/evomaster-$(date +%Y-%m-%d).log`.

## Installation
Run `consolidate-crontab.sh` to synchronize these tasks with the system crontab.
