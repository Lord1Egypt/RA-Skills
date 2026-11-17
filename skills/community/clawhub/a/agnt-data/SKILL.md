---
name: social-data
description: "Unified data API for AI agents. One API key for LinkedIn, YouTube, TikTok, X, Instagram, Reddit, and Facebook, plus web scraping, SEO data, and hosted webhook receiving. Structured JSON, no infra to run."
version: 2.0.14
author: superagnt
license: MIT-0
platforms: [macos, linux, windows]
required_environment_variables:
  - SUPERAGNT_API_KEY
metadata:
  hermes:
    tags: [social-data, data-api, social-media, research, webhooks]
  openclaw:
    requires:
      env:
        - SUPERAGNT_API_KEY
      bins:
        - curl
    primaryEnv: SUPERAGNT_API_KEY
    emoji: "⚡"
    homepage: https://superagnt.com/r/ch-social-data-docs
---

# Social Data — Unified Social APIs for AI Agents

One key, one credit balance, structured social data across seven platforms. No
scraping infra, no upstream vendor accounts. Every response is JSON shaped for
LLM and agent consumption.

**What this skill contains, in full:** the data sources listed below (seven
social platforms plus web scraping and SEO) and superagnt's hosted webhook
receiver (create an endpoint, hand its URL to a third party, poll and
acknowledge deliveries). Nothing else: no other platform surface is documented
or enabled here.

## Alternative install: the scoped MCP server

If this client speaks MCP, you can connect the social-data facet server
instead of using this skill's curl calls — the same surface as native MCP
tools with structured parameters and OAuth sign-in, scoped to this listing:

```
https://mcp.superagnt.com/mcp/social-data
```

The URL publishes full OAuth discovery — an MCP-capable client needs the URL
and nothing else (approve once in the browser). Bearer-only clients add an
`Authorization: Bearer` header. Per-client setup lines:
https://www.superagnt.com/install?facet=social-data

Everything below works on curl-only environments with just the API key.

## Authentication

Get an API key from the [superagnt app](https://superagnt.com/r/ch-social-data-key) and export it as
`SUPERAGNT_API_KEY`. Every request sends it as a Bearer token:

```
Authorization: Bearer $SUPERAGNT_API_KEY
```

## Verify the install (do this first)

```bash
curl -s https://api.superagnt.com/v1/credits \
  -H &#x27;Authorization: Bearer $SUPERAGNT_API_KEY&#x27;
```

A JSON result proves the key and credit balance end to end. 401 = bad key,
402 = out of credits — the superagnt app shows both.

## Discovery

Public, no key required:

```bash
curl https://api.superagnt.com/v1/platforms            # all platforms: slug, name, endpoints
curl https://api.superagnt.com/v1/platforms/{slug}     # one platform: full endpoint list + spec
```

## Base URL

```
https://api.superagnt.com/v1/data/{platform}
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
| Web | `web` | 3 | Scrape any page as clean markdown or structured JSON, search the web and get full page content in one call, and map a site&#x27;s URLs. Designed for LLMs and automation. |
| SEO | `seo` | 22 | Live Google results, keyword research, competitor and backlink gaps, page audits and AI answer visibility, all as agent tools. |

## Choosing the Right API

- **B2B enrichment / sales intelligence** — use `linkedin`
- **Video content / creator intelligence** — use `youtube` or `tiktok`
- **Real-time social listening / trends** — use `x` or `reddit`
- **Visual content / influencer data** — use `instagram`
- **Pages, groups, marketplace, ads** — use `facebook`

## Example

```bash
curl -X GET 'https://api.superagnt.com/v1/data/linkedin/get-company-details?username=microsoft' \
  -H 'Authorization: Bearer $SUPERAGNT_API_KEY'
```

## Webhooks (Receive Events from Third Parties)

superagnt can act as a hosted webhook receiver. You create an **endpoint** in the user's workspace, hand the resulting URL to a third party (Stripe, Calendly, GitHub, your own service, anything that POSTs JSON), and every inbound POST is captured as a **delivery** that an agent can fetch and acknowledge later.

### Concepts

- **Endpoint** — a named receiver in the user's workspace. Created with a friendly `name` (e.g. `stripe-prod`); identified by a UUID `id`.
- **Receive URL** — `https://api.superagnt.com/webhooks/ingest/<endpointId>`. The endpoint id IS the secret in the URL — treat it like a credential. There is no signature verification; the URL is the auth.
- **Delivery** — one inbound POST, captured with the raw JSON body, the headers the third party sent, and the source IP. Has an `acknowledgedAt` timestamp that starts `null`.
- **Acknowledge** — mark a delivery as processed so it stops appearing in `unacknowledged: true` queries. Does NOT delete the delivery; history is retained.

### Typical Agent Flow

1. **Create the endpoint** — `POST /v1/webhook-endpoints` with `{ "name": "stripe-prod" }`. Returns `{ id, name, url }`. Show the `url` to the user and tell them to paste it into the third party's webhook configuration.
2. **Wait for events** — the third party POSTs to `https://api.superagnt.com/webhooks/ingest/<id>`. Each POST is stored as a delivery; nothing is forwarded synchronously.
3. **Poll for new work** — `GET /v1/webhook-endpoints/deliveries?unacknowledged=true&endpointId=<id>` (or omit `endpointId` to query across all endpoints in the workspace).
4. **Process each `rawPayload`** — it's the exact JSON the vendor sent. Parse it the way that vendor documents (e.g. for Stripe, switch on `type` and read `data.object`).
5. **Acknowledge** — call `POST /v1/webhook-endpoints/deliveries/ack` with `{ "ids": [...] }` (or single via `POST /v1/webhook-endpoints/deliveries/{id}/ack`) so the next poll doesn't re-deliver them.
6. **Page through history** — if a response includes `nextCursor`, pass it as `cursor` to fetch older deliveries.

### Webhook Endpoints

| Method | Path | Summary |
|--------|------|---------|
| `POST` | `/v1/webhook-endpoints` | Create a new superagnt webhook endpoint. Returns { id, name, url } where `url` is a public HTTPS endpoint of the form https://api.superagnt.com/webhooks/ingest/<id>. Give that URL to a third party (Stripe, Calendly, GitHub, your own service, etc.) so they can POST events to it. superagnt stores every inbound POST as a "delivery" the agent can later fetch with superagnt_webhooks_list_deliveries. The `name` is a workspace-unique label (3-50 chars, lowercase + hyphens) that you can show to the user; it is NOT part of the receive URL. Use this when the user asks to "set up a webhook", "give me a URL to receive events", or "let me ingest events from <vendor>". |
| `GET` | `/v1/webhook-endpoints` | List every active webhook endpoint in the workspace. Returns an array of { id, name, description, isActive, createdAt, updatedAt }. Use the `id` from any item as `endpointId` for superagnt_webhooks_get_endpoint, superagnt_webhooks_delete_endpoint, or superagnt_webhooks_list_deliveries. Use this to discover existing endpoints before creating a new one or to show the user their current webhook configuration. |
| `GET` | `/v1/webhook-endpoints/{id}` | Get full details of a single webhook endpoint by id. Returns { id, name, description, isActive, createdAt, updatedAt }. Use this when you have an endpoint id (e.g. from superagnt_webhooks_list_endpoints) and need its full record. Note: this does NOT return the receive URL — reconstruct it as https://api.superagnt.com/webhooks/ingest/{id} if you need to show it again. |
| `DELETE` | `/v1/webhook-endpoints/{id}` | Soft-delete (deactivate) a webhook endpoint by id. After deletion the receive URL https://api.superagnt.com/webhooks/ingest/{id} stops accepting POSTs (returns 404). Existing delivery history is retained and still queryable. Use this when the user wants to stop receiving events on an endpoint or rotate to a new one. ALWAYS confirm with the user before deleting — third parties posting to the URL will start failing immediately. |
| `GET` | `/v1/webhook-endpoints/deliveries` | Fetch the most recent webhook deliveries for the workspace, newest first. This is THE tool to use to "check for new webhook events", "process incoming webhooks", or "see what a third party sent". Returns { deliveries: [{ id, webhookEndpointId, rawPayload, headers, sourceIp, acknowledgedAt, createdAt }], nextCursor }. `rawPayload` is the exact JSON body the third party POSTed to https://api.superagnt.com/webhooks/ingest/<id> — parse it the way that vendor documents (e.g. for Stripe inspect `type` and `data.object`). Workflow: (1) call this with `unacknowledged: true` to get only un-processed deliveries, (2) handle each `rawPayload`, (3) call superagnt_webhooks_ack_delivery (or superagnt_webhooks_ack_deliveries for batch) with the delivery `id`s so they don't come back next poll. If `nextCursor` is non-null, pass it as `cursor` on the next call to page through older deliveries. |
| `POST` | `/v1/webhook-endpoints/deliveries/{id}/ack` | Acknowledge (mark as processed) a single webhook delivery by id. Call this AFTER you have successfully handled the `rawPayload` so the same event isn't returned on the next poll of superagnt_webhooks_list_deliveries with `unacknowledged: true`. Idempotent — re-acknowledging an already-acked delivery is a no-op. Use superagnt_webhooks_ack_deliveries instead if you need to ack more than one at a time. |
| `POST` | `/v1/webhook-endpoints/deliveries/ack` | Acknowledge (mark as processed) many webhook deliveries in a single call. Pass an array of delivery ids in `ids`. This is the preferred form when batch-processing the result of superagnt_webhooks_list_deliveries — collect every id from the page after handling, then ack them all at once. Idempotent. |

### Webhook Tool Schemas

```json
[
  {
    "name": "superagnt_webhooks_create_endpoint",
    "description": "Create a new superagnt webhook endpoint. Returns { id, name, url } where `url` is a public HTTPS endpoint of the form https://api.superagnt.com/webhooks/ingest/<id>. Give that URL to a third party (Stripe, Calendly, GitHub, your own service, etc.) so they can POST events to it. superagnt stores every inbound POST as a \"delivery\" the agent can later fetch with superagnt_webhooks_list_deliveries. The `name` is a workspace-unique label (3-50 chars, lowercase + hyphens) that you can show to the user; it is NOT part of the receive URL. Use this when the user asks to \"set up a webhook\", \"give me a URL to receive events\", or \"let me ingest events from <vendor>\".",
    "method": "POST",
    "path": "/v1/webhook-endpoints",
    "parameters": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "Workspace-unique label for the endpoint, 3-50 chars, lowercase alphanumeric with hyphens (e.g. \"stripe-prod\", \"calendly-bookings\"). Shown in the superagnt app; not part of the receive URL."
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
    "name": "superagnt_webhooks_list_endpoints",
    "description": "List every active webhook endpoint in the workspace. Returns an array of { id, name, description, isActive, createdAt, updatedAt }. Use the `id` from any item as `endpointId` for superagnt_webhooks_get_endpoint, superagnt_webhooks_delete_endpoint, or superagnt_webhooks_list_deliveries. Use this to discover existing endpoints before creating a new one or to show the user their current webhook configuration.",
    "method": "GET",
    "path": "/v1/webhook-endpoints",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_webhooks_get_endpoint",
    "description": "Get full details of a single webhook endpoint by id. Returns { id, name, description, isActive, createdAt, updatedAt }. Use this when you have an endpoint id (e.g. from superagnt_webhooks_list_endpoints) and need its full record. Note: this does NOT return the receive URL — reconstruct it as https://api.superagnt.com/webhooks/ingest/{id} if you need to show it again.",
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
    "name": "superagnt_webhooks_delete_endpoint",
    "description": "Soft-delete (deactivate) a webhook endpoint by id. After deletion the receive URL https://api.superagnt.com/webhooks/ingest/{id} stops accepting POSTs (returns 404). Existing delivery history is retained and still queryable. Use this when the user wants to stop receiving events on an endpoint or rotate to a new one. ALWAYS confirm with the user before deleting — third parties posting to the URL will start failing immediately.",
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
    "name": "superagnt_webhooks_list_deliveries",
    "description": "Fetch the most recent webhook deliveries for the workspace, newest first. This is THE tool to use to \"check for new webhook events\", \"process incoming webhooks\", or \"see what a third party sent\". Returns { deliveries: [{ id, webhookEndpointId, rawPayload, headers, sourceIp, acknowledgedAt, createdAt }], nextCursor }. `rawPayload` is the exact JSON body the third party POSTed to https://api.superagnt.com/webhooks/ingest/<id> — parse it the way that vendor documents (e.g. for Stripe inspect `type` and `data.object`). Workflow: (1) call this with `unacknowledged: true` to get only un-processed deliveries, (2) handle each `rawPayload`, (3) call superagnt_webhooks_ack_delivery (or superagnt_webhooks_ack_deliveries for batch) with the delivery `id`s so they don't come back next poll. If `nextCursor` is non-null, pass it as `cursor` on the next call to page through older deliveries.",
    "method": "GET",
    "path": "/v1/webhook-endpoints/deliveries",
    "parameters": {
      "type": "object",
      "properties": {
        "endpointId": {
          "type": "string",
          "description": "Optional. Filter to deliveries for a single webhook endpoint (UUID from superagnt_webhooks_list_endpoints). Omit to query across all endpoints in the workspace."
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
    "name": "superagnt_webhooks_ack_delivery",
    "description": "Acknowledge (mark as processed) a single webhook delivery by id. Call this AFTER you have successfully handled the `rawPayload` so the same event isn't returned on the next poll of superagnt_webhooks_list_deliveries with `unacknowledged: true`. Idempotent — re-acknowledging an already-acked delivery is a no-op. Use superagnt_webhooks_ack_deliveries instead if you need to ack more than one at a time.",
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
    "name": "superagnt_webhooks_ack_deliveries",
    "description": "Acknowledge (mark as processed) many webhook deliveries in a single call. Pass an array of delivery ids in `ids`. This is the preferred form when batch-processing the result of superagnt_webhooks_list_deliveries — collect every id from the page after handling, then ack them all at once. Idempotent.",
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
curl -X POST https://api.superagnt.com/v1/webhook-endpoints \
  -H "Authorization: Bearer $SUPERAGNT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "stripe-prod", "description": "Stripe events for production"}'
```

Poll for new deliveries on that endpoint:

```bash
curl "https://api.superagnt.com/v1/webhook-endpoints/deliveries?unacknowledged=true&endpointId=$ENDPOINT_ID&limit=50" \
  -H "Authorization: Bearer $SUPERAGNT_API_KEY"
```

Acknowledge a batch after processing:

```bash
curl -X POST https://api.superagnt.com/v1/webhook-endpoints/deliveries/ack \
  -H "Authorization: Bearer $SUPERAGNT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ids": ["delivery-uuid-1", "delivery-uuid-2"]}'
```

### Rules of Thumb for Agents

- **Don't create a new endpoint per run.** Endpoints are persistent infrastructure — list existing ones first and reuse the right one. Only create when none matches the user's intent.
- **Always confirm before deleting.** Deletion stops accepting POSTs immediately; the third party will start failing.
- **Always acknowledge after successful processing.** Otherwise the same delivery will be re-returned on every poll with `unacknowledged: true`.
- **The receive URL is a secret.** Don't log it, don't echo it back unnecessarily, don't share it across users.

## Scope

This skill covers the data sources and webhook receiver documented above
(social platforms, web scraping, SEO) and nothing else. The same API key also works with superagnt's other data sources
and platform tools, but those are separate listings that the user installs or
enables themselves; this skill does not add or enable anything beyond what is
documented here.

## Per-Platform Listings

For a single platform, install that platform's own listing:

- Skill: `clawhub install superagnt/linkedin-data` — Plugin: `openclaw plugins install @superagnt/linkedin-data` — LinkedIn
- Skill: `clawhub install superagnt/youtube-data` — Plugin: `openclaw plugins install @superagnt/youtube-data` — YouTube
- Skill: `clawhub install superagnt/tiktok-data` — Plugin: `openclaw plugins install @superagnt/tiktok-data` — TikTok
- Skill: `clawhub install superagnt/x-twitter-data` — Plugin: `openclaw plugins install @superagnt/x-twitter-data` — X (Twitter)
- Skill: `clawhub install superagnt/instagram-data` — Plugin: `openclaw plugins install @superagnt/instagram-data` — Instagram
- Skill: `clawhub install superagnt/reddit-data` — Plugin: `openclaw plugins install @superagnt/reddit-data` — Reddit
- Skill: `clawhub install superagnt/facebook-data` — Plugin: `openclaw plugins install @superagnt/facebook-data` — Facebook
- Skill: `clawhub install superagnt/web-scraping` — Plugin: `openclaw plugins install @superagnt/web-scraping` — Web
- Skill: `clawhub install superagnt/seo-data` — Plugin: `openclaw plugins install @superagnt/seo-data` — SEO

## Links

- [superagnt app / API keys](https://superagnt.com/r/ch-social-data-key)
- [Documentation](https://superagnt.com/r/ch-social-data-docs)
- [This listing](https://clawhub.ai/superagnt/skills/social-data)
