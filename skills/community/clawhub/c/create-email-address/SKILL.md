---
name: crustacean-email-gateway
description: use this skill when you need to register an openclaw identity with crustacean email gateway, recover a lost bearer token for an already-registered instance, save or reuse its bearer token, check mailbox, inbox, or outbox, update read or unread or archive status, configure mailbox forwarding, or send outbound email through the api.
---

# Crustacean Email Gateway Skill

Use this skill when the user asks to manage email for an OpenClaw instance through Crustacean Email Gateway.

## Defaults
- API base: `https://api.crustacean.email/api/v1`
- Identity file: `/root/.openclaw/identity/device.json`
- Local token file: `~/.crustacean-email/token.json`

These can be overridden with script flags or env vars:
- `CRUSTACEAN_API_BASE`
- `OPENCLAW_IDENTITY_PATH`
- `CRUSTACEAN_TOKEN_PATH`

## Quick workflow
1. **Register first** (challenge-response + PoW + signature):
    - `python3 scripts/register_mailbox.py`
2. **Lost token recovery** (already-registered instance, challenge-response + PoW + signature):
    - `python3 scripts/recover_token.py`
3. **Mailbox lookup**:
    - `python3 scripts/get_mailbox.py`
4. **Inbox list**:
    - `python3 scripts/get_inbox.py`
5. **Inbox message detail**:
    - `python3 scripts/get_inbox.py --message-id 550e8400-e29b-41d4-a716-446655440000`
6. **Outbox list**:
    - `python3 scripts/get_outbox.py`
7. **Outbox message detail**:
    - `python3 scripts/get_outbox.py --message-id 550e8400-e29b-41d4-a716-446655440000`
8. **Status update**:
    - `python3 scripts/update_message_status.py 550e8400-e29b-41d4-a716-446655440000 read`
9. **Forwarding settings**:
    - Show forwarding: `python3 scripts/configure_forwarding.py --json`
    - Enable or update forwarding destination: `python3 scripts/configure_forwarding.py --enable --forward-to-email me@example.com`
    - Disable forwarding: `python3 scripts/configure_forwarding.py --disable`
10. **Send**:
    - `python3 scripts/send_message.py --to '["alice@example.com"]' --subject 'Hello' --body-text 'Hi there'`
    - HTML body example: `python3 scripts/send_message.py --to '["alice@example.com"]' --subject 'Hello' --body-html '<p>Hi there</p>'`
    - Optional sender display name: `--from-name 'Claw Agent Email'`

## Agent behavior rules
- Always attempt token-backed calls using the saved token file.
- If the token file is missing for an already-registered instance, use `recover_token.py`.
- If the token file is missing and the instance has never been registered, use `register_mailbox.py`.
- On API failure, report HTTP status + `error.code` + `error.message`.
- If the API returns `rate_limited`, report the `retry_after_seconds` value clearly.
- Treat outbound message `id` as the public id used by `GET /outbox/{id}`.
- For queued outbound messages, explain that delivery can happen later when limits allow.
- Use `configure_forwarding.py` when the user asks to show, enable, change, remove, or disable mailbox forwarding.
- Forwarding uses mailbox-token auth, supports only one destination, and has no verification flow.
- Forwarding to the same mailbox address or any `crustacean.email` address/subdomain is not allowed.
- Forwarded inbound mail is queued through normal outbound send and counts against normal outbound limits.
- Summarize successful responses in concise human-readable bullet points.
- Never request or mention IMAP or SMTP credentials.

## Registration implementation contract
The registration script must:
1. Read OpenClaw identity JSON.
2. POST `/challenge` with `instance_id`.
3. Solve PoW using server difficulty with hash input:
    - `instance_id|challenge_nonce|pow`
4. Sign exact message string:
    - `instance_id:challenge_nonce`
5. POST `/register` with:
    - `instance_id`
    - `public_key_pem`
    - `challenge_nonce`
    - `proof.signature`
    - `proof.pow`
6. Save bearer token + metadata locally for reuse.

## Recovery implementation contract
The recovery script must:
1. Read OpenClaw identity JSON.
2. POST `/challenge` with `instance_id`.
3. Solve PoW using server difficulty with hash input:
    - `instance_id|challenge_nonce|pow`
4. Sign exact message string:
    - `instance_id:challenge_nonce`
5. POST `/recover` with:
    - `instance_id`
    - `challenge_nonce`
    - `proof.signature`
    - `proof.pow`
6. Save refreshed bearer token + metadata locally for reuse.

## Current limits
- Challenge:
    - 10 requests per 10 minutes per IP
    - 100 requests per day per IP
- Register:
    - 1 registration per day per IP
    - 1 registration per day per OpenClaw instance
- Send:
    - 1 message per minute per mailbox
    - No more than 10 recipients (to + cc + bcc) per message
    - 10 messages per day per mailbox for new mailboxes (registered less than 24 hours ago)
    - 25 messages per day per mailbox once mailbox age is 24 hours or more
    - 200 messages total per day from all mailboxes in the `crustacean.email` domain
    - `POST /send` may return an outbound message with `status=queued` immediately; outbox status can later become `sent`, or remain queued when send caps are hit.
    - Note: these limits are subject to change as the product evolves.

## Limitations (current)
- One mailbox per OpenClaw instance.
- `crustacean.email` domain only.
- Token refresh exists when caller still has a valid bearer token.
- No attachments.

## References
- API contract and payload shapes: `references/api.md`
- Usage patterns and natural language mapping: `references/examples.md`
