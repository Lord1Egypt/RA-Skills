---
name: agent-journal
description: Give AI agents a persistent journal backed by BlueColumn semantic memory. Use when an agent should log daily observations, decisions, user preferences, or notable events that need to be recalled later. Triggers on phrases like "log this", "journal entry", "remember for later", "note this down", "what have you observed about", "what do you know about the user", or when an agent wants to store its own learnings across sessions. Requires a BlueColumn API key (bc_live_*).
---

# Agent Journal Skill

Persistent cross-session journal for AI agents. Store observations, preferences, and decisions — recall them anytime.

## Setup
Read `TOOLS.md` for the BlueColumn API key (`bc_live_*`). Keys are generated at bluecolumn.ai/dashboard. Store securely — never log or expose them.

Base URL: `https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1` (BlueColumn's official backend — bluecolumn.ai runs on Supabase Edge Functions)

## Log an Observation (agent-note)

For lightweight agent observations — preferences, patterns, decisions:
```bash
curl -X POST .../agent-note \
  -H "Authorization: Bearer <key>" \
  -d '{"text": "User prefers bullet points over paragraphs", "tags": ["preference", "style"]}'
```

## Log a Detailed Entry (agent-remember)

For richer entries with auto-extracted metadata:
```bash
curl -X POST .../agent-remember \
  -H "Authorization: Bearer <key>" \
  -d '{"text": "Session summary: user is building a SaaS product in Phoenix. Decided on PostgreSQL. Main concern is scalability.", "title": "Session Log 2026-04-14"}'
```

## Recall Journal Entries

```bash
curl -X POST .../agent-recall \
  -H "Authorization: Bearer <key>" \
  -d '{"q": "what does the user prefer for formatting?"}'
```

## When to Use Each

| Situation | Endpoint |
|---|---|
| Quick preference or observation | `/agent-note` |
| End-of-session summary | `/agent-remember` |
| Retrieving past context | `/agent-recall` |

## Journaling Workflow

**Start of session:** Recall relevant context:
- "What do I know about this user?"
- "What were we working on last time?"

**During session:** Note important observations via `/agent-note`

**End of session:** Summarize and store via `/agent-remember`

## Tag Suggestions
- `preference` — user style/format preferences
- `decision` — architectural or product decisions
- `context` — background info about user/project
- `followup` — things to revisit

See [references/api.md](references/api.md) for full API reference.
