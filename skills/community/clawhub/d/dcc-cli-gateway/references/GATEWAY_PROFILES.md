## Gateway Profiles And Local-First Inventory

`dcc-mcp-cli` has a built-in `local` profile. In local mode, agent-control
commands first ensure the machine-wide loopback gateway is healthy, then
`list` reads FileRegistry; `search`, `describe`, `call`, and guarded
`stop-instance` use the selected instance endpoints. `load-skill` uses the
ensured gateway to update its capability index; `--no-auto-gateway` retains
direct loading. `wait-ready` uses discovery MCP when readyz cannot report
`skill_catalog`. Remote machines use named gateway profiles:
Treat `list` as inventory plus diagnostics, not proof that a row is callable.
It intentionally keeps live `booting` / `dispatch_status=unavailable` sidecar
rows visible. Local control routes only to ready rows; gateway-owned
`load-skill` targets the same row and refreshes its capabilities. Per-DCC sidecar
rows become local MCP routes once they report `dispatch_status=ready`; before
that, they remain visible for diagnostics. Use `wait-ready` or `doctor` when a
listed instance is still booting.

```bash
dcc-mcp-cli gateway register https://workstation.example:19293 --name pcA
dcc-mcp-cli gateway list
dcc-mcp-cli gateway set pcA
dcc-mcp-cli gateway set local
dcc-mcp-cli list --gateway pcA
```

Use `--gateway <name>` to override the current profile for one command.
`--base-url` / `DCC_MCP_BASE_URL` remain direct endpoint overrides for legacy
scripts and smoke checks.

Use `--require-gateway` for any local workflow whose calls must appear in
Gateway audit/stats. Pair it with `--agent-session-id <task-id>` so every
single or batched call gets the same `_meta.agent_context.session_id` without
hand-editing `--meta-json`. A conflicting session value in `--meta-json` is an
error. Direct local call output reports `control_route=local_mcp_direct` and
`gateway_stats_recorded=false`; gateway-routed output reports
`control_route=gateway` and `gateway_stats_recorded=true`.

Agent-control commands (`list`, `search`, `describe`, `load-skill`, `call`,
`wait-ready`, `reload-skills`, and `stop-instance`) and endpoint-level commands
such as `health`, `update`, and `smoke` without an explicit `--url` auto-ensure
loopback HTTP gateway targets. File-only commands and explicit lifecycle
commands do not auto-start the gateway.
When startup state is unclear, run `dcc-mcp-cli doctor` before troubleshooting
adapters. It reports profile config/current selection, the registry directory
and local inventory, direct-control readiness counts, gateway daemon status, and
server binary path/source/version without launching or downloading anything.
When `list` shows local rows, prefer `direct_control.recommended_next_action`
over guessing from status text; sidecar rows are local tool-call routes only
after `direct_control.ready=true`. If `direct_control.ready=false`, inspect
`direct_control.diagnostics.failure_stage`, `failure_reason`, `host_rpc_*`, and
any `diagnostics.logs.*` paths before retrying. `doctor` summarizes the same
not-ready rows under `local.inventory.direct_control.not_ready_instances`.

Detailed daemon lifecycle, profile commands, release assets, and fallback
behavior live in [CLI cheatsheet](CLI_CHEATSHEET.md). Read it only
when setup, lifecycle, or transport troubleshooting is needed.
