---
name: drin-agent-inbox
description: Run an autonomous email inbox with Drin — receive inbound email on a domain, read conversation threads, and reply in-thread. Use when building or operating an agent that must read and respond to email (support triage, scheduling, an "email me to do X" interface), set up inbound receiving, test the receive pipeline, or process new inbound messages and act on them.
version: 1.0.0
---

# Operating an agent email inbox with Drin

Drin is bidirectional: besides sending, a domain can **receive** email, which
Drin parses into conversation **threads** your agent can read and reply to. This
is the foundation for an agent you can email.

## 1. Enable receiving on a domain

- Turn it on: `set_domain_receiving` with `enabled: true` (or
  `PATCH /v1/domains/:id/receiving`). Drin returns the **MX record(s)** to
  publish.
- Publish the MX record(s) in DNS. Until they propagate, no inbound arrives.
- Verify with `get_domain_receiving` / `GET /v1/domains/:id/receiving`.

The domain must already be verified for sending (see `drin-email-best-practices`)
so the agent can also reply.

## 2. Create an inbox (a receive address)

- `create_inbox` with `{ address: "support@acme.com", domainId: "<id>" }`
  (or `POST /v1/inboxes`). This is the address people email to reach the agent.
- List existing ones with `list_inboxes`.

## 3. Read inbound — threads, not raw mailboxes

Inbound and outbound messages are joined into threads.

- `list_threads` (optionally `inboxId`) — most-recent-first feed. Each thread has
  a `lastMessageAt` and subject.
- `get_thread` with the thread id — the full conversation, oldest→newest, both
  directions, including each message's `direction`, `from`, `to`, `subject`, and
  status.
- For a single message's full content: `get_email` (detail/lifecycle),
  `get_email_body` (the archived `{ html, text }`), and
  `list_email_attachments` (download bytes via the authenticated `url`).

Two ways to know when new mail arrives:
- **Poll**: periodically `list_threads` and diff against the last id/timestamp
  you processed.
- **Webhook (preferred for real-time)**: register a webhook for the inbound
  events with `create_webhook`
  (`drin webhooks create --url <url> --event inbound_received` / `POST /v1/webhooks`);
  Drin POSTs a signed payload when mail is received, and returns a `signingSecret`
  ONCE on creation. Verify the signature (`drin.webhooks.verify` in the SDK)
  before trusting it.

## 4. Decide, then reply in-thread

For each new inbound message:

1. Read the body (`get_email_body`) and any attachments.
2. Decide what to do (answer, take an action with other tools, escalate).
3. Reply **on the thread** so the recipient's client keeps the conversation
   together: `reply_email` with `{ messageId: "<inbound id>", text: "...", html: "..." }`
   (or `POST /v1/emails/:id/reply`). Drin sets `In-Reply-To`/`References` and the
   `Re:` subject automatically; `from` defaults to the inbox address and `to` to
   the original sender.

Keep a record of which message ids you've already handled so you never reply
twice (idempotency). When replying to action requests, pass an `idempotencyKey`.

## 5. Test without real email

Use the simulator to exercise the whole receive → thread → (webhook) path safely:

- `simulate_inbound` with `{ to: "support@acme.com", from: "Customer <c@example.com>", subject: "Help", text: "..." }`
  (or `POST /v1/inbound/simulate`). The synthesized message is flagged
  `test_mode` (excluded from metrics/billing) but flows through ingest, threads,
  and any webhooks exactly like a real one — so you can build and verify the
  agent loop before pointing real DNS at it.

## Minimal agent loop (pseudocode)

```
seen = load_processed_ids()
for thread in list_threads(inboxId):
    convo = get_thread(thread.id)
    for msg in convo.messages where msg.direction == "inbound" and msg.id not in seen:
        body = get_email_body(msg.id)
        action = decide(convo, body)          # your agent's reasoning
        reply_email(messageId=msg.id, text=action.reply, idempotencyKey=msg.id)
        seen.add(msg.id)
save_processed_ids(seen)
```

Always honor suppressions and never reply to mail you can't authenticate as
genuinely inbound (verify webhook signatures).
