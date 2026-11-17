---
name: deepseek-web-search
description: Use when you need up-to-date information, current events, or answers beyond your knowledge cutoff and want a synthesized answer with source URLs rather than a raw result list. Server-side web search via DeepSeek's built-in web_search tool (handles Chinese and English web). Not for structured result lists.
license: MIT
compatibility: Node.js 18+; requires network access and a DeepSeek API key (config.json or DEEPSEEK_API_KEY)
metadata:
  author: mingzeng21
  version: "1.0.0"
---

# DeepSeek Web Search

Searches the web server-side via DeepSeek's Responses API `web_search` tool and returns a synthesized answer with the source URLs the model consulted.

## When to Use

- User asks about current events, recent news, or time-sensitive facts.
- You want a ready answer where someone reads pages and summarizes (vs. getting raw results).
- Chinese or English web coverage needed.
- **When NOT to use:** if you need a raw, structured list of search results (titles/URLs/snippets) to extract or analyze yourself, this skill is not the right fit — DeepSeek only returns its synthesis + consulted URLs.

## Usage

Run the bundled script from this skill's directory (where this `SKILL.md` lives):

```bash
node ./search.mjs "<query>" [maxOutputTokens]
```

- `query` (required): The search query or question.
- `maxOutputTokens` (optional): Cap on answer length (default 8000, max 16384).

## Output

Returns a JSON object:

```json
{
  "answer": "Synthesized answer text",
  "sources": ["https://page-the-model-opened.example", "..."],
  "query": "original query",
  "model": "deepseek-v4-flash",
  "usage": { "input_tokens": 0, "output_tokens": 0, "total_tokens": 0 },
  "engine": "deepseek-web-search"
}
```

## Notes

- The model performs multi-round search (search → open pages → re-search) server-side, so calls take **15–70 seconds**. Don't treat a delay as failure; the script allows up to 120s.
- API key comes from `config.json` (next to `search.mjs`) or the `DEEPSEEK_API_KEY` env var. If both are missing, the script reports an error.
- `sources` are the URLs the model opened while researching — a "pages consulted" list, not per-claim citations. Treat the answer as model synthesis; verify critical facts against the sources before trusting them.
- The model may notice and correct false premises in the query (e.g. "2026 Paris Olympics" → Milan-Cortina 2026 Winter Olympics).
- Always cite source URLs when presenting information to the user.
