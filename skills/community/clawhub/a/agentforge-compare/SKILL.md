---
name: agentforge-compare
version: 2.0.0
description: "AI coding tool comparison MCP server -- compare Claude Code vs Cursor vs Windsurf vs Devin vs Copilot side-by-side with feature matrices, pricing breakdowns, and AI-powered recommendations. Use when: (1) user asks 'compare Cursor and Windsurf' or 'which AI coding tool is best', (2) user says 'tell me about Devin' or 'Copilot features', (3) user needs 'recommend an AI tool for my team of 5', (4) user asks 'how much does Cursor cost' or 'calculate AI tool costs', (5) user says 'list AI coding tools' or 'browse by category'. 15+ tools tracked, 7 comparison dimensions. Zero install, sub-100ms on Cloudflare Workers. Free + Pro $9/mo."
read_when:
  - user wants to compare AI coding tools like Cursor, Windsurf, Copilot, Devin, or Claude Code
  - user asks which AI coding assistant is best for their use case or team
  - user needs pricing information or cost calculation for AI development tools
  - user wants a profile or feature breakdown of a specific AI coding tool
  - user asks for AI tool recommendations based on team size, budget, or workflow
metadata:
  openclaw:
    emoji: "\u2694\uFE0F"
    homepage: https://github.com/yedanyagamiai-cmd/openclaw-mcp-servers
    always: false
---

# OpenClaw AgentForge Compare v2.0

**Pick the right AI tool -- 5 tools to compare, profile, recommend, and calculate costs for 15+ AI coding assistants across 7 dimensions.**

## Quick Reference

| You say... | Protocol | Tool | Tier |
|------------|----------|------|------|
| "Compare Cursor vs Windsurf" | BattleCard | `compare_tools` | Free |
| "Tell me about Devin" | DeepProfile | `get_tool_profile` | Free |
| "List AI coding tools" | Arsenal | `list_categories` | Free |
| "Which tool for my team?" | MatchMaker | `get_recommendations` | Pro |
| "How much would Cursor cost us?" | CostRadar | `pricing_calculator` | Pro |

## Quick Start

```json
{
  "openclaw-agentforge": {
    "type": "streamable-http",
    "url": "https://agentforge-compare-mcp.yagami8095.workers.dev/mcp"
  }
}
```

Add to Claude Desktop, Cursor, Windsurf, VS Code, or any MCP-compatible client. Works immediately -- no API key required for Free tier.

## What's New in v2.0

- :crossed_swords: **15+ Tools Tracked** -- Claude Code, Cursor, Windsurf, Devin, GitHub Copilot, Cody, Aider, Continue, Tabnine, Amazon Q, Codeium, JetBrains AI, Replit Agent, and more. Updated weekly.
- :brain: **AI-Powered Recommendations** (Pro) -- Describe your use case, team size, budget, and must-haves. Get ranked recommendations with match scores and migration tips.
- :abacus: **TCO Calculator** (Pro) -- Total cost of ownership factoring team seats, usage patterns, add-ons, and annual vs. monthly billing. Includes per-developer breakdown.
- :bar_chart: **7 Comparison Dimensions** -- Code generation, debugging, refactoring, chat, terminal, multi-file editing, and agent mode.

## Detection Triggers

This skill activates when the user:

| Trigger Phrase | Maps To |
|----------------|---------|
| "compare Claude Code and Cursor" / "Cursor vs Windsurf" | `compare_tools` |
| "which AI coding tool" / "best AI assistant" | `compare_tools` |
| "Devin vs Copilot" / "compare AI tools" | `compare_tools` |
| "tell me about Cursor" / "Windsurf features" | `get_tool_profile` |
| "what is Devin" / "Copilot pricing" | `get_tool_profile` |
| "list AI coding tools" / "browse by category" | `list_categories` |
| "what tools exist" / "AI tool categories" | `list_categories` |
| "recommend an AI tool for" / "which tool for my team" | `get_recommendations` |
| "best tool for startups" / "best for solo dev" | `get_recommendations` |
| "how much does Cursor cost" / "calculate AI tool costs" | `pricing_calculator` |
| "AI tool pricing" / "annual vs monthly" | `pricing_calculator` |

## Named Protocols

### BattleCard Protocol -- Side-by-Side Comparison Engine
Generates structured comparison matrices for 2-5 AI coding tools across 7 dimensions: code generation quality, debugging capabilities, refactoring power, chat interface, terminal integration, multi-file editing, and autonomous agent mode. Each dimension is rated 1-10 with a summary verdict.

### DeepProfile Protocol -- Comprehensive Tool Dossier
Builds a complete profile for any single tool: description, all pricing tiers (free/pro/enterprise), supported AI models, IDE integrations, key features, strengths, weaknesses, best-for scenarios, alternatives, and recent changelog highlights. Think of it as the "Wirecutter review" for AI tools.

### Arsenal Protocol -- Category Browser
Organizes all 15+ tracked tools into categories: IDE-integrated assistants, CLI-based agents, cloud agents, code review tools, and specialized tools (testing, docs, security). Each category includes tool count, top picks, and quick comparison notes.

### MatchMaker Protocol -- AI Recommendation Engine (Pro)
Takes your use case description, team size, monthly budget, must-have features, and preferred IDE, then returns top 3 tools ranked by match score with detailed reasoning, tradeoffs, and migration tips from your current setup.

### CostRadar Protocol -- Total Cost Calculator (Pro)
Computes monthly and annual costs for any tool configuration: team seats, plan tier, estimated usage (requests/day), and add-ons. Returns per-developer cost and automatically compares against alternatives at the same scale.

## Tools (5)

### `compare_tools` -- BattleCard Protocol
Compare 2-5 AI coding tools side-by-side across all dimensions.

**Input:**
- `tools` -- Array of tool names, e.g., `["Claude Code", "Cursor", "Windsurf"]`

**Output:**
- Feature comparison matrix (7 dimensions, rated 1-10)
- Pricing breakdown per tool
- Model support comparison
- IDE compatibility matrix
- Strengths/weaknesses per tool
- Verdict summary with winner per dimension

**Tracked Tools:** Claude Code, Cursor, Windsurf, Devin, GitHub Copilot, Sourcegraph Cody, Aider, Continue, Tabnine, Amazon Q Developer, Codeium, JetBrains AI Assistant, Replit Agent, Sweep, and more.

### `get_tool_profile` -- DeepProfile Protocol
Get a comprehensive profile for any single AI coding tool.

**Input:**
- `tool_name` -- Name of the tool (e.g., `"Cursor"`)

**Output:**
- Description and positioning
- Pricing: free tier, pro tier, enterprise tier with exact prices
- Supported AI models (GPT-4, Claude, etc.)
- IDE integrations
- Key features list
- Strengths and weaknesses
- Best-for scenarios
- Top alternatives
- Recent changelog highlights

### `list_categories` -- Arsenal Protocol
Browse all tracked AI tools organized by category.

**Output:**
- **IDE-Integrated**: Cursor, Windsurf, Copilot, Cody, Tabnine, Codeium, JetBrains AI, Amazon Q
- **CLI-Based**: Claude Code, Aider, Continue
- **Cloud Agents**: Devin, Replit Agent, Sweep
- **Code Review**: Copilot PR Review, CodeRabbit, Sourcery
- **Specialized**: Testing, documentation, security-focused tools

Each category: tool count, top picks, brief comparison notes.

### `get_recommendations` (Pro) -- MatchMaker Protocol
Describe your situation and get AI-powered ranked recommendations.

**Input:**
- `use_case` -- What you're building or doing (e.g., "full-stack web app, React + Node")
- `team_size` -- Number of developers
- `budget` -- Monthly budget per developer
- `must_have` -- Required features (e.g., "multi-file editing, agent mode")
- `preferred_ide` -- VS Code, JetBrains, Neovim, etc.

**Output:**
- Top 3 tools ranked by match score (0-100)
- Detailed reasoning for each recommendation
- Tradeoff analysis (what you gain vs. what you lose)
- Migration tips from your current tool

### `pricing_calculator` (Pro) -- CostRadar Protocol
Calculate complete costs for any AI tool configuration.

**Input:**
- `tool_name` -- Which tool to calculate
- `team_size` -- Number of seats
- `plan` -- `free`, `pro`, or `enterprise`
- `usage` -- Estimated requests per day per developer
- `add_ons` -- Any additional features needed

**Output:**
- Monthly cost (total and per-developer)
- Annual cost with savings vs. monthly
- Feature breakdown at selected tier
- Automatic comparison with 2 alternatives at same scale and budget

## Wrong vs. Right

### Example 1: Too Many Tools in One Comparison

**Wrong:**
```
User: "Compare all AI coding tools"
Agent: [calls compare_tools with 12 tools]  // Unwieldy, unreadable output
```

**Right:**
```
User: "Compare all AI coding tools"
Agent: "There are 15+ tools tracked. Let me help narrow it down. Are you looking for:
  - IDE-integrated (Cursor, Windsurf, Copilot)?
  - CLI-based (Claude Code, Aider)?
  - Cloud agents (Devin, Replit)?
Pick a category and I'll compare the top 2-3."
```

### Example 2: Stale Pricing Assumptions

**Wrong:**
```
User: "How much is Cursor?"
Agent: "Cursor Pro is $20/mo."  // Recalled from training data, may be outdated
```

**Right:**
```
User: "How much is Cursor?"
Agent: [calls get_tool_profile("Cursor")]  // Gets latest tracked pricing
Agent: "According to our latest data (updated weekly), Cursor Pro is $20/mo. Always verify on cursor.com for flash sales or plan changes."
```

### Example 3: Recommendation Without Context

**Wrong:**
```
User: "Which AI tool should I use?"
Agent: [calls get_recommendations with empty fields]  // Garbage in, garbage out
```

**Right:**
```
User: "Which AI tool should I use?"
Agent: "To give you a good recommendation, I need a few details:
  1. What are you building? (web app, mobile, data science, etc.)
  2. Team size? (solo, small team, enterprise)
  3. Monthly budget per developer?
  4. Must-have features? (agent mode, multi-file editing, etc.)
  5. Preferred IDE? (VS Code, JetBrains, Neovim, etc.)"
```

## Security & Privacy

| Concern | How We Handle It |
|---------|------------------|
| **No Tool Telemetry** | We don't track which tools you compare or recommend. |
| **No Team Data Stored** | Team size, budget, and use case inputs are processed and discarded -- never logged. |
| **Pricing Source** | All pricing data sourced from official public pages. No scraping of private accounts. |
| **Rate Limiting** | Per-IP limits prevent abuse. Free: 10/day, Pro: 1000/day. |
| **Edge Processing** | All computation on Cloudflare Workers -- no centralized database of user queries. |
| **Unbiased Results** | No affiliate deals or sponsored rankings. Comparisons are data-driven. |

## Pricing

| Tier | Calls/Day | Price | What You Get |
|------|-----------|-------|--------------|
| **Free** | 10 | $0/mo | 3 tools: compare, profile, categories |
| **Pro** | 1,000 | $9/mo | All 5 tools + recommendations + calculator + all 9 OpenClaw servers |
| **x402** | Pay-per-call | $0.05 USDC | No account needed, crypto-native |

**Get Pro Key**: https://buy.stripe.com/4gw5na5U19SP9TW288

One Pro key unlocks all 9 servers. Cancel anytime.

## The OpenClaw Intelligence Stack

| Server | Tools | Best For |
|--------|-------|----------|
| **JSON Toolkit** | 6 | Format, validate, diff, query, transform JSON |
| **Regex Engine** | 5 | Test, extract, replace, explain regex patterns |
| **Color Palette** | 5 | Generate, convert, harmonize, accessibility-check colors |
| **Timestamp Converter** | 5 | Parse, format, diff, timezone-convert timestamps |
| **Prompt Enhancer** | 6 | Optimize, rewrite, score, A/B test AI prompts |
| **Market Intelligence** | 6 | AI market trends, GitHub stats, competitor analysis |
| **Fortune & Tarot** | 3 | Daily fortune, tarot readings, I Ching |
| **Content Publisher** | 8 | MoltBook posts, social content, newsletter |
| **AgentForge Compare** | **5** | **Compare AI tools, frameworks, MCP servers** |

All 9 servers share one Pro key. **$9/mo = 49 tools.**
