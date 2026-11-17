## DCC-host route

For a registered DCC instance, use the DCC-MCP UI Control tools or their CLI
projection:

```bash
dcc-mcp-cli load-skill ui-control --instance-id <instance-id> --output toon
dcc-mcp-cli ui-control snapshot --instance-id <instance-id> --json '{"session_id":"ui","process_id":1234,"window_handle":5678}'
dcc-mcp-cli ui-control act --instance-id <instance-id> --json '{"session_id":"ui","control_id":"ok","action":"click","snapshot_id":"<snapshot-id>"}'
dcc-mcp-cli ui-control act --instance-id <instance-id> --json '{"session_id":"ui","action":"invoke_menu","menu_path":["Window","Arrange","Left"]}'
dcc-mcp-cli ui-control stop --instance-id <instance-id> --json '{"session_id":"ui"}'
```

Use the same exact instance and session throughout the action chain. Do not
switch to another DCC process because it looks similar.

For occlusion or foreground recovery, follow the router's
[scoped window recovery decision](https://github.com/dcc-mcp/dcc-mcp-agent-plugins/blob/main/plugins/dcc-mcp/skills/dcc-mcp/references/UI_WORKFLOWS.md#scoped-window-recovery).
An independently authorized blocker task never widens the original DCC task.

If the adapter owner configured an integrity-pinned `pixels_only` runtime,
follow the [owned pixels and secondary popup workflow](https://github.com/dcc-mcp/dcc-mcp-agent-plugins/blob/main/plugins/dcc-mcp/skills/dcc-mcp/references/UI_WORKFLOWS.md#owned-pixels-and-secondary-popup-observations)
and the installed runtime schema instead of the semantic action examples above.
Honor that workflow's release gate before using secondary popup fields.
Secondary popup images require an independently enabled owner ceiling, grant
no input authority, and never change the bound main window. Missing capability
or native proof remains a refusal; do not switch input routes.

