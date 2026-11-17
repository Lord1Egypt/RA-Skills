---
name: everysearch
description: "Use EverySearch for current web, news, forum, academic, semantic, page-reading, crawling and cross-check retrieval (17 search tools). Use when a task needs up-to-date sources, cited factual verification, or content from a specific public URL or site."
metadata:
  openclaw:
    homepage: https://everyinfra.com/en/docs?utm_source=clawhub&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=everysearch
    primaryEnv: EVERYINFRA_API_KEY
    requires:
      env:
        - EVERYINFRA_API_KEY
---

# EverySearch

Use the MCP tool `everyinfra_search`. Its live input schema is the source of truth for available
`tool` values and parameters.

- Use the narrowest retrieval mechanism that matches the user's question.
- Use `crosscheck` for a concrete claim such as a current version, price, policy, availability, or
  API behavior. It is designed to compare mechanism-distinct retrieval paths.
- Use page-reading or crawl tools for known URLs instead of searching for the same page again.
- Keep query and result limits proportional to the task. Empty or failed results must not be
  presented as proof that nothing exists.
- Cite the original sources returned by the search result when producing factual conclusions.
- Read the returned `billing` state. Failed or empty calls may be uncharged, but do not infer that
  without the response.

Do not silently replace semantic retrieval with keyword retrieval when result meaning matters.
If the requested tool is not in the current MCP schema, state that it is unavailable.


## Setup in OpenClaw

1. Create an API key at https://everyinfra.com/en/docs?utm_source=clawhub&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=everysearch#quickstart and export it as `EVERYINFRA_API_KEY`. Capability discovery needs no key; paid calls do.
2. Add the remote MCP server once: `openclaw mcp add everyinfra --url https://api.everyinfra.com/mcp --transport streamable-http`, then set its `Authorization: Bearer` header to the key in Settings -> MCP (keep the key out of config literals). Check it with `openclaw mcp doctor everyinfra --probe`.
3. The live MCP tool list is the runtime truth. EveryInfra failed or empty calls are reported in the response `billing` block; read it instead of assuming.
