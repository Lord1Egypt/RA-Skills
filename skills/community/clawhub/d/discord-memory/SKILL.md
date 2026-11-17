---
name: discord-memory
description: Give AI agents Remember Discord conversations. using BlueColumn persistent memory. Use when an agent operates in Discord servers and needs continuity; when the user wants to store, recall, or search discord memory context. Requires a BlueColumn API key (bc_live_*).
---

# Discord Memory — BlueColumn Skill

Remember discord conversations.. Powered by BlueColumn (bluecolumn.ai) persistent vector memory.

## Setup
Read `TOOLS.md` or the platform secret store for the BlueColumn API key (`bc_live_*`). Base URL: `https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1`

## Store
```bash
curl -X POST .../agent-remember \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "#community: user reported bug in v1.2, fix shipped in v1.2.1.", "title": "discord-memory - note"}'
```

## Quick note
```bash
curl -X POST .../agent-note \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "#community: user reported bug in v1.2, fix shipped in v1.2.1.", "tags": ["discord-memory"]}'
```

## Recall
```bash
curl -X POST .../agent-recall \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"q": "What issues have community members reported?"}'
```

## Workflow
1. On new context, first recall: `What issues have community members reported?`
2. Use the answer to personalize the response
3. After the interaction, store the summary via `/agent-remember`

## Docs
Full API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
