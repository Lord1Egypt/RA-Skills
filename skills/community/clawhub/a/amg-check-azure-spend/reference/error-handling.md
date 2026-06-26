# Error Handling

Recovery procedures for common failures during the cost analysis workflow.

| Error | Recovery |
|-------|----------|
| Datasource UID no longer works | Re-run `amgmcp_datasource_list`, update `memory/amg-check-azure-spend/config.md` with new UID |
| 429 Too Many Requests (first occurrence) | Wait 2 minutes (`sleep 120`), then retry the same subscription |
| 429 Too Many Requests (second occurrence) | Wait 5 minutes (`sleep 300`), then retry once more |
| 429 Too Many Requests (third occurrence) | Skip this subscription, note "Rate-limited — skipped" in report, continue with next subscription after 5-minute wait |
| Empty cost data for subscription | Subscription may have no resources or billing not configured — note "No cost data" and continue |
| MCP tool timeout | Note the failure, wait 1 minute, continue with next subscription |
| Zero subscriptions from listing | Report "No accessible subscriptions found" and stop |
| Subscription ID from arguments not found in list | Warn the user, skip the invalid ID, continue with valid ones |
| Result too large for context window | Save to temp file, then parse with whichever interpreter is installed — `node -e "..."`, `python -c "..."`, `jq`, or `pwsh -Command "..."`. You'll be prompted to approve the `Bash(...)` call the first time. |
| Config file missing at runtime | The `!` pre-computation will show `NOT_CONFIGURED` — run First-Run Setup before proceeding |
| Multiple Azure Monitor datasources | Prefer `uid == "azure-monitor-oob"`; if none has that UID, ask the user to choose |
