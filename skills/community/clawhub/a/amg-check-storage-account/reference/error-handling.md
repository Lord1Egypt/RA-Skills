# Error Handling

Recovery procedures for common failures during the health check workflow.

| Error | Recovery |
|-------|----------|
| Datasource UID no longer works | Re-run `amgmcp_datasource_list`, update `memory/amg-check-storage-account/config.md` with new UID |
| Pulse check timeout or failure | Retry once; if still failing, note in report |
| Pulse check scanned count < Phase 1 count | Note the gap; if >10% missing, fall back to batched `amgmcp_query_resource_metric` for unscanned accounts |
| Empty `timeSeries` in deep dive | Mark individual metrics as N/A — not an error (account may have no traffic) |
| MCP tool timeout | Note the failure, continue with remaining accounts |
| Zero accounts from Resource Graph | Report "No Storage Accounts found" and stop |
| Rate limiting / throttling | Reduce batch size to 4-5 parallel calls |
| Subagent MCP permission denied | Do NOT retry with subagents — MCP tools are unavailable to subagents. Query directly from main context |
| `timespan` parameter error | Use separate `from` and `to` parameters, not `timespan` |
| `UsedCapacity` interval error | Use `PT1H` only — `PT6H` and `P1D` are NOT supported for this metric |
| Resource logs unavailable | Diagnostic settings may not be configured — try `StorageTableLogs` or `StorageQueueLogs` as fallback, then note and skip |
| Result too large for context window | Save to temp file, then parse with whichever interpreter is installed — `node -e "..."`, `python -c "..."`, `jq`, or `pwsh -Command "..."`. Approve the Bash prompt on first use. |
| Config file missing at runtime | The `!` pre-computation will show `NOT_CONFIGURED` — run First-Run Setup before proceeding |
| Multiple Azure Monitor datasources | Prefer `uid == "azure-monitor-oob"`; if none has that UID, ask the user to choose |
