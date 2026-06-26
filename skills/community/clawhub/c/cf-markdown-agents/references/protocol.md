# Markdown for Agents Protocol

## Overview

Markdown for Agents is Cloudflare's content negotiation feature that automatically converts HTML pages to Markdown format when requested by AI agents and crawlers.

## How It Works

### Content Negotiation

The client sends an `Accept` header indicating preference for Markdown:

```
Accept: text/markdown, text/html
```

Cloudflare's network:
1. Detects the `text/markdown` preference
2. Fetches the original HTML from origin
3. Converts HTML to Markdown in real-time
4. Returns Markdown with appropriate headers

### Request Headers

| Header | Value | Description |
|--------|-------|-------------|
| `Accept` | `text/markdown, text/html` | Request Markdown, fallback to HTML |
| `Accept` | `text/markdown` | Request Markdown only |
| `Accept` | `text/markdown, text/html;q=0.9` | Prefer Markdown, lower priority for HTML |

### Response Headers

| Header | Example | Description |
|--------|---------|-------------|
| `content-type` | `text/markdown; charset=utf-8` | Content is Markdown |
| `x-markdown-tokens` | `725` | Estimated token count |
| `content-signal` | `ai-train=yes, search=yes, ai-input=yes` | Usage permissions |
| `vary` | `accept` | Response varies by Accept header |

## Content Signals

The `Content-Signal` header indicates how the content can be used:

- `ai-train=yes` - Can be used for AI training
- `search=yes` - Can be used for search indexing
- `ai-input=yes` - Can be used as AI input (including agents)

Future versions will support custom content signal policies.

## Token Savings

Markdown for Agents significantly reduces token usage:

| Example | HTML Tokens | Markdown Tokens | Reduction |
|---------|-------------|-----------------|-----------|
| Cloudflare blog post | 16,180 | 3,150 | ~80% |
| Typical documentation | ~1,000 | ~200 | ~80% |

HTML elements that consume tokens but add no semantic value are removed:
- `<div>` wrappers
- Navigation bars
- Script tags
- Style attributes
- CSS classes

## Enabling for Your Site

To enable Markdown for Agents on your Cloudflare zone:

1. Log in to [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Select your account and zone
3. Find "Quick Actions"
4. Toggle "Markdown for Agents" to enable

**Availability:** Currently in beta, free for Pro, Business, Enterprise plans and SSL for SaaS customers.

## Alternative Conversion Methods

If your content source doesn't support Markdown for Agents:

### Workers AI AI.toMarkdown()

Supports multiple document types with summarization:

```typescript
import { Ai } from '@cloudflare/ai';

const ai = new Ai(env.AI);
const markdown = await ai.toMarkdown({
  html: htmlContent,
  summary: true  // Optional summarization
});
```

### Browser Rendering API

For dynamic pages requiring browser rendering:

```bash
curl "https://api.cloudflare.com/client/v4/accounts/{account_id}/browser-rendering/markdown" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

## Tracking Usage

Cloudflare Radar provides insights into AI bot traffic:

- Global AI insights: https://radar.cloudflare.com/ai-insights#content-type
- Individual bot pages: https://radar.cloudflare.com/bots/directory/{bot_name}
- API access: Available via Cloudflare API

The `content_type` dimension shows content type distribution for AI agents.

## References

- [Cloudflare Documentation](https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/)
- [Blog Announcement](https://blog.cloudflare.com/markdown-for-agents/)
- [Content Signals Framework](https://contentsignals.org/)
