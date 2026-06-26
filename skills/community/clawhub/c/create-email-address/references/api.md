# Crustacean Email Gateway API Reference (v1)

Base URL default: `https://api.crustacean.email/api/v1`

## Auth and registration

### POST /challenge
Request JSON:
```json
{
  "instance_id": "instance-123"
}
```

Success response fields:

* `data.challenge_nonce`
* `data.challenge.difficulty`
* `data.expires_at`

Rate limits:

* 10 requests per 10 minutes per IP
* 100 requests per day per IP

### POST /register
Request JSON:
```json
{
  "instance_id": "instance-123",
  "public_key_pem": "-----BEGIN PUBLIC KEY-----...",
  "challenge_nonce": "uuid",
  "proof": {
    "signature": "base64-signature",
    "pow": "nonce-string"
  }
}
```

Rules:

* Signature input string is exactly: `instance_id:challenge_nonce`
* PoW is accepted when SHA-256 of `instance_id|challenge_nonce|pow` has enough leading zeroes for challenge difficulty.
* Challenge is single-use.
* Existing `instance_id` registration returns HTTP 409 (`instance_already_registered`).

Rate limits:

* 1 registration per day per IP
* 1 registration per day per OpenClaw instance

Registration success includes:

* `data.mailbox`
* `data.token` (bearer token)
* `data.expires_at`

### POST /recover
Request JSON:
```json
{
  "instance_id": "instance-123",
  "challenge_nonce": "uuid",
  "proof": {
    "signature": "base64-signature",
    "pow": "nonce-string"
  }
}
```

Rules:

* Used for lost-token recovery on an already-registered `instance_id`.
* Signature input string is exactly: `instance_id:challenge_nonce`
* PoW is accepted when SHA-256 of `instance_id|challenge_nonce|pow` has enough leading zeroes for challenge difficulty.
* Challenge is single-use.
* Recovery verifies against the public key already stored for the mailbox identity.
* Recovery does not create a mailbox; it mints a new token for the existing mailbox.
* Unknown `instance_id` returns HTTP 404 (`instance_not_registered`).

Recovery success includes:

* `data.mailbox`
* `data.token` (new bearer token)
* `data.expires_at`

## Authenticated mailbox/inbox/outbox/send endpoints
Use header: `Authorization: Bearer <token>`

### GET /mailbox
Returns mailbox info (`id`, `instance_id`, `address`, `status`, etc.). `id` is the mailbox public UUID.

### GET /mailbox/forwarding
Returns current forwarding state for the authenticated mailbox.

Response includes:

* `data.forwarding_enabled` (boolean)
* `data.forward_to_email` (string or null)

### POST /mailbox/forwarding
Updates forwarding state for the authenticated mailbox.

Request JSON fields:

* `forwarding_enabled` (required boolean)
* `forward_to_email` (nullable string; required when enabling forwarding)

Rules and restrictions:

* Mailbox-token authentication is required.
* Only one forwarding destination is supported.
* There is no forwarding verification flow.
* Forwarding to the mailbox's own address is not allowed.
* Forwarding to internal service addresses is not allowed:
  * `crustacean.email`
  * subdomains like `api.crustacean.email`
* Successful update returns the updated forwarding state (`data.forwarding_enabled`, `data.forward_to_email`).
* Forwarded inbound mail is queued through the normal outbound queue.
* Forwarded mail counts against normal mailbox outbound limits.
* When outbound limits are hit, forwarded mail remains queued and is sent later as capacity allows.

### GET /inbox
Optional query:

* `status`: `unread` | `read` | `archived`
* `per_page`: integer
* `page`: integer

Returns:

* `data`: array of messages
* `meta`: pagination metadata
* `links`: pagination links

### GET /messages/{id}

Returns one inbound message. `{id}` is the message public UUID.

### POST /messages/{id}/read
Sets message status to `read`.

### POST /messages/{id}/unread
Sets message status to `unread`.

### POST /messages/{id}/archive
Sets message status to `archived`.

### POST /messages/{id}/unarchive
Sets message status to `unread`.

### GET /outbox
Optional query:

* `per_page`: integer
* `page`: integer

Returns:

* `data`: array of outbound messages
* `meta`: pagination metadata
* `links`: pagination links

### GET /outbox/{public_id}
Returns one outbound message for the authenticated mailbox.

Important id mapping:

* Outbox response field `id` is the outbound message public id.
* Use that `id` value as `{public_id}` in `GET /outbox/{public_id}`.

Outbox-visible fields (when present):

* `id`
* `status`
* `provider_message_id`
* `sent_at`
* `failed_at`
* `error_code`
* `error_message`
* `queue_reason`
* `next_eligible_at`

### POST /send
Request JSON fields:

* `to` (required array, at least 1)
* `cc` (array)
* `bcc` (array)
* `subject` (string)
* `body_text` (string, optional if `body_html` provided)
* `body_html` (string, optional if `body_text` provided)

Also currently supported by the API:

* `from_name` (optional string, max 255)

At least one of `body_text` or `body_html` is required.

Queued-send behavior:

* `POST /send` may return immediately with an outbound message in `status: queued`.
* Queued messages may later transition to `sent`.
* Queued messages may also remain queued when send caps are reached; in that case `queue_reason` and `next_eligible_at` may appear in outbox responses.

Current send limits:

* 1 message per minute per mailbox
* No more than 10 total recipients across `to`, `cc`, and `bcc` per message
* 10 messages per day per mailbox for new mailboxes less than 24 hours old
* 25 messages per day per mailbox once mailbox age is 24 hours or more
* 200 messages per day total across all mailboxes in the `crustacean.email` domain

## Error shape
```json
{
  "ok": false,
  "error": {
    "code": "machine_code",
    "message": "human-readable message"
  }
}
```

Possible rate-limit example:

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

The scripts should show errors in this format:

* `HTTP <status> <error.code>: <error.message>`

If `retry_after_seconds` is present, scripts should surface that value too.
