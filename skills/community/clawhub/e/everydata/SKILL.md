---
name: everydata
description: "Discover and call EveryInfra structured-data capabilities (414 across 90 platforms): TikTok, Instagram, X, YouTube, LinkedIn, Reddit, Amazon, Google results, plus RedNote (Xiaohongshu) and Douyin. Use when the user needs profiles, posts, comments, search results, listings or reviews as structured JSON."
metadata:
  openclaw:
    homepage: https://everyinfra.com/en/docs?utm_source=clawhub&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=everydata
    primaryEnv: EVERYINFRA_API_KEY
    requires:
      env:
        - EVERYINFRA_API_KEY
---

# EveryData

Use the MCP tools `everyinfra_list_capabilities` and `everyinfra_call_api`.

1. Call `everyinfra_list_capabilities` first. Pass `platform` when the platform is already known.
2. Select the exact `platform` and `action` from the returned catalog. Read required parameters,
   optional parameters, `max_limit` and current price. Use availability only when the catalog
   actually returns it; catalog membership alone is not proof that live inventory exists.
3. Put only catalog-declared parameters under `params`. Do not add other fields, and do not guess
   an action name.
4. Call `everyinfra_call_api`. Request the largest useful result within `max_limit` when that avoids
   needless repeated charges.
5. Treat empty, partial and failed results according to the response fields. Report the returned
   `billing` block rather than estimating cost from a stale document.

EveryData returns a normalized and redacted customer contract. Do not promise raw internal output,
internal identifiers, private data, or fields not present in the live capability catalog.

To clean, label or summarize collected records, use EveryAI (`everyinfra_chat`), which is free for
accounts that have topped up. The former data cleanup tools were retired on 2026-10-09.


## Setup in OpenClaw

1. Create an API key at https://everyinfra.com/en/docs?utm_source=clawhub&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=everydata#quickstart and export it as `EVERYINFRA_API_KEY`. Capability discovery needs no key; paid calls do.
2. Add the remote MCP server once: `openclaw mcp add everyinfra --url https://api.everyinfra.com/mcp --transport streamable-http`, then set its `Authorization: Bearer` header to the key in Settings -> MCP (keep the key out of config literals). Check it with `openclaw mcp doctor everyinfra --probe`.
3. The live MCP tool list is the runtime truth. EveryInfra failed or empty calls are reported in the response `billing` block; read it instead of assuming.
