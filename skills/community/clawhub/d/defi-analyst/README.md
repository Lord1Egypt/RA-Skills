# DeFi Analyst Skill

Research DeFi protocols, track yields, analyze TVL trends, and monitor the competitive landscape using Tavily MCP, GeckoTerminal API, and DeFiLlama.

## Install

```bash
# Clone the repo
git clone https://github.com/0x-wzw/defi-analyst.git ~/.openclaw/skills/defi-analyst

# Or install via ClawHub (when published)
clawhub install defi-analyst
```

## Configure

### Tavily MCP (required)

```bash
export TAVILY_API_KEY="tvlY-dev-4WhK0Z-GBC7w91QlmfFozImB6ZG7hU6gCaUai2fQStmwlL5rk"
mcporter config add tavily "https://mcp.tavily.com/mcp/?tavilyApiKey=$TAVILY_API_KEY"
```

Get a free API key at [tavily.io](https://tavily.io) if you need a different one.

### Optional: jq for JSON parsing

```bash
sudo apt install jq  # Debian/Ubuntu
brew install jq     # macOS
```

## Quick Start

```bash
# Research a protocol
curl -s "https://api.llama.fi/protocol/aave" | jq '{name, tvl, change_1d, change_7d}'

# Search for recent news
mcporter call tavily.tavily_search query="Aave V3 audit exploit update 2026" max_results=5

# Get trending pools
curl -s "https://api.geckoterminal.com/api/v2/networks/eth/pools" | jq '.[0:5]'
```

## Skills

This skill is part of the 0x-wzw agent swarm. Related skills:

- **[swarm-workflow-protocol](https://github.com/0x-wzw/swarm-workflow-protocol)** — Multi-agent orchestration
- **[agent-identity](https://github.com/0x-wzw/agent-identity)** — ERC-8004 agent identity
- **[x-interact](https://github.com/0x-wzw/x-interact)** — X.com via Tavily
- **[moltbook-interact](https://github.com/0x-wzw/moltbook-interact)** — Moltbook social

## License

MIT
