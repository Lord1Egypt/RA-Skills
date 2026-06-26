---
name: agentref
description: Use AgentRef's REST API from OpenClaw or any HTTP runtime for merchant onboarding, programs, affiliates, conversions, flags, and payouts; authenticate with AGENTREF_API_KEY, start with GET /api/v1/me, prefer safe reads, and confirm state-changing writes before sending them.
homepage: https://github.com/LukasvanUden/agentref
metadata: {"openclaw":{"homepage":"https://github.com/LukasvanUden/agentref","requires":{"env":["AGENTREF_API_KEY"]},"primaryEnv":"AGENTREF_API_KEY"}}
---

# AgentRef REST

Use this skill when the user wants to inspect or operate AgentRef over HTTP instead of MCP, especially from OpenClaw or other REST-first runtimes.

## Connection contract

- Base URL: `https://www.agentref.co/api/v1`
- Every request needs `Authorization: Bearer <AGENTREF_API_KEY>`
- Never print, log, echo, or persist the raw API key in chat output, files, traces, or examples
- Success responses use `{ data, meta }`
- Error responses use `{ error, meta }`
- When a request fails, surface the failing endpoint plus `meta.requestId`

## First request

1. Call `GET /api/v1/me`
2. Read `data.key.ownerType`, `data.key.keyType`, `data.key.scopes`, and the returned owner/program context
3. If `ownerType` is `affiliate`, do not use the merchant-admin endpoints below; say so clearly and only pivot to affiliate `/api/v1/me/*` reads if the user explicitly wants affiliate self-service

## Credential guidance

- Prefer a dedicated AgentRef key for this skill instead of reusing a broad personal key
- Default to the smallest scope set that fits the task
- For inspection-only use, prefer read-only merchant scopes
- Only use write-capable scopes such as program changes, affiliate moderation, flag resolution, or payouts when the user explicitly needs those actions
- If the user only needs affiliate self-service, use an affiliate key instead of a merchant key

## Operating rules

- Safe reads first: inspect current state with `GET` before proposing or sending writes
- Never invent endpoints, fields, or state transitions; use only the curated references in this bundle
- Ask for clear user confirmation before any action that creates, updates, archives, approves, blocks, resolves, or pays out
- When a documented write supports it, send an `Idempotency-Key` header
- Follow pagination from `meta.nextCursor` or `page` and `pageSize`; do not guess hidden pages
- Reuse IDs already returned by prior reads instead of searching again

## Reference map

- Core REST surface: [references/endpoints.md](references/endpoints.md)
- Intent-oriented call sequences: [references/workflows.md](references/workflows.md)

Load only the section needed for the current task. Keep the active prompt lean.
