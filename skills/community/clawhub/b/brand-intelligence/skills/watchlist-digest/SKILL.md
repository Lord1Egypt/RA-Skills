# Watchlist Digest

Get a compact intelligence update for a set of brands you're tracking.

## When to use
- User says "what's happening with my companies?" or "update me on X, Y, Z"
- User has a list of brands they want monitored
- User needs a daily/weekly competitive briefing

## How to use
1. Call `sigai_get_brand_digest({ slugs: ["slug1", "slug2", ...] })`
2. For each brand in the digest, highlight: AI visibility score + trend, key signals, notable edges
3. Summarize: which brands are rising, which are declining, any notable events

## Example
User: "Update me on Cursor, OpenAI, and Anthropic"
1. `sigai_get_brand_digest({ slugs: ["cursor", "openai", "anthropic"] })`
2. Summarize: scores, trends, and key relationships for each
