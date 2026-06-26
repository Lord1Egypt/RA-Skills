# Reference — Endpoints / Tools

The skill operates through the **four MCP tools** of the Anthropic MCP server. Each maps to one or more Anthropic API endpoints (base `https://api.anthropic.com/v1`).

For full schemas and I/O examples, see the MCP tools reference: [../../mcp/docs/03-tools-reference.md](../../mcp/docs/03-tools-reference.md).

---

## Tool → endpoint map

| Tool | Method + path | Billed? | Purpose |
|------|---------------|---------|---------|
| `anthropic_messages` | `POST /messages` | **Yes** | Chat, tool use, vision, documents, extended thinking. `max_tokens` **required**. |
| `anthropic_count_tokens` | `POST /messages/count_tokens` | No (not generation) | Estimate input tokens. |
| `anthropic_models` | `GET /models` or `/models/{id}` | No | List/inspect models. |
| `anthropic_request` | any method + path | Depends on path | Passthrough: `/messages/batches`, `/files` (beta), etc. |

---

## Required headers (handled by the server)

| Header | Value | Notes |
|--------|-------|-------|
| `x-api-key` | `<ANTHROPIC_API_KEY>` | Auth; redacted in logs. |
| `anthropic-version` | `2023-06-01` (default) | **Required** by the API. |
| `anthropic-beta` | `<ANTHROPIC_BETA>` | Only when set; needed for beta endpoints. |

---

## `anthropic_request` common paths

| Path | Method | Needs beta? | Use |
|------|--------|-------------|-----|
| `/messages/batches` | POST | No | Create a batch (~50% off). |
| `/messages/batches/{id}` | GET | No | Poll batch status. |
| `/messages/batches/{id}/results` | GET | No | Fetch batch results. |
| `/files` | GET/POST | **Yes** | Files API (beta). |
| `/messages/count_tokens` | POST | No | Token counting (same as the typed tool). |

> Verification needed: confirm endpoint paths and beta flags at https://docs.anthropic.com/en/api

---

See also:
- Parameters: [parameters.md](parameters.md)
- Errors: [common-errors.md](common-errors.md)
- Best practices: [best-practices.md](best-practices.md)
