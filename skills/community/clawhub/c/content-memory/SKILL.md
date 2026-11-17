---
name: content-memory
description: Give AI agents Remember content ideas and drafts. using BlueColumn persistent memory. Use when an agent supports content creation and needs idea continuity; when the user wants to store, recall, or search content memory context. Requires a BlueColumn API key (bc_live_*).
---

# Content Memory — BlueColumn Skill

Remember content ideas and drafts.. Powered by BlueColumn (bluecolumn.ai) persistent vector memory.

## Setup
Read `TOOLS.md` or the platform secret store for the BlueColumn API key (`bc_live_*`). Base URL: `https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1`

## Store
```bash
curl -X POST .../agent-remember \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Idea: 'Replace conversation history with semantic memory' — draft outline started 7/30.", "title": "content-memory - note"}'
```

## Quick note
```bash
curl -X POST .../agent-note \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Idea: 'Replace conversation history with semantic memory' — draft outline started 7/30.", "tags": ["content-memory"]}'
```

## Recall
```bash
curl -X POST .../agent-recall \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"q": "What content ideas have I been working on?"}'
```

## Workflow
1. On new context, first recall: `What content ideas have I been working on?`
2. Use the answer to personalize the response
3. After the interaction, store the summary via `/agent-remember`

## Docs
Full API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
