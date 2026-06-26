---
name: cf-markdown-agents
description: Fetch web content using Cloudflare's Markdown for Agents protocol. Automatically converts HTML to Markdown with 80% token reduction. Use when fetching web pages for AI processing, web scraping, content extraction, or when the user mentions "Markdown for Agents", "cf-markdown", or needs structured web content in Markdown format.
---

# Cloudflare Markdown for Agents

This skill enables fetching web content using Cloudflare's Markdown for Agents protocol, which automatically converts HTML pages to clean, structured Markdown format.

## What is Markdown for Agents?

Cloudflare's Markdown for Agents is a content negotiation feature that:
- Automatically converts HTML to Markdown at the edge
- Reduces token usage by ~80% compared to raw HTML
- Returns clean, structured content perfect for AI processing
- Adds `x-markdown-tokens` header showing estimated token count
- Includes `Content-Signal` headers for AI usage permissions

## Usage

### Basic Fetch

Use the provided script to fetch any URL with Markdown for Agents support:

```bash
scripts/fetch-markdown.sh <URL>
```

Example:
```bash
scripts/fetch-markdown.sh "https://developers.cloudflare.com/agents/"
```

### In Code

TypeScript/JavaScript example:
```typescript
const response = await fetch("https://example.com/page", {
  headers: {
    Accept: "text/markdown, text/html",
  },
});

const tokenCount = response.headers.get("x-markdown-tokens");
const markdown = await response.text();
```

cURL example:
```bash
curl https://example.com/page -H "Accept: text/markdown"
```

## Response Headers

- `content-type: text/markdown; charset=utf-8` - Content is Markdown
- `x-markdown-tokens: <number>` - Estimated token count
- `content-signal: ai-train=yes, search=yes, ai-input=yes` - Usage permissions

## Supported Sites

Any site using Cloudflare with Markdown for Agents enabled:
- Cloudflare Developer Documentation (developers.cloudflare.com)
- Cloudflare Blog (blog.cloudflare.com)
- Any site with the feature enabled in Cloudflare dashboard

## Benefits

| Aspect | HTML | Markdown |
|--------|------|----------|
| Tokens | 16,180 | 3,150 |
| Reduction | - | ~80% |
| Structure | Complex | Clean |
| AI Parsing | Hard | Easy |

## References

- Full protocol details: [references/protocol.md](references/protocol.md)
- API examples: [references/examples.md](references/examples.md)
