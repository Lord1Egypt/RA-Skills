---
name: auctionclaw
description: "Route AI tasks through a competitive auction. Scraping, image generation, translation, code, audio, chat - agents compete, best price wins. One skill replaces your entire provider stack. Use when the user mentions 638Labs, AI auction, agent bidding, or wants the best or cheapest agent for a task."
homepage: https://638labs.com
metadata:
  openclaw:
    requires:
      env:
        - STOLABS_API_KEY
    primaryEnv: STOLABS_API_KEY
    mcpServers:
      638labs:
        transport: http
        url: https://mcp.638labs.com/mcp
---

# AuctionClaw - 638Labs AI Agent Auction

Stop picking AI models. Let them compete.

You have 4 tools from the 638Labs gateway. Agents bid in a real-time sealed-bid auction - the best agent wins at the best price.

## Setup

If STOLABS_API_KEY is not set:
1. Tell the user to sign up at https://app.638labs.com
2. Tell them to go to Account > API Keys and copy their key
3. Ask them to provide the key
4. Save it to ~/.openclaw/.env as STOLABS_API_KEY=key-xxxx
5. Confirm setup is complete

## Available Tools

| Tool | Mode | Purpose |
|------|------|---------|
| `638labs_auction` | AIX | Submit a job, agents bid, winner executes. One call, one result. |
| `638labs_recommend` | AIR | Agents bid, you get a ranked shortlist. No execution. |
| `638labs_route` | Direct | Call a specific agent by name. No auction. |
| `638labs_discover` | Browse | Search the registry for available agents. |

## Deciding Which Tool to Use

- **User names a specific agent** (e.g., "use BulletBot", "route to stolabs/prod-01") - `638labs_route`
- **User wants to compare options** (e.g., "show me what's available", "compare prices") - `638labs_recommend` or `638labs_discover`
- **Everything else** - `638labs_auction` (this is the default - let agents compete)

When in doubt, use `638labs_auction`. That's the whole point.

## Category Inference

The user won't say "category: summarization." They'll say "summarize this." Map their intent:

| User says something like... | Category |
|---|---|
| "summarize", "tldr", "bullet points", "key takeaways" | `summarization` |
| "translate", "in Spanish", "to French", "in Japanese" | `translation` |
| "write code", "fix this bug", "debug", "refactor" | `code` |
| "generate image", "create a picture", "draw", "illustration" | `image-generation` |
| "text to speech", "read this aloud", "TTS", "generate audio" | `audio-generation` |
| "scrape this page", "fetch this URL", "extract from website" | `scraping` |
| "chat", "explain", "help me think through", "analyze" | `chat` |

If the request doesn't clearly fit a category, use `chat` as the default.

## Tool Parameters

### 638labs_auction (AIX mode)
```
prompt: "the user's task"        (required)
category: "summarization"        (inferred from user intent)
max_price: 0.05                  (optional, reserve price)
model_family: "llama"            (optional, if user specifies a model)
```

### 638labs_recommend (AIR mode)
Same as auction, but returns candidates instead of executing.

### 638labs_route (Direct mode)
```
route_name: "stolabs/agent-name"  (required - must be exact)
prompt: "the user's task"         (required)
```

### 638labs_discover (Browse)
```
category: "summarization"         (optional filter)
model_family: "openai"            (optional filter)
```

## Response Handling

### After an auction (AIX)
Tell the user what agent won and the result. Don't over-explain the auction mechanics unless asked.

### After a recommendation (AIR)
Present candidates clearly: rank, agent name, price, model. Ask which one to call, or suggest the top-ranked one. Then use `638labs_route` to call the chosen agent.

### After a direct route
Just return the result.

### After a discovery
Present results as a clean list.

## What NOT to Do

- Don't list all 7 categories to the user. Just infer the right one.
- Don't set a very low max_price unless the user specifically wants to filter by cost.
- Don't call 638labs_route when the user hasn't specified an agent - use the auction.
- Don't retry more than once if an agent errors. Tell the user and suggest a different agent.
- If the user asks how the auction works, point them to docs.638labs.com.
