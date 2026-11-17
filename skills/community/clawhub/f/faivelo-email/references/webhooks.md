# Faivelo webhooks

Endpoints are added at https://faivelo.com/settings/developers/webhooks?via=clawhub
(Pro and Business). Each has a signing secret `whsec_...`, shown once.

## Events

`message.received`, `message.sent` (Pro and Business), `email.delivered`,
`email.bounced`, `email.complained`, `mailbox.created`, `mailbox.deleted`,
`account.sending_paused`, `account.sending_resumed`,
`account.storage_warning`, `domain.verified`, `domain.dns_broken`,
`domain.expiring`.

## Payload

```json
{
  "id": "evt_01J8ZK3V5QXR7",
  "type": "message.received",
  "created_at": "2026-09-20T14:02:11Z",
  "data": {
    "mailbox": "support@acme.com",
    "message_id": "eaaaaab",
    "thread_id": "b",
    "folder": "INBOX",
    "from": { "name": "Dana", "address": "dana@northwind.io" },
    "to": [{ "name": "Acme Support", "address": "support@acme.com" }],
    "subject": "Question about our invoice",
    "snippet": "Hi team, ...",
    "received_at": "2026-09-20T14:02:11Z",
    "attachments": [{ "name": "invoice.pdf", "content_type": "application/pdf", "size": 48213 }]
  }
}
```

Fetch the full message with
`GET /api/v1/mailboxes/{data.mailbox}/messages/{data.message_id}`.

## Verify the signature

Header `X-Faivelo-Signature: t=<unix seconds>,v1=<hex>`. The hex is
HMAC-SHA256 of `<t>.<raw body>` keyed with the signing secret. Right after a
secret rotation the header carries two `v1` values; either may match. Reject
timestamps older than 5 minutes.

Node:

```ts
import { Faivelo, FaiveloWebhookError } from 'faivelo'

app.post('/webhooks/faivelo', express.raw({ type: 'application/json' }), async (req, res) => {
  try {
    const event = await Faivelo.webhooks.verify(
      req.body.toString('utf8'),               // raw body, not parsed JSON
      req.headers['x-faivelo-signature'] as string,
      process.env.FAIVELO_WEBHOOK_SECRET!,
    )
    res.sendStatus(200) // answer within 10 s, then do the work
    if (event.type === 'message.received') handleReply(event.data)
  } catch (e) {
    if (e instanceof FaiveloWebhookError) return res.sendStatus(400)
    throw e
  }
})
```

Python:

```python
from faivelo import verify_webhook, FaiveloWebhookError

event = verify_webhook(raw_body, headers["x-faivelo-signature"], os.environ["FAIVELO_WEBHOOK_SECRET"])
```

## Delivery rules

Answer any 2xx within 10 seconds. Failures retry with growing pauses for 24
hours. The same event can arrive twice (dedupe on `id`) and out of order
(use `created_at`). An endpoint failing for 5 days is switched off.
