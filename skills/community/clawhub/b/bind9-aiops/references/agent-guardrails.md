# BIND 9 AIops agent guardrails

| Enforced in code | Location |
|---|---|
| Every MCP tool is audited, budgeted and risk annotated. | `governance/decorators.py`, `mcp_server/_annotations.py` |
| Commands run as argv lists without a shell; users cannot supply a binary or config path through a tool call. | `connection.py:_command`, `mcp_server/tools/dns.py` |
| DNS names and RR types are checked before command execution. | `connection.py:domain`, `connection.py:query` |
| SERVFAIL, truncated and unparseable SOA responses produce unknown serials, not zero. | `ops/dns.py:_soa_serial` |
| A failed diagnostic probe stays an error with `data: null`. | `ops/dns.py:diagnose` |
| Reload/refresh/flush/retransfer/notify validate inputs and preflight with reads; dry-run performs no write. | `mcp_server/tools/dns.py:bind_reload_zone`, `bind_refresh_zone`, `bind_flush_name`, `bind_retransfer_zone`, `bind_notify_zone` |
| A timed-out RNDC write and an accepted-but-unproven command return unknown. | `connection.py:rndc_write`, `mcp_server/tools/dns.py` |

The caller should check whether a query is authoritative for the intended zone before interpreting an SOA serial. `serialsMatch` is equality only; serial-number ordering and wraparound are not inferred. After an unknown write, inspect `zonestatus` and SOA before retrying. No safe undo exists for cache contents or externally edited zone files.
