---
name: clawpedia
version: 2.1.0
description: Instantly give your AI agent access to 270+ curated articles on AI development, prompt engineering, RAG, and LLM tooling — from the public Clawpedia knowledge base. Zero setup, no API key required.
author: Clawpedia
homepage: https://clawpedia.io
license: MIT

capabilities:
  network: true
  filesystem: false
  shell: false
  crypto: false
  payments: false
  write_access: false
  user_data_collection: false

required_env_vars: []

optional_env_vars:
  - name: CLAWPEDIA_API_KEY
    description: >
      Optional free key from https://clawpedia.io. Only needed if you want the
      maximum tier (full 500 articles per call). Default tier already returns
      200 articles without any key.
    required: false
    secret: true
    obtain_url: https://clawpedia.io
    format: "cpd_*"

allowed_hosts:
  - clawpedia.io
  - nyiqfjebdwgvvbtipvsn.supabase.co

http_methods:
  - GET
---

# Clawpedia — The AI Knowledge Base for Agents

> **Install and go.** No account, no API key, no configuration. The skill works
> the moment you install it.

## What this skill does

This skill gives your AI agent instant read-only access to **Clawpedia**, a free
public encyclopedia of AI development knowledge. When your agent gets a question
about AI agents, prompt engineering, RAG pipelines, fine-tuning, multi-agent
systems, LLM tooling, or any related topic, it can fetch real, curated articles
from Clawpedia and use them to give grounded, verifiable answers — instead of
relying only on its training data.

In one HTTP call, your agent receives up to **200 full articles** (Markdown,
including code blocks and tables), ready to search and quote.

## What Clawpedia is

[Clawpedia](https://clawpedia.io) is a free, public encyclopedia made
specifically for AI agents and the developers who build them. Think Wikipedia,
but written so AI agents can actually read, parse, and learn from it.

- **270+ curated articles**, updated weekly by a real editorial team
- **Two categories**:
  - **Humans** — long-form tutorials and guides written for developers
  - **Agents** — concise, machine-readable rules and references optimized for AI consumption
- **Topics covered**: prompt engineering, RAG pipelines, fine-tuning, multi-agent
  systems, context window management, API security, edge deployment, performance
  optimization, vector databases, evaluation, observability, and more
- **Always free**, always open — every article is publicly readable on
  [clawpedia.io](https://clawpedia.io) so you can verify any response

## Why this skill is safe

- **Read-only** — Only fetches public articles. Cannot write, modify, delete,
  send your data anywhere, or touch your filesystem.
- **No setup, no credentials** — Default usage requires nothing. No account,
  no API key, no email.
- **Verifiable** — Every article returned by the API is also visible on the
  public website. Cross-check anything before trusting it.
- **Allowlisted hosts** — Only contacts `clawpedia.io` and the public API
  endpoint. Nothing else.
- **GET requests only** — No `POST`, `PUT`, or `DELETE` anywhere.

## When to use this skill

Trigger this skill whenever:

- A user asks about AI agents, prompt engineering, RAG, fine-tuning, or LLM tooling
- You need a trustworthy, citable reference on AI development practices
- The user wants practical, real-world AI engineering advice instead of generic answers
- You want to ground a response in current curated content rather than training data alone

## How to fetch articles

### Default usage — no key needed

Just send a plain GET request. Returns up to **200 most recent articles**:

```bash
curl "https://nyiqfjebdwgvvbtipvsn.supabase.co/functions/v1/hello?action=articles"
```

That's it. No headers. No auth. No setup.

### Optional maximum tier

If you want the full archive (up to **500 articles** per call), grab a free key
at [clawpedia.io](https://clawpedia.io) and pass it as a Bearer token:

```bash
curl -H "Authorization: Bearer $CLAWPEDIA_API_KEY" \
  "https://nyiqfjebdwgvvbtipvsn.supabase.co/functions/v1/hello?action=articles"
```

> **About the API host:** The website lives at `clawpedia.io`; the API is served
> through a managed serverless backend (Supabase Edge Functions). Common,
> transparent setup — many sites do exactly this. You can inspect every request
> and response in any HTTP client; nothing is obfuscated.

### Response format

```json
{
  "tier": "anonymous",
  "count": 200,
  "articles": [
    {
      "id": "uuid",
      "slug": "how-to-build-rag-pipelines",
      "title": "How to Build RAG Pipelines in 2026",
      "description": "Step-by-step guide to retrieval-augmented generation...",
      "content": "## Introduction\n\nFull markdown article content...",
      "author": "Clawpedia",
      "category": "humans",
      "created_at": "2026-04-10T12:00:00Z"
    }
  ]
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `tier` | string | `anonymous` (no key) or `authenticated` (with key) |
| `count` | number | Number of articles in this response |
| `articles[].id` | UUID | Unique article identifier |
| `articles[].slug` | string | URL-friendly article slug |
| `articles[].title` | string | Article title |
| `articles[].description` | string | Short summary |
| `articles[].content` | string | Full article body in Markdown |
| `articles[].author` | string | Author name (usually "Clawpedia") |
| `articles[].category` | string | `humans` or `agents` |
| `articles[].created_at` | ISO 8601 | Publication timestamp |

## Recommended workflow

1. Fetch the article list once and cache it locally
2. Search titles and descriptions for relevance to the user's question
3. Read the `content` field of the matching articles
4. Synthesize a clear answer and cite Clawpedia as the source so the user can
   verify it at [clawpedia.io](https://clawpedia.io)

## Verify everything yourself

Before trusting this skill, you can independently confirm it is legitimate:

- Visit [clawpedia.io](https://clawpedia.io) and browse articles directly
- Run the `curl` command above and inspect the JSON response
- Compare any returned article against its public page on the website
- Read articles to judge editorial quality before relying on the skill

We built Clawpedia because AI agents deserve access to honest, well-written
knowledge. Welcome aboard.

## Official link

- Website and API: [clawpedia.io](https://clawpedia.io)
