# Provider webhook adapters

Use a webhook adapter only when a third-party provider is the source of truth or
the application cannot emit after its own business transaction commits. When the
application owns the transaction, prefer a direct Bellwire call after commit.

- [Required flow](#required-flow)
- [Mapping rules](#mapping-rules)
- [Delivery and response contract](#delivery-and-response-contract)
- [Provider-neutral handler shape](#provider-neutral-handler-shape)
- [Focused tests](#focused-tests)

## Required flow

```text
raw request -> verify provider signature -> normalize -> deduplicate -> map -> Bellwire
```

Keep provider-specific verification at the boundary. Pass only a small,
provider-neutral record into the mapping layer:

```ts
type VerifiedWebhook = {
  provider: string;
  eventId: string;
  eventType: string;
  occurredAt: string;
  payload: unknown;
};
```

Implement one adapter per provider. Each adapter must:

1. Read the raw request bytes exactly once.
2. Verify the signature and timestamp before parsing or trusting any field.
3. Return a stable provider event ID and provider event time.
4. Reject invalid signatures without calling Bellwire.
5. Ignore unsupported event types with a successful response so providers do not retry forever.

Use the provider's official verification library when the project already uses
it or when the signature algorithm is easy to implement incorrectly. Never
invent a generic verifier across providers.

## Mapping rules

- Map provider names to lowercase dotted Bellwire Event names, such as
  `payment.succeeded`, `payment.refunded`, or `subscription.canceled`.
- Use `provider:eventType:eventId` as the Bellwire `Idempotency-Key`. Retries of
  the same provider event must produce the same key.
- Send only fields required by the Event Spec. Do not forward the raw provider
  payload.
- Mark customer identifiers and free-form customer data as sensitive. Do not
  place them in notification templates.
- Use an Event for durable history, failure, recovery, or a decision boundary.
- Use a live Surface for current aggregate state. Reuse a stable key.
- For revenue, balances, usage, or counts, recompute the absolute value from the
  source database or provider API and overwrite the Surface. Never increment a
  Surface from webhook deltas: providers retry and may deliver out of order.
- If one webhook needs both an Event and a Surface update, treat the Event as the
  durable fact and the Surface as a refreshable projection. A failed Surface
  update must not create a second Event.

## Delivery and response contract

Choose one durability boundary:

1. **Direct:** await Bellwire. Return `2xx` only after Bellwire returns `201` or
   `200 deduplicated`; return a retryable `5xx` when Bellwire is unavailable.
2. **Queued:** verify and enqueue durably, then return `202`. The queue consumer
   calls Bellwire with the original stable idempotency key.
3. **Committed source plus repair:** commit the business record first, start the
   Bellwire call as a bounded side effect, and run a cursor-based reconciliation
   job that replays committed records with the same stable idempotency key. Use
   this only when the application database is a sufficient replayable source of
   truth.

Do not return `2xx` merely because work was started with `waitUntil`; a process
failure can lose the event while preventing the provider from retrying. A
`waitUntil` design satisfies option 3 only when the repair job and cursor are
implemented, tested, deployed, and able to reconstruct the Event.

Return `400` for malformed requests and `401` or `403` for invalid signatures.
Return `2xx` for verified duplicates and deliberately ignored event types.
Keep handlers bounded with timeouts and never log signing secrets, Bellwire
tokens, authorization headers, or raw payloads.

## Provider-neutral handler shape

```ts
export async function handleProviderWebhook(request: Request, env: Env) {
  const rawBody = await request.text();
  const verified = await verifyProviderWebhook(rawBody, request.headers, env.WEBHOOK_SECRET);
  if (!verified) return new Response("Invalid signature", { status: 401 });

  const mapped = mapProviderEvent(verified);
  if (!mapped) return new Response(null, { status: 204 });

  const response = await fetch(
    `https://api.bellwire.app/v1/events/${env.BELLWIRE_PROJECT_ID}`,
    {
      method: "POST",
      signal: AbortSignal.timeout(5_000),
      headers: {
        authorization: `Bearer ${env.BELLWIRE_INGEST_TOKEN}`,
        "content-type": "application/json",
        "idempotency-key": `${verified.provider}:${verified.eventType}:${verified.eventId}`,
      },
      body: JSON.stringify(mapped),
    },
  );

  return response.ok
    ? new Response(null, { status: 204 })
    : new Response("Bellwire unavailable", { status: 503 });
}
```

Treat this as a control-flow template, not a signature implementation. Adapt
the raw-body API, provider verifier, secret binding, and response codes to the
repository's framework and provider contract.

## Focused tests

Cover at least:

- valid signature maps the expected Event type and minimal fields;
- invalid signature makes no Bellwire request;
- duplicate delivery reuses the same idempotency key;
- unsupported event type returns success without a Bellwire request;
- Bellwire failure returns a retryable response or retries through the queue;
- committed-source recovery replays a missed Event with the same idempotency key;
- out-of-order revenue events overwrite from an absolute source-of-truth value;
- logs and error responses contain no secrets or raw customer payloads.
