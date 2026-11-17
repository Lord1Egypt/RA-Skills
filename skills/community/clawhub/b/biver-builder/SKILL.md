---
name: biver-builder
description: Manage Biver landing pages, sections, products, forms, gallery assets, subdomains, custom domains, workspace settings, analytics, checkout data, and AI generation through the authenticated Biver API or MCP server. Use when an agent needs to read or change a Biver workspace.
metadata:
  openclaw:
    requires:
      env:
        - BIVER_API_KEY
    primaryEnv: BIVER_API_KEY
    envVars:
      - name: BIVER_API_KEY
        required: true
        description: Biver API key with only the scopes needed for the task.
      - name: BIVER_API_BASE_URL
        required: false
        description: Optional REST base URL; defaults to https://api.biver.id.
      - name: BIVER_MCP_URL
        required: false
        description: Optional MCP URL; defaults to https://mcp.biver.id/mcp.
    homepage: https://github.com/RamaAditya49/biver-builder
---

# Biver Builder

Use the remote MCP server when the client supports authenticated Streamable HTTP. Otherwise call the REST API directly.

- MCP: `https://mcp.biver.id/mcp`
- REST: `https://api.biver.id`
- Live REST contract: `https://api.biver.id/SKILL.md`
- Authentication: `Authorization: Bearer $BIVER_API_KEY` or `X-API-Key: $BIVER_API_KEY`

All Biver API keys can affect the workspace attached to the key. A key prefix does not create a sandbox. Start with read-only scopes and add write scopes only when the task requires them.

## Safety policy

Read-only calls do not need confirmation. Before a high-impact call, state the exact target and impact and obtain explicit user confirmation. An explicit request that already names the action and target counts; a vague request to “manage” or “clean up” does not.

Confirmation is required for:

- every `DELETE` request;
- page deploy or publish;
- custom-domain creation, update, primary selection, or deletion;
- subdomain creation, update, publication, or deletion;
- gallery deletion;
- workspace settings, branding, or SEO mutation.

For MCP, pass `confirm: true` only after that confirmation. Never reuse confirmation for another resource. Never log, print, or place the API key in a URL, file, prompt, or response.

## Scope contract

Scopes are enforced by the API. `all` bypasses individual scope checks and should be reserved for tightly controlled administration.

| Resource | Read | Write |
|---|---|---|
| Pages | `pages:read` | `pages:write` |
| Sections | `sections:read` | `sections:write` |
| Products | `products:read` | `products:write` |
| Forms and submissions | `forms:read` | `forms:write` |
| Gallery | `gallery:read` | `gallery:write` |
| Custom domains | `domains:read` | `domains:write` |
| Subdomains | `subdomains:read` | `subdomains:write` |
| Workspace | `workspace:read` | `workspace:write` |
| AI | `ai:generate` | `ai:generate` |
| Tracking | — | `tracking:write` |
| Wallet | `wallet:read` | — |
| Analytics | `analytics:read` | — |
| Checkout orders | `checkout:read` | — |

`GET` and `HEAD` use the read scope. Other methods use the write scope. AI routes always use `ai:generate`. Unknown `/v1/<resource>` routes fail closed unless the key has `all`.

## MCP

Connect to `https://mcp.biver.id/mcp` with the API key in an authorization header. The server exposes one tool:

### `biver_request`

Arguments:

| Field | Type | Required | Description |
|---|---|---|---|
| `path` | string | yes | A `/v1/...` API path without a query string. |
| `method` | string | no | `GET`, `POST`, `PATCH`, `PUT`, or `DELETE`; defaults to `GET`. |
| `query` | object | no | String, number, or boolean query values. |
| `body` | object | no | JSON request body. |
| `confirm` | boolean | for high-impact calls | Set only after explicit confirmation. |

The MCP server validates browser origins, API keys, scopes, path shape, methods, and confirmation. It returns the REST status and body as structured content. Multipart gallery upload remains a REST-only operation.

## REST endpoint map

Use the live contract for request fields and response details. Do not guess fields that are not listed there.

| Resource | Endpoints |
|---|---|
| Pages | `GET/POST /v1/pages`, `GET/PATCH/DELETE /v1/pages/:id`, `POST /v1/pages/:id/deploy`, publish status and deployment history |
| Sections | `GET/POST /v1/sections`, `PATCH/DELETE /v1/sections/:id`, bulk create and reorder |
| Products | `GET/POST /v1/products`, `GET/PATCH/DELETE /v1/products/:id` |
| Forms | `GET/POST /v1/forms`, `GET/PATCH /v1/forms/:id`, submissions endpoints |
| Gallery | `GET/POST /v1/gallery`, `GET/DELETE /v1/gallery/:id` |
| Subdomains | `GET/POST /v1/subdomains`, `GET/PATCH/DELETE /v1/subdomains/:id` |
| Domains | `GET/POST /v1/domains`, `GET/PATCH/DELETE /v1/domains/:id`, `POST /v1/domains/:id/primary` |
| Workspace | `GET /v1/workspace/settings`, `PATCH/PUT` settings, branding, and SEO, `GET /v1/workspace/public` |
| AI | context, page, section, and image generation routes under `/v1/ai` |
| Wallet | `GET /v1/wallet`, `GET /v1/wallet/transactions` |
| Analytics | `GET /v1/analytics/revenue`, `GET /v1/analytics/traffic` |
| Checkout | `GET /v1/checkout/orders`, `GET /v1/checkout/orders/:idOrOrderId` |

The API Worker requires authentication for every `/v1/*` route, including form-submit and workspace-public routes. Visitor-facing forms use Biver’s published-page flow, not an unauthenticated agent call.

## Minimal REST call

```bash
curl --fail-with-body \
  -H "Authorization: Bearer $BIVER_API_KEY" \
  "${BIVER_API_BASE_URL:-https://api.biver.id}/v1/pages?limit=20"
```

Send JSON mutations with `Content-Type: application/json`. Send gallery uploads as `multipart/form-data` with a `file` field. Use only one authentication header.

## Response handling

Successful responses use `{ "success": true, "data": ... }`. Errors use `{ "success": false, "error": { "code", "message" } }`.

- `401`: missing, invalid, expired, or revoked key.
- `403`: required scope is missing.
- `404`: resource not found in the key’s workspace.
- `409`: conflicting slug, subdomain, or domain.
- `422`: invalid input.
- `429`: rate limit reached; respect `Retry-After`.

Treat mutation retries conservatively. Re-read the resource after an ambiguous timeout before retrying a create, deploy, or delete operation.

## Install

```bash
clawhub install @ramaaditya49/biver-builder
```

Configure `BIVER_API_KEY` in the client’s secret store, not in the skill directory. Review the installed `SKILL.md` before granting write scopes.
