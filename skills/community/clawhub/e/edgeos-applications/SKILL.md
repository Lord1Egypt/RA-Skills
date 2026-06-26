---
name: edgeos-applications
description: Apply to an EdgeOS popup city and buy tickets through OpenClaw. Use when users ask to authenticate by email OTP, submit/check popup applications, retrieve accepted applications and attendees, browse active products, purchase with checkout links, or settle crypto payments via /agent/buy-ticket (x402 + USDC on Base, optional AgentKit discount).
---

# OpenClaw Popup Application (v1)

Run the EdgeOS application flow with a strict, reliable sequence:

1. Authenticate user via OTP once per session.
2. Persist and reuse JWT for all subsequent calls in that session.
3. Resolve target popup.
4. Collect required application fields.
5. Submit application.
6. Check status on demand.
7. After acceptance, guide product selection and payment.

Read these references before executing:
- `{baseDir}/references/conversation-flow.md`
- `{baseDir}/references/flow.md`
- `{baseDir}/references/api-contract.md` (API source of truth)

Before collecting fields, read workspace `USER.md` and use it as prefill context when values are relevant and trustworthy for the current user.

## Runtime configuration

This v1 skill is intentionally pinned to PROD backend values (no user setup required).
Values are defined once in:
- `{baseDir}/scripts/env.sh`

Do not ask users to configure runtime values in v1.
Use the values from `scripts/env.sh` consistently for auth and API calls.

## Script-first rule

Prefer scripts in `{baseDir}/scripts` over ad-hoc curl construction:
- `auth_request_otp.sh`
- `auth_login.sh` (persists JWT in local state file)
- `submit_application.sh`
- `check_application_status.sh` (supports `--application-id` or `--citizen-id` + `--popup-city-id`)
- `payment_preview.sh`
- `payment_create.sh`
- `payment_status.sh`
- `buy_ticket_challenge.sh` (x402 challenge from `/agent/buy-ticket`)
- `buy_ticket_submit.sh` (x402 submit with `PAYMENT-SIGNATURE`, optional `AGENTKIT`)

Only fall back to raw curl if a script cannot handle the case.

## Data collection policy (strict minimal questions)

Use this exact sequence:
1. Determine required + optional application fields.
2. Fill all required fields and all optional fields using source priority (below), taking reasonable defaults only where policy allows.
3. Ask only for required fields that are still missing after source resolution.
4. Build a full field review covering all form questions and values (required + optional), excluding only internal workflow fields like `status`.
5. For every unresolved field, ask the user and label it as required or optional.
6. After all fields are resolved (or explicitly skipped if optional), ask if the user wants changes or submit as-is; submit only after explicit approval.

### Source priority (authoritative order)
1. `USER.md` (primary source for all mappable fields)
2. Authenticated API profile/application context
3. Current session and prior user turns
4. Channel sender metadata inference

If a field is present in `USER.md`, prefer that value unless the user explicitly overrides it in the current conversation.

Additional rules:
- For names specifically, infer before asking (profile -> known identity -> sender display name parsing).
- Infer gender from pronouns/known context by default; ask only if completely unknown.
- Infer `local_resident` from known residence/location context by default (example: user based in Buenos Aires => not local resident for Edge Esmeralda).
- Treat `duration` as required and normalize it to one of: `1 week`, `1 weekend`, `2 weeks`, `a few days`, `full length`.
- Never re-ask a field that is already known unless the user asks to change it.
- Treat generic confirmations ("yes", "ok") as approval signals, not as field values.
- Infer optional booleans from user context when plausible (e.g., technical builder profile => `builder_boolean=true`; investor intent absent => `investor=false`).
- If boolean inference is not possible, ask the user (marking as optional) instead of silently defaulting.
- Do not invent personal free-text answers (e.g., goals). Ask when unknown (marking as optional).
- Required fields must always be resolved before submit.

## Session auth handling

- After successful OTP login, persist JWT using `auth_login.sh` and reuse it for all subsequent API requests.
- Runtime scripts auto-load JWT from per-email state files under `{baseDir}/scripts/.state/`.
- State is keyed by email; set `SESSION_EMAIL` when running scripts to select the correct token.
- Do not request OTP again while JWT works.
- On unauthorized responses, reload JWT from script state and retry once before asking for new OTP.
- Only re-authenticate when an API call still returns unauthorized/invalid token (401) after retry, or token is truly missing.

## Crypto payment support (x402)

When the user chooses to pay with crypto, the skill uses `POST /agent/buy-ticket` (x402 protocol).
The skill gets payment requirements from the server, provides them to the agent, and the agent
signs the USDC transfer with whatever wallet it has configured (CDP, MCP tool, etc.).
The skill does NOT handle wallet signing — it provides the data and the agent handles signing.

World ID-verified agents (via AgentKit) receive a 10% discount automatically when the
`AGENTKIT` header is included with a valid signed payload.

## Guardrails

- Never expose full OTP codes or JWTs.
- Never force server-owned status transitions.
- Never create a payment unless application status is `accepted`.
- Never submit an application for a popup that has already ended (`end_date < now`).
- Keep prompts short and ask one question at a time.
- Confirm before final submission.
- Do not show internal IDs (product IDs, popup IDs, attendee IDs, citizen IDs, payment IDs) unless the user explicitly asks.
- Present products in user-friendly terms (name, what it includes, price), then map to IDs internally.
- Never expose wallet private keys or raw transaction signatures in chat output.
- When presenting x402 payment info, show human-readable amounts (e.g. "$10.00 USDC") not atomic units.
- Convert USDC atomic amounts: divide by 1,000,000 for display (e.g. "1000000" → "$1.00").

## Outputs to return

- current `status`
- concise next step guidance
- include IDs only when operationally useful or when explicitly requested by the user

On duplicate submissions, return existing application status instead of surfacing a raw failure.
