# domani.run - Email Reference

Complete email operations for built-in mailboxes. See the main [SKILL.md](https://domani.run/SKILL.md) for setup and mailbox creation.

## Send email

```bash
curl -s -X POST "https://domani.run/api/domains/PROJECT_NAME.dev/email/hello/send" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "recipient@example.com",
    "subject": "Hello from my domain",
    "text": "Plain text body",
    "html": "<p>HTML body (optional)</p>"
  }'
```

**Optional fields:** `cc`, `bcc` (strings), `reply_to`, `in_reply_to` / `references` (for threading), `idempotency_key` (dedup), `attachments` (array, max 10 files, 10 MB each, 40 MB total):

```json
{
  "attachments": [
    {
      "filename": "report.pdf",
      "content": "BASE64_ENCODED_DATA",
      "content_type": "application/pdf"
    }
  ]
}
```

**Rate limit:** 100 sends/hour per mailbox.

## Read messages

```bash
# List messages (cursor pagination)
curl -s "https://domani.run/api/domains/PROJECT_NAME.dev/email/hello/messages" \
  -H "Authorization: Bearer $DOMANI_API_KEY"
# Optional params: ?direction=in|out, ?from=x, ?to=x, ?subject=x, ?cursor=x, ?limit=50

# Get a single message (full content + delivery events)
curl -s "https://domani.run/api/domains/PROJECT_NAME.dev/email/hello/messages/MSG_ID" \
  -H "Authorization: Bearer $DOMANI_API_KEY"
```

Messages include: `id`, `direction` (in/out), `from`, `to`, `cc`, `subject`, `text`, `html`, `attachments` (array with `filename`, `content_type`, `size`, `url`), `status`, `is_read`, `events`, `created_at`. Attachments have permanent download URLs.

## Message operations

```bash
# Mark messages as read (bulk, up to 100)
curl -s -X PATCH "https://domani.run/api/domains/PROJECT_NAME.dev/email/hello/messages" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ids": ["MSG_ID_1", "MSG_ID_2"], "is_read": true}'

# Delete a single message
curl -s -X DELETE "https://domani.run/api/domains/PROJECT_NAME.dev/email/hello/messages/MSG_ID" \
  -H "Authorization: Bearer $DOMANI_API_KEY"

# Bulk delete messages (up to 100)
curl -s -X DELETE "https://domani.run/api/domains/PROJECT_NAME.dev/email/hello/messages" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ids": ["MSG_ID_1", "MSG_ID_2"]}'

# Forward a message
curl -s -X POST "https://domani.run/api/domains/PROJECT_NAME.dev/email/hello/messages/MSG_ID/forward" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"to": "someone@example.com"}'

# Reply to a message (auto-threads via In-Reply-To + References)
curl -s -X POST "https://domani.run/api/domains/PROJECT_NAME.dev/email/hello/messages/MSG_ID/reply" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Thanks for your email!", "reply_all": false}'
```

## Inbound email

```bash
# Set a webhook to receive inbound emails as JSON POST
curl -s -X PUT "https://domani.run/api/domains/PROJECT_NAME.dev/email/hello" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"webhook_url": "https://your-app.com/api/inbound-email"}'

# Or forward inbound emails to a personal address
curl -s -X PUT "https://domani.run/api/domains/PROJECT_NAME.dev/email/hello" \
  -H "Authorization: Bearer $DOMANI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"forward_to": "personal@gmail.com"}'
```

## Check email health

```bash
curl -s "https://domani.run/api/domains/PROJECT_NAME.dev/email/check" \
  -H "Authorization: Bearer $DOMANI_API_KEY"
```

Returns MX propagation status, SPF record, DMARC policy, and DKIM selectors. Auto-detects the email provider.

## Message statuses

`queued` → `sent` → `delivered`. Failures: `bounced`, `failed`, `delayed`, `complained`, `suppressed`.
