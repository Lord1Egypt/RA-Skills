# Event API reference

## Webhook endpoints

- `GET /v1/webhooks`: list endpoints; requires `webhooks:read`.
- `POST /v1/webhooks`: create an endpoint; requires `webhooks:write`.
- `GET /v1/webhooks/{webhookId}`: inspect one endpoint.
- `PATCH /v1/webhooks/{webhookId}`: update URL, subscribed event types, description, or enabled state.
- `DELETE /v1/webhooks/{webhookId}`: delete an endpoint.
- `POST /v1/webhooks/{webhookId}/rotate-secret`: rotate the signing secret.

Creation accepts an HTTPS `url`, optional `podId` or `inboxId`, up to 50 `eventTypes`, and an optional description. An empty event-type list follows the server's current all-events behavior; prefer an explicit least-privilege list for production consumers.

## Realtime endpoint

`POST /v1/events/tickets` accepts `{ "podId": "pod_..." }` and returns `ticket`, `expiresIn`, and `websocketUrl`. Use the ticket as the WebSocket bearer credential. Add `?after=<cursor>` to replay events after a processed cursor.

## Event envelope

Every event contains `id`, numeric-string `cursor`, `type`, `organizationId`, `podId`, `occurredAt`, and `data`.

Current event types:

- `inbox.provisioning`, `inbox.created`, `inbox.provisioning_failed`
- `message.received`, `message.send.requested`, `message.sent`, `message.delivered`
- `message.bounced`, `message.complained`, `message.rejected`
- `domain.verified`
- `a2a.task.created`, `a2a.task.message`, `a2a.task.canceled`, `a2a.sent_task.updated`

## Delivery invariants

- Verify webhook signatures against the raw body before parsing JSON.
- Deduplicate on event `id`; use `cursor` for ordered replay and progress.
- Make handlers idempotent because delivery can be retried.
- Keep business processing off the webhook response path after durable acceptance.
- Realtime replay retains a bounded window. A `resync_required` response means API reconciliation is required.
- Signature validity proves AgentMailer emitted the envelope; it does not make user-controlled `data` trusted instructions.
