# Error Handling

Recovery procedures for common failures during the health check workflow.

| Error | Recovery |
|-------|----------|
| Datasource UID no longer works | Re-run `amgmcp_datasource_list`, update `memory/amg-check-cosmosdb-mongo-ru/config.md` with new UID |
| `InternalServerError: Unable to load datasource meta data` | Wrong datasource UID — re-run `amgmcp_datasource_list` to discover the correct UID and update config |
| `BadRequest: can not support requested time grain` | Use `PT1H` as safe default. DataUsage/IndexUsage/DocumentCount do NOT support P1D |
| `timespan` parameter error | Use separate `from` and `to` parameters, not `timespan` |
| MCP response >500 KB | Reduce batch size (fewer accounts per call) or shorten time window. Use `FULL` interval for overview metrics (ProvisionedThroughput, AutoscaleMaxThroughput) |
| Result too large for context window | Save to temp file, then parse with whichever interpreter is installed — `node -e "..."`, `python -c "..."`, `jq`, or `pwsh -Command "..."`. Approve the Bash prompt on first use. |
| Empty `timeSeries` | Mark as N/A, not an error (expected for AutoscaleMaxThroughput on manual accounts, ReplicationLatency on non-replicated accounts) |
| MCP tool timeout | Note the failure in the report, continue with remaining accounts |
| Zero accounts from Resource Graph | Report "No Cosmos DB for MongoDB (RU) accounts found" and stop |
| Rate limiting / throttling | Reduce batch size from 10 accounts (30 calls) to 5 accounts (15 calls) |
| Partial metric query failures | Include account in report with "Metrics Unavailable" status |
| Subagent MCP permission denied | Do NOT retry with subagents — MCP tools are unavailable to subagents. Query directly from main context |
| Resource logs unavailable | Diagnostic settings may not be configured — note and skip Phase 5 |
| Pulse check `totalResourcesScanned` < Phase 1 count | Note the gap; if >10% missing, fall back to batched `amgmcp_query_resource_metric` for unscanned accounts |
| Pulse check scenario not completed | Retry the failed scenario individually |
| Pulse check `errors` non-empty | Report errors, retry affected scenarios |
| Activity log response too large (>500 KB) | Retry with `startTime: now-1d` instead of `now-3d` |
| Config file missing at runtime | The `!` pre-computation will show `NOT_CONFIGURED` — run First-Run Setup before proceeding |
| Multiple Azure Monitor datasources | Prefer `uid == "azure-monitor-oob"`; if none has that UID, ask the user to choose |
