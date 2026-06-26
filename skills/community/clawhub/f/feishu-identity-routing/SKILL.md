---
name: feishu-identity-routing
description: Build and use a Feishu/Lark cross-app identity master for multi-agent, multi-account routing. Use when mapping the same user across different Feishu app open_id values, resolving app-specific open_id from union_id/user_id, routing outbound actions with the correct accountId, or setting up reusable identity merge/review workflows.
---

# Feishu Identity Routing

Use this skill when a workspace needs a reusable way to:

- merge the same human across multiple Feishu apps/accounts
- store app-local `open_id` under one canonical user subject
- resolve the right `open_id` for a target `accountId` / `app_context`
- route outbound actions correctly in multi-agent setups

## What to create

Create these workspace files if missing:

- `identity/feishu-user-master.json` — canonical data store
- `identity/feishu-user-master.md` — human-readable summary

## Core rules

1. One person = one subject
2. Merge by `union_id` first, then `user_id`
3. Treat `open_id` as **app-local only**
4. Before any outbound action:
   - resolve the user subject globally
   - resolve the target app/account-specific `open_id`
   - build the provider target from that local identity

For Feishu DM routing, use:

- `accountId=<target account>`
- `target=user:<open_id>`

## Scripts

Use bundled scripts when you need deterministic updates:

- `scripts/merge_feishu_identity.js` — merge one record
- `scripts/merge_feishu_identity_batch.js` — merge many records
- `scripts/review_feishu_pending.js` — approve/reject pending merges

## When to read references

- Read `references/workflow.md` when setting up or extending the process
- Read `references/schema-example.json` when creating a new master file
- Read `references/pending-review-policy.md` when conflicts appear
- Read `references/outbound-routing-patterns.md` when implementing outbound delivery or cross-agent routing
- Read `references/examples.md` when you want concrete merge/routing examples

## Notes

- Do not hardcode a specific agent like `main` or `infoIntelOfficer` into the design.
- Model routing as: **global subject resolution → app-context identity selection → provider-specific outbound target**.
- Keep the skill reusable across future agents and Feishu accounts.
