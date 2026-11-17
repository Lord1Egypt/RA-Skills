---
name: finance-memory
description: Give AI agents Remember finances and budgets. using BlueColumn persistent memory. Use when an agent tracks budgets and financial context; when the user wants to store, recall, or search finance memory context. Requires a BlueColumn API key (bc_live_*).
---

# Finance Memory — BlueColumn Skill

Remember finances and budgets.. Powered by BlueColumn (bluecolumn.ai) persistent vector memory.

## Setup
Read `TOOLS.md` or the platform secret store for the BlueColumn API key (`bc_live_*`). Base URL: `https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1`

## Store
```bash
curl -X POST .../agent-remember \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Budget Jul: $4k, spent $3.2k. Subscriptions: $89/mo total.", "title": "finance-memory - note"}'
```

## Quick note
```bash
curl -X POST .../agent-note \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Budget Jul: $4k, spent $3.2k. Subscriptions: $89/mo total.", "tags": ["finance-memory"]}'
```

## Recall
```bash
curl -X POST .../agent-recall \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"q": "What's my spending trend this quarter?"}'
```

## Workflow
1. On new context, first recall: `What's my spending trend this quarter?`
2. Use the answer to personalize the response
3. After the interaction, store the summary via `/agent-remember`

## Docs
Full API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
