# Connect AlgoRover Research in OpenClaw

Install this Skill from ClawHub. Configure its hosted MCP connection separately; installing instructions alone does not connect or authorize the service.

- Name: `algorover-research`
- URL: `https://research.algorover.ai/mcp`
- Transport: Streamable HTTP
- Personal runs and reports: browser OAuth with `research:read research:run`

For OpenClaw versions supporting the native MCP CLI:

```sh
openclaw mcp add algorover-research --url https://research.algorover.ai/mcp --transport streamable-http
openclaw mcp doctor algorover-research --probe
openclaw mcp login algorover-research
```

Alternatively, add the server in Settings → MCP. Complete browser authorization before personal research, then verify `search_strategies` and an authorized read such as `get_profile`. Preserve existing MCP connections. See https://docs.openclaw.ai/tools/mcp for current client instructions.

The hosted service has been exercised in other MCP clients. OpenClaw-specific OAuth, interactive cards and full backtest execution have not yet been validated. Report connection or authorization errors without claiming these capabilities passed validation.

Public discovery uses no account. Personal task inputs are sent to the hosted Research service and associated with the signed-in account. Credentials stay in the client's authorization flow. The service does not connect exchange accounts or execute trading orders.

Privacy: https://www.algorover.ai/privacy/
Terms: https://www.algorover.ai/terms/
Support: https://www.algorover.ai/en/help/
