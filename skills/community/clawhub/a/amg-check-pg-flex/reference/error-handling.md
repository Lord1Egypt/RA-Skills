# Error Handling

Recovery procedures for common failures during the health check workflow.

| Error | Recovery |
|-------|----------|
| Datasource UID no longer works | Re-run `amgmcp_datasource_list`, update `memory/amg-check-pg-flex/config.md` with new UID |
| Pulse check `totalResourcesScanned` < Phase 1 count | Note the gap in the report; if >10% missing, fall back to batched `amgmcp_query_resource_metric` for unscanned servers |
| Pulse check scenario not completed | Retry the failed scenario individually (e.g., `scenarios: pg_flex_cpu`) |
| Pulse check `errors` non-empty | Report errors, retry affected scenarios |
| Activity log response too large (>500 KB) | Retry with `startTime: now-6h` instead of `now-3d` |
| Empty `timeSeries` in Phase 3 metric response | Mark metric as N/A — not an error (server may be a primary with no replicas) |
| MCP tool timeout | Note the failure in the report, continue with remaining servers |
| Rate limiting / throttling (Phase 3) | Reduce batch size from 50 → 25 → 10 resource IDs per call |
| Zero servers from Resource Graph | Report "No PostgreSQL Flexible Servers found" and stop |
| Subagent MCP permission denied | Do NOT retry with subagents — MCP tools are unavailable to subagents. Query directly from main context |
| Result too large for context window | Save response to `/tmp/pg-result.json` via Bash, then parse with whichever interpreter is installed — `node -e "const d=require('/tmp/pg-result.json'); ..."`, `python -c "import json; d=json.load(open('/tmp/pg-result.json')); ..."`, `jq`, or `pwsh -Command "..."`. Approve the Bash prompt on first use. |
| Config file missing at runtime | The `!` pre-computation will show `NOT_CONFIGURED` — run First-Run Setup before proceeding |
| Multiple Azure Monitor datasources | Prefer `uid == "azure-monitor-oob"`; if none has that UID, ask the user to choose |
