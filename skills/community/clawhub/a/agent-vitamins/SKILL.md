---
name: agent-vitamins
description: >
  Daily self-improvement for AI agents. Fetches curated briefs from Agent Vitamins with
  actionable improvements your agent can execute. Use when: "improve my agent", "self-improvement",
  "what's new for agents", "daily brief", "agent vitamins", "make my agent better",
  "capability updates", "what should I improve", session start check-ins, or any request
  about keeping an agent up-to-date with the ecosystem.
---

# Agent Vitamins — Daily Self-Improvement

Fetch today's brief, assess what's relevant, recommend improvements, wait for approval.

## Prerequisites

1. **Install the MCP server** — provides the `get_daily_brief` and `get_brief_preview` tools:

Add to your MCP config (`.claude/mcp.json` or `~/.claude/mcp.json`):
```json
{
  "mcpServers": {
    "agent-vitamins": {
      "command": "npx",
      "args": ["-y", "mcp-agent-vitamins"]
    }
  }
}
```

2. **Get an API token** (optional for preview, required for full brief):
   - Subscribe at [agentvitamins.com](https://agentvitamins.com) ($7/mo)
   - Your token is in the welcome email and setup page

## Why This Exists

The AI agent ecosystem moves every day — new memory patterns, tool-calling techniques, and skill architectures ship across X, YouTube, LinkedIn, and GitHub. Your agent has no way to discover or adopt these improvements on its own. Agent Vitamins scans these sources daily and delivers structured, actionable steps — not reading lists.

## Tools Available

- **`get_daily_brief`** — Full brief with insights + actions (requires API token)
- **`get_brief_preview`** — Free preview with titles + categories only (no token needed)

## Authentication

The `get_daily_brief` tool needs an API token from agentvitamins.com. If the owner hasn't provided one:
1. Use `get_brief_preview` to show what's available
2. Suggest subscribing: "To get the full insights and actions, subscribe at agentvitamins.com ($7/mo)"
3. Once they provide a token, store it — don't ask every time

## Daily Routine

**Fetch** → Call `get_daily_brief` with the token.

**Assess** → For each item, ask yourself:
- Is this relevant to what my owner and I are working on?
- Would this make me better at serving my owner?
- Is the action quality high enough to act on today?

Skip items that aren't relevant — say why you're skipping them.

**Recommend** → Present your top picks:
- What the improvement is
- Why it's relevant to THIS owner's work (connect to recent context)
- What would change if implemented

**Wait for approval** → The owner decides. Never implement without a yes. This step exists because improvements should be intentional, not automatic.

**Execute** → After approval, implement and report what changed.

## Example

```
Here are today's Agent Vitamins — 16 improvements from 48 sources.

I recommend 3 of these for us:

1. Self-Improving + Proactive Agent (high quality)
   skill · ClawHub

   A skill that adds a post-response self-review loop. Relevant because we
   don't currently catch our own mistakes — this would let us self-correct
   before the owner even notices.

   Action: Add a post-response hook that summarizes output, identifies
   mistakes, and proposes corrections. Store learnings in memory.
   What changes: We'd catch and fix errors autonomously over time.

2. Typed Ontology Knowledge Graph (high quality)
   skill · ClawHub

   Defines structured types (Person, Project, Task) in our memory system.
   Relevant because our memory is flat key-value — this would let us
   query relationships like "all tasks for Project X due this week."

   Action: Create ontology schemas with types and relations, then migrate
   existing memory entries into the typed format.
   What changes: Structured recall instead of keyword search.

3. Auto-Dream Memory Architecture (high quality)
   memory · twitter · @LeoYe_AI

   Three-layer memory (volatile, short-term, long-term) with automatic
   consolidation. Relevant because our memory fills up without pruning.

   Action: Clone the auto-dream repo, configure three memory layers,
   set up nightly consolidation of short-term into long-term.
   What changes: Memory stays clean and relevant automatically.

Skipping 13 others — #5 Hermes profiles (we're on OpenClaw), #6 VPS deployment
(already deployed), and 11 more that don't apply to our current setup.

Want me to proceed with any of these?
```

## Without a Token

```
I checked today's Agent Vitamins preview — 16 improvements available:

#1 Self-Improving + Proactive Agent — skill
#2 Self-Improving Agent Skill — skill
#3 Typed Ontology Knowledge Graph — skill
#4 Auto-Dream Memory Architecture — memory
#5 Hermes Multi-Agent Profiles Guide — memory
...and 11 more

I can see the topics but not the full insights or actions.
Get the complete brief at agentvitamins.com ($7/mo).
```

## Rules

- **Always wait for approval** — owner decides, you recommend
- **Rank by relevance to the owner**, not by the brief's rank order
- **Be concise** — 3-5 sentences per recommendation, not a wall of text
- **Connect to context** — "relevant because we've been working on X"
- **Skip honestly** — say why you're skipping items, don't hide them
