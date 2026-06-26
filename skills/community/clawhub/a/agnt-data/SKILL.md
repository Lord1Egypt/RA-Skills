---
name: agnt-data
description: "Unified social data API for AI agents. One API key for LinkedIn, YouTube, TikTok, X, Instagram, Reddit, and Facebook."
version: 1.0.15
metadata:
  openclaw:
    requires:
      env:
        - AGNTDATA_API_KEY
      bins:
        - curl
    primaryEnv: AGNTDATA_API_KEY
    emoji: "\u26A1"
    homepage: https://agntdata.dev
---

# agnt-data — Unified Social Data for AI Agents

One subscription, one API key, access to structured social data across seven platforms. No scraping infra, no managing upstream vendor accounts. Every response is structured JSON optimized for LLM and agent consumption.

## Recommended: Install the agnt-data Plugin

**For the best experience, install the agnt-data plugin instead of this skill.** The plugin provides:

- Native MCP tools for each platform (no curl required)
- Automatic authentication with browser-based login
- Structured tool schemas with full parameter validation
- Direct integration with your agent's tool system

**Master skill** (this bundle):

```bash
clawhub install agnt-data
```

**Master plugin** (all platforms; npm name matches generated `package.json`):

```bash
openclaw plugins install @agntdata/openclaw-agnt-data
```

For a single platform only, use that platform’s skill and plugin instead, for example:

```bash
clawhub install agntdata-facebook
openclaw plugins install @agntdata/openclaw-facebook
```

This skill is useful for environments where plugins are not supported, or when you need a lightweight reference.

## Authentication

Before making API calls, you need an API key. Get one from the [agntdata dashboard](https://app.agntdata.dev/dashboard).

The API key should be available as the `AGNTDATA_API_KEY` environment variable. Every request must include it as a Bearer token:

```
Authorization: Bearer $AGNTDATA_API_KEY
```

If the environment variable is not set, ask the user to provide their API key or direct them to https://app.agntdata.dev/dashboard to create one.

## API Key Activation

After setting your API key, activate it by calling the registration endpoint. This only needs to be done once per key:

```bash
curl -X POST https://api.agntdata.dev/v1/register \
  -H "Authorization: Bearer $AGNTDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"intendedApis": ["linkedin", "youtube"], "useCase": "Brief description of your use case"}'
```

Replace `intendedApis` with the platforms you plan to use, and `useCase` with a short description of how you plan to use the API.

## Discovery Endpoints

These public endpoints (no API key required) help you explore available platforms and their capabilities:

**List all platforms:**

```bash
curl https://api.agntdata.dev/v1/platforms
```

Returns: slug, name, endpoint count, and description for each platform.

**Get platform details:**

```bash
curl https://api.agntdata.dev/v1/platforms/{slug}
```

Returns: full endpoint list, OpenAPI spec, features, use cases, and documentation links.

Use these endpoints to discover capabilities before making authenticated API calls.

## Base URL

```
https://api.agntdata.dev/v1/data/{platform}
```

## Available APIs

| Platform | Slug | Endpoints | Description |
|----------|------|-----------|-------------|
| LinkedIn | `linkedin` | 52 | Enrich companies and profiles in real time. Designed for agents that need reliable structured data without managing dozens of vendor accounts. |
| YouTube | `youtube` | 22 | Unified access to video metadata, channel discovery, comments, subtitles, and recommendations. Built for LLMs and automation — not one-off scraping. |
| TikTok | `tiktok` | 12 | Unified access to video details, creator profiles, and search across accounts and videos. Built for LLMs and automation — not one-off scraping. |
| X (Twitter) | `x` | 52 | Unified access to tweets, user profiles, followers, search, and hashtag streams. Built for LLMs and automation — not one-off scraping. |
| Instagram | `instagram` | 22 | Unified access to user profiles, reels, explore, locations, and hashtag media. Built for LLMs and automation — not one-off scraping. |
| Reddit | `reddit` | 29 | Unified access to subreddit metadata, post threads, user activity, and search. Built for LLMs and automation — not one-off scraping. |
| Facebook | `facebook` | 35 | Unified access to page and group posts, marketplace listings, video content, and ad discovery. Built for LLMs and automation — not one-off scraping. |

## Choosing the Right API

- **B2B enrichment / sales intelligence** — use `linkedin`
- **Video content / creator intelligence** — use `youtube` or `tiktok`
- **Real-time social listening / trends** — use `x` or `reddit`
- **Visual content / influencer data** — use `instagram`
- **Pages, groups, marketplace, ads** — use `facebook`

## Example

```bash
curl -X GET 'https://api.agntdata.dev/v1/data/linkedin/get-company-details?username=microsoft' \
  -H 'Authorization: Bearer $AGNTDATA_API_KEY'
```

## Webhooks (Receive Events from Third Parties)

agntdata can act as a hosted webhook receiver. You create an **endpoint** in the user's workspace, hand the resulting URL to a third party (Stripe, Calendly, GitHub, your own service, anything that POSTs JSON), and every inbound POST is captured as a **delivery** that an agent can fetch and acknowledge later.

### Concepts

- **Endpoint** — a named receiver in the user's workspace. Created with a friendly `name` (e.g. `stripe-prod`); identified by a UUID `id`.
- **Receive URL** — `https://api.agntdata.dev/webhooks/ingest/<endpointId>`. The endpoint id IS the secret in the URL — treat it like a credential. There is no signature verification; the URL is the auth.
- **Delivery** — one inbound POST, captured with the raw JSON body, the headers the third party sent, and the source IP. Has an `acknowledgedAt` timestamp that starts `null`.
- **Acknowledge** — mark a delivery as processed so it stops appearing in `unacknowledged: true` queries. Does NOT delete the delivery; history is retained.

### Typical Agent Flow

1. **Create the endpoint** — `POST /v1/webhook-endpoints` with `{ "name": "stripe-prod" }`. Returns `{ id, name, url }`. Show the `url` to the user and tell them to paste it into the third party's webhook configuration.
2. **Wait for events** — the third party POSTs to `https://api.agntdata.dev/webhooks/ingest/<id>`. Each POST is stored as a delivery; nothing is forwarded synchronously.
3. **Poll for new work** — `GET /v1/webhook-endpoints/deliveries?unacknowledged=true&endpointId=<id>` (or omit `endpointId` to query across all endpoints in the workspace).
4. **Process each `rawPayload`** — it's the exact JSON the vendor sent. Parse it the way that vendor documents (e.g. for Stripe, switch on `type` and read `data.object`).
5. **Acknowledge** — call `POST /v1/webhook-endpoints/deliveries/ack` with `{ "ids": [...] }` (or single via `POST /v1/webhook-endpoints/deliveries/{id}/ack`) so the next poll doesn't re-deliver them.
6. **Page through history** — if a response includes `nextCursor`, pass it as `cursor` to fetch older deliveries.

### Webhook Endpoints

| Method | Path | Summary |
|--------|------|---------|
| `POST` | `/v1/webhook-endpoints` | Create a new agntdata webhook endpoint. Returns { id, name, url } where `url` is a public HTTPS endpoint of the form https://api.agntdata.dev/webhooks/ingest/<id>. Give that URL to a third party (Stripe, Calendly, GitHub, your own service, etc.) so they can POST events to it. agntdata stores every inbound POST as a "delivery" the agent can later fetch with agntdata_webhooks_list_deliveries. The `name` is a workspace-unique label (3-50 chars, lowercase + hyphens) that you can show to the user; it is NOT part of the receive URL. Use this when the user asks to "set up a webhook", "give me a URL to receive events", or "let me ingest events from <vendor>". |
| `GET` | `/v1/webhook-endpoints` | List every active webhook endpoint in the workspace. Returns an array of { id, name, description, isActive, createdAt, updatedAt }. Use the `id` from any item as `endpointId` for agntdata_webhooks_get_endpoint, agntdata_webhooks_delete_endpoint, or agntdata_webhooks_list_deliveries. Use this to discover existing endpoints before creating a new one or to show the user their current webhook configuration. |
| `GET` | `/v1/webhook-endpoints/{id}` | Get full details of a single webhook endpoint by id. Returns { id, name, description, isActive, createdAt, updatedAt }. Use this when you have an endpoint id (e.g. from agntdata_webhooks_list_endpoints) and need its full record. Note: this does NOT return the receive URL — reconstruct it as https://api.agntdata.dev/webhooks/ingest/{id} if you need to show it again. |
| `DELETE` | `/v1/webhook-endpoints/{id}` | Soft-delete (deactivate) a webhook endpoint by id. After deletion the receive URL https://api.agntdata.dev/webhooks/ingest/{id} stops accepting POSTs (returns 404). Existing delivery history is retained and still queryable. Use this when the user wants to stop receiving events on an endpoint or rotate to a new one. ALWAYS confirm with the user before deleting — third parties posting to the URL will start failing immediately. |
| `GET` | `/v1/webhook-endpoints/deliveries` | Fetch the most recent webhook deliveries for the workspace, newest first. This is THE tool to use to "check for new webhook events", "process incoming webhooks", or "see what a third party sent". Returns { deliveries: [{ id, webhookEndpointId, rawPayload, headers, sourceIp, acknowledgedAt, createdAt }], nextCursor }. `rawPayload` is the exact JSON body the third party POSTed to https://api.agntdata.dev/webhooks/ingest/<id> — parse it the way that vendor documents (e.g. for Stripe inspect `type` and `data.object`). Workflow: (1) call this with `unacknowledged: true` to get only un-processed deliveries, (2) handle each `rawPayload`, (3) call agntdata_webhooks_ack_delivery (or agntdata_webhooks_ack_deliveries for batch) with the delivery `id`s so they don't come back next poll. If `nextCursor` is non-null, pass it as `cursor` on the next call to page through older deliveries. |
| `POST` | `/v1/webhook-endpoints/deliveries/{id}/ack` | Acknowledge (mark as processed) a single webhook delivery by id. Call this AFTER you have successfully handled the `rawPayload` so the same event isn't returned on the next poll of agntdata_webhooks_list_deliveries with `unacknowledged: true`. Idempotent — re-acknowledging an already-acked delivery is a no-op. Use agntdata_webhooks_ack_deliveries instead if you need to ack more than one at a time. |
| `POST` | `/v1/webhook-endpoints/deliveries/ack` | Acknowledge (mark as processed) many webhook deliveries in a single call. Pass an array of delivery ids in `ids`. This is the preferred form when batch-processing the result of agntdata_webhooks_list_deliveries — collect every id from the page after handling, then ack them all at once. Idempotent. |

### Webhook Tool Schemas

```json
[
  {
    "name": "agntdata_webhooks_create_endpoint",
    "description": "Create a new agntdata webhook endpoint. Returns { id, name, url } where `url` is a public HTTPS endpoint of the form https://api.agntdata.dev/webhooks/ingest/<id>. Give that URL to a third party (Stripe, Calendly, GitHub, your own service, etc.) so they can POST events to it. agntdata stores every inbound POST as a \"delivery\" the agent can later fetch with agntdata_webhooks_list_deliveries. The `name` is a workspace-unique label (3-50 chars, lowercase + hyphens) that you can show to the user; it is NOT part of the receive URL. Use this when the user asks to \"set up a webhook\", \"give me a URL to receive events\", or \"let me ingest events from <vendor>\".",
    "method": "POST",
    "path": "/v1/webhook-endpoints",
    "parameters": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "Workspace-unique label for the endpoint, 3-50 chars, lowercase alphanumeric with hyphens (e.g. \"stripe-prod\", \"calendly-bookings\"). Shown in the dashboard; not part of the receive URL."
        },
        "description": {
          "type": "string",
          "description": "Optional human-readable description of what this endpoint receives (e.g. \"Stripe checkout.session.completed events for production\")."
        }
      },
      "required": [
        "name"
      ]
    }
  },
  {
    "name": "agntdata_webhooks_list_endpoints",
    "description": "List every active webhook endpoint in the workspace. Returns an array of { id, name, description, isActive, createdAt, updatedAt }. Use the `id` from any item as `endpointId` for agntdata_webhooks_get_endpoint, agntdata_webhooks_delete_endpoint, or agntdata_webhooks_list_deliveries. Use this to discover existing endpoints before creating a new one or to show the user their current webhook configuration.",
    "method": "GET",
    "path": "/v1/webhook-endpoints",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "agntdata_webhooks_get_endpoint",
    "description": "Get full details of a single webhook endpoint by id. Returns { id, name, description, isActive, createdAt, updatedAt }. Use this when you have an endpoint id (e.g. from agntdata_webhooks_list_endpoints) and need its full record. Note: this does NOT return the receive URL — reconstruct it as https://api.agntdata.dev/webhooks/ingest/{id} if you need to show it again.",
    "method": "GET",
    "path": "/v1/webhook-endpoints/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "UUID of the webhook endpoint. Required path parameter; substituted into the URL."
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "agntdata_webhooks_delete_endpoint",
    "description": "Soft-delete (deactivate) a webhook endpoint by id. After deletion the receive URL https://api.agntdata.dev/webhooks/ingest/{id} stops accepting POSTs (returns 404). Existing delivery history is retained and still queryable. Use this when the user wants to stop receiving events on an endpoint or rotate to a new one. ALWAYS confirm with the user before deleting — third parties posting to the URL will start failing immediately.",
    "method": "DELETE",
    "path": "/v1/webhook-endpoints/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "UUID of the webhook endpoint to deactivate. Required path parameter; substituted into the URL."
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "agntdata_webhooks_list_deliveries",
    "description": "Fetch the most recent webhook deliveries for the workspace, newest first. This is THE tool to use to \"check for new webhook events\", \"process incoming webhooks\", or \"see what a third party sent\". Returns { deliveries: [{ id, webhookEndpointId, rawPayload, headers, sourceIp, acknowledgedAt, createdAt }], nextCursor }. `rawPayload` is the exact JSON body the third party POSTed to https://api.agntdata.dev/webhooks/ingest/<id> — parse it the way that vendor documents (e.g. for Stripe inspect `type` and `data.object`). Workflow: (1) call this with `unacknowledged: true` to get only un-processed deliveries, (2) handle each `rawPayload`, (3) call agntdata_webhooks_ack_delivery (or agntdata_webhooks_ack_deliveries for batch) with the delivery `id`s so they don't come back next poll. If `nextCursor` is non-null, pass it as `cursor` on the next call to page through older deliveries.",
    "method": "GET",
    "path": "/v1/webhook-endpoints/deliveries",
    "parameters": {
      "type": "object",
      "properties": {
        "endpointId": {
          "type": "string",
          "description": "Optional. Filter to deliveries for a single webhook endpoint (UUID from agntdata_webhooks_list_endpoints). Omit to query across all endpoints in the workspace."
        },
        "unacknowledged": {
          "type": "boolean",
          "description": "If true, return only deliveries with `acknowledgedAt: null`. This is the right value when an agent is polling for new work. Defaults to false (returns all deliveries regardless of ack state)."
        },
        "limit": {
          "type": "integer",
          "description": "Max deliveries to return per page (1-100, default 50)."
        },
        "cursor": {
          "type": "string",
          "description": "Opaque pagination cursor from a previous response's `nextCursor`. Pass to fetch the next page of older deliveries. Omit on the first call."
        }
      }
    }
  },
  {
    "name": "agntdata_webhooks_ack_delivery",
    "description": "Acknowledge (mark as processed) a single webhook delivery by id. Call this AFTER you have successfully handled the `rawPayload` so the same event isn't returned on the next poll of agntdata_webhooks_list_deliveries with `unacknowledged: true`. Idempotent — re-acknowledging an already-acked delivery is a no-op. Use agntdata_webhooks_ack_deliveries instead if you need to ack more than one at a time.",
    "method": "POST",
    "path": "/v1/webhook-endpoints/deliveries/{id}/ack",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "UUID of the delivery to acknowledge. Required path parameter; substituted into the URL."
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "agntdata_webhooks_ack_deliveries",
    "description": "Acknowledge (mark as processed) many webhook deliveries in a single call. Pass an array of delivery ids in `ids`. This is the preferred form when batch-processing the result of agntdata_webhooks_list_deliveries — collect every id from the page after handling, then ack them all at once. Idempotent.",
    "method": "POST",
    "path": "/v1/webhook-endpoints/deliveries/ack",
    "parameters": {
      "type": "object",
      "properties": {
        "ids": {
          "type": "array",
          "description": "Non-empty array of webhook delivery UUIDs to acknowledge."
        }
      },
      "required": [
        "ids"
      ]
    }
  }
]
```

### Examples

Create an endpoint:

```bash
curl -X POST https://api.agntdata.dev/v1/webhook-endpoints \
  -H "Authorization: Bearer $AGNTDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "stripe-prod", "description": "Stripe events for production"}'
# => { "success": true, "data": { "id": "…", "name": "stripe-prod", "url": "https://api.agntdata.dev/webhooks/ingest/…" } }
```

Poll for new deliveries on that endpoint:

```bash
curl "https://api.agntdata.dev/v1/webhook-endpoints/deliveries?unacknowledged=true&endpointId=$ENDPOINT_ID&limit=50" \
  -H "Authorization: Bearer $AGNTDATA_API_KEY"
```

Acknowledge a batch after processing:

```bash
curl -X POST https://api.agntdata.dev/v1/webhook-endpoints/deliveries/ack \
  -H "Authorization: Bearer $AGNTDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ids": ["delivery-uuid-1", "delivery-uuid-2"]}'
```

### Rules of Thumb for Agents

- **Don't create a new endpoint per run.** Endpoints are persistent infrastructure — list existing ones first (`agntdata_webhooks_list_endpoints`) and reuse the right one. Only create when none matches the user's intent.
- **Always confirm before deleting.** Deletion stops accepting POSTs immediately; the third party will start failing.
- **Always acknowledge after successful processing.** Otherwise the same delivery will be re-returned on every poll with `unacknowledged: true`.
- **The receive URL is a secret.** Don't log it, don't echo it back unnecessarily, don't share it across users.

## Per-Platform Plugins

Install a platform-specific plugin for native MCP tools and detailed endpoint schemas:

- Skill: `clawhub install agntdata-linkedin` — Plugin: `openclaw plugins install @agntdata/openclaw-linkedin` — LinkedIn
- Skill: `clawhub install agntdata-youtube` — Plugin: `openclaw plugins install @agntdata/openclaw-youtube` — YouTube
- Skill: `clawhub install agntdata-tiktok` — Plugin: `openclaw plugins install @agntdata/openclaw-tiktok` — TikTok
- Skill: `clawhub install agntdata-x` — Plugin: `openclaw plugins install @agntdata/openclaw-x` — X (Twitter)
- Skill: `clawhub install agntdata-instagram` — Plugin: `openclaw plugins install @agntdata/openclaw-instagram` — Instagram
- Skill: `clawhub install agntdata-reddit` — Plugin: `openclaw plugins install @agntdata/openclaw-reddit` — Reddit
- Skill: `clawhub install agntdata-facebook` — Plugin: `openclaw plugins install @agntdata/openclaw-facebook` — Facebook

## Links

- [Dashboard](https://app.agntdata.dev/dashboard)
- [Documentation](https://agnt.mintlify.app)
- [ClawHub skill](https://clawhub.ai/agntdata/agnt-data)
