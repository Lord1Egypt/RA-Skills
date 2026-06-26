# Retrieval Protocol

## Purpose

This module defines how `clink-integ-skills` should retrieve facts while the skill is being developed or maintained.

## Source Of Truth

The official maintainer source is:

- `https://docs.clinkbill.com/llms-full.txt`

Download and cache that document to the fixed local path:

- `.cache/official-docs/llms-full.txt`

This cache path is for skill authors and maintainers. It is not a runtime requirement for merchants using the skill.

When the current task needs official docs, run this before reading the cache:

- `node scripts/load_official_docs.mjs`

This command:

- downloads the official docs if they are missing
- checks the last download time before every use
- automatically refreshes the cache when it is older than 7 days
- keeps using the existing cache when it is still within 7 days
- falls back to stale cache only when refresh fails and a previous cache exists

Do not read or cite `.cache/official-docs/llms-full.txt` before this freshness check step for doc-dependent tasks.

## Payment Skill Context Sources

For merchant skill for generic agent integration and merchant skill for OpenClaw integration, the current payment skill repositories are also source context.

Before generating code, generating integration guidance, or reviewing a merchant skill integration that depends on a payment skill, run the scenario-specific loader.

For OpenClaw agent review, run:

- `node scripts/load_payment_skill_contexts.mjs --dependency openclaw-payment-skills --print-path`

For generic agent review, run:

- `node scripts/load_payment_skill_contexts.mjs --dependency agentic-payment-skills --print-path`

Then read the generated context file printed by the command before checking the merchant skill implementation.

This command:

- downloads only the requested GitHub codeload zip context for `agentic-payment-skills` or `openclaw-payment-skills`
- writes the requested context file under `.cache/payment-skill-contexts/<dependency>.md`
- records source, ref, commit, and fallback status in metadata files under `.cache/payment-skill-contexts/`
- never runs `git pull` in sibling working trees and never mutates local payment skill worktrees
- falls back to sibling local skill files only when zip download fails, and marks that fallback in the metadata

Default zip download sources:

- `https://codeload.github.com/clinkbillcom/agentic-payment-skills/zip/refs/heads/main`
- `https://codeload.github.com/clinkbillcom/openclaw-payment-skills/zip/refs/heads/main`

Fallback candidate zip download sources:

- `https://codeload.github.com/clinkbillcom/agentic-payment-skill/zip/refs/heads/main`
- `https://codeload.github.com/clinkbillcom/openclaw-payment-skill/zip/refs/heads/main`

Environment overrides:

- `CLINK_AGENTIC_PAYMENT_SKILLS_URL`
- `CLINK_OPENCLAW_PAYMENT_SKILLS_URL`
- `CLINK_AGENTIC_PAYMENT_SKILLS_PATH`
- `CLINK_OPENCLAW_PAYMENT_SKILLS_PATH`

If the command reports `latestRemoteContext: false` or a fallback warning, state that the payment-skill context is not confirmed latest before relying on exact tool names, exit handling, message-routing directives, or ownership rules.

Review the merchant skill against the loaded payment skill context for correctness and completeness. For OpenClaw, verify the merchant skill integrates with `openclaw-payment-skills` contracts. For generic agent integration, verify the merchant skill or adapter integrates with `agentic-payment-skills` / `clink-payment-skill` contracts.

If the user explicitly asks to refresh or update the docs, run:

- `node scripts/refresh_official_docs.mjs --force`

If you only need the current cache status, run:

- `node scripts/refresh_official_docs.mjs --status`

## Default Sources

- `llms-full.txt`
- sections in `llms-full.txt` that correspond to quickstart, integration, API reference, and webhook behavior

## Standard Integration Retrieval

For standard integration, read the smallest useful set first:

1. quickstart content in `llms-full.txt`
2. integration content in `llms-full.txt`
3. checkout session content in `llms-full.txt`
4. refund content in `llms-full.txt`
5. API reference content in `llms-full.txt`

When webhook implementation is involved, also inspect the related webhook docs and webhook schemas.

## Agent Integration Retrieval

For merchant skill for OpenClaw integration, read:

1. the OpenClaw payment skill context from `node scripts/load_payment_skill_contexts.mjs --dependency openclaw-payment-skills --print-path`
1. overview and integration content in `llms-full.txt`
2. API reference content in `llms-full.txt`
3. local docs and schemas related to:
   - `POST /order/payment-session`
   - `GET /order/payment-session/{sessionId}`
   - `WEBHOOK customer.verify`

For merchant skill for generic agent integration, read:

1. the generic agent payment skill context from `node scripts/load_payment_skill_contexts.mjs --dependency agentic-payment-skills --print-path`
1. overview and integration content in `llms-full.txt`
2. API reference content in `llms-full.txt`
3. local docs and schemas related to:
   - `POST /order/payment-session`
   - `GET /order/payment-session/{sessionId}`
   - `WEBHOOK customer.verify`
4. the local merchant skill for generic agent integration module for runtime-contract, callback, adapter, and resume requirements

## Precision Rules

- for every task that needs official docs, run the freshness check command before reading cached docs
- refresh the cached official docs before use if the cache is older than 7 days
- if the user explicitly asks to refresh docs, force-refresh before continuing
- use the freshest cached `llms-full.txt` before naming exact endpoints, fields, schemas, or webhook events
- use the freshest available payment skill context before naming exact payment skill tools, CLI behavior, handoff ownership rules, notification directives, or review findings about `agentic-payment-skills` / `openclaw-payment-skills`
- do not infer a public API exists unless local docs support it
- if local docs are incomplete, state that clearly

## Bilingual Rule

If the user wants Chinese or bilingual output, also inspect:

- the relevant Chinese or bilingual sections available in the official docs cache
