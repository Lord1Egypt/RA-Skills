---
name: ebay-photo-lister
description: Turn a photo + one-line caption into a complete, eBay-validated draft listing — AI title/description, auto category, item specifics (incl. trading-card condition descriptors), photo upload, price from caption. The agent drives the pipeline; you approve before anything goes live.
metadata:
  category: commerce
  tags: [ebay, reselling, listings, automation]
---

# eBay Photo Lister (ListBlitz lite)

Give your agent the ability to build eBay listings from photos.

## What it does

When the user sends a photo of an item with a caption (what it is,
condition, price), the agent:

1. saves the photo(s) and builds a job JSON,
2. runs `orchestrate.py <job> --draft` — uploads photos to eBay,
   auto-picks the category, writes the title/description, infers item
   specifics, and runs eBay's own validator,
3. relays the draft to the user for approval,
4. on approval runs `orchestrate.py <job> --live --yes` and returns the
   live listing URL.

## Setup

This skill wraps the ListBlitz pipeline (not bundled — get it at the
link below and place it in your workspace as `listblitz/`). Configure
`config.env` per its SETUP.md (eBay developer keyset, Anthropic key).

Full kit — standalone Telegram bot, per-category specifics inference,
docs and support: **https://jenkinsscotty.gumroad.com/l/zmtxiu**

## Guardrails

- NEVER run `--live` without explicit user approval of the exact draft.
- If eBay verify fails, show the errors and fix the job JSON (usually a
  missing required item specific like Brand/Type) before retrying.
- Trading cards: use condition `ungraded`/`graded` — never `used`.
