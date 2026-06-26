---
name: free-web-browser
description: Browse web through OpenClaw web_search and web_fetch with Ollama as search provider, no external API key required. Use when user asks to search web, verify current facts, compare sources, open result pages, summarize articles, or browse live web content cheaply through local or Ollama-backed search instead of paid search APIs or full browser automation.
---

# Free Web Browser

Use `web_search` for discovery, then `web_fetch` for page content.

## Quick workflow

1. Rewrite vague request into concrete search query.
2. Run `web_search` first.
3. Pick 1 to 3 promising URLs.
4. Run `web_fetch` on source pages you actually need.
5. Cross-check important claims across more than one source.
6. Summarize findings with links, caveats, and date sensitivity when relevant.

## Query patterns

Prefer short, specific queries.

- Current fact: `site:docs.openclaw.ai web_search ollama`
- Product compare: `ollama web search brave searxng comparison`
- Official docs first: `site:github.com OR site:docs.openclaw.ai <topic>`
- Recent news: `<topic> 2026`

If first query weak, tighten scope instead of fetching random pages.

## Tool choice

### `web_search`

Use for:

- finding sources
- checking whether topic has changed recently
- locating official docs, repos, blog posts, issues
- getting top candidate URLs before deeper reading

### `web_fetch`

Use for:

- extracting readable page content
- summarizing article, doc, or blog post
- verifying exact wording from source page
- pulling details after search already found target URL

Prefer `extractMode: "markdown"` unless plain text is better for logs or machine-like parsing.

## Quality rules

- Prefer official docs, project repos, vendor docs, standards bodies, and primary sources.
- Do not trust snippets alone for important claims. Fetch source page.
- For time-sensitive topics, say info may change and mention recency.
- When sources disagree, say so plainly.
- Avoid unnecessary fetch spam. Search once, fetch only best pages.

## Ollama-specific guidance

This skill assumes `web_search` is configured to use Ollama-backed search, so no separate search API key is needed.

- Use normal `web_search` tool. Do not shell out to Ollama manually unless debugging config.
- If search fails, suspect provider setup before blaming query.
- If Ollama search returns thin snippets, fetch source pages for substance.
- If current runtime does not expose `web_search`, this skill cannot browse live web.

## Failure handling

- No results: broaden query once, then try official-site search.
- Low-quality results: add site filters or product/version terms.
- Fetch blocked or empty: choose alternate source from search results.
- Ambiguous request: ask one clarifying question only after one good-faith search attempt.

## Output pattern

Default answer shape:

- direct answer first
- 2 to 5 bullets with evidence
- source links
- brief uncertainty note if needed

## Read next

For troubleshooting and example prompts, read `references/ollama-web-browser-notes.md`.
