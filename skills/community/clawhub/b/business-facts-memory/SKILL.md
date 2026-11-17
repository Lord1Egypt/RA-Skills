---
name: business-facts-memory
description: Maintain approved prices, policies, and service details with dates and sources; flag conflicting or expired information so customer-facing agents never repeat an old price or policy. Use when agents must give dependable, current answers about a business. Requires a BlueColumn API key (bc_live_*).
---

# Verified Business Memory — BlueColumn Skill

An agent that repeats last year's price or a retired policy doesn't just annoy a customer — it creates a liability. This skill keeps one verified source of truth for prices, policies, and service details, and flags anything conflicting or expired.

## Setup

Get a free key at https://bluecolumn.ai/login (no card). Keys look like `bc_live_*`. Base URL: `https://api.bluecolumn.ai`.

## Store an approved fact

Every fact carries a date and a source, so it can be verified later.

```bash
curl -X POST https://api.bluecolumn.ai/remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "APPROVED FACT — Price: residential deep clean $189 (was $169). Effective: 2026-09-01. Source: pricing update memo 08-28, finance dept. Policy: cancellation free up to 24h before appointment; after that 50% fee. Source: terms v3.2. Service: we no longer offer carpet steam cleaning. Effective: 2026-08-15. Source: service line retirement notice.",
    "title": "verified - cleaning pricing and policies"
  }'
```

## Answer from the verified record

Customer-facing agents recall before answering, so they quote current facts.

```bash
curl -X POST https://api.bluecolumn.ai/recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "What is the current price for a residential deep clean and the current cancellation policy?"}'
```

## Flag a conflict the moment you see one

```bash
curl -X POST https://api.bluecolumn.ai/note \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "CONFLICT: website still lists deep clean at $169; verified price is $189 since 09-01. Source of conflict: /pricing page.", "tags": ["verified", "conflict", "pricing"]}'
```

## Workflow

1. **Publish** — when price, policy, or service details change, store the new fact with an effective date and source.
2. **Recall first** — agents recall the verified record before answering any customer question.
3. **Flag** — any time an agent sees information that disagrees with the verified record, log a conflict note with the source of the discrepancy.
4. **Sweep** — weekly recall for conflicts and expired facts; fix the source (website, FAQ, prompts).

## Billing

If the API returns `402` or `429`, read `topup_url` / `upgrade_url` from the error body and surface that link to the user — do not retry.

## Docs

API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
