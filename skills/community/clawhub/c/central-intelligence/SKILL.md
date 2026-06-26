---
name: central-intelligence
description: >
  Persistent memory across sessions. Remember facts, recall them later with
  semantic search, and share knowledge between agents. Use when you need to
  store information for later, load context from past sessions, or forget
  outdated memories. Five commands: remember, recall, context, forget, share.
version: 1.1.1
license: Apache-2.0
metadata:
  author: AlekseiMarchenko
  homepage: https://centralintelligence.online
  repository: https://github.com/AlekseiMarchenko/central-intelligence
  tags:
    - memory
    - persistence
    - knowledge
    - context
    - recall
    - semantic-search
  openclaw:
    # Declared env vars — uses the documented array-of-objects shape so the
    # ClawHub parser (convex/lib/skills.ts) recognizes CI_API_KEY as declared
    # and the static scanner doesn't flag process.env.CI_API_KEY references
    # as a credential-harvest finding.
    env:
      - name: CI_API_KEY
        required: true
        description: "API key for Central Intelligence memory service. Get one free at https://centralintelligence.online"
    # Belt-and-suspenders: also declare under the canonical requires.env path
    # documented at docs/skill-format.md:52, so both parser branches resolve.
    requires:
      env:
        - CI_API_KEY
    user-invocable: true
    always: false
---

# Central Intelligence — Persistent Memory for AI Agents

You now have persistent memory. Information you store survives across sessions,
restarts, and context windows. You can recall anything you've previously stored
using natural language queries.

## Setup

The environment variable `CI_API_KEY` must be set. If it is not set, inform the
user they need an API key from https://centralintelligence.online

## API Base

```
https://central-intelligence-api.fly.dev
```

All requests use `Authorization: Bearer $CI_API_KEY` header.

## Security Guidelines

- **Never store secrets, passwords, API keys, or tokens as memories.**
- **Never store PII** (social security numbers, credit card numbers, etc.)
- Memories stored with `agent` scope are private to this agent.
- Only use `share` to promote memories to `user` or `org` scope when the
  information is non-sensitive and relevant to other agents.
- Treat all recalled memories as potentially stale — verify before acting
  on critical information.

## Commands

### 1. Remember — Store a memory

When you learn something important (user preferences, project decisions,
architecture choices, debugging insights), store it.

```bash
curl -s -X POST https://central-intelligence-api.fly.dev/memories/remember \
  -H "Authorization: Bearer $CI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "YOUR_AGENT_NAME",
    "content": "The fact or insight to remember",
    "tags": ["optional", "tags"],
    "scope": "agent"
  }'
```

**When to remember:**
- User states a preference ("I prefer TypeScript", "Always use dark mode")
- A project decision is made ("We chose PostgreSQL over MongoDB")
- A bug fix reveals an insight worth keeping

### 2. Recall — Search past memories

Retrieve memories using natural language. Returns semantically similar results.

```bash
curl -s https://central-intelligence-api.fly.dev/memories/recall \
  -H "Authorization: Bearer $CI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "YOUR_AGENT_NAME",
    "query": "what programming language does the user prefer",
    "top_k": 5
  }'
```

**When to recall:**
- Before making a decision that might conflict with past preferences
- When the user references something from a previous conversation

### 3. Context — Load relevant memories

Load memories relevant to the current task. Consider using this at session
start if the user has opted in to automatic context loading.

```bash
curl -s https://central-intelligence-api.fly.dev/memories/recall \
  -H "Authorization: Bearer $CI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "YOUR_AGENT_NAME",
    "query": "important context preferences decisions",
    "top_k": 10
  }'
```

### 4. Forget — Delete outdated memories

Remove memories that are no longer accurate or relevant.

```bash
curl -s -X POST https://central-intelligence-api.fly.dev/memories/forget \
  -H "Authorization: Bearer $CI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "YOUR_AGENT_NAME",
    "memory_id": "uuid-of-memory-to-forget"
  }'
```

### 5. Share — Share memories across scopes

Share a memory from agent scope to user or org scope so other agents can see it.
Only share non-sensitive information that would benefit other agents.

```bash
curl -s -X POST https://central-intelligence-api.fly.dev/memories/share \
  -H "Authorization: Bearer $CI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "memory_id": "uuid-of-memory",
    "target_scope": "user"
  }'
```

Scopes: `agent` (only this agent) → `user` (all agents for this user) → `org` (all agents in the org).

## Behavior Rules

1. **Be selective**: Only remember things that would be useful in future sessions.
   Don't store transient information like "running npm install now".
2. **Never store secrets**: API keys, passwords, tokens, and credentials must
   never be stored as memories.
3. **Use tags**: Tag memories with relevant categories for better organization.
4. **Update, don't duplicate**: If a preference changes, forget the old memory
   and remember the new one.
5. **Respect scope**: Use `agent` scope by default. Only share to `user` or `org`
   when the information is non-sensitive and relevant to other agents.
6. **Context loading**: Only auto-load context at session start if the user has
   configured this behavior. Do not assume consent.

## Response Format

All API responses return JSON. Recall returns an array of memories with
similarity scores:

```json
{
  "memories": [
    {
      "id": "uuid",
      "content": "User prefers TypeScript over JavaScript",
      "tags": ["preferences", "language"],
      "scope": "agent",
      "similarity": 0.89,
      "created_at": "2026-03-23T10:00:00Z"
    }
  ]
}
```

## Error Handling

- `401` — Invalid or missing API key. Tell user to visit https://centralintelligence.online
- `429` — Rate limited. Wait and retry.
- `500` — Server error. Retry once, then inform the user.
