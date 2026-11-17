# Sync — Mirroring API Data Into a Local Store

## Strategy Ladder

Take the highest rung the provider offers:

1. **Delta/sync endpoint** (Google Calendar `syncToken`, Dropbox cursor, Salesforce `getUpdated`) — built for this; returns exactly what changed, including deletions where supported.
2. **`updated_since` incremental polling** — works on any API with an updated-at filter; deletion-blind (below).
3. **Webhook ping + fetch** — lowest latency; webhooks announce that something changed, the API provides current state (→ `webhooks.md` Delivery). Never sync from payload contents alone.
4. **Full re-fetch and diff** — last resort for small datasets, and the periodic reconciliation layer for all the others.

## Incremental by updated_since

- Query from `last_max_updated_at − overlap`, then dedupe by ID: records committed slightly out of timestamp order, and server-vs-you clock differences, fall inside the overlap instead of being lost. Size the overlap to the provider's worst observed write-to-visibility lag; a few minutes covers most APIs.
- Advance the watermark to the max `updated_at` the SERVER returned — never to your local receive time; the two clocks are not the same clock.
- Records sharing one `updated_at` across a page boundary get skipped by a naive `> watermark` filter — use `>=` plus ID dedupe (that is what the overlap gives you), or paginate on an (updated_at, id) compound cursor where the API offers one.
- Not every mutation bumps `updated_at` on every API — nested/child-object edits are the classic silent case. Test the mutations you care about; anything that doesn't bump lives on the reconciliation layer.

## Deletions

- Incremental fetches never show a deleted record — the default outcome is a local mirror that only grows. In order of preference: the provider's tombstones/`deleted` flag or deletion webhooks; else a periodic ID sweep — list all remote IDs (IDs-only endpoint or minimal fields), diff against local, mark the missing as deleted.
- Archived, hidden, or unshared is not deleted: a record can vanish from your query scope while still existing. Distinguish "gone" from "out of scope" before destroying local data — losing access to a folder must not delete its mirror.

## Sync Tokens

- Persist the new token only AFTER the page's changes are durably applied — token saved first + crash = changes lost forever, and nothing will ever look wrong.
- Tokens expire: Google Calendar returns 410 Gone for an expired `syncToken`, and the required response is a full resync. Build and TEST the full-resync path on day one — it is the recovery path for every corruption, not an edge case.
- A full resync must not fire deletion side effects for records it simply hasn't reached yet — reconcile deletions only after the resync completes.

## Reconciliation and Backfill

- Webhooks drop and polls miss: run a periodic incremental sweep beneath the live channel, and alert when the sweep finds changes the live channel missed — that alert is your delivery-degradation detector.
- Backfill order: capture the live-channel cursor (or start webhook capture) FIRST, then run the historical backfill, then process the captured live events. Backfill-then-subscribe leaves a gap exactly as long as the backfill took.
- Rate-limit budget: a backfill at max page size competes with your live traffic for the same bucket (→ `rate-limits.md` Multiple Instances) — throttle the backfill, not the live channel.
