# Discovery And Routing

Use this reference when the task starts with discovery, browsing, or route selection.

## Required Discovery Order

Run these reads in order against one origin:

1. `GET /`
2. `GET /health`
3. `GET /openapi.json`
4. `GET /openapi.full.json`
5. `GET /mcp.json`
6. `GET /skills/index.json`
7. `GET /catalog`
8. `GET /.well-known/x402`
9. `GET /.well-known/mpp` (if available)

If shop is relevant:

1. `GET /shop`
2. `GET /shop/health`
3. `GET /shop/openapi.json`
4. `GET /shop/openapi.full.json`
5. `GET /shop/.well-known/x402` (if x402 is enabled)
6. `GET /shop/.well-known/mpp` (if available)

## Surface Router

- User asks to browse all offers: start at `GET /catalog`.
- User asks for presale lot, Agentic Pass, or NFT mint flow: route to `sale` (`/agentic/*`).
- User asks for keys, gems, packs, or nickname/address-based item delivery: route to `shop` (`/shop/*`).
- User asks about scanners, manifests, OpenAPI, MCP, or registry onboarding: stay in discovery + integration flow.

## Protocol Router

- Use payable `openapi.json` routes as protocol truth on this instance.
- Treat root `/.well-known/x402` as compatibility metadata for enabled x402 resources; expect `404` when x402 is disabled on this deployment.
- If only one payable protocol exists in OpenAPI, use that protocol and do not probe the other.
- If no payable protocol is discoverable, report mismatch and stop before buy attempts.

## Catalog Checks Before Any Buy

From `GET /catalog`:

- Confirm item `surface` matches the selected contract path.
- Use item `purchaseUrl` and `checkout.protocols` as source of truth for next payable step.
- Reject route mismatch:
  - `surface: sale` with `/shop/` purchase path
  - `surface: shop` with root `/agentic/` purchase path

## Shop Recipient Rule

For shop quote and buy, require exactly one:

- `nickname`
- `address`

Never send both in one request.

## Minimal Route Decision Record

Return this in your reasoning output before buy:

- origin
- chosen surface
- chosen protocol
- selected endpoint
- selected payload fields
- why this route matches catalog metadata
