# Server Skill Workflows

Dinzee server-side skills are metered workflow packages. The client submits only:

```json
{
  "skill_slug": "momentum-product-scout",
  "params": {
    "domain": 1,
    "review_limit": 199,
    "monthly_sold_min": 5000,
    "sample_limit": 50
  }
}
```

The server loads `server-skills/index.json`, validates params against the selected manifest, creates a `workflow_run`, estimates total skill points, charges once with `provider=hermes` and `workflow_id=<skill_slug>`, executes the workflow, records internal tool execution details, renders artifacts, uploads reports, and returns:

```json
{
  "workflow_run_id": "wr_xxx",
  "status": "succeeded",
  "points_charged": 42,
  "report_url": "https://report.dinzee.ai/xxx.html",
  "artifacts": [],
  "tool_usage": [],
  "summary": {}
}
```

## Required Server Tables

- `skills`: slug, version, manifest_json, status.
- `workflow_runs`: user_id, skill_slug, params_json, status, estimated_points, final_points, result_json, report_url.
- `tool_call_ledger`: workflow_run_id, step_id, provider_alias, tool_alias, request_json, response_summary_json, status, raw_units, point_cost. Internal tool rows are execution details, not separate billing rows.
- `workflow_artifacts`: workflow_run_id, type, url, metadata_json.

## Execution Rules

- Workflow steps with `type=mcp_call` must go through the Dinzee MCP gateway.
- Client-submitted credentials are not accepted.
- Manifests use neutral `provider_alias`/`tool_alias`; the server maps them to allowlisted upstream tools.
- Point settlement is a single Hermes charge per skill run. The amount is estimated as `base_points + configured billable workflow step costs`.
- Failed workflows must return the ledger and partial artifacts when available.

## Alias Mapping

Server manifests never expose real upstream providers or tool names. Production must set:

```bash
export DINZEE_SERVER_SKILL_ALIAS_MAP='{
  "product_intelligence.product_finder": {"provider": "PUBLIC_PROVIDER", "tool": "REAL_TOOL"},
  "product_intelligence.product_details_batch": {"provider": "PUBLIC_PROVIDER", "tool": "REAL_TOOL"},
  "report_hosting.upload_artifacts": {"provider": "PUBLIC_PROVIDER", "tool": "REAL_TOOL"}
}'
```

Each mapped `provider/tool` must already exist in the public MCP policy manifest. The runner reads that policy at runtime to get `chargeable` and `points_cost`; billing is still settled once under `provider=hermes` and `workflow_id=<skill_slug>`.

## Point Audit Formula

The response is auditable by design:

```text
points_charged == tool_usage[0].point_charged
```

The first ledger row has `type=skill_charge`, `billing_provider=hermes`, `workflow_id=<skill_slug>`, `point_cost`, `point_charged`, `billing_idempotency_key`, `billing_ledger_id`, and `authority_correlation_id`. Later tool rows use `billing_scope=included_in_skill_charge` and `point_charged=0`.
