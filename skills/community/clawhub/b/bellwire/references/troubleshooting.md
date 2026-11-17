# Troubleshooting

| Symptom | Check | Resolution |
| --- | --- | --- |
| `401 UNAUTHORIZED` on management route | `BELLWIRE_AGENT_TOKEN` prefix and binding age | Generate a new iOS binding code and bind again |
| `401 INVALID_TOKEN` on event ingest | Runtime secret and project ownership | Create a new project-scoped Ingest Token and update the platform secret |
| `422 EVENT_SCHEMA_NOT_FOUND` | Event `type` and active schema | Create the schema or correct the dotted event name |
| `422 SCHEMA_VALIDATION_FAILED` | Error `details` array | Fix required types and remove fields not declared in the schema |
| `200 deduplicated: true` unexpectedly | `Idempotency-Key` construction | Use the stable business/run ID, but include event kind when two events share one ID |
| Event exists, no Delivery row | Registered device, project pause, Surface enabled | Open the iOS app, enable notifications, and check project state |
| `retryable:QueueUnavailable` | Cloudflare Queue quota and binding health | Restore Queue capacity, then resend the same idempotency key to retry dispatch safely |
| `BadDeviceToken` or `Unregistered` | APNs environment and app reinstall | Reopen the app to register the new device token; match sandbox/production |
| Delivery `failed` with provider-token error | APNs Key ID, Team ID, private key | Repair Worker secrets without placing them in the repository |
| Test works, production does not | Source adapter, deployed bundle, runtime secret, and real trigger | Confirm the adapter is committed or otherwise persisted, inspect the active deployment, then run a real source operation |
| Provider webhook returns `401` | Raw-body preservation, signing secret, timestamp tolerance | Verify the unmodified body with the secret for that exact endpoint and environment |
| Provider retries a successful webhook | Response timing and durable handoff | Return `2xx` after Bellwire accepts/deduplicates it, after a durable queue accepts it, or after committing a record covered by tested reconciliation |
| Revenue or counts drift | Duplicate, reordered, or replayed provider events | Recompute the absolute value from the source of truth and overwrite the stable Surface |

For diagnosis, preserve the Event ID, error code, and timestamps. Do not paste raw sensitive payloads into logs or chat.

If configuration and test Events succeed but no real Event exists, treat the
integration as incomplete and follow [production-verification.md](production-verification.md).
