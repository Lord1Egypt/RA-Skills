# Report Format

The health-check script should always print one complete report unless explicitly configured for threshold-only alerts.

Recommended shape:

```text
OpenClaw Cron Health Report - <INSTANCE_NAME>
Generated: <YYYY-MM-DD HH:MM TZ>
Summary: <healthy>/<total> healthy or informational | <issue_count> attention points | overall <STATUS>

System
- [OK|WARNING|CRITICAL|INFO] cron.service: <state>
- [OK|WARNING|CRITICAL|INFO] process manager: <state>
- [OK|WARNING|CRITICAL|INFO] failed units: <summary>

OpenClaw Jobs
- [OK|WARNING|CRITICAL|INFO] <name> - last: <time>, next: <time>, schedule: <schedule>, status: <last_status>

System Crons
- [OK|WARNING|CRITICAL|INFO] <source> - command/script <status> | runtime proof <status> | errors <count/status>

Known System Jobs
- [OK|WARNING|CRITICAL|INFO] <name> - command <status> | log <fresh/stale/missing/no-log> | validation <result>

Project Scheduler Checks
- [OK|WARNING|CRITICAL|INFO] <name> - <short validation result>

Registry Notes
- [OK|WARNING|CRITICAL|INFO] <short report-only note>

Conclusion: <short operational conclusion>
```

Rules:

- Keep the report concise enough for chat delivery.
- Include every enabled OpenClaw scheduled job.
- Redact before printing any log line, command output, config-derived value, or delivery error.
- Quote only the shortest useful error line for warning/critical items.
- Truncate long lines aggressively.
- Keep inventory-only and intentionally paused items as `INFO`.
