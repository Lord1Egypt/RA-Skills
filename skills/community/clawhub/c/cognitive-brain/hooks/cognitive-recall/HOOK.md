---
name: cognitive-recall
description: "Cross-session memory recall via Cognitive Brain - injects user context from PostgreSQL memory store"
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "events": ["agent:bootstrap", "message:preprocessed"],
        "requires": { "bins": ["node"] }
      }
  }
---

# Cognitive Recall Hook

Automatically recalls user context from Cognitive Brain's PostgreSQL memory store at session bootstrap, enabling cross-session memory continuity.

## What It Does

1. Triggers on agent bootstrap (session start)
2. Queries Cognitive Brain for user preferences, important facts, recent episodes
3. Injects memory context into the bootstrap files for the agent to see

## Requirements

- Cognitive Brain skill must be installed
- PostgreSQL must be running with `cognitive_brain` database
- Redis (optional, for caching)

## Configuration

The hook reads Cognitive Brain's config from:
`~/.openclaw/workspace/skills/cognitive-brain/config.json`

Default connection (configure via environment variables):
- PostgreSQL: ${PGHOST}:${PGPORT}/${PGDATABASE}
- User: ${PGUSER}
- Password: ${PGPASSWORD}
