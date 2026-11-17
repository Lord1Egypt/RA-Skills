---
name: agent-tools
description: Find x402 paid APIs, MCP servers and A2A agents by intent via agent-tools.cloud, and optionally pay-test an x402 service once from your own wallet.
metadata: {"openclaw": {"emoji": "🛒", "homepage": "https://agent-tools.cloud", "requires": {"bins": ["uvx"]}, "install": [{"id": "uv", "kind": "uv", "package": "agent-tools-mcp", "bins": ["agent-tools-mcp"], "label": "Install via uv (recommended)"}, {"id": "pip", "kind": "pip", "package": "agent-tools-mcp", "bins": ["agent-tools-mcp"], "label": "Install via pip"}]}}
---

# agent-tools

Find x402 paid APIs, MCP servers and A2A agents by intent, from the
[agent-tools.cloud](https://agent-tools.cloud) directory.

## When to use

- The user needs a third-party API, MCP server or agent and hasn't named one.
- Not for well-known free APIs or a provider the user already chose.

## Tools

| Tool | Purpose |
|---|---|
| `search(intent, top_k?, max_price_usd?, category?)` | Find x402 paid services |
| `get(slug)` | Full x402 record and call template |
| `list_categories()` | x402 categories |
| `search_mcp_servers(intent, top_k?, chain?)` | Find MCP servers |
| `get_mcp_server(slug)` | Full MCP server record |
| `search_agents(intent, top_k?, x402_only?)` | Find A2A agents |
| `get_agent(slug)` | Full A2A agent card |
| `search_all(intent, protocol?, top_k?)` | Search all three |
| `stats()` | Directory size and health |
| `ask(question, ...)` | Plain-language recommendation |
| `recommend(intent, ...)` | Scored x402 shortlist |
| `prepare_paid_verification(slug, payer)` | Quote a one-off paid test; returns `typed_data` to sign |
| `execute_paid_verification(id, signature)` | Pay once (Base USDC, ≤ $1, straight to the service) and score the result |
| `get_paid_verification(id)` | Read the result |
| `create_api_key(name?)` | Free account key, returned once |
| `directory_stats(view?, topic?, month?, api_key?)` | Daily statistics and monthly reports |

Flow: `search_all` (or a protocol-specific search) → `get*` → call the service
with your own x402 client.

## Configuration

| Env | Purpose |
|---|---|
| `AGENT_TOOLS_API_BASE` | Default `https://agent-tools.cloud` |
| `AGENT_TOOLS_API_KEY` | Needed only for paid-verification tools. Free: `POST https://agent-tools.cloud/api/v1/keys` |

## Cost and safety

Directory tools are free. Tools never pay or sign for you; show the price to
the user before paying any service.

## Links

- Site: <https://agent-tools.cloud>
- Remote MCP: <https://agent-tools.cloud/mcp-discovery/>
- Source: <https://github.com/AgentTools-Cloud/AgentToolsCollection>
- PyPI: <https://pypi.org/project/agent-tools-mcp/>
