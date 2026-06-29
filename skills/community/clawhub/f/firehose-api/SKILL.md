---
name: firehose-api
description: Firehose monitors the web in real-time — you create rules (Lucene queries), and every crawled page that matches gets delivered via an SSE stream. Use when implementing or discussing API endpoints.
homepage: https://firehose.com
metadata:
    { 'clawdbot': { 'requires': { 'bins': ['curl'], 'env': ['FIREHOSE_MANAGEMENT_KEY', 'FIREHOSE_TAP_TOKEN'] }, 'primaryEnv': 'FIREHOSE_TAP_TOKEN' } }
---

# Firehose API

Firehose monitors the web in real time. You create **rules** (Lucene queries) on a
**tap**, and every crawled page that matches a rule is delivered to that tap over a
Server-Sent Events stream. (URL Watch — tracking a fixed list of pages for changes — is a
separate product; see the docs index at the end.)

This file covers the common Stream API tasks inline so you can act without fetching. For
the full Lucene field semantics, the complete category/type label lists, the validate
contract, URL Watch, and billing, follow the links under **Documentation** at the end —
that section is generated from the live docs, so it never goes stale.

## Authentication

Base URL: `https://api.firehose.com`. Bearer token, two kinds (both issued from the
Firehose dashboard):

- **Management key** (`fhm_` prefix) — create, list, update, and delete taps. Cannot manage rules or stream.
- **Tap token** (`fh_` prefix) — manage the rules on one tap and open its stream.

```
Authorization: Bearer fh_your_tap_token
```

## Endpoints

**Tap management** — management key:

| Method           | Path           | Purpose                                         |
| ---------------- | -------------- | ----------------------------------------------- |
| `GET`            | `/v1/taps`     | List taps; response includes each tap's `token` |
| `POST`           | `/v1/taps`     | Create a tap (returns its token)                |
| `GET PUT DELETE` | `/v1/taps/:id` | Get, rename, or delete a tap                    |

**Rules & streaming** — tap token:

| Method           | Path            | Purpose                                                      |
| ---------------- | --------------- | ------------------------------------------------------------ |
| `GET`            | `/v1/rules`     | List the tap's rules                                         |
| `POST`           | `/v1/rules`     | Create a rule                                                |
| `GET PUT DELETE` | `/v1/rules/:id` | Get, update, or delete a rule                                |
| `POST`           | `/v1/validate`  | Validate a query before saving (`/v1/validate/public`: no auth) |
| `GET`            | `/v1/stream`    | Open the SSE stream of matching pages                        |

## Rules & queries

A rule object has: `value` (Lucene query, required), `tag` (label, optional, ≤255 chars),
`nsfw` (bool, default `false`), and `quality` (bool, default `true` — drops pagination,
tag/category, and stale pages).

Queries use **Lucene ClassicQueryParser**. The default field is `added` (text from inserted
diff chunks). Key fields:

- **Text** (tokenized, case-insensitive): `added`, `removed`, `added_anchor`, `removed_anchor`, `title`
- **Keyword** (exact, case-sensitive): `url`, `domain`, `publish_time`, `page_category`, `page_type`, `language`
- **Number** (range queries): `dr` — Ahrefs Domain Rating 0–100
- **Filter**: `recent:<n>h|<n>d|<n>mo` — only pages published within the window

Operators: `AND` `OR` `NOT`, `"exact phrases"`, and on `url`/`domain` wildcards (`*` `?`)
and regex (`/.../`) — escape `/` as `\/` (and `\\/` in JSON). Example queries:

```
tesla AND language:en
title:tesla AND page_category:"/News" AND recent:24h
domain:techcrunch.com AND NOT url:*\/tag\/*
```

## Streaming (SSE)

`GET /v1/stream` emits four event types: `connected` (open), `update` (a match),
`error`, and `end` (timeout/limit reached — reconnect to continue). An `update`'s `data`
is `{ tap_id, query_id, matched_at, document }`, where `document` carries `url`, `title`,
`publish_time`, `diff.chunks[]` (`{ typ: "ins"|"del", text }`), `page_category[]`,
`page_types[]`, `language`, `domain_rating`, and `markdown`. Null/empty fields are omitted.

## Examples

```bash
# Create a tap (management key) — the response contains the new tap token
curl -s -X POST -H "Authorization: Bearer $FIREHOSE_MANAGEMENT_KEY" \
  -H "Content-Type: application/json" -d '{"name":"Brand Mentions"}' \
  https://api.firehose.com/v1/taps

# Create a rule, then list the tap's rules (tap token)
curl -s -X POST -H "Authorization: Bearer $FIREHOSE_TAP_TOKEN" \
  -H "Content-Type: application/json" -d '{"value":"ahrefs OR semrush","tag":"seo"}' \
  https://api.firehose.com/v1/rules
curl -s -H "Authorization: Bearer $FIREHOSE_TAP_TOKEN" https://api.firehose.com/v1/rules

# Open the match stream (keep the connection open)
curl -N -H "Authorization: Bearer $FIREHOSE_TAP_TOKEN" https://api.firehose.com/v1/stream
```

## Rate limits & errors

`/v1/rules` — 60 requests/min per tap. `/v1/stream` — 30 connections/min per tap. Errors:
`401` invalid/missing token, `403` resource not in your org, `404` not found, `422`
validation error, `429` rate limit exceeded.

## Documentation

The full documentation. Each link is the page's raw Markdown — append `.md` to any page URL. Read the relevant page for anything not covered above.

### Get started

- [Introduction](https://docs.firehose.com/get-started/introduction.md): What Firehose is, who it's for, and how the real-time pipeline turns your rules into a live stream of matching web pages — plus where to go next.
- [Quickstart](https://docs.firehose.com/get-started/quickstart.md): Go from zero to a live stream of matching web pages in about five minutes — get a management key, create a tap, add a rule, then open the stream.
- [Core concepts](https://docs.firehose.com/get-started/core-concepts.md): The objects you work with in Firehose — organizations, taps, rules, matches, keys, and URL Watch — and how each one relates to the others.
- [Stream vs URL Watch](https://docs.firehose.com/get-started/stream-vs-url-watch.md): Firehose monitors the web two ways — Stream matches the whole crawl against your rules, URL Watch tracks a fixed list of pages. Pick the right one.
- [Authentication](https://docs.firehose.com/get-started/authentication.md): How management keys (fhm_) and tap tokens (fh_) differ, what each one authorizes, the API base URL, and how to pass them as a bearer token on requests.

### Stream

- [Stream overview](https://docs.firehose.com/stream/overview.md): The core Firehose product — your rules match every crawled page and matches are delivered over a live SSE stream. When to use it, and how a match is made.
- [Rules & query syntax](https://docs.firehose.com/stream/rules.md): Create, read, update, and delete the queries attached to a tap — and the full query language they're written in.
- [Streaming (SSE)](https://docs.firehose.com/stream/streaming.md): Open the Server-Sent Events connection, pass the right query parameters, handle each event type, and reconnect cleanly without missing matches.
- [Match payload](https://docs.firehose.com/stream/match-payload.md): Every field on an update event and the page document it delivers, with an example payload and the full list of category and type labels to match on.

### URL Watch

- [URL Watch overview](https://docs.firehose.com/url-watch/overview.md): Track a specific list of URLs for changes on a schedule and capture the diff between crawls. When to use URL Watch over the Stream, and how it works.
- [Creating watches](https://docs.firehose.com/url-watch/creating-watches.md): Add a single URL to watch, choose how often it's crawled, preview the render, check its status, and bulk-import many URLs at once from a list.
- [Diffs & crawl history](https://docs.firehose.com/url-watch/diffs-and-history.md): Read what changed between two crawls of a watched URL, including the added and removed content, and work through the recorded crawl history.
- [Quotas & limits](https://docs.firehose.com/url-watch/quotas.md): Monthly check quotas, watched-URL caps, and the fastest crawl frequency allowed on each plan — and how Firehose behaves when a watch hits a limit.

### Dashboard

- [The live feed](https://docs.firehose.com/dashboard/feed.md): Watch matches arrive in real time in the dashboard, review them as they stream in, then save the ones that matter and export your selection for later.
- [Filters & domain lists](https://docs.firehose.com/dashboard/filters.md): Reusable query fragments and domain/URL lists you attach to taps to shape what they match — plus AI query generation.

### Organizations & Access

- [Taps](https://docs.firehose.com/organizations/taps.md): Taps are the API tokens (fh_) that own a set of rules and that you stream from. Why to keep one tap per use case, and how to create and manage them.
- [Management keys](https://docs.firehose.com/organizations/management-keys.md): Organization-scoped credentials (fhm_) for creating and managing taps programmatically — how to create one, what it unlocks, and when to use it.

### Billing

- [Plans & pricing](https://docs.firehose.com/billing/plans.md): The Firehose subscription tiers from Free to Business plus the API-only plan — what each one includes, its quotas, and who it's the right fit for.
- [How billing works](https://docs.firehose.com/billing/how-billing-works.md): How prepaid credit, per-match metering, and monthly grants fit together — what counts as a billable match, what doesn't, and how the quotas relate.

### API reference

- [Management-key endpoints](https://docs.firehose.com/api-reference/management-key-endpoints.md): List, create, fetch, update, and revoke taps over HTTP with an organization management key (fhm_), with the request and response shape for each call.
- [URL Watch endpoints](https://docs.firehose.com/api-reference/url-watch-endpoints.md): List, create, update, and delete URL Watch subscriptions and read their crawl diffs over HTTP, authenticated with an organization management key (fhm_).
- [Tap-token endpoints](https://docs.firehose.com/api-reference/tap-token-endpoints.md): Create, read, update, and delete rules and open the SSE match stream with a tap token (fh_) — endpoint reference, parameters, and the tap's rate limits.
- [Validate a query](https://docs.firehose.com/api-reference/validate.md): Check a Lucene query against query-core before saving it as a rule — validity, diagnostics, and the compiled query, with an unauthenticated public variant for try-it pages.
- [Errors & limits](https://docs.firehose.com/api-reference/errors-and-limits.md): Every HTTP status code the API returns, the per-endpoint and stream rate limits, and the error events the SSE stream sends before it closes.
- [Code examples](https://docs.firehose.com/api-reference/examples.md): End-to-end snippets for taps, rules, streaming, and URL Watch in curl, JavaScript, and Python — copy, paste, and adapt them to your own keys.

### Troubleshooting

- [Why am I not getting matches?](https://docs.firehose.com/troubleshooting/no-matches.md): The usual reasons a stream or feed stays empty — crawl coverage, url: filters, the quality filter, the recency window, a too-strict query, or no credit.
- [Stream disconnects or errors](https://docs.firehose.com/troubleshooting/stream-disconnects.md): Why a stream closes or returns 401, 402, or 429, why it can seem to skip events, and how to recover from each — including after a dropped connection.

### Resources

- [Using Firehose with AI agents](https://docs.firehose.com/resources/ai-agents.md): Feed these docs and the Firehose API to an LLM or coding agent using per-page Markdown, the whole-site llms.txt files, and the installable API skill.

The whole documentation in one file: [llms-full.txt](https://docs.firehose.com/llms-full.txt).
