# Continuity, batching, and token budgets

For a runtime that advertises continuity support, retain exact target binding,
latest frame and observation ID, action-evidence epoch, last receipt, pending
candidates and completed targets in the Host. Do not reconstruct authority by
replaying model history or assume that a packaged skill installs this capability.

## Epoch ownership and discovery

The Host owns the action-evidence epoch. It advances when action-scoped evidence
is invalidated, including mutations and observation/session refreshes that
invalidate existing evidence. It is not a counter of all read requests.

Read-only discovery that neither publishes nor invalidates action-scoped evidence
does not consume an epoch and may run in parallel. A discovery observation that
refreshes or invalidates that evidence does consume an epoch, even if it sends no
input. Serialize such observations with the action chain; do not interleave them
between a receipt and its required next observation. If the runtime cannot prove
discovery is independent of action evidence, keep it sequential outside the batch.
Never suppress or renumber a Host epoch to hide a gap.

## Receipt chain

Batching is a bounded sequence, not coordinate replay. Each mutating step consumes
the preceding action receipt and a newly published observation. Require matching
PID/HWND, a completed receipt, a non-empty transition fence, and the observation
parent matching the receipt's `post_observation_id`. Its epoch must be exactly
`receipt.post_action_evidence_epoch + 1` (the chain's `previous_epoch + 1`).

Abort on stale observation, changed target, missing receipt, failed effect
verification or epoch gap. If this chain is unavailable, batch only independent
non-mutating discovery. Serialize all mutating actions.

## Checkpoint and resume

Saving a Host checkpoint does not itself consume an epoch or grant authority.
Retain the Host-issued epoch, receipt, observation and exact binding unchanged.
On resume apply the same advancement rules as above: independent discovery
consumes no epoch; any evidence-invalidating refresh consumes an epoch. Recheck
current binding, permissions, interruption state and evidence against the saved
checkpoint before continuing. If refresh or intervening activity breaks the
required receipt chain, discard pending candidates and establish a fresh verified
chain; do not replay the previous mutation or reset the Host counter. User
interruption still requires fresh authorization before resuming.

## Compact evidence

Prefer semantic deltas and local candidate sets over repeating full screenshots.
Capture full frames at task start, scene change or recovery, and use region or
semantic deltas after stable actions when they suffice for grounding. Invalidate
cached candidates after navigation, popups, resize, focus changes or evidence
epoch changes.

Report available action/observation counts, model calls, input/output tokens,
stale rejections and recovery attempts; leave unavailable metrics unknown.
The model proposes candidates; the Host owns freshness, exact-target checks,
effect verification, retry limits and checkpoint/resume. Successful dispatch
without verified destination state is not success. Keep trace output to IDs,
deltas, counters and failure reasons unless full images are needed for grounding.
