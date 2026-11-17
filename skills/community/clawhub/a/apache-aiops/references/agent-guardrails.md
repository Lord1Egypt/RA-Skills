# Apache AIops agent guardrails

| Enforced in code | Location |
|---|---|
| Every MCP tool is audited, budgeted and risk annotated. | `governance/decorators.py`, `mcp_server/_annotations.py` |
| Read commands accept only fixed `apachectl` arguments and no shell; graceful is a separate fixed write. | `connection.py:command`, `connection.py:graceful` |
| The HTTP probe URL is configured by the operator; the agent cannot choose a URL. | `config.py:TargetConfig`, `mcp_server/tools/httpd.py` |
| HTTP probe reads headers and status without returning a body. | `connection.py:probe` |
| A failed diagnostic probe remains an error with `data: null`; a completed but unhealthy HTTP probe appears in `unhealthyProbes` and sets `healthy: false`. | `ops/httpd.py:diagnose` |
| `mod_status`, error-log and access-log reads are operator configured and bounded; the access summary returns no raw request data. | `config.py:TargetConfig`, `connection.py:server_status`, `connection.py:error_log`, `connection.py:access_status` |
| Graceful reload first runs configtest; dry-run never invokes graceful. | `mcp_server/tools/httpd.py:apache_graceful_reload` |

A successful `configtest` proves syntax, not that upstream application backends are healthy. A missing HTTP probe is an unperformed check (`healthy: null`); `complete: true` only means the configured probes ran without errors. A returned graceful command still reports unknown because existing workers may hold old config; inspect status and traffic before retrying.
