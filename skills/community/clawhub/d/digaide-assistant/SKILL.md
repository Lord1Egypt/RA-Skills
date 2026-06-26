---
name: digaide-memory-layer
description: Persistent identity and memory context layer for AI agents across platforms.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - DIGAIDE_API_KEY
      bins:
        - curl
    primaryEnv: DIGAIDE_API_KEY
    homepage: https://digaide.com
---

# Digaide Memory Layer

Digaide provides a persistent identity and long-term memory layer for AI agents.

## What this skill helps with

- Keep one user identity across sessions and platforms.
- Enrich context with memory before response generation.
- Keep assistant behavior consistent with selected persona.
- Improve long task UX with progress-aware workflows.

## Setup

1. Prepare `DIGAIDE_API_KEY`.
2. Set `DIGAIDE_API_BASE` if you use non-production API endpoint.
3. Configure your agent runtime hooks.
4. Use Digaide API endpoints for initialize, enrich, and wrap flows.

## Links

- Website: https://digaide.com
- API: https://api.digaide.com
