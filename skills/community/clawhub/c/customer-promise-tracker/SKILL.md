---
name: customer-promise-tracker
description: Extract commitments from calls and messages — who promised what, by when, and whether it happened — and produce an overdue list with links to the original evidence. Use when an agency, sales team, or account manager must never miss a commitment made to a customer. Requires a BlueColumn API key (bc_live_*).
---

# Customer Promise Tracker — BlueColumn Skill

A missed commitment is a lost renewal, a chargeback, or a churned account. This skill extracts every promise made in calls and messages, tracks whether it was kept, and surfaces the overdue list before it becomes a problem.

## Setup

Get a free key at https://bluecolumn.ai/login (no card). Keys look like `bc_live_*`. Base URL: `https://api.bluecolumn.ai`.

## Store a promise

After a call or thread, store each commitment with who, what, when, and the source.

```bash
curl -X POST https://api.bluecolumn.ai/remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "PROMISE — Made by: Sarah (account manager). To: Acme Corp (contact: Dana). What: send revised security review + SOC2 report. By: 2026-09-30. Source: call 09-28, transcript in CRM. Status: open. Evidence: https://crm.example.com/calls/88213",
    "title": "promise - Acme Corp - SOC2 by 09-30"
  }'
```

## Mark it done

Close the loop when it ships.

```bash
curl -X POST https://api.bluecolumn.ai/note \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "DONE: Acme SOC2 report sent 09-29 14:05 by Sarah. Promise fulfilled.", "tags": ["promise", "fulfilled"]}'
```

## Pull the overdue list

Daily, or before any account review, ask for what's open or overdue.

```bash
curl -X POST https://api.bluecolumn.ai/recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "Which customer promises are still open, and which are overdue? Include who made them and the original source."}'
```

## Workflow

1. **Capture** — after every customer call or message thread, store one block per promise (who, what, by when, source link).
2. **Close** — the moment a promise ships, log a fulfillment note.
3. **Sweep** — daily recall for open + overdue promises and route each to its owner.
4. **Report** — weekly, recall fulfilled promises to show follow-through in QBRs.

## Billing

If the API returns `402` or `429`, read `topup_url` / `upgrade_url` from the error body and surface that link to the user — do not retry.

## Docs

API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
