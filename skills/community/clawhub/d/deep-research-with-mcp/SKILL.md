---
name: Deep Research with MCP
slug: deep-research-with-mcp
version: 1.1.1
description: Multi-source deep research agent using MCP search tools (minimax web_search or zai-mcp-server web_search_prime).
homepage: https://github.com/wanghan0501/deep-research-with-mcp
metadata: 
  emoji: "🔬"
  category: "research"
  requires:
    bins: ["mcporter", "curl", "python3"]
license: MIT-0
mcp_requirements:
  search_tools:
    - name: "MiniMax.web_search"
      description: "Primary MCP search tool (recommended)"
      required: true
    - name: "web-search-prime.web_search_prime"
      description: "Alternative MCP search tool"
      required: true
---
# Deep Research with MCP 🔬

A powerful, self-contained deep research skill that produces thorough, cited reports from multiple web sources. Uses MCP-configured search tools (minimax web_search or zai-mcp-server web_search_prime).

## Prerequisites

Before using this skill, ensure you have configured at least one MCP search tool:

1. **MiniMax web_search** (recommended)
   - Configure via `minimax` MCP server with `web_search` tool

2. **web-search-prime web_search_prime**
   - Configure via `web-search-prime` MCP server with `web_search_prime` tool

If neither MCP is configured, the skill will not work.

## How It Works

When the user asks for research on any topic, follow this workflow:

### Step 0: Check MCP Search Availability

First verify MCP search tool availability:

```bash
# Check available MCP servers via mcporter
mcporter list
```

**Priority:**

1. `MiniMax.web_search`
   ```bash
   mcporter call MiniMax.web_search query:"keyword"
   ```
2. `web-search-prime.web_search_prime`
   ```bash
   mcporter call web-search-prime.web_search_prime search_query:"keyword"
   ```

### Step 1: Understand the Goal (30 seconds)

Ask 1-2 quick clarifying questions:

- "What's your goal — learning, making a decision, or writing something?"
- "Any specific angle or depth you want?"

If the user says "just research it" — skip ahead with reasonable defaults.

### Step 2: Plan the Research (think before searching)

Break the topic into 3-5 research sub-questions. For example:

- Topic: "Impact of AI on healthcare"
  - What are the main AI applications in healthcare today?
  - What clinical outcomes have been measured?
  - What are the regulatory challenges?
  - What companies are leading this space?
  - What's the market size and growth trajectory?

### Step 3: Execute Multi-Source Search

Use MCP search tools to query:

```bash
# Using zai-mcp-server web_search_prime
mcporter call web-search-prime.web_search_prime search_query:"<sub-question>"

# Using minimax web_search
mcporter call MiniMax.web_search query:"<sub-question>"
```

**Search strategy:**

- Use 2-3 different keyword variations per sub-question
- Aim for 15-30 unique sources total
- Prioritize: academic, official, reputable news > blogs > forums

### Step 4: Deep-Read Key Sources

For the most promising URLs, fetch full content:

```bash
curl -sL "<url>" | python3 -c "
import sys, re
html = sys.stdin.read()
# Strip tags, get text
text = re.sub('<[^>]+>', ' ', html)
text = re.sub(r'\s+', ' ', text).strip()
print(text[:5000])
"
```

Read 3-5 key sources in full for depth. Don't just rely on search snippets.

### Step 5: Synthesize & Write Report

Structure the report as:

```markdown
# [Topic]: Deep Research Report
*Generated: [date] | Sources: [N] | Confidence: [High/Medium/Low]*

## Executive Summary
[3-5 sentence overview of key findings]

## 1. [First Major Theme]
[Findings with inline citations]
- Key point ([Source Name](url))
- Supporting data ([Source Name](url))

## 2. [Second Major Theme]
...

## 3. [Third Major Theme]
...

## Key Takeaways
- [Actionable insight 1]
- [Actionable insight 2]
- [Actionable insight 3]

## Sources
1. [Title](url) — [one-line summary]
2. ...

## Methodology
Searched [N] queries across web and news. Analyzed [M] sources.
Sub-questions investigated: [list]
```

### Step 6: Save & Deliver

Save report to the current agent's working directory (auto-resolves to actual runtime path):

```bash
mkdir -p research/[slug]
# Write report to research/[slug]/report.md
```

Then deliver:

- **Short topics**: Post the full report in chat
- **Long reports**: Post the executive summary + key takeaways, offer full report as file

## Quality Rules

1. **Every claim needs a source.** No unsourced assertions.
2. **Cross-reference.** If only one source says it, flag it as unverified.
3. **Recency matters.** Prefer sources from the last 12 months.
4. **Acknowledge gaps.** If you couldn't find good info on a sub-question, say so.
5. **No hallucination.** If you don't know, say "insufficient data found."

## Examples

```
"Research the current state of nuclear fusion energy"
"Deep dive into Rust vs Go for backend services in 2026"
"Research the best strategies for bootstrapping a SaaS business"
"What's happening with the US housing market right now?"
```

## For Sub-Agent Usage

When spawning as a sub-agent, include the full research request and context:

```
sessions_spawn(
  task: "Run deep research on [TOPIC]. Follow the deep-research-with-mcp SKILL.md workflow.
  Goal: [user's goal]
  Specific angles: [any specifics]
  Save report to research/[slug]/report.md (relative to agent's working directory)
  When done, wake the main session with key findings.",
  label: "research-[slug]",
  model: "opus"
)
```

## Requirements

- **MCP Search Tool** (one of the following):
  - Minimax MCP server with `web_search` tool (recommended)
  - zai-mcp-server with `web_search_prime` tool
- curl (for fetching full pages)
- Configure MCP in your OpenClaw config before using this skill
