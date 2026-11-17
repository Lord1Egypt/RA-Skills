# Async Jobs — 202s, Polling, Batch Operations

## The Pattern

POST returns 202 (or 200 with `status: pending`) plus a job ID or `Location` header → poll the status endpoint until a terminal state → fetch the result. Prefer the provider's completion webhook when one exists (→ `webhooks.md`); poll as the fallback, not the default.

## Polling Discipline

- Interval: use the provider's documented interval; absent one, start at 2s and multiply by 1.5 per poll up to a 30s ceiling — a tight fixed loop spends your rate limit on "not yet". A `Retry-After` on the status response overrides your schedule (same precedence as SKILL.md Core Rule 2).
- Cap total wait explicitly, and report timeout as its own outcome: "still running, job ID X" is not a failure — surface the ID so the job can be checked later.
- Treat unknown status values as still-running until your cap, never as failure — providers add states without notice (same tolerant-reader law as `versioning.md`).
- Terminal states are more than succeeded/failed: `canceled` and `expired` exist and need distinct handling — a switch with only two arms mislabels them.
- Results expire: download or persist promptly after completion; job-artifact retention is short and provider-specific.

## Job Creation Idempotency

- Submitting the same job twice creates two jobs — and bills twice. A timeout on the create call is an unknown outcome: list recent jobs before resubmitting, or use the API's client-reference/idempotency support when it has one (→ `resilience.md` Retry Logic).

## Batch Endpoints

- Batch success is per-item: a 200 or 207 Multi-Status can carry item-level failures — check every item's status, never assume all-or-nothing (SKILL.md Core Rule 5).
- Retry only the failed items with backoff, and only the retryable statuses per item — re-sending the whole batch duplicates the items that succeeded.
- Response order may not match request order: correlate by the ID or index the API defines, not by position.
- Respect the max-items-per-call limit, and make the splitter handle a remainder batch of one — the classic off-by-one lives there.

## Exports and Reports

- Large data lives behind async export jobs: request → poll → download URL. The URL is usually presigned and expiring (→ `files.md` Downloads).
- Exports are snapshots of the REQUEST time: data changed while the job ran is not in the file — timestamp the export by when you requested it, not when you downloaded it.
