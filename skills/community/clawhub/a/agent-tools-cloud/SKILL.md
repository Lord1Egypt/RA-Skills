---
name: agent-tools
description: Discover agent-callable resources via the agent-tools.cloud directory — x402 paid services (pay-per-call USDC on Base), MCP servers (tools/context), and A2A agents (task delegation). Use when the user wants to find an on-demand paid API, an MCP tool server, or a peer agent to hand a task to. Tools - `search(intent)` finds x402 paid services, `search_mcp_servers(intent)` finds MCP servers, `search_agents(intent)` finds A2A agents, `search_all(intent)` searches all three at once, and the matching `get*(slug)` returns the full call template.
metadata: {"openclaw": {"emoji": "🛒", "homepage": "https://agent-tools.cloud", "requires": {"bins": ["uvx"]}, "install": [{"id": "uv", "kind": "uv", "package": "agent-tools-mcp", "bins": ["agent-tools-mcp"], "label": "Install via uv (recommended)"}, {"id": "pip", "kind": "pip", "package": "agent-tools-mcp", "bins": ["agent-tools-mcp"], "label": "Install via pip"}]}}
---

# agent-tools

Discovery layer for the **agent economy**. Lets an agent find an agent-callable
resource by intent, read its full call template, and use it.

Backed by [agent-tools.cloud](https://agent-tools.cloud), an open directory that
indexes **three** kinds of resources:

| Resource | What it solves | Typical object |
|---|---|---|
| **x402 service** | pay-per-call HTTP API (USDC on Base) | `/.well-known/x402`, 402 endpoint |
| **MCP server** | external tools & context via MCP | Streamable-HTTP / stdio MCP servers |
| **A2A agent** | delegate a task to another agent | `/.well-known/agent-card.json`, A2A JSON-RPC |

> A2A tells agents *who* can do the job. x402 lets them *pay* for it. MCP gives them the *tools* to do it.

Sources include `awesome-x402`, `x402scan`, `x402.org/ecosystem`, the MCP
registry / PulseMCP, and public A2A agent-cards, plus a handful of self-hosted
services on the same host.

## When to use

Use this skill when the user asks for any of:

- "find an API / MCP server / agent that does X"
- "is there a paid service for Y" / "what x402 services exist"
- "call a token signal / on-chain query / DeFi planner / chat completion"
- "find an MCP server for Z" / "is there an agent I can delegate this to"
- Any task that needs a third-party resource and the user has not pinned a
  specific provider — search first, then decide.

Do **not** use this skill for:

- Free, well-known APIs (CoinGecko, Defillama public). Call those directly.
- The user explicitly named a non-indexed provider (OpenAI, Anthropic, etc.).

## How to use

### 1. Find a resource

The MCP server (installed via the installer specs above) exposes these tools:

| Tool | Purpose |
|---|---|
| `search(intent, top_k?, max_price_usd?, category?)` | Find **x402 paid services** |
| `get(slug)` | Full x402 record (URL, schema, price, x402 bazaar info) |
| `list_categories()` | Browse x402 categories |
| `search_mcp_servers(intent, top_k?, chain?)` | Find **MCP servers** |
| `get_mcp_server(slug)` | Full MCP server record (endpoint, transport, capabilities) |
| `search_agents(intent, top_k?, x402_only?)` | Find **A2A agents** |
| `get_agent(slug)` | Full A2A agent card (endpoint, skills, auth, x402 info) |
| `search_all(intent, protocol?, top_k?)` | **Unified** search across all three; each result tagged with `protocol` |
| `stats()` | Live directory size + health across x402 / MCP / A2A |

If you don't know which resource type fits, start with `search_all`. Otherwise
use the protocol-specific search, pick the highest-ranked result that fits the
budget, then `get*(slug)` for the full call template.

### 2. Read the call template

For x402 services hosted on **agent-tools.cloud**, `get()` includes the full
x402 v2 `extensions.bazaar` block — request body example, JSON Schema, output
example — so the agent can construct a request without trial-and-error.
MCP servers return their endpoint URL + transport; A2A agents return their
agent-card (skills, endpoint, auth). Third-party entries are passed through as
scraped; when in doubt, call the endpoint with an empty body and read the 402
challenge (x402) or fetch the agent-card / MCP `tools/list` for guidance.

### 3. Call + pay (x402 only)

1. POST to the endpoint with no payment header → receive HTTP 402 + `payment-required`
   header (base64-encoded x402 v2 challenge).
2. Decode, sign with a Base-mainnet USDC wallet, attach as `X-Payment` header.
3. Re-POST → receive 200 + the actual response.

Use any x402-compatible payment lib (`x402-axios`, `x402-fetch`, the Python
`x402.payment` helpers, …) to handle steps 1–3. MCP servers and A2A agents are
connected/called via their own protocol, not x402 (unless flagged x402-capable).

## Configuration

Set in `~/.openclaw/openclaw.json` (optional):

```json
{
  "skills": {
    "entries": {
      "agent-tools": {
        "enabled": true,
        "env": {
          "AGENT_TOOLS_API_BASE": "https://agent-tools.cloud"
        }
      }
    }
  }
}
```

`AGENT_TOOLS_API_BASE` lets you point at a self-hosted directory if you ever
deploy your own.

## Cost

The directory itself is **free** (all `search*`, `get*`, `list_categories`,
`stats` are unauthenticated, no rate limit announced). Only the underlying paid
x402 services charge — typically $0.001–$0.50 per call. MCP servers and A2A
agents have their own pricing (many are free).

## Safety

- The skill never auto-pays. It only **discovers** and returns call templates.
  The agent / user is in full control of which 402 challenge to actually settle.
- Always show `price_usd` to the user before paying.
- Cap `max_price_usd` in `search()` if the user mentioned a budget.

## Related

- Project home: <https://agent-tools.cloud>
- Source: <https://github.com/AgentTools-Cloud/AgentToolsCollection>
- PyPI: <https://pypi.org/project/agent-tools-mcp/>
- x402 spec: <https://x402.org>
- MCP spec: <https://modelcontextprotocol.io>
- A2A spec: <https://a2a.dev>
