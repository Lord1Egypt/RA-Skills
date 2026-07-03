# AgentCash / Poncho Discovery

Any hosted endpoint for this package should be AgentCash-compatible and Poncho-ready:

- Serve `/openapi.json`.
- Serve `/.well-known/x402.json`.
- Add `info.contact.email`.
- Add `info.x-guidance`.
- Add operation-level `x-payment-info` with `price.mode`, `price.currency`, `price.amount`, and `protocols`.
- Add request and response schemas for agent invocation.
- Include `402` responses on paid operations.

Validate with:

```bash
npx -y @agentcash/discovery@latest discover "$TARGET_URL"
npx -y @agentcash/discovery@latest check "$TARGET_URL"
```

Use "AgentCash-compatible" and "Poncho-ready" unless there is an explicit partnership or certification.

## Preloaded ForgeMesh Catalog

The ClawHub package may preload known ForgeMesh x402 products in local config before using AgentCash/X402Scan. This is useful because AgentCash discovery is an external validation/discovery layer, while the package already knows first-party ForgeMesh endpoints.

Discovery order:

1. Preloaded ForgeMesh catalog for first-party products.
2. AgentCash/X402Scan discovery for broader x402 server search and validation.

Do not claim AgentCash endorsement from preloading ForgeMesh products.
