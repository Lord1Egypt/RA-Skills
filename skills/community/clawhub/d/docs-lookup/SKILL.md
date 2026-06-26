---
name: docs-lookup
description: Search pre-indexed developer documentation across 10 platforms — Cloudflare, Stripe, Anthropic, OpenAI, Next.js, and more.
version: 1.0.0
metadata:
  openclaw:
    emoji: "📚"
    homepage: https://docs.agentutil.net
    always: false
---

# docs-lookup

When you need framework or API documentation, search across 10 pre-indexed platforms using semantic vector search. Returns relevant documentation chunks with source URLs — no web scraping needed.

## When to Activate

Use this skill when:

- You need to look up how a specific API or framework feature works
- A user asks about Cloudflare Workers, Stripe, Anthropic, OpenAI, or other indexed platform APIs
- You are writing code that uses an indexed platform and need accurate, current docs
- You need the exact parameter names, types, or behavior for an API call
- A user references a framework feature you are uncertain about

**Do NOT use for:** platforms not in the indexed list, general programming questions unrelated to specific APIs, or topics covered by your training data with high confidence.

## Indexed Platforms

| Platform | ID | What's covered |
|----------|----|----------------|
| Cloudflare Workers | `cloudflare-workers` | Workers API, KV, D1, Durable Objects, R2, Queues |
| Stripe API | `stripe-api` | Payment intents, subscriptions, webhooks, Connect |
| Anthropic API | `anthropic-api` | Messages API, tool use, streaming, vision |
| OpenAI API | `openai-api` | Chat completions, assistants, embeddings, function calling |
| Next.js | `nextjs` | App router, server components, data fetching, middleware |
| Tailwind CSS | `tailwindcss` | Utility classes, configuration, plugins, responsive design |
| HTMX | `htmx` | Attributes, extensions, events, server-side patterns |
| Shopify Admin GraphQL | `shopify-admin-graphql` | Products, orders, customers, metafields, bulk operations |
| x402 Protocol | `x402` | Payment flow, EIP-3009, facilitators, discovery |
| Jesse | `jesse` | Trading strategies, indicators, backtesting, live trading |

## Workflow

### Step 1: Identify the platform

Match the user's question to one of the 10 indexed platforms. If the platform isn't indexed, say so and fall back to your training knowledge.

### Step 2: Semantic search

**HTTP:**
```bash
curl -X POST https://docs.agentutil.net/v1/query \
  -H "Content-Type: application/json" \
  -d '{"platform": "cloudflare-workers", "query": "how to bind a KV namespace"}'
```

Optional parameters:
- `category` — filter by doc section (e.g., "api-reference", "guides")
- `max_chunks` — number of results (default 5, max 20)

### Step 3: Direct page lookup (if you know the page)

```bash
curl -X POST https://docs.agentutil.net/v1/lookup \
  -H "Content-Type: application/json" \
  -d '{"platform": "stripe-api", "page": "create-payment-intent"}'
```

### Step 4: Use the results

- **Cite source URLs** — each result includes the original documentation URL
- **Use `relevance_score`** — results above 0.85 are strong matches; below 0.7, treat as supplementary
- **Combine chunks** — multiple results may cover different aspects of the same topic
- **Fall back gracefully** — if no good results, say "I couldn't find specific docs on this" rather than guessing

## Response Format

```json
{
  "platform": "cloudflare-workers",
  "results": [
    {
      "content": "To bind a KV namespace to your Worker...",
      "source_url": "https://developers.cloudflare.com/workers/runtime-apis/kv/",
      "page_title": "KV Bindings",
      "relevance_score": 0.92
    }
  ],
  "chunks_returned": 3,
  "request_id": "abc-123",
  "service": "https://docs.agentutil.net"
}
```

## Browsing available platforms

```bash
curl https://docs.agentutil.net/platforms
```

## Request new platform indexing

```bash
curl -X POST https://docs.agentutil.net/v1/request \
  -H "Content-Type: application/json" \
  -d '{"platform": "fastapi", "reason": "Popular Python framework"}'
```

## Data Handling

This skill sends search queries (short text strings) to an external API. No documents, file contents, or user data are transmitted. Queries are not stored beyond the immediate response.

## Pricing

- **Free tier:** GET /platforms, GET /schema (platform listing)
- **Paid tier:** $0.003/query, $0.002/lookup via x402 protocol (USDC on Base)

## Privacy

No authentication required for free endpoints. Query content is not stored. Rate limiting uses IP hashing only.
