---
name: agent-resume
description: Save a structured checkpoint of an agent's work before a restart or model change — completed work, unfinished tasks, decisions, blockers, next steps — and restore it into the next session. Use when an OpenClaw operator or team needs continuity across agent restarts, model swaps, or context resets. Requires a BlueColumn API key (bc_live_*).
---

# Agent Resume — BlueColumn Skill

Paying an agent to rediscover its own work is the most expensive line item on the bill. This skill checkpoints an agent's state before any restart, model change, or context wipe, then restores it cleanly into the next session.

## Setup

Get a free key at https://bluecolumn.ai/login (no card). Keys look like `bc_live_*`. Base URL: `https://api.bluecolumn.ai`.

## Save a checkpoint

Before any restart, model swap, or context reset, store the state that matters.

```bash
curl -X POST https://api.bluecolumn.ai/remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "AGENT CHECKPOINT 2026-09-29 17:50 — Project: client onboarding automation. Completed: scraper for CRM import, field mapping docs, test run on 3 accounts (all pass). Unfinished: webhook retry logic (50% done), rate-limit handling (not started). Decisions: using Redis for retry queue, not Postgres; webhook signature = HMAC-SHA256. Blockers: staging webhook URL needs whitelisting by client IT (ticket #441). Next: finish retry logic, then ask client to whitelist staging URL.",
    "title": "agent-resume - client onboarding automation - 09-29"
  }'
```

## Restore into the next session

On a fresh session, pull the latest checkpoint first thing.

```bash
curl -X POST https://api.bluecolumn.ai/recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "What is the latest agent checkpoint and what was in progress, decided, blocked, and next?"}'
```

## Log small decisions mid-run

Capture a decision the moment it happens, so it survives the next wipe.

```bash
curl -X POST https://api.bluecolumn.ai/note \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Decision: retry queue uses Redis Streams, consumer group per tenant. Do not use Postgres SKIP LOCKED.", "tags": ["agent-resume", "decision"]}'
```

## Workflow

1. **Checkpoint trigger** — before `restart`, `model change`, `context reset`, or when the agent is told to "hand off".
2. **Save** — completed work, unfinished work, decisions, blockers, and next steps as one structured block.
3. **Restore** — new session recalls the latest checkpoint first, before doing anything else.
4. **Verify** — after restore, the agent states "resuming from checkpoint: <project>, next: <next step>" so the operator can confirm continuity.

## Billing

If the API returns `402` or `429`, read `topup_url` / `upgrade_url` from the error body and surface that link to the user — do not retry.

## Docs

API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
