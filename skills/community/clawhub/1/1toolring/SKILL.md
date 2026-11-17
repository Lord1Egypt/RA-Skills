---
name: 1toolring
description: Call live data tools through 1ToolRing (1toolring.com), one key and one prepaid balance for thousands of pay-per-call tools. Use when a task needs live Google search results, keyword search volume and SEO data, Google Maps places, Amazon or other e-commerce product prices, stock, crypto or exchange-rate data, social media data, web page scraping, jobs or weather data, or AI image, video and voice tools, and the agent has no direct vendor account for them.
license: MIT
homepage: https://1toolring.com
metadata:
  author: Khaisa Studio
  version: "1.0.0"
---

# 1ToolRing

1ToolRing puts one API key and one prepaid balance in front of a catalog of thousands of callable tools from third-party providers. Every tool shows its price before it runs, and a failed call is never charged. The flow is always the same: discover a tool by describing the job, inspect it for the input schema and price, then run it.

## 1. Connect

**MCP (preferred).** Remote server, Streamable HTTP:

- URL: `https://mcp.1toolring.com/mcp`
- Server name: `1toolring`
- Auth: OAuth 2.1 sign-in in the browser (dynamic client registration, PKCE). Clients without OAuth send `Authorization: Bearer <API key>`.

```json
{"mcpServers": {"1toolring": {"type": "http", "url": "https://mcp.1toolring.com/mcp"}}}
```

Claude Code: `claude mcp add --transport http 1toolring https://mcp.1toolring.com/mcp`, then `/mcp`, select 1toolring, Authenticate, and the person clicks Allow. Per-client steps for Codex, Cursor, VS Code, Gemini CLI and others: https://1toolring.com/install/

**REST.** Base URL `https://api.1toolring.com`, header `Authorization: Bearer <API key>`.

## 2. Account and key (the person does this)

You cannot create an account or key yourself. The person signs up at https://app.1toolring.com (email, Google or GitHub, open to everyone) and verifies the email. A new verified account gets a one-time Rp10.000 starter balance. API keys are created at https://app.1toolring.com/keys and shown once. Treat a key as a secret: keep it in an environment variable such as `ONETOOLRING_API_KEY`, never echo it back or commit it.

## 3. Find, inspect, run

MCP tools:

| Tool | Use | Cost |
|---|---|---|
| `discover_tools` | Describe the job in plain words, get tool ids, short descriptions and prices | Free |
| `inspect_tool` | Read one tool's input schema, price model and health | Free |
| `run_tool` | Run the tool from the prepaid balance | Per call |
| `get_tool_run` | Poll a slow run started by `run_tool` | Free |

REST equivalents:

- `POST /api/v1/tools/discover` with `{"query": "google search results for a keyword", "limit": 5}`
- `POST /api/v1/tools/inspect` with `{"tool": "<tool id>"}`
- `POST /api/v1/tools/run` with `{"tool": "<tool id>", "input": {"body": {...}}}`. Returns 200 with the result, or 202 with `run_id` for slow tools.
- `GET /api/v1/tools/runs/{run_id}` to poll.
- `GET /api/v1/pricing/tools/search?q=<words>` is public and needs no key, useful to show prices before sign-up.

Always inspect before the first run of a tool: input shapes differ per provider.

## 4. Money

- Prices are per call, per result or per unit, shown as `{"usd", "idr"}`. The most a run can cost is held when it starts and settled to the real cost. The `X-ToolRing-Cost-USD` and `X-ToolRing-Cost-IDR` headers carry the amount actually charged.
- Failed or provider-error runs cost 0.
- Spend small amounts without asking: run it when one call costs Rp1.000 (about $0.05) or less and the whole request stays under Rp5.000 (about $0.30). Ask first when a single run costs more, the request would pass Rp5.000 in total, or it would use more than half of the remaining balance. When done, state the cost once in a few words, for example "Cost Rp96".
- If the balance is too low (402 INSUFFICIENT_BALANCE), tell the person to top up at https://app.1toolring.com/billing (from Rp10.000 by Indonesian bank virtual account or Alfamart/Indomaret, or from $1 by card). Do not retry until they have.

## 5. Errors

Envelope: `{"error": {"code", "message"}}`. Common codes: UNAUTHORIZED / INVALID_API_KEY (401, reconnect or check the key), VALIDATION_ERROR (400, re-read the input schema), INSUFFICIENT_BALANCE (402), RATE_LIMITED (429, back off), TOOL_NOT_FOUND (404, discover again), TOOL_BLOCKED (403, not available right now, nothing charged), RUN_TOO_LARGE (400, split the request), UPSTREAM_ERROR (502/503, try another tool from discover).

## Links

- Tools and prices: https://1toolring.com/tools/
- Docs: https://docs.1toolring.com/overview/
- Full setup text: https://1toolring.com/llms.txt
