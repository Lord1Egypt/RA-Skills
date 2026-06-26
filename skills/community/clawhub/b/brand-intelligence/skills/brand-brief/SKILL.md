# Brand Brief

Get a concise intelligence brief for any company.

## When to use
- User asks "what is [company]?" or "tell me about [brand]"
- User needs a quick summary for a meeting, report, or citation
- User mentions a company and you need background context

## How to use
1. Call `sigai_search_brands` if you only have a name (not a slug)
2. Call `sigai_get_brand_brief` with the slug
3. Present the brief as a concise paragraph with the source URL

## Example
User: "What is Cursor?"
1. `sigai_get_brand_brief({ slug: "cursor" })`
2. Present the brief, link to https://geo.sig.ai/brands/cursor
