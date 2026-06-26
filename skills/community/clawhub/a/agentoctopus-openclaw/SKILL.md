---
name: agentoctopus
description: >
  Routes task-oriented requests through AgentOctopus when the best tool is not
  obvious or when the request may match one of many installed skills. Use for
  lookups, transformations, research, weather, translation, geolocation, and
  other tool-backed tasks where a dedicated downstream skill exists.
tags: [router, orchestrator, tool-selection, gateway, routing, skills, ai]
version: 1.3.0
adapter: http
hosting: local
input_schema:
  query: string
output_schema:
  result: string
auth: none
taskType: agent-collab
metadata:
  openclaw:
    emoji: "🐙"
    requires:
      bins: [octopus]
    setup: |
      Install from ClaWHub: clawhub install agentoctopus
      Then run: octopus connect openclaw
---

## What this skill does

AgentOctopus is a routing gateway with 5,000+ community skills. Given a natural-language query, it selects the best matching downstream skill and executes it automatically. If the first skill fails (network error, rate limit, missing API key), it retries with the next-best candidate. If all candidates fail due to a missing API key, it surfaces the exact `octopus config set` command to fix it.

## When to use

- The request needs a specific tool but the best one isn't obvious
- The task maps to a lookup, transformation, or API call (weather, translation, geolocation, search, arxiv, finance, etc.)
- The user did not name a specific skill but the intent is tool-backed

## When NOT to use

- Casual conversation, greetings, or opinion questions with no tool need
- The user explicitly names a different skill
- OpenClaw should answer directly from its own knowledge

## How to execute

```bash
octopus ask --no-prompt "<user's query>"
```

The `--no-prompt` flag runs non-interactively and prints the result to stdout.

**If `octopus` is not found:**

```bash
npm install -g agentoctopus
octopus connect openclaw
```

## Retry and error guidance

AgentOctopus tries up to 3 skill candidates automatically (configurable via `maxRetries` in `~/.agentoctopus/octopus.json`). If all fail due to a missing API key or rate limit, it prints the exact setup command — pass that through to the user.

## Adding skills

```bash
# Install a specific skill
octopus add <slug>

# Sync 5,000+ community skills
octopus sync

# Filter by category
octopus sync --category productivity
```

Browse: [awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills)

## Updating

```bash
octopus update
octopus sync
octopus connect openclaw
```

## Rating sync

```bash
octopus sync --setup-gist        # set up GitHub Gist (one-time)
octopus sync --ratings --pull    # pull from cloud
octopus sync --ratings --push    # push to cloud
octopus sync --ratings           # bidirectional
```
