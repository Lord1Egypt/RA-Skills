# Porting Checklist

Before enabling the scheduled health check on a destination OpenClaw instance:

- Set the destination instance name and timezone.
- Set the destination OpenClaw home path.
- Set the destination scheduler source: structured list command or read-only jobs file.
- Set the destination chat/topic target, or use origin delivery from the desired target.
- Do not use the runtime service manager as the OpenClaw cron inventory source.
- Keep crontab files separate from run-parts directories.
- Build the `known_system_jobs` list from the destination server's own cron files and logs.
- Set expected log freshness thresholds slightly above each job interval.
- Add dry-run/status checks only through logs, scheduler metadata, or a local derivative with a fixed documented argv template.
- Add project scheduler checks only for projects present on the destination instance.
- Set registry and callback file paths only if they exist on that instance.
- Keep registry reconciliation report-only unless a separate maintenance workflow authorizes writes.
- Run the script manually once from the destination user account.
- Confirm the script rejects shell syntax and does not use shell expansion.
- Confirm command probes are limited to the fixed diagnostic argv allowlist.
- Confirm missing scripts, stale logs, ambiguous runtime proof, and command failures are not reported as `OK`.
- Confirm run-parts scripts are not parsed as crontab files.
- Confirm placeholder defaults do not generate false `CRITICAL` entries.
- Confirm redaction works before sending the first report to a chat.
- Create the OpenClaw scheduled job in script-only/no-agent mode.
- After creation, list the job and verify name, schedule, next run, script path, delivery target, and script-only/no-agent mode.

Recommended schedules:

```text
0 */6 * * *   # every 6 hours for general automation hosts
0 0,12 * * *  # twice daily for low-volume hosts
```

Use hourly checks only for high-volume or customer-facing scheduled automation.
