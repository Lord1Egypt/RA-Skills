# Public Repository Manifest

This repository (`ASGCompute/asgcard-public`) is a **read-only public mirror** of the private operational repository.

## Included

| Directory | Contents |
|---|---|
| `api/src/` | API source (Express, x402 middleware, routes) |
| `api/__tests__/` | Unit and integration tests |
| `api/scripts/` | Automation scripts (preflight, E2E) |
| `sdk/src/` | SDK source (`@asgcard/sdk`, Stellar x402 v2) |
| `cli/src/` | CLI source (`@asgcard/cli`, terminal card management) |
| `mcp-server/src/` | MCP Server source (`@asgcard/mcp-server`, AI agent tool server) |
| `web/src/` | Frontend source (landing, docs page) |
| `web/public/` | Static assets (openapi.json, docs.md, icons) |
| `web/docs/` | Docs page entry |
| `docs/adr/` | Architecture Decision Records |
| `.github/workflows/` | CI (gitleaks, secret scan, content guardrail) |
| Root | README, LICENSE (MIT), CONTRIBUTING, AUDIT, SECURITY |

## Excluded (never published)

| Category | Description |
|---|---|
| **Secrets / env files** | All `.env` variants, API keys, tokens |
| **Debug / test scripts** | One-off E2E scripts, webhook test scripts |
| **Ops reports** | Preflight reports, baseline snapshots |
| **Deploy config** | Vercel project tokens and settings |
| **Internal ops docs** | Runbooks, evaluation docs, POC specs |
| **Internal planning** | Execution context, grant docs, comms packs |
| **Partner proposals** | All partner-specific proposal pages and routes |
| **Financial data** | Spreadsheets, financial models |
| **Build artifacts** | `dist/`, `node_modules/`, temp files |

## Synchronization

Changes flow: private repo → staging → push to public. Never push directly.

## Security

- Gitleaks runs on every push and PR
- Content guardrail CI blocks internal terms and validates structure
- Report vulnerabilities to `security@asgcard.dev` (see SECURITY.md)
