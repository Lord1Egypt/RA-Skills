# Integration Playbook

Use this reference for scanner, registry, MCP, and integration validation tasks.

## Discovery Targets

Root:

- `GET /mcp.json`
- `GET /.well-known/mcp.json`
- `GET /mcp` (Streamable HTTP MCP endpoint)
- `GET /skills/index.json`
- `GET /.well-known/skills/index.json`
- `GET /openapi.json`
- `GET /openapi.full.json`
- `GET /skill.md`
- `GET /llms.txt`
- `GET /.well-known/x402` (expect `404` when x402 is disabled)
- `GET /.well-known/mpp` when MPP is enabled
- `GET /.well-known/agent.json`
- `GET /.well-known/agents.json`

Shop:

- `GET /shop/openapi.json`
- `GET /shop/openapi.full.json`
- `GET /shop/skill.md`
- `GET /shop/llms.txt`
- `GET /shop/.well-known/agent.json`
- `GET /shop/.well-known/agents.json`

## MCP Validation

Validate that MCP discovery is consistent between `GET /mcp.json`, `GET /.well-known/mcp.json`, and `GET /mcp`:

- transport type
- command and args
- gateway base URL environment variable
- listed tools/resources/prompts

If MCP exists but command metadata is inconsistent with docs, report both values explicitly.

## OpenAPI Validation

- Treat `/openapi.json` as protocol-aware payable discovery for the current instance.
- Treat `/openapi.full.json` as the full contract.
- For shop, treat `/shop/openapi.full.json` as canonical full shop contract.

Report mismatches when:

- payable protocol is missing from protocol-aware OpenAPI but buy endpoints still answer as active
- catalog `purchaseUrl` points to route missing from protocol-aware OpenAPI

## Report Format

Return concrete, endpoint-level findings:

1. origin
2. enabled protocols
3. sale discovery status
4. shop discovery status
5. MCP status
6. OpenAPI consistency status
7. mismatches with exact endpoint + status + short evidence

Do not return generic statements such as "integration seems broken" without route-level proof.
