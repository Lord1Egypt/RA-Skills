# Usage Examples

## Natural language → script actions

- “use the current openclaw identity to create a mailbox on crustacean.email”
  - `python3 scripts/register_mailbox.py`

- “recover my crustacean token”
  - `python3 scripts/recover_token.py`

- “I lost my bearer token, recover access using my current OpenClaw identity”
  - `python3 scripts/recover_token.py`

- “check my crustacean inbox”
  - `python3 scripts/get_inbox.py`


- “check my crustacean outbox”
  - `python3 scripts/get_outbox.py`

- “show queued outbound messages”
  - `python3 scripts/get_outbox.py --json`
  - then filter where `data[].status == "queued"`

- “check whether my last email has been sent”
  - `python3 scripts/get_outbox.py --per-page 1`

- “show outbound message 550e8400-e29b-41d4-a716-446655440000”
  - `python3 scripts/get_outbox.py --message-id 550e8400-e29b-41d4-a716-446655440000`

- “show message 550e8400-e29b-41d4-a716-446655440000”
  - `python3 scripts/get_inbox.py --message-id 550e8400-e29b-41d4-a716-446655440000`

- “forward this mailbox to me”
  - `python3 scripts/configure_forwarding.py --enable --forward-to-email me@example.com`

- “enable forwarding to me@example.com”
  - `python3 scripts/configure_forwarding.py --enable --forward-to-email me@example.com`

- “change forwarding to other@example.com”
  - `python3 scripts/configure_forwarding.py --enable --forward-to-email other@example.com`

- “remove the forwarding email”
  - `python3 scripts/configure_forwarding.py --disable`

- “disable mailbox forwarding”
  - `python3 scripts/configure_forwarding.py --disable`

- “show my forwarding settings”
  - `python3 scripts/configure_forwarding.py`

- “mark message 550e8400-e29b-41d4-a716-446655440000 as read”
  - `python3 scripts/update_message_status.py 550e8400-e29b-41d4-a716-446655440000 read`

- “archive message 550e8400-e29b-41d4-a716-446655440000”
  - `python3 scripts/update_message_status.py 550e8400-e29b-41d4-a716-446655440000 archive`

- “send an email to alice@example.com with subject Hello and body Hi there”
  - `python3 scripts/send_message.py --to '["alice@example.com"]' --subject 'Hello' --body-text 'Hi there'`

- “send an html email to alice@example.com”
  - `python3 scripts/send_message.py --to '["alice@example.com"]' --subject 'Hello' --body-html '<p>Hi there</p>'`

- “send an email as Claw Agent Email to alice@example.com”
  - `python3 scripts/send_message.py --to '["alice@example.com"]' --from-name 'Claw Agent Email' --subject 'Hello' --body-text 'Hi there'`

## Useful overrides

Use a different identity file:
```bash
python3 scripts/register_mailbox.py \
  --identity-path /tmp/custom-device.json
```

Use a different API base:
```bash
python3 scripts/get_mailbox.py \
  --api-base https://api.crustacean.email/api/v1
```

Use a different token file:
```bash
python3 scripts/get_inbox.py \
  --token-path /tmp/crustacean-token.json
```

## JSON output mode for tool chaining
```bash
python3 scripts/get_inbox.py --json
python3 scripts/get_outbox.py --json
python3 scripts/configure_forwarding.py --json
python3 scripts/send_message.py \
  --to '["alice@example.com"]' --body-text 'Ping' --body-html '<p>Ping</p>' --json
```

## Rate limit examples

Challenge rate limit example:

```json
{
  "ok": false,
  "error": {
    "code": "rate_limited",
    "message": "Too many challenge requests from this IP. Try again later.",
    "retry_after_seconds": 483
  }
}
```

Register rate limit example:

```json
{
  "ok": false,
  "error": {
    "code": "rate_limited",
    "message": "This IP has reached the daily registration limit.",
    "retry_after_seconds": 86119
  }
}
```

Send rate limit example:

```json
{
  "ok": false,
  "error": {
    "code": "rate_limited",
    "message": "This mailbox can only send one message per minute.",
    "retry_after_seconds": 60
  }
}
```

Agent behavior for these cases:

* Report the API error code and message clearly.
* If `retry_after_seconds` is present, tell the user how long to wait.
* Do not retry immediately when the API has already rate-limited the request.
