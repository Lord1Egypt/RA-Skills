---
name: drin-send-email
description: Send a transactional email through Drin reliably. Use when the user or agent needs to send an email (notification, receipt, OTP, alert, password reset, reply) via the Drin email API — covers picking a verified sending domain, composing the message, sending it, and handling suppressed/rate-limited errors. Works through the @drin00/mcp tools, the drin CLI, the drin SDK, or the raw /v1 REST API.
version: 1.0.0
---

# Sending a transactional email with Drin

Drin sends transactional email over an HTTP API (and SMTP). You authenticate
with a single API key (`Authorization: Bearer <key>`). Use this skill any time
you need to actually deliver an email.

## 1. Pick a verified `from` domain

You can only send from a **verified** domain. Never guess the domain.

- MCP: call `list_domains` with `status: "verified"`.
- CLI: `drin domains list --status verified`.
- REST: `GET /v1/domains?status=verified`.

Use any verified domain for the `from` local part, e.g. `notifications@<domain>`.
If there are no verified domains, stop and tell the user to verify one (see the
`drin-email-best-practices` skill) — or use the shared onboarding domain, which
in test mode can only deliver to the account owner's own address.

## 2. Compose the message

Required: `from`, `to`, and content (`html` and/or `text`, **or** a `templateId`
+ `data`). Always include a `text` part alongside `html` for deliverability and
accessibility.

Addresses are objects `{ "email": "...", "name": "..." }`. The MCP tools and CLI
also accept the string form `"Name <email>"`.

## 3. Send it

- **MCP tool** `send_email`:
  ```json
  {
    "from": "Acme <notifications@acme.com>",
    "to": "user@example.com",
    "subject": "Your receipt",
    "html": "<p>Thanks for your order.</p>",
    "text": "Thanks for your order.",
    "idempotencyKey": "order-1042-receipt"
  }
  ```
- **CLI**: `drin send --from "Acme <notifications@acme.com>" --to user@example.com --subject "Your receipt" --text "Thanks"`
- **REST**:
  ```
  POST /v1/emails
  Authorization: Bearer $DRIN_API_KEY
  Content-Type: application/json
  { "from": {"email":"notifications@acme.com"}, "to": [{"email":"user@example.com"}],
    "subject": "Your receipt", "html": "<p>…</p>", "text": "…" }
  ```

A success returns `{ "id": "...", "status": "queued" }` (or `"scheduled"`). The
send is asynchronous; track delivery with `get_email`/`GET /v1/emails/:id` or
webhooks.

### Important options
- **Idempotency**: pass an `idempotencyKey` (or `Idempotency-Key` header) on
  retryable sends (receipts, OTPs). It is honored for 24h per sender, so a retry
  never double-sends.
- **Account-wide keys**: if the key is not scoped to one product, set the sender
  (`X-Drin-Sender` header / `sender` field / `DRIN_SENDER` env / `--sender`).
- **Scheduling**: set `scheduledAt` to an ISO-8601 time to send later.
- **Templates**: send `templateId` + `data` instead of inline `html`/`text` to
  render a saved template server-side.
- **Batch**: send up to 100 at once with `send_batch` / `POST /v1/emails/batch`.
- **Replies**: to answer an inbound message, use `reply_email` /
  `POST /v1/emails/:id/reply` so threading headers are set automatically.

## 4. Handle errors honestly

- `422 validation_error` — fix the payload (often `from` not on a verified
  domain, or missing content). The `param` field names the offender.
- `409 suppressed` — the recipient is on the suppression list (prior hard bounce
  or complaint). Do **not** work around it; report it. Check with
  `list_suppressions`.
- `429 rate_limited` — back off and retry after `Retry-After` seconds.
- `401 authentication_error` — the key is wrong/revoked, or an account-wide key
  was used without naming a sender.

Report the real outcome. If a send was queued, say so with the id; if it failed,
quote the error rather than claiming success.
