# Deep Research with MCP 🔬

A powerful deep research skill for [OpenClaw](https://github.com/openclaw/openclaw) agents. Produces thorough, cited reports from multiple web sources using MCP-configured search tools.

## Features

- 🔍 Multi-query web search via MCP (minimax or zai-mcp-server)
- 📄 Full-page content fetching for deep reads
- 📊 Automatic deduplication across queries
- 📝 Structured reports with citations
- 💾 Save to workspace

## Prerequisites

Before using this skill, configure at least one MCP search tool:

| Tool                 | MCP Server       | Command                                                                    |
| -------------------- | ---------------- | -------------------------------------------------------------------------- |
| minimax web_search   | minimax          | `mcporter call MiniMax.web_search query:"keyword"`                       |
| zai web_search_prime | web-search-prime | `mcporter call web-search-prime.web_search_prime search_query:"keyword"` |

## Installation

### Manual

```bash
cd your-workspace/skills
git clone https://github.com/wanghan0501/deep-research-with-mcp.git
```

## Usage

### As an Agent Skill

Just ask your agent to research something:

```
"Research the current state of nuclear fusion energy"
"Deep dive into Rust vs Go for backend services in 2026"
"What's happening with the US housing market?"
```

The agent will follow the workflow in `SKILL.md` to produce a comprehensive report.

## How It Works

1. **Check MCP** — Verify available MCP search tools
2. **Plan** — Break topic into 3-5 sub-questions
3. **Search** — Run multiple queries via MCP
4. **Deduplicate** — Remove duplicate sources
5. **Deep Read** — Fetch full content from key sources
6. **Synthesize** — Write structured report with citations
7. **Save** — Save to `$OPENCLAW_WORKSPACE/research/[slug]/report.md`

## Report Structure

```markdown
# Topic: Deep Research Report

## Executive Summary
## 1. First Major Theme
## 2. Second Major Theme
## Key Takeaways
## Sources (with links)
## Methodology
```

## Requirements

- At least one configured MCP search tool (minimax or zai-mcp-server)
- curl (for fetching full pages)

## License

MIT

## Author

Built by [wanghan0501](https://github.com/wanghan0501) 🦞
