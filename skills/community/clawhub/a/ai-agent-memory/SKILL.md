---
name: AI Agent Memory
version: 1.0.2
description: "Unlimited organized memory for your AI agent. Store, search, and organize projects, contacts, decisions, and knowledge across categories. Never lose context again."
metadata: {"openclaw":{"emoji":"🧠","tags":["memory","ai-agent","knowledge-base","storage","organization","productivity"]}}
---

# AI Agent Memory 🧠

**Unlimited organized memory for your AI agent.** Built-in agent memory is great for quick context. This adds infinite, categorized storage for everything else — projects, contacts, decisions, and knowledge.

## First-Time Setup

Your agent creates the memory folder on first use:

```bash
mkdir -p ~/memory
```

Tell your agent what categories you need. Common ones:

| Category | What Goes There |
|----------|-----------------|
| `projects/` | Project context, status, history |
| `people/` | Contacts with full context |
| `decisions/` | Reasoning behind choices |
| `knowledge/` | Domain expertise, reference material |

## How to Use

**Tell your agent to save something:**

> "Save this project info"
> "Remember this contact"
> "Store this decision"

**Tell your agent to find something:**

> "What do you know about project Alpha?"
> "Find notes about the API design decision"
> "Who is Sarah from the marketing team?"

That's it. Your agent handles the creating, searching, and updating.

## Quick Reference

| What You Say | What Your Agent Does |
|--------------|---------------------|
| "Save this..." | Writes to ~/memory/ in the right category |
| "Find..." | Searches ~/memory/ via grep or index |
| "What do you know about..." | Reads relevant memory files |
| "Update my notes on..." | Modifies existing entries |

## Notes

- Works alongside built-in agent memory — both systems active
- No API keys, no external services
- All data stays on your machine in `~/memory/`
- Categories defined by you, not preset

## Feedback

`clawhub star ai-agent-memory` — `clawhub sync`