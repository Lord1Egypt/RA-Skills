# Bellwire Private and Direct v2

- [Establish a device connection](#establish-a-device-connection)
- [Manifest v2](#manifest-v2)
- [Signed request](#signed-request)
- [Private outbox and wake](#private-outbox-and-wake)
- [Direct endpoint responses](#direct-endpoint-responses)
- [Conformance](#conformance)

Private is the default project mode. Bellwire stores only control-plane metadata
and an opaque wake reference; notification, Inbox, and Surface content travels
directly from the user's HTTPS service to the iPhone.

## Establish a device connection

1. Bind with the six-digit code. Bellwire returns `deviceKey` containing `id`,
   `agreementPublicKey`, `signingPublicKey`, `installationId`, and `algorithm`.
2. Store `deviceKey.id`, `deviceKey.signingPublicKey`, account/project ownership,
   and revocation state in the user's database. One row per device is required.
3. Implement all three signed HTTPS endpoints described below. If the source verifier pins one device in secrets or environment variables instead of using a trusted-key table, update `deviceKey.id` and `deviceKey.signingPublicKey` together with an atomic/bulk secret operation before publishing the manifest. A newly paired key cannot inherit the old key's verifier configuration.
4. Create a manifest v2 from
   [direct-connection.manifest.json](../assets/templates/direct-connection.manifest.json).
   It contains only public
   display identity and endpoint paths—never a bearer token, cookie, password,
   provider secret, or embedded URL credential.
5. Encrypt and publish it:

   ```bash
   node <skill-dir>/scripts/bellwire.mjs publish-direct-connection \
     --device-key-id "$BELLWIRE_DEVICE_KEY_ID" \
     --agreement-public-key "$BELLWIRE_AGREEMENT_PUBLIC_KEY" \
     --file direct-connection.json
   ```

The CLI uses ephemeral P-256 ECDH, HKDF-SHA256 with
`bellwire-direct-connection-v2`, and AES-256-GCM. The envelope declares the
plaintext Bellwire project ID and manifest version. The phone rejects a
decrypted manifest whose project ID differs, persists it in device-only
Keychain, and acknowledges the envelope. Ack atomically records readiness and
deletes the ciphertext.

If iOS later loses the locally cached manifest, it creates one idempotent
control-plane recovery request scoped to the signed-in user, project,
installation, and previously acknowledged device key. The request contains no
manifest plaintext, endpoint, credential, Event, Inbox, or Surface data. Run
`list-direct-recoveries`, rebuild the manifest from the source service's own
configuration, and publish a fresh device-encrypted envelope. Publishing that
replacement clears the pending request.

## Manifest v2

```json
{
  "version": 2,
  "connectionId": "opaque-connection-id",
  "baseUrl": "https://service.example.com",
  "project": {
    "id": "bellwire-project-uuid",
    "name": "Example",
    "icon": "bolt.fill",
    "logoUrl": "https://service.example.com/logo.png",
    "displayOrder": 10,
    "category": "automation"
  },
  "endpoints": {
    "notification": "/bellwire/v2/notification",
    "inbox": "/bellwire/v2/inbox",
    "surfaces": "/bellwire/v2/surfaces"
  },
  "capabilities": ["notification_detail", "inbox", "surfaces"]
}
```

`title` is limited to 240 characters, `body` to 1,000, and `subtitle` to 240.
`logoUrl` must be public HTTPS. `deepLink` must be HTTPS or use the Bellwire
app's configured URL scheme; embedded URL credentials are rejected.

`baseUrl` must be public HTTPS without credentials. Endpoint values are absolute
paths beginning with one `/`, and all cursor/reference values must be opaque.

## Signed request

The App sends:

```http
X-Bellwire-Connection: <connectionId>
X-Bellwire-Key-Id: <deviceKey.id>
X-Bellwire-Timestamp: <unix seconds>
X-Bellwire-Nonce: <random value>
X-Bellwire-Signature: <base64 P-256 signature>
```

The signed UTF-8 value is:

```text
METHOD
PERCENT_ENCODED_PATH_AND_QUERY
UNIX_TIMESTAMP
NONCE
LOWERCASE_SHA256_BODY_HEX
```

Use [verify-direct-request.mjs](../scripts/verify-direct-request.mjs). Resolve
connection and key ownership before verification, reject timestamps outside
five minutes, and atomically insert `keyId + nonce` under a unique database
constraint. A KV read-then-write check is unsafe. Return the same `401` for
unknown connections, revoked keys, stale timestamps, bad signatures, and replay.

## Private outbox and wake

After the real business transaction succeeds:

1. Generate at least 16 random bytes and encode them as a 22–200 character
   base64url reference.
2. In the same durable transaction, save notification detail and the reference
   with an expiry no later than 24 hours.
3. Send only `{ "reference": "...", "priority": "normal" }` to the Bellwire
   Private wake endpoint using `BELLWIRE_WAKE_TOKEN`.
4. Reuse one stable `Idempotency-Key` for all retries of that wake.

The reference must not contain an order number, email, task name, customer ID,
project name, or timestamp. The wake call should have a short timeout and be
best-effort after commit. Never fall back to a Hosted Event if it fails.

## Direct endpoint responses

Notification:

```http
GET /bellwire/v2/notification?ref=<opaque-reference>
```

Return at most 64 KB:

```json
{
  "reference": "opaque-reference",
  "eventType": "payment.success",
  "title": "Payment received",
  "body": "Creator plan renewed",
  "subtitle": "Just now",
  "occurredAt": "2026-07-25T10:00:00Z",
  "data": { "amount": "$29.99" },
  "deepLink": "https://example.com/orders/detail",
  "logoUrl": "https://example.com/logo.png"
}
```

Inbox:

```http
GET /bellwire/v2/inbox?cursor=<opaque-cursor>&limit=50
```

Return at most 1 MB with no more than 50 events:

```json
{ "events": [], "nextCursor": null }
```

Surfaces:

```http
GET /bellwire/v2/surfaces
```

Return the standard `{ "surfaces": [...] }` response, at most 1 MB. Content is
never uploaded to Bellwire Cloud.

## Conformance

Register a dedicated test device key, store its PKCS#8 P-256 private key only in
the local secret environment, seed one valid outbox reference, then run:

```bash
BELLWIRE_SIGNING_PRIVATE_KEY='<base64-pkcs8>' \
node <skill-dir>/scripts/conformance-direct.mjs \
  --manifest direct-connection.json \
  --device-key-id "$BELLWIRE_DEVICE_KEY_ID" \
  --reference "$BELLWIRE_TEST_REFERENCE"
```

Conformance validates signed access, response size, Event and typed Surface
shape, project ownership, reference equality, Inbox page size, all declared
capabilities, replayed nonce, stale timestamp, a well-formed unknown key, and
tampered query behavior. Every authentication failure must return the same
`401` status, content type, and body.
