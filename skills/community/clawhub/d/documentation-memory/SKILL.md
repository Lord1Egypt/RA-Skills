---
name: documentation-memory
description: Give AI agents Remember docs you've written and read. using BlueColumn persistent memory. Use when an agent maintains documentation and needs to reuse it; when the user wants to store, recall, or search documentation memory context. Requires a BlueColumn API key (bc_live_*).
---

# Documentation Memory — BlueColumn Skill

Remember docs you've written and read.. Powered by BlueColumn (bluecolumn.ai) persistent vector memory.

## Setup
Read `TOOLS.md` or the platform secret store for the BlueColumn API key (`bc_live_*`). Base URL: `https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1`

## Store
```bash
curl -X POST .../agent-remember \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Wrote onboarding doc: install → add key → done. Published to docs site 7/30.", "title": "documentation-memory - note"}'
```

## Quick note
```bash
curl -X POST .../agent-note \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Wrote onboarding doc: install → add key → done. Published to docs site 7/30.", "tags": ["documentation-memory"]}'
```

## Recall
```bash
curl -X POST .../agent-recall \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"q": "What documentation have we published and where?"}'
```

## Workflow
1. On new context, first recall: `What documentation have we published and where?`
2. Use the answer to personalize the response
3. After the interaction, store the summary via `/agent-remember`

## Docs
Full API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
