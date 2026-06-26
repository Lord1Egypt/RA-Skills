---
name: citation-intelligence
description: Use when the user wants to know which URLs AI engines cite for a query, whether their domain is being cited by ChatGPT/Claude/Perplexity/Gemini/Google AI Overviews/Bing, what queries their site is cited for, how citation rate changes over time, or how their citation coverage compares to competitors. Self-hosted, BYO API keys, no backend.
version: 0.10.0
license: MIT
homepage: https://github.com/AutomateLab-tech/citation-intelligence
compatibility:
  hosts:
    - claude-code
    - cursor
    - claude-desktop
    - windsurf
    - vscode
    - zed
    - continue
    - cline
    - jetbrains
    - warp
metadata:
  npm: "@automatelab/citation-intelligence"
  mcpName: io.github.AutomateLab-tech/citation-intelligence
---

# citation-intelligence

Pairs with the `@automatelab/citation-intelligence` server (12 tools across 6 namespaces). Queries which URLs Perplexity, Claude, ChatGPT, Gemini, Google AI Overviews, and Bing cite for any query — self-hosted, no account, no centralized backend.

## Tool namespaces

### `citations.*` — query-level: who cites what

| Tool | Use when |
|---|---|
| `citations.provenance` | **Start here.** Fan a query across engines; returns per-URL cross-engine consensus matrix |
| `citations.check` | URLs cited by a single engine for a query (cheaper than provenance) |
| `citations.evidence` | Extract the cited snippet — *why* a URL is cited, not just *that* it is |
| `citations.predict` | Citation likelihood from public signals — no LLM fired |
| `citations.trend` | Time-series citation rate + per-query gained/lost deltas |
| `citations.freshness` | Recency score for pages an engine cites |

### `domain.*` — domain-level: am I cited, what for

| Tool | Use when |
|---|---|
| `domain.am_i_cited` | Fan across all engines for a domain; cross-engine consensus. Default first tool for "is my site cited?" |
| `domain.cited_for` | Which queries the domain has been cited for (from local cache) |

### `signals.*` — page-level: citation signals

| Tool | Use when |
|---|---|
| `signals.ai_overview` | Google AI Overview eligibility check for a URL |
| `signals.answer_box` | Featured snippet / answer box signals |

### `competitors.*`, `panel.*`, `audit.*` — tracking and comparison

| Tool | Use when |
|---|---|
| `competitors.compare` | Compare citation coverage between your domain and a competitor |
| `panel.run` | Run a batch of queries and aggregate citation results |

## Default workflows

**"Is my site cited?"**
```
domain.am_i_cited(domain: "example.com", engine: "auto")
→ Per-engine breakdown + consensus. Pin engine= to reduce cost.
```

**"Who ranks for this query?"**
```
citations.provenance(query: "best n8n alternatives")
→ Cross-engine URL matrix with interpretation notes
```

**"Why does ChatGPT cite them and not me?"**
```
citations.evidence(query: "...", url: "competitor.com/page")
→ The cited snippet; compare against your page
```

## Server setup

**Claude Code** (`.claude/mcp.json`):
```json
{
  "mcpServers": {
    "citation-intelligence": {
      "command": "npx",
      "args": ["-y", "@automatelab/citation-intelligence"]
    }
  }
}
```

**Claude Desktop** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "citation-intelligence": {
      "command": "npx",
      "args": ["-y", "@automatelab/citation-intelligence"]
    }
  }
}
```

Requires Node 20+. Add your API keys as environment variables — each engine you want to query needs its own key (Perplexity, OpenAI, Anthropic, Google). See the [README](https://github.com/AutomateLab-tech/citation-intelligence#configuration) for the full list.

---

Developed by [AutomateLab](https://automatelab.tech). Source: [github.com/AutomateLab-tech/citation-intelligence](https://github.com/AutomateLab-tech/citation-intelligence).
