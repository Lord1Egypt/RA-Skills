---
name: everyinfra
description: "Route a task to the right EveryInfra product and use its MCP or REST contract safely. One API key covers structured data from 90 platforms (TikTok, Instagram, X, YouTube, LinkedIn, Reddit, Amazon, RedNote, Douyin), web search, AI, CAPTCHA, phone numbers, email and proxies. Use when the user mentions EveryInfra or is unsure which product fits."
metadata:
  openclaw:
    homepage: https://everyinfra.com/en/docs?utm_source=clawhub&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=everyinfra
    primaryEnv: EVERYINFRA_API_KEY
    requires:
      env:
        - EVERYINFRA_API_KEY
---

# EveryInfra router

Use the remote `everyinfra` MCP server for capability discovery and the four MCP-enabled product
lines. Use `https://api.everyinfra.com` only for a REST-only product. Never copy the API key into a
prompt, file, command output, log, URL query string, or response; read it from `EVERYINFRA_API_KEY`.

## Route by outcome

- Structured public platform data: EveryData.
- Current web, semantic, academic, forum, page or site retrieval: EverySearch.
- Text completion, extraction, classification, translation or summarization, including cleaning and
  labeling data collected with EveryData: EveryAI, the AI API.
- Captcha or anti-bot challenge solving on a target the user is authorized to access: EverySolve.
- Activation or rental phone number: EveryNumber.
- Transactional email: EveryMail.
- Traffic-billed proxy credentials: EveryProxy.

Do not infer a tool from an old document. MCP tool discovery and the free REST catalogs are the
runtime truth. If the requested product is unavailable, report that state instead of silently
substituting a different mechanism.

## Common workflow

1. Identify the requested outcome and whether it has external side effects or a charge.
2. Use a free discovery tool or catalog before the first paid call.
3. Validate required parameters, limits, solution shape, availability and current price.
4. Invoke the paid operation only when the user's request authorizes that operation.
5. Read returned `billing`, `quota`, status and error fields when present; never infer success,
   availability, or a charge from HTTP 200 or catalog membership alone. If a tool omits billing,
   report that the charge is not observable from that response.
6. Report the useful result, the actual charge state and any remaining external action separately.

EveryInfra uses one account, API key and wallet across product lines, but product-specific scopes
may still deny a call. A scope error is not a reason to broaden or replace the key automatically.

The former data cleanup tools were retired on 2026-10-09; do not look for them. EveryAI
(`everyinfra_chat`) is free for accounts that have topped up, with per-minute limits that follow
cumulative top-ups; an account that has not topped up receives `ai_topup_required`.


## Setup in OpenClaw

1. Create an API key at https://everyinfra.com/en/docs?utm_source=clawhub&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=everyinfra#quickstart and export it as `EVERYINFRA_API_KEY`. Capability discovery needs no key; paid calls do.
2. Add the remote MCP server once: `openclaw mcp add everyinfra --url https://api.everyinfra.com/mcp --transport streamable-http`, then set its `Authorization: Bearer` header to the key in Settings -> MCP (keep the key out of config literals). Check it with `openclaw mcp doctor everyinfra --probe`.
3. The live MCP tool list is the runtime truth. EveryInfra failed or empty calls are reported in the response `billing` block; read it instead of assuming.
