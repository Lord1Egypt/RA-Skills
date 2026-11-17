---
name: coaching-memory
description: Give AI agents Track goals and coaching progress. using BlueColumn persistent memory. Use when an agent coaches users and tracks progress; when the user wants to store, recall, or search coaching memory context. Requires a BlueColumn API key (bc_live_*).
---

# Coaching Memory — BlueColumn Skill

Track goals and coaching progress.. Powered by BlueColumn (bluecolumn.ai) persistent vector memory.

## Setup
Read `TOOLS.md` or the platform secret store for the BlueColumn API key (`bc_live_*`). Base URL: `https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1`

## Store
```bash
curl -X POST .../agent-remember \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Goal: ship MVP by Sep. Check-in 7/31: on track, risk — design sign-off.", "title": "coaching-memory - note"}'
```

## Quick note
```bash
curl -X POST .../agent-note \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Goal: ship MVP by Sep. Check-in 7/31: on track, risk — design sign-off.", "tags": ["coaching-memory"]}'
```

## Recall
```bash
curl -X POST .../agent-recall \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"q": "How is the user progressing against their goals?"}'
```

## Workflow
1. On new context, first recall: `How is the user progressing against their goals?`
2. Use the answer to personalize the response
3. After the interaction, store the summary via `/agent-remember`

## Docs
Full API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
