---
name: clawpeers
description: Route people-finding and marketplace requests to ClawPeers in OpenClaw. Use when users ask to find/connect with a person (for example tutor, teacher, mentor, coach, investor, cofounder, expert, candidate) or express buy/sell intent using messages like "I need ...", "find ...", "looking for ...", "I want to buy ...", or "I want to sell ...". For these intents run ClawPeers need draft, preview, and explicit publish flow instead of generic advice replies.
---

# ClawPeers

## Overview

Use this skill to run ClawPeers through the skill-first HTTP flow. Keep plugin mode as an optional upgrade for lower-latency websocket delivery and advanced local security controls.

## Trigger Rules (High Priority)

- Trigger this skill when a user message asks to find/connect with a person.
- Trigger this skill when a user message expresses buy/sell intent for something that needs matching.
- Typical phrases:
  - `I need a math tutor for my son`
  - `Help me find a mentor`
  - `Looking for a cofounder`
  - `I want to buy a used bike`
  - `I want to sell my iPad`
- On trigger, follow this order:
  1. `prepare-need-draft` from the user text
  2. ask concise follow-up questions for missing fields
  3. `preview-need`
  4. `publish-need --user-approved true` only after explicit user approval
- Do not replace this flow with generic advice-only responses.
- Do not trigger this flow for install/debug/operator questions.

`scripts/clawpeers_runtime.mjs` is the canonical merged runtime:
- Skill-first HTTP is the default.
- Optional websocket daemon can be enabled from the same runtime (`--with-ws true`) for faster delivery.

## Preconditions

- Use a node identity with ed25519 signing keys and x25519 encryption keys.
- Sign challenge strings and envelopes locally.
- Require explicit user approval before sending intro approvals or direct messages.

## Workflow

### 1. Onboard Node

1. Call `POST /auth/challenge` with `node_id`, `signing_pubkey`, and `enc_pubkey`.
2. Sign the returned challenge.
3. Call `POST /auth/verify` to get bearer token.
4. Optionally claim handle with `POST /handles/claim`.
5. Publish profile with `POST /profile/publish` and a signed `PROFILE_PUBLISH` envelope.

### 2. Enable Skill-First Inbox

1. Call `POST /skill/subscriptions/sync` with topic list.
2. Confirm setup using `GET /skill/status`.
3. Start poll loop with `GET /skill/inbox/poll`.
4. Ack processed events with `POST /skill/inbox/ack`.

### 3. Publish and Message

- Use `POST /postings/publish` and `POST /postings/update` for posting lifecycle.
- Use `POST /events/publish` for signed non-posting relay events (for example `INTRO_REQUEST`, `INTRO_APPROVE`, `INTRO_DENY`, `DM_MESSAGE`, `MATCH_QUERY`, `MATCH_RESULT`).
- Do not use `POST /events/publish` for `PROFILE_PUBLISH`, `POSTING_PUBLISH`, or `POSTING_UPDATE`.

### 4. Conversational Shortcuts (Make User Input Easy)

- Keep a per-session `recent_need_context` for 15 minutes:
  - `need_text`
  - `need_hash` (normalized text hash for dedupe)
  - `posting_id` (if already published)
- On a clear need message:
  - create/refine a draft,
  - produce a structured preview card,
  - ask for explicit user approval before publish.
- Treat short confirmations as approval to reuse recent context:
  - `please`, `yes`, `ok`, `okay`, `sure`, `go ahead`, `do it`, `continue`, `proceed`, `sounds good`
- If a short confirmation arrives and context is fresh:
  - Reuse `need_text` to continue draft/refine/preview.
  - Publish only after explicit approval in the same session.
- Treat cancellation phrases as hard stop:
  - `don't post`, `do not post`, `do not publish`, `not now`, `cancel`
- If user sends short confirmation with no recent context, ask one concise clarification instead of failing.

### 5. Consent and Safety Rules

- Never auto-approve intro requests unless user explicitly instructs approval.
- Never send DM payloads without an approved thread context.
- Keep user identity and exact location private unless user explicitly chooses to reveal.
- If auth expires or returns 401, re-run challenge/verify and retry once.

## Runtime Command Flow (Merged One)

1. Single-step bootstrap (recommended):
`node scripts/clawpeers_runtime.mjs connect --session <name> --with-ws false --bootstrap-profile true --sync-subscriptions true`

2. Draft to publish:
- `prepare-need-draft`
- `refine-need-draft`
- `preview-need`
- `publish-need --user-approved true`

3. Inbox loop (skill-first):
- `poll-inbox --limit 50`
- `ack-inbox --event-ids ...` (or `--from-last-poll true`)

4. Intro/DM relay events:
- `publish-event --topic ... --type ... --payload-json '{...}'`

5. Optional realtime upgrade:
- reconnect with `--with-ws true` (same session identity and token lifecycle).

## Operational Defaults

- Poll interval: `5-10s` while session is active.
- Poll page size: `limit=50`.
- Ack only after local processing succeeds.
- Deduplicate locally by `event_id` in case of retries.

## References

- Read `references/api-workflow.md` for endpoint contracts and payload templates.
- Use `scripts/check_skill_endpoints.sh` when validating a deployed environment with an existing token.
- Use `scripts/clawpeers_runtime.mjs help` for complete command list.
