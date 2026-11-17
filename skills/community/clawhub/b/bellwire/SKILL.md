---
name: bellwire
description: Add, update, test, diagnose, or maintain Private-first Bellwire live cards, inbox events, and phone notifications in application backends, Node.js, Cloudflare Workers, CI/CD workflows, and shell automation. Use for Bellwire binding, signed Direct v2 endpoints, opaque references and outboxes, wake tokens, Hosted Events and Surfaces, mode-change approval, provider webhooks, delivery checks, conformance, or notification troubleshooting.
license: MIT-0
---

# Bellwire

Connect repository state and events to the user's Bellwire cards, inbox, and iPhone. New projects are Private by default: Bellwire relays only an opaque wake while the phone fetches content directly from the user's HTTPS service. Hosted storage is opt-in and requires approval in the App.

## Workflow

1. Inspect the repository, its secret-management convention, tests, and the exact successful or failed state that should trigger the event.
2. Clarify only product decisions that code cannot answer: notification frequency, sensitive values, and whether a high-priority interruption is justified.
3. Ensure `BELLWIRE_AGENT_TOKEN` is available outside tracked files. If it is missing, ask the user for the six-digit code shown in the iOS app and run:

   ```bash
   bellwire_secret_dir="$(mktemp -d)"
   node <skill-dir>/scripts/bellwire.mjs bind \
     --code 123456 \
     --name "Codex on Mac" \
     --secret-output "$bellwire_secret_dir/agent-token"
   ```

   The CLI creates the file with mode `0600` and never prints the Token. Import it
   into the user's approved secret store without displaying it, then remove the
   temporary file. Never commit it.
4. Run `list-projects`, then create or reuse the Bellwire project. Search existing configuration before creating another project. Never create a second project just to change delivery mode.
5. Keep the project Private unless the user explicitly wants Bellwire Cloud to store Event, Inbox, and Surface content:
   - Private: implement signed Direct v2 notification, inbox, and surfaces endpoints; persist device keys, one-time nonces, an opaque-reference outbox, and the 24-hour reference expiry in the user's real database. Read [direct-connections.md](references/direct-connections.md).
   - Hosted: request the change with `request-mode-change`; stop until the signed-in user approves it in Bellwire. Then create Hosted schemas, Surfaces, and Ingest Tokens.
6. For Private runtime delivery, create a wake-only token, store it in the source app's real secret manager, and call `private-wakes` best-effort after the source transaction and outbox record commit. Bellwire must never receive title, body, data, Logo URL, project name, or service hostname.
7. Choose the display primitive:
   - Surface: current state that updates in place. Read [surfaces.md](references/surfaces.md).
   - Inbox event: durable history, completion, failure, recovery, or a decision boundary. In Private mode it stays in the user's service; in Hosted mode use [event-spec.md](references/event-spec.md).
8. Use stable Surface keys and opaque, random references. Reuse a stable idempotency key for retries of the same wake or Hosted write.
9. Modify the smallest reliable trigger point. Send only after the underlying business operation commits.
   - Prefer a direct post-commit Bellwire call when the application owns the business operation.
   - When a payment, commerce, deployment, or automation provider is the source of truth, read [webhooks.md](references/webhooks.md) and add a provider-specific webhook adapter.
10. Run unit tests for signature, timestamp, unknown key, tampered target, and atomic nonce replay; then run `conformance-direct.mjs`. If the database cannot atomically consume a nonce, stop and explain the safety blocker.
11. Run the repository's existing tests plus a focused trigger test. Never weaken a business test to make Bellwire pass.
12. Persist and deploy the source-side adapter and its secrets through the repository's real source of truth.
13. Complete one real source operation and verify the outbox, wake acceptance, delivery, signed phone fetch, and displayed result using [production-verification.md](references/production-verification.md). A manual wake is not production verification.

## Integration status

Use these exact boundaries in progress and final reports:

- **Configured:** the Bellwire project, schema, token, Surface, or test Event exists. This is not a production integration.
- **Integrated, awaiting production verification:** source-side adapter code, runtime secrets, focused tests, and deployment are present, but no real source operation has completed the path.
- **Production verified:** a real business operation created the expected Event or Surface, Delivery was checked, and any claimed device presentation was confirmed by the user.

Never describe `send-test`, a manually upserted Surface, or secret creation as an actual production integration.

## Commands

Use [scripts/bellwire.mjs](scripts/bellwire.mjs) for API operations. It defaults to the official hosted API and accepts `BELLWIRE_API_URL` for self-hosted installations.

```bash
bellwire_secret_dir="$(mktemp -d)"
node <skill-dir>/scripts/bellwire.mjs list-projects
node <skill-dir>/scripts/bellwire.mjs create-project --name "VideoSays" --logo-url "https://videosays.com/logo.png"
node <skill-dir>/scripts/bellwire.mjs create-wake-token --project <id> --name production --secret-output "$bellwire_secret_dir/wake-token"
node <skill-dir>/scripts/bellwire.mjs generate-reference
node <skill-dir>/scripts/bellwire.mjs send-wake --project <id> --reference <opaque-ref> --idempotency-key <stable-key>
node <skill-dir>/scripts/bellwire.mjs request-mode-change --project <id> --to hosted
node <skill-dir>/scripts/bellwire.mjs update-project --project <id> --logo-url "https://cdn.example.com/logo.png"
node <skill-dir>/scripts/bellwire.mjs set-project-order --project <id> --order 10
node <skill-dir>/scripts/bellwire.mjs delete-project --project <id>
node <skill-dir>/scripts/bellwire.mjs create-schema --project <id> --file event-spec.json
node <skill-dir>/scripts/bellwire.mjs create-token --project <id> --name production --secret-output "$bellwire_secret_dir/ingest-token"
node <skill-dir>/scripts/bellwire.mjs upsert-surface --project <id> --key prod-api --file surface.json
node <skill-dir>/scripts/bellwire.mjs list-surfaces --project <id>
node <skill-dir>/scripts/bellwire.mjs list-direct-recoveries
node <skill-dir>/scripts/bellwire.mjs set-surface-order --project <id> --key prod-api --order 20
node <skill-dir>/scripts/bellwire.mjs send-test --project <id> --file test-event.json
node <skill-dir>/scripts/bellwire.mjs event --event <event-id>
node <skill-dir>/scripts/bellwire.mjs health --project <id>
node <skill-dir>/scripts/bellwire.mjs publish-direct-connection \
  --device-key-id <id> \
  --agreement-public-key <base64> \
  --file direct-connection.json
node <skill-dir>/scripts/conformance-direct.mjs \
  --manifest direct-connection.json \
  --device-key-id <id> \
  --reference <known-test-reference>
```

Run `node <skill-dir>/scripts/bellwire.mjs --help` for validation, revocation,
deletion, and encryption commands. Secret-returning commands require
`--secret-output`; never read their Token into chat or command output.

`delete-project` is permanent and cascades through the project's schemas, tokens, events,
deliveries, and live Surfaces. Resolve the exact project ID and require explicit user intent
before running it.

Use `--json` for machine-readable non-secret output. Read [api.md](references/api.md) when adding another operation or diagnosing an error response.

## Adapter routing

- Read [adapters.md](references/adapters.md) for Node.js, Cloudflare Worker, Shell, and GitHub Actions patterns.
- Read [webhooks.md](references/webhooks.md) when receiving Stripe-like payment events or any third-party callback before updating Bellwire.
- Prefer the project's existing HTTP client. Do not add an SDK dependency for one request.
- Treat event sending as a bounded side effect: set a timeout, avoid logging payloads, and decide explicitly whether notification failure may affect the business operation. Default to best-effort after the business operation succeeds.
- Keep token values out of generated diffs, test snapshots, CI logs, and error telemetry.

## Private rules

- Generate at least 128 random bits for each reference and encode it as 22–200 URL-safe characters. Never derive it from an order, email, task, customer, or timestamp.
- Write notification detail to a database-backed outbox before sending the wake. Expire the reference after at most 24 hours.
- A wake call is bounded and best-effort after commit. Do not roll back the real business operation because Bellwire is unavailable.
- `MONTHLY_SIGNAL_LIMIT_REACHED` is terminal until the returned UTC reset time or an upgrade. Do not loop or retry it.
- Private detail and Inbox responses come from the user's service and may be cached on the phone for 30 days; Bellwire Cloud never receives them.

## Hosted Event rules

- Use lowercase dotted names such as `payment.success`, `deployment.failed`, or `agent.waiting`.
- Include only fields needed for the inbox, notification, deep link, or diagnosis.
- Never reference a sensitive field in a notification template; the API rejects it.
- Use order IDs, deployment IDs, task IDs, or run IDs for Hosted idempotency. Do not expose those identifiers as Private references.
- Avoid high-frequency progress events. Prefer completion, failure, recovery, and decision-required boundaries.
- Ask for explicit user approval before requesting `priority: high`.

## Surface rules

- Reuse a meaningful stable key such as `sales-today`, `prod-api`, or `nightly-backup`.
- Preserve the assigned `displayOrder` during routine updates. Change it only when the user explicitly asks to reorder a card.
- Send display-ready values. For example, compute revenue in the source system and send `¥2,430`; Bellwire does not infer business aggregation from raw events.
- For private or customer-derived metrics, prefer a signed Bellwire Direct endpoint so the card payload never enters Bellwire storage.
- Choose one of the supported native types. Never embed HTML, JavaScript, Swift, CSS, or arbitrary rendering instructions.
- Prefer a Surface for frequent progress and metric updates; avoid flooding the Event inbox.
- Use `open_url` actions only when the destination is expected and safe for the user.
- Project logos must be public HTTPS images no larger than 5 MB. Bellwire uses
  them in native avatars and expanded rich notifications, then falls back to a
  project monogram if the image is missing or cannot be downloaded.

## Verification and recovery

If setup fails, read [troubleshooting.md](references/troubleshooting.md). Check in this order:

1. API reachability and management-token scope.
2. Project ID and active schema version.
3. Secret availability in the actual runtime.
4. Payload type and required fields.
5. Stable `Idempotency-Key` behavior.
6. Source adapter presence in the deployed version and a real source operation.
7. Event detail, Surface state, and Delivery status.
8. iOS notification permission, device registration, and sandbox versus production APNs environment.

Never rotate, revoke, or replace a working token unless the user requested it or compromise is suspected.
