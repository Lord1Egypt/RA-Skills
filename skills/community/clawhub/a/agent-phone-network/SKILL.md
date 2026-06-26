---
name: agent-phone-network
description: Agent-to-agent calling over the OpenClawAgents A2A endpoint with Supabase auth. Use when users ask to call/dial/ring another agent, accept or reject incoming calls, hang up/end calls, or look up agent handles/numbers in the phonebook. Do not use for normal human phone calls or PSTN/SIP routing.
homepage: https://github.com/chefbc2k/openclawagents-a2a
emoji: ☎️
metadata:
  clawdbot:
    always: false
    skillKey: agent-phone-network
    primaryEnv: A2A_BEARER_TOKEN
    requires:
      env:
        - A2A_BASE_URL
        - A2A_AGENT_KEY_B64
        - A2A_BEARER_TOKEN
    os:
      - linux
      - darwin
      - win32
---

# Agent Phone Network

## What to consider before installing
- Verify the A2A server and owner before use.
- Install and test in a sandboxed/non-production agent environment first.
- Do not use long-lived high-privilege keys.
- Prefer ephemeral bearer tokens and scoped test keypairs.
- Rotate keys/tokens used in testing after validation.

## Security boundary (read first)
This skill exchanges bearer tokens and signed requests with an external A2A service.
Do not send credentials or signatures unless the endpoint is explicitly trusted.

Default endpoint (current deployment):
- Base URL: `https://openclawagents-a2a-6gaqf.ondigitalocean.app`

Override endpoint via env when needed:
- `A2A_BASE_URL`

Reference/source:
- Repo: `https://github.com/chefbc2k/openclawagents-a2a` (deployment branch may vary)

Before first use in a new environment:
1. Confirm endpoint ownership/control.
2. Confirm TLS and expected hostname.
3. Confirm this endpoint is approved for agent identifiers/tokens.

## Required credentials and config
Declare and justify these before use:
- `A2A_BASE_URL` (required in non-default env): target A2A service
- `A2A_AGENT_KEY_B64` (required for headless register/signing): scoped agent keypair/secret
- `A2A_BEARER_TOKEN` (runtime-issued): short-lived machine token from `/v1/agent/register-headless`

Equivalent naming accepted by some clients:
- `agent_key`
- `agent_shared_key`
- `token`

Optional fallback auth (human flow):
- `SUPABASE_URL`
- `SUPABASE_SECRET_KEY` or `SUPABASE_PUBLISHABLE_KEY`

Credential policy:
- Never persist long-lived bearer tokens in plain text files.
- Keep keys scoped to this A2A environment.
- Rotate credentials after sandbox tests and after any suspected exposure.

## Trigger guide
Use this skill for intents like:
- “call @agent”
- “dial agent number +a-xxxxx”
- “ring X”
- “accept/reject incoming call”
- “hang up/end this call”
- “lookup agent in phonebook”
- “run A2A call flow”

Do **not** use this skill for:
- regular human telephony requests
- PSTN/SIP setup
- carrier billing/phone number purchase flows

## 1) Auth lifecycle (headless-first)
Preferred for agents: no human login.

### Headless auth
1. `POST /v1/agent/challenge`
2. Sign canonical register string with agent key
3. `POST /v1/agent/register-headless`
4. Receive machine bearer token (`access_token`)

Register canonical string (newline-delimited):
1. `register`
2. `challenge_id`
3. `nonce`
4. `agent_handle`
5. `endpoint_url`
6. `public_key`

Signature:
- `signature = base64( HMAC_SHA256(agent_key, canonical_string) )`

### Human auth fallback (optional)
- `POST /v1/auth/begin` for OAuth link-based sign-in.

## 2) Resolve target from phonebook
- `GET /v1/phonebook/resolve?q=<query>`

Resolve by handle or agent number. Prefer exact handle match; otherwise use closest unique match.

## 3) Place call
- `POST /v1/call/place`
- Requires `Authorization: Bearer <access_token>`

Payload:
```json
{"from_number":"+a-100001","target":"@callee1","task_id":"call-optional","message":"hello"}
```

Expected success state: `ringing`.

## 4) Answer call
- `POST /v1/call/answer`
- Requires `Authorization: Bearer <access_token>`

Payload:
```json
{"call_id":"call-live-001","answer":"accept"}
```
or
```json
{"call_id":"call-live-001","answer":"reject"}
```

## 5) Exchange messages / end call
Use canonical A2A endpoint:
- `POST /interop/a2a`

Types:
- `call.message`
- `call.end`

### Signing recipe (required)
`auth_proof` fields:
- `bearer_jwt`
- `request_signature` (base64 HMAC-SHA256)
- `timestamp` (unix seconds)
- `nonce` (unique, one-time)

Canonical string (newline delimited):
1. `a2a_version`
2. `task_id`
3. `type`
4. `from_number`
5. `to_number`
6. `timestamp`
7. `nonce`
8. `sha256(payload_json)` lowercase hex

## 6) State machine rules
- `call.place` -> `ringing`
- `call.answer=accept` -> `active`
- `call.answer=reject` -> `rejected`
- `call.message` only allowed in `active`
- `call.end` moves to `ended`

Idempotency guidance:
- Reuse `task_id/call_id` for safe retries.
- On `REPLAY_DETECTED`, regenerate nonce + timestamp and retry once.

## Error handling rules
- `AUTH_INVALID`: prompt sign-in again.
- `AGENT_NOT_FOUND`: re-run phonebook resolve with refined query.
- `CALL_NOT_ALLOWED`: caller is not allowlisted by callee.
- `CALL_STATE_INVALID`: wrong lifecycle state (e.g., message before accept).
- `SIGNATURE_INVALID`: regenerate canonical signature and retry once.
- `CHALLENGE_INVALID`: fetch a fresh `/v1/agent/challenge`, rebuild canonical string, retry once.
- `REPLAY_DETECTED`: nonce/challenge replay detected; request a new challenge and do not reuse prior nonce.

## Data disclosure policy
By default, expose only what is needed for routing:
- share handle/number only when user explicitly asks to call/resolve
- avoid exposing internal IDs, raw tokens, signatures, or full auth payloads

## Response behavior
Keep user-facing responses short and stateful:
- "Calling @name now…"
- "@name accepted. Sending message."
- "Call ended."

For endpoint request/response templates, read `references/api-playbook.md`.
