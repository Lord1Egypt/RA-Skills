# Integration adapters

- [Choose a delivery mode](#choose-a-delivery-mode)
- [Private wake after commit](#private-wake-after-commit)
- [Hosted Node.js](#hosted-nodejs)
- [Hosted Cloudflare Worker](#hosted-cloudflare-worker)
- [Hosted Shell](#hosted-shell)
- [GitHub Actions](#github-actions)

## Choose a delivery mode

Choose the runtime path from the project's delivery mode:

- Private uses `BELLWIRE_WAKE_TOKEN`, an opaque-reference outbox, and signed
  Direct v2 endpoints. Start from
  [private-direct.mjs](../assets/examples/node/private-direct.mjs) or
  [bellwire-direct.ts](../assets/examples/cloudflare-worker/bellwire-direct.ts).
  For D1, also copy the adjacent nonce and outbox SQL assets.
- Hosted uses `BELLWIRE_INGEST_TOKEN` and the Event/Surface adapters below.

Never send Private content through the Hosted snippets as a fallback.

## Private wake after commit

Generate and persist a random 128-bit reference with the notification detail in
the same transaction as the source operation. After commit, send a bounded,
best-effort wake:

```ts
await fetch(
  `https://api.bellwire.app/v1/projects/${projectId}/private-wakes`,
  {
    method: "POST",
    signal: AbortSignal.timeout(5_000),
    headers: {
      authorization: `Bearer ${process.env.BELLWIRE_WAKE_TOKEN}`,
      "content-type": "application/json",
      "idempotency-key": `wake-${sourceOperation.id}`,
    },
    body: JSON.stringify({ reference: outbox.reference, priority: "normal" }),
  },
);
```

Do not put a customer, order, deployment, task, or timestamp in `reference`.
Treat `MONTHLY_SIGNAL_LIMIT_REACHED` as non-retryable until `resetAt`.

## Hosted Node.js

Use the existing HTTP client when possible. For Node 22+:

```ts
type BellwireEvent = {
  type: string;
  data: Record<string, unknown>;
  occurredAt: string;
};

export async function sendBellwireEvent(
  projectId: string,
  idempotencyKey: string,
  event: BellwireEvent,
): Promise<void> {
  const token = process.env.BELLWIRE_INGEST_TOKEN;
  if (!token) return;

  const response = await fetch(
    `https://api.bellwire.app/v1/events/${projectId}`,
    {
      method: "POST",
      signal: AbortSignal.timeout(5_000),
      headers: {
        authorization: `Bearer ${token}`,
        "content-type": "application/json",
        "idempotency-key": idempotencyKey,
      },
      body: JSON.stringify(event),
    },
  );
  if (!response.ok) {
    throw new Error(`Bellwire request failed with status ${response.status}`);
  }
}
```

Call this after the business transaction succeeds. If notification is best-effort, catch the error at the call site and log only status/code, never the event payload or token.

## Hosted Cloudflare Worker

Add `BELLWIRE_INGEST_TOKEN` with `wrangler secret put` and expose it in the environment type. Use `waitUntil` only when the committed source record can be replayed by a queue, outbox, or scheduled reconciliation job:

```ts
ctx.waitUntil(
  sendBellwireEvent(env, projectId, `deploy-${deployment.id}`, {
    type: "deployment.succeeded",
    data: { deploymentId: deployment.id, environment: deployment.environment },
    occurredAt: new Date().toISOString(),
  }),
);
```

`waitUntil` extends execution time but is not a durable handoff. If there is no
replay path, await Bellwire before returning or add durable storage first. For
provider callbacks, follow [webhooks.md](webhooks.md); do not copy this snippet
into a webhook and return `2xx` without a durability boundary.

Do not put the token in `[vars]` in `wrangler.toml`.

## Hosted Shell

```bash
curl --fail-with-body --silent --show-error \
  --max-time 5 \
  --request POST \
  --header "Authorization: Bearer ${BELLWIRE_INGEST_TOKEN:?missing}" \
  --header 'Content-Type: application/json' \
  --header "Idempotency-Key: job-${RUN_ID:?missing}" \
  --data "${BELLWIRE_EVENT_JSON:?missing}" \
  "https://api.bellwire.app/v1/events/${BELLWIRE_PROJECT_ID:?missing}"
```

Build JSON with the repository's existing JSON tool. Do not interpolate untrusted text into hand-written JSON.

## GitHub Actions

Store the Ingest Token as an Actions secret and the project ID as a repository variable:

```yaml
env:
  BELLWIRE_INGEST_TOKEN: ${{ secrets.BELLWIRE_INGEST_TOKEN }}
  BELLWIRE_PROJECT_ID: ${{ vars.BELLWIRE_PROJECT_ID }}
```

Use `${{ github.run_id }}-${{ github.run_attempt }}` in the idempotency key. Send the event in a final step with the correct `if: success()` or `if: failure()` boundary. Keep shell tracing disabled while constructing authentication headers.
