---
name: customer-support-memory
description: Give AI agents Customer support that never re-asks. using BlueColumn persistent memory. Use when an agent handles support tickets and needs full context; when the user wants to store, recall, or search customer support memory context. Requires a BlueColumn API key (bc_live_*).
---

# Customer Support Memory — BlueColumn Skill

Customer support that never re-asks.. Powered by BlueColumn (bluecolumn.ai) persistent vector memory.

## Setup
Read `TOOLS.md` or the platform secret store for the BlueColumn API key (`bc_live_*`). Base URL: `https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1`

## Store
```bash
curl -X POST .../agent-remember \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Ticket #4412: Jane reported rate limiting on Developer plan. Escalated to billing.", "title": "customer-support-memory - note"}'
```

## Quick note
```bash
curl -X POST .../agent-note \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Ticket #4412: Jane reported rate limiting on Developer plan. Escalated to billing.", "tags": ["customer-support-memory"]}'
```

## Recall
```bash
curl -X POST .../agent-recall \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"q": "What is the history of Jane's support tickets?"}'
```

## Workflow
1. On new context, first recall: `What is the history of Jane's support tickets?`
2. Use the answer to personalize the response
3. After the interaction, store the summary via `/agent-remember`

## Docs
Full API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
