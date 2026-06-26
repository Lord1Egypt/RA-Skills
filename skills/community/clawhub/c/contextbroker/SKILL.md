---
name: contextbroker
description: A cross-agent memory and context SDK for AI systems. Provides structured context injection, conversation memory portability, and context enrichment.
metadata:
  openclaw:
    emoji: "🔗"
    requires:
      bins: ["contextbroker"]
    install:
      - id: skill-install
        kind: skill
        label: "Context Broker skill is installed — type /contextbroker in any chat"
---

# contextbroker — Cross-Agent Memory SDK

## What It Is

A **cross-agent memory SDK** — gives AI agents structured, persistent context across sessions, tools, and platforms. Works with any AI Model.

## When to Use

- Building multi-agent orchestration systems
- Giving agents persistent memory across sessions
- Migrating context between AI platforms
- Structured context injection for RAG pipelines

## Syntax

```
/contextbroker push --session-id abc123 --context "user preferences..."
/contextbroker pull --session-id abc123
/contextbroker export --format openai --output memory.json
```

## Free Tier

**100 context operations/month free** with any Signalloom API key.

Get your free key: https://signalloomai.com/signup
