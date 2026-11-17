# Mailfully webhooks

How to receive delivery events from Mailfully and verify that they really came from Mailfully.

## Creating an endpoint

- The user creates the endpoint in the dashboard: Webhooks, then Add webhook. They enter the public
  HTTPS URL of the app's handler and pick the events.
- The dashboard shows the signing secret (`whsec_…`) once, right after the endpoint is created. The
  user pastes it into the app's env file as `MAILFULLY_WEBHOOK_SECRET`. The agent never sees it, never
  prints it and never writes it into a file.
- Webhook management needs a dashboard session. An API key cannot create an endpoint:
  `POST /v1/webhooks` (and the SDK's `mailfully.webhooks.create({ url, events })`) answer a key with
  403 `insufficient_scope`. So the agent writes the handler, and the user registers its URL.

## Event names

Subscribe to these names exactly:

| Event | Sent when |
| --- | --- |
| `email.delivered` | The recipient's mail server accepted the message. |
| `email.bounced` | The message hard-bounced. Details are in `data.bounce`. |
| `email.complained` | The recipient marked the message as spam. Details are in `data.complaint`. |
| `email.failed` | The message was rejected while it was being sent and will not be sent. A message refused before that fires no event: it ends with `last_event` `failed` or `rejected` on `GET /v1/emails/{id}`, so read `last_event` to catch every failure. |
| `email.delivery_delayed` | Delivery is delayed. The message may still be delivered. |
| `email.opened` | The recipient opened the message (only when open tracking is on). |
| `email.clicked` | The recipient clicked a tracked link. |
| `email.received` | A domain with receiving turned on got an inbound message. |
| `email.suppressed` | Subscribable, but not delivered today. Do not build on it. |
| `email.unsubscribed` | Subscribable, but not delivered today. Use the dashboard's opt-out list instead. |

Every event body is JSON shaped `{ "type", "created_at", "data" }`. For message events `data` holds
`email_id`, `from`, `to`, `subject`, `created_at` and `tags`, plus the event's own details.

## Headers

Each delivery carries three headers:

- `webhook-id`: a stable id for the event. Delivery is at least once, so the same event can arrive
  more than once. Store the ids you have processed and skip a repeat.
- `webhook-timestamp`: Unix seconds when the delivery was signed. Reject anything more than 300
  seconds from now.
- `webhook-signature`: one or more space-separated `v1,<base64>` tokens. Accept the delivery when any
  `v1` token matches.

Answer with any 2xx quickly, and do slow work after responding.

## Verify the raw body

Verify the RAW request body, exactly as received. Never verify `JSON.stringify(req.body)` or any
other re-serialized JSON: key order and whitespace change and the signature no longer matches.

- Next.js (App Router): `await req.text()`.
- Next.js (Pages Router): export `config = { api: { bodyParser: false } }` from the route, then
  read the raw bytes from `req` yourself. With the default parser on, the raw body is already gone.
- Express: mount `express.raw({ type: "application/json" })` on the webhook route only.
- Flask: `request.get_data()`.

Do not use a stock Svix or Standard Webhooks library. Mailfully secrets are `whsec_` followed by
base64url (43 characters, no padding), and those libraries decode standard base64, so they reject most
real Mailfully secrets. Use the verifiers below.

## Node verifier

Save as `lib/mailfully-webhook.js` in an ESM project, or `lib/mailfully-webhook.mjs` otherwise. In a
TypeScript project, save it as `lib/mailfully-webhook.ts` and type the parameters. It needs Node's
`crypto` and nothing else.

<!-- test:webhook-verifier-node -->
```js
import { createHmac, timingSafeEqual } from "node:crypto";

const TOLERANCE_SEC = 300;
/** A real secret decodes to 32 bytes. An unset, empty or cut-short one must never verify anything. */
const MIN_KEY_BYTES = 32;

// Mailfully secrets are `whsec_` + base64url. Svix and Standard Webhooks libraries expect standard
// base64 and reject most of them, so decode by hand. Standard base64 is accepted too.
function decodeKey(secret) {
  const raw = secret.startsWith("whsec_") ? secret.slice("whsec_".length) : secret;
  const b64url = raw.replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  return Buffer.from(b64url, "base64url");
}

/**
 * True when the delivery is authentic and fresh.
 * headers: an object with lowercase keys `webhook-id`, `webhook-timestamp`, `webhook-signature`.
 * rawBody: the request body exactly as received (string or Buffer).
 */
export function verifyMailfullyWebhook({ secret, headers, rawBody, nowSec }) {
  const id = headers["webhook-id"];
  const timestamp = headers["webhook-timestamp"];
  const signature = headers["webhook-signature"];
  if (!id || !timestamp || !signature) return false;

  // HMAC takes a key of any length, so an empty or short key would verify a delivery forged with it.
  const key = decodeKey(String(secret ?? ""));
  if (key.length < MIN_KEY_BYTES) return false;

  const now = nowSec ?? Math.floor(Date.now() / 1000);
  const ts = Number(timestamp);
  if (!Number.isFinite(ts) || Math.abs(now - ts) > TOLERANCE_SEC) return false;

  const expected = createHmac("sha256", key)
    .update(`${id}.${timestamp}.${rawBody}`)
    .digest();

  for (const token of String(signature).split(" ")) {
    if (!token.startsWith("v1,")) continue;
    const given = Buffer.from(token.slice(3), "base64");
    if (given.length === expected.length && timingSafeEqual(given, expected)) return true;
  }
  return false;
}
```

Next.js route handler. It pins the Node.js runtime: the verifier needs Node's `crypto`, which the
edge runtime does not have.

```ts
// app/api/webhooks/mailfully/route.ts
import { verifyMailfullyWebhook } from "@/lib/mailfully-webhook";

export const runtime = "nodejs";

export async function POST(req: Request): Promise<Response> {
  const secret = process.env.MAILFULLY_WEBHOOK_SECRET;
  if (!secret) return new Response("webhook secret not configured", { status: 500 });

  const rawBody = await req.text();
  const headers = {
    "webhook-id": req.headers.get("webhook-id") ?? "",
    "webhook-timestamp": req.headers.get("webhook-timestamp") ?? "",
    "webhook-signature": req.headers.get("webhook-signature") ?? "",
  };
  if (!verifyMailfullyWebhook({ secret, headers, rawBody })) {
    return new Response("invalid signature", { status: 401 });
  }

  const event = JSON.parse(rawBody) as { type: string; data: Record<string, unknown> };
  // Skip the event if headers["webhook-id"] was already processed, then handle event.type.
  console.log("mailfully event", event.type);
  return new Response(null, { status: 204 });
}
```

Express route (Node's `req.headers` keys are already lowercase). Register this route before any global
`app.use(express.json())`: a JSON parser that runs first consumes the body, and every delivery then
fails verification. Every route here answers 500 when `MAILFULLY_WEBHOOK_SECRET` is unset or empty,
before it reads the body; the verifiers also refuse a key under 32 bytes, so a missing secret can
never let a forged delivery through.

```js
import express from "express";
import { verifyMailfullyWebhook } from "./lib/mailfully-webhook.js";

const app = express();

app.post("/webhooks/mailfully", express.raw({ type: "application/json" }), (req, res) => {
  const secret = process.env.MAILFULLY_WEBHOOK_SECRET;
  if (!secret) return res.status(500).send("webhook secret not configured");

  const rawBody = req.body.toString("utf8");
  const ok = verifyMailfullyWebhook({ secret, headers: req.headers, rawBody });
  if (!ok) return res.status(401).send("invalid signature");
  const event = JSON.parse(rawBody);
  // Skip the event if req.headers["webhook-id"] was already processed, then handle event.type.
  console.log("mailfully event", event.type);
  return res.status(204).end();
});
```

## Python verifier

Save as `mailfully_webhooks.py`. Standard library only.

<!-- test:webhook-verifier-python -->
```python
import base64
import hashlib
import hmac
import time

TOLERANCE_SEC = 300
# A real secret decodes to 32 bytes. An unset, empty or cut-short one must never verify anything.
MIN_KEY_BYTES = 32


def _decode_key(secret):
    # Mailfully secrets are "whsec_" + base64url with no padding. Map the alphabet and restore the
    # padding before decoding; standard base64 is accepted too.
    raw = secret[len("whsec_"):] if secret.startswith("whsec_") else secret
    raw = raw.replace("+", "-").replace("/", "_").rstrip("=")
    raw += "=" * (-len(raw) % 4)
    return base64.urlsafe_b64decode(raw)


def verify_mailfully_webhook(secret, headers, raw_body, now_sec=None):
    """True when the delivery is authentic and fresh.

    headers: a mapping with the keys webhook-id, webhook-timestamp, webhook-signature.
    raw_body: the request body exactly as received (bytes or str).
    """
    msg_id = headers.get("webhook-id")
    timestamp = headers.get("webhook-timestamp")
    signature = headers.get("webhook-signature")
    if not msg_id or not timestamp or not signature:
        return False

    # HMAC takes a key of any length, so an empty or short key would verify a delivery forged with it.
    key = _decode_key(secret or "")
    if len(key) < MIN_KEY_BYTES:
        return False

    now = int(time.time()) if now_sec is None else now_sec
    try:
        ts = int(timestamp)
    except ValueError:
        return False
    if abs(now - ts) > TOLERANCE_SEC:
        return False

    if isinstance(raw_body, str):
        raw_body = raw_body.encode()
    signed = f"{msg_id}.{timestamp}.".encode() + raw_body
    expected = hmac.new(key, signed, hashlib.sha256).digest()

    for token in signature.split(" "):
        if not token.startswith("v1,"):
            continue
        try:
            given = base64.b64decode(token[3:])
        except ValueError:
            continue
        if hmac.compare_digest(given, expected):
            return True
    return False
```

Flask route (Flask's `request.headers` is case-insensitive, so it can be passed straight in):

```python
import json
import os

from flask import Flask, request

from mailfully_webhooks import verify_mailfully_webhook

app = Flask(__name__)


@app.post("/webhooks/mailfully")
def mailfully_webhook():
    secret = os.environ.get("MAILFULLY_WEBHOOK_SECRET", "")
    if not secret:
        return "webhook secret not configured", 500

    raw_body = request.get_data()
    if not verify_mailfully_webhook(secret, request.headers, raw_body):
        return "invalid signature", 401
    event = json.loads(raw_body)
    # Skip the event if request.headers["webhook-id"] was already processed, then handle event["type"].
    app.logger.info("mailfully event %s", event["type"])
    return "", 204
```

## Other languages: port and prove

There is no tested verifier for other languages. Port the Node verifier, and do not ship it until it
accepts this vector and rejects it with one body byte changed. Run the check with the vector's
`timestamp` as "now", because the vector is older than the 300-second window.

<!-- test:webhook-vector -->
```json
{
  "secret": "whsec_-_-_----_v8-f21haWxmdWxseS10ZXN0LXZlY3Rvci0",
  "id": "evt_01K6T0V3B6XWJ7Q9R2M4N8P5ZD",
  "timestamp": 1790000000,
  "body": "{\"type\":\"email.delivered\",\"created_at\":\"2026-10-03T12:00:05.000Z\",\"data\":{\"email_id\":\"01K6T0V1Q5H8C3D7E9F2G4J6KM\",\"from\":\"app@example.com\",\"to\":[\"user@example.com\"],\"subject\":\"Welcome\",\"created_at\":\"2026-10-03T12:00:00.000Z\",\"tags\":[]}}",
  "signature": "v1,UWjA1OpsMcNvLR5J01K2DymCtvWhBF4hPy65RfoPArg="
}
```

The vector's secret contains both `-` and `_`. A port that decodes it as standard base64 fails this
vector, which is the point: that is the bug stock libraries have.
