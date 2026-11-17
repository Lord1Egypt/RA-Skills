# Bellwire API

Default base URL: `https://api.bellwire.app`

Management routes require `Authorization: Bearer $BELLWIRE_AGENT_TOKEN`.
Private runtime wakes use a project-scoped `bw_wake_...` token. Hosted Event
and Surface writes use the narrower project-scoped `bw_live_...` token.

| Method | Route | Purpose |
| --- | --- | --- |
| `POST` | `/v1/device-bindings/confirm` | Exchange a six-digit code for an Agent token |
| `POST` | `/v1/direct-connections` | Publish an encrypted Direct connection manifest for the bound device |
| `GET` | `/v1/direct-connections?deviceKeyId={id}` | Fetch pending encrypted manifests as the signed-in user |
| `POST` | `/v1/direct-connections/{id}/ack` | Atomically record readiness and consume a Direct v2 envelope |
| `POST` | `/v1/projects/{id}/direct-connection-recovery` | Idempotently report one previously acknowledged manifest missing on the signed-in installation |
| `GET` | `/v1/direct-connection-recoveries` | List pending device-scoped re-issuance requests as the connected Agent |
| `POST` | `/v1/projects` | Create a project |
| `GET` | `/v1/projects` | List projects |
| `GET` | `/v1/projects/{id}` | Read schema, Surface, and delivery health |
| `PATCH` | `/v1/projects/{id}` | Update project identity, status, or Logo URL |
| `PATCH` | `/v1/projects/{id}/order` | Explicitly change the project's stable display order |
| `DELETE` | `/v1/projects/{id}` | Permanently delete an owned project and its project-scoped data |
| `POST` | `/v1/projects/{id}/delivery-mode-requests` | Ask the user to approve switching Private/Hosted |
| `GET` | `/v1/delivery-mode-requests?status=pending` | List mode requests as the signed-in user |
| `POST` | `/v1/delivery-mode-requests/{id}/approve` | Approve a mode request as the signed-in user |
| `POST` | `/v1/delivery-mode-requests/{id}/reject` | Reject a mode request as the signed-in user |
| `POST` | `/v1/projects/{id}/event-schemas` | Create the next schema version |
| `POST` | `/v1/projects/{id}/notification-surfaces` | Create the next notification Surface version |
| `GET` | `/v1/surfaces` | List current live Surfaces across owned projects |
| `GET` | `/v1/projects/{id}/surfaces` | List current live Surfaces for one project |
| `PUT` | `/v1/projects/{id}/surfaces/{key}` | Create or replace a live Surface by stable key; accepts the owning Agent token or that project's Ingest Token |
| `PATCH` | `/v1/projects/{id}/surfaces/{key}/order` | Explicitly change a live Surface's stable display order |
| `DELETE` | `/v1/projects/{id}/surfaces/{key}` | End and remove a live Surface |
| `POST` | `/v1/projects/{id}/ingest-tokens` | Create a one-time-visible Ingest Token |
| `DELETE` | `/v1/projects/{id}/ingest-tokens/{tokenId}` | Revoke an Ingest Token |
| `POST` | `/v1/projects/{id}/wake-tokens` | Create a one-time-visible Private wake token |
| `DELETE` | `/v1/projects/{id}/wake-tokens/{tokenId}` | Revoke a Private wake token |
| `POST` | `/v1/projects/{id}/private-wakes` | Accept one opaque Private wake |
| `POST` | `/v1/projects/{id}/events/test` | Validate, store, and dispatch a test event |
| `POST` | `/v1/inbox/read-all` | Mark every unread event owned by the caller as read |
| `GET` | `/v1/events/{eventId}` | Read event and delivery detail |
| `GET` | `/v1/projects/{id}/delivery-health` | Read project delivery counts |
| `GET` | `/v1/projects/{id}/export` | Export Hosted Event and delivery history as JSON; server-authoritative Pro only |

Real event ingestion:

```http
POST /v1/events/{projectId}
Authorization: Bearer bw_live_...
Content-Type: application/json
Idempotency-Key: payment-ord_123
```

Status semantics:

- `201`: a new event was accepted.
- `200` with `deduplicated: true`: that project/idempotency key already exists.
- `accepted_by_apns`: APNs accepted the request; device presentation is not confirmed.
- `422`: schema missing or payload validation failed.
- `429`: short-term rate limit or monthly Signal quota exceeded.

Private wake:

```http
POST /v1/projects/{projectId}/private-wakes
Authorization: Bearer bw_wake_...
Content-Type: application/json
Idempotency-Key: source-operation-stable-key

{"reference":"22-or-more-url-safe-random-characters","priority":"normal"}
```

The body is limited to 512 bytes and unknown fields are rejected. This route
must never receive notification title, body, project identity, Logo URL,
service hostname, or Event data. A `MONTHLY_SIGNAL_LIMIT_REACHED` response is
terminal until its `resetAt`; clients must not loop.

Live Surface writes are idempotent by `(projectId, surfaceKey)`. Reusing the
same key updates the existing Surface and increments `version` only when the
rendered payload changes. Routine writes preserve `displayOrder`; list APIs sort
by `displayOrder` and then stable ID, so content refreshes never move cards.

Application runtimes should write live Surfaces with their project-scoped
`BELLWIRE_INGEST_TOKEN`, not a management Agent token:

```http
PUT /v1/projects/{projectId}/surfaces/revenue-today
Authorization: Bearer bw_live_...
Content-Type: application/json
```

Projects accept an optional `logoUrl` on create or update. It must be a public
HTTPS URL up to 2048 characters. Send `{"logoUrl": null}` to remove it. The
iOS app uses it for project avatars, and APNs marks notifications as mutable so
the Notification Service Extension can add the image as a rich attachment.
