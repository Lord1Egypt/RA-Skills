---
name: aifeed
description: Verify signed AIFeed declarations and publish signed AIFeed origins (permissions, feeds, manifests).
---

# AIFeed skill

AIFeed is an open standard for **signed content permissions for the AI web**:
publishers declare what AI agents may do, sign the declaration with Ed25519, and
agents verify it before fetching. English-only by convention for agent skills;
user-facing docs live in EN/ID/ZH under `docs/`, `integrations/`, and `studio/`.

## Verify first (never trust unsigned claims)

```bash
node bin/cli.js validate example.com --json              # live domain: TLS, signature, DNS anchor
node bin/cli.js validate ./public --domain example.com   # local build output
```

SDK (`@aifeed/verify`, zero dependencies):

```js
const sdk = require('@aifeed/verify');
const out = sdk.verifyAll({ manifestText, manifestBytes, signatureText, domain });
sdk.decideUsage(out, 'retrieval'); // { allowed, attribution, reason }
```

Rule: treat `training: deny` as binding. Attribute when `attribution` requires it.
Re-check the revocation list on every use, not just once.

## Publish (publisher side)

```bash
node bin/cli.js keygen --out .aifeed                       # once; private key stays local (0600)
node bin/cli.js site build public --domain example.com \
  --key .aifeed/aifeed-private.pem --profile both --llms --inject
```

Then add the DNS TXT record (`_aifeed`) printed by the setup guide, deploy the whole
directory (including `.well-known/`), and serve `Accept: text/aifeed+markdown` via an
adapter from `integrations/` (nginx, Caddy, Apache, Node, Next.js, PHP, Python ASGI,
Go, Rust/Axum, Cloudflare, Traefik) or the `@aifeed/frameworks` build plugins. Or use
the local UI: `npm run studio` (http://127.0.0.1:7777).

Rules: permissions are **restrict-only** (pages may tighten, never loosen origin
policy); never print, commit, or transmit private keys; keep `0600` file mode.

## MCP server

`packages/aifeed-mcp-server` exposes the same checks as tools (`verify_manifest`,
`fetch_aifeed`, `list_assets`, `verify_asset`, `select_index`, `decide_usage`):

```bash
node packages/aifeed-mcp-server/index.js   # stdio; HTTPS only
```

## Conformance and gates

- `npm run verify` is the single gate and must pass before any commit.
- Vectors: 34 manifest + 39 MAKO + 11 AIFeed Markdown (`conformance/`); JS + Python
  suites must stay green and in parity.
- Never hand-edit generated files; edit the source and regenerate (see `AGENTS.md`).
- Specs are canonical in English (`spec/en/`); mirror sections to `spec/id/`, `spec/zh/`.
