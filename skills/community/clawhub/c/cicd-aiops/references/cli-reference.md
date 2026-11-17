# cicd-aiops — CLI reference

All commands accept `--target/-t <name>` (default: the first target in
config.yaml). Writes accept `--dry-run` and double-confirm before executing;
confirmed writes run through the same governed path as the MCP tools (audited).

## Setup / health

```bash
cicd-aiops init                 # onboarding wizard (platform, base URL, encrypted token)
cicd-aiops doctor               # config + secrets + connectivity + token-scope probe
cicd-aiops doctor --skip-auth   # config/secrets checks only
cicd-aiops overview             # version, identity, projects, runners
cicd-aiops projects [--search x] [--limit N]
```

## Pipelines

```bash
cicd-aiops pipelines list <project> [--status failed] [--limit N]
cicd-aiops pipelines show <project> <pipeline>
cicd-aiops pipelines jobs <project> <pipeline>
cicd-aiops pipelines trace <project> <job> [--lines 60]
cicd-aiops pipelines retry <project> <pipeline> [--dry-run]    # governed write
cicd-aiops pipelines cancel <project> <pipeline> [--dry-run]   # governed write
```

## Runners

```bash
cicd-aiops runners list [--status offline]
cicd-aiops runners show <runner>
cicd-aiops runners pause <runner> [--dry-run]     # governed write, undo-recorded
cicd-aiops runners resume <runner> [--dry-run]    # governed write, undo-recorded
```

## Artifacts

```bash
cicd-aiops artifacts list <project>
cicd-aiops artifacts delete <project> [--older-than-days 30] [--dry-run] [--acknowledge-unknown-inventory]
# risk=high: requires CICD_AUDIT_APPROVED_BY (+ CICD_AUDIT_RATIONALE)
```

## Flagship RCAs

```bash
cicd-aiops rca pipelines <project> [--limit 10]   # classify failed pipelines
cicd-aiops rca runners                            # offline/stale/saturation
cicd-aiops rca storage [--old-days 30]            # bloat + reclaimable bytes
cicd-aiops rca stale <project> [--mr-days 14] [--branch-days 90]
```

## Secrets

```bash
cicd-aiops secret set <target>      # store a token (encrypted)
cicd-aiops secret list              # names only, never values
cicd-aiops secret remove <target>
cicd-aiops secret migrate           # legacy .env → encrypted store
```

## MCP

```bash
cicd-aiops mcp                      # start the MCP server (stdio)
```

## Environment variables

| Var | Purpose |
|---|---|
| `CICD_AIOPS_HOME` | relocate config/audit/undo/secrets (default `~/.cicd-aiops`) |
| `CICD_AIOPS_CONFIG` | explicit config.yaml path for the MCP server |
| `CICD_AIOPS_MASTER_PASSWORD` | unlock secrets.enc non-interactively |
| `CICD_AUDIT_APPROVED_BY` / `CICD_AUDIT_RATIONALE` | optional audit annotations (who/why) — recorded, never required |
| `CICD_MAX_TOOL_CALLS` / `CICD_MAX_TOOL_SECONDS` | budget caps |
| `CICD_RUNAWAY_MAX` / `CICD_RUNAWAY_WINDOW_SEC` | runaway breaker |
| `CICD_<TARGET>_SECRET` | legacy plaintext token fallback (deprecated) |
