---
name: family-memory
description: Give AI agents Remember family details. using BlueColumn persistent memory. Use when an agent supports family coordination; when the user wants to store, recall, or search family memory context. Requires a BlueColumn API key (bc_live_*).
---

# Family Memory — BlueColumn Skill

Remember family details.. Powered by BlueColumn (bluecolumn.ai) persistent vector memory.

## Setup
Read `TOOLS.md` or the platform secret store for the BlueColumn API key (`bc_live_*`). Base URL: `https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1`

## Store
```bash
curl -X POST .../agent-remember \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Mom's birthday Aug 2. Kid's school event 8/10.", "title": "family-memory - note"}'
```

## Quick note
```bash
curl -X POST .../agent-note \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Mom's birthday Aug 2. Kid's school event 8/10.", "tags": ["family-memory"]}'
```

## Recall
```bash
curl -X POST .../agent-recall \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"q": "What family dates are coming up?"}'
```

## Workflow
1. On new context, first recall: `What family dates are coming up?`
2. Use the answer to personalize the response
3. After the interaction, store the summary via `/agent-remember`

## Docs
Full API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
