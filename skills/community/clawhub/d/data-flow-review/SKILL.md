---
name: "data-flow-review"
description: "通用数据流 code review：追踪状态、分支、字段语义与持久化一致性。"
---

# Data Flow Review

Use when Codex needs to review code by tracing how data actually moves through a system instead of judging files in isolation.

This skill is for code review, audits, and patch checks where correctness depends on:

- where data is first created
- how it is transformed
- where it is persisted
- which branch conditions change meaning or timing
- which downstream consumers rely on the value

Prefer real code paths, actual callers, request builders, store writes, event payloads, and state transitions over comments, interface names, or assumptions.

## Use This For

- code review focused on state consistency and semantic correctness
- end-to-end flow reconstruction across files or layers
- patch review where a small change may shift persistence timing or branch behavior
- API field provenance checks across UI, store, backend, queue, and downstream consumers
- audits of whether retries, cancels, refreshes, resumes, or failures leave dirty state behind
- review of whether semantically different fields are being mixed, aliased, collapsed, or reused unsafely

## Reconstruct The Real Flow

Trace the real path before judging any field.

1. Find the entry point.
   This may be a page action, button handler, route, controller, job consumer, event handler, cron, queue worker, or API endpoint.

2. Walk the full chain.
   Build a minimal path map in the shape:

   `entry -> transform -> store/cache/db write -> request/event -> downstream consumer -> next state`

3. Mark every branch point explicitly.
   Common branch types:
   - success vs failure
   - confirm vs cancel
   - retry vs first attempt
   - resume vs fresh initialization
   - sync vs async continuation
   - fallback value chosen vs canonical value available
   - feature-flag path A vs path B

4. Do not stop at the first apparently-correct local use.
   A field may be correct in one API call but stale or incorrect in the next page, store read, queue payload, or follow-up transition.

## Track Canonical Entities And Fields

List the small set of entities or fields whose meaning must remain stable through the flow.

Typical categories:

- identifiers: ids, keys, slugs, trace ids, correlation ids, external ids
- ownership or actor fields: user id, tenant id, session id, operator id
- state/control fields: status, phase, mode, source, type, flags, version
- business fields: amount, currency, plan id, order id, biz id, product id, record id
- time fields: createdAt, expiresAt, validUntil, scheduledAt
- derived or transformed values: normalized input, OCR result, parsed payload, formatted request field

For each important field, record:

- source: where the value is first produced
- transformation: whether it is normalized, parsed, merged, defaulted, or reformatted
- persistence: where it is written to store/session/cache/db/message payload
- consumers: which later code paths read it
- required meaning: what downstream code assumes the field represents

If one field temporarily carries a different concept, flag it. Do not accept "it is corrected later" unless all intermediate consumers are proven safe.

## Inspect State Boundaries

Review every place where meaning can drift because data crosses a boundary.

Common boundaries:

- local variable -> component state
- component state -> global store
- store -> request builder
- request -> backend handler
- handler -> database row
- database row -> DTO/view model
- service -> queue/event payload
- queue/event -> downstream consumer
- memory state -> persisted cache/session/local storage

At each boundary, ask:

- Is this the canonical source or a cached copy?
- Can the value become stale before the next consumer reads it?
- Is a partial success writing persistent state too early?
- Is a success-only value written before success is truly confirmed?
- Is a fallback value hiding semantic mismatch?

## Check Each Branch

For every branch point, verify these questions in order:

1. Does the flow continue, block, defer, retry, or only show/log a result?
2. Does any state mutation happen before the branch is confirmed safe?
3. If the user cancels or the downstream step fails, will dirty state remain?
4. Do later consumers read the latest local value or an older persisted copy?
5. Are success-only values written only after the success condition is truly satisfied?
6. Does the branch alter retries, refreshes, resumes, or back-navigation behavior?
7. Does async follow-up use the same canonical value or reconstruct a different one?

Pay special attention to:

- writing ids or statuses before transition APIs succeed
- cancel branches that leave persisted intermediate state
- fallback expressions such as `a || b` that silently collapse meaning
- one step using a correct local value while later steps still read stale store state
- branch-specific writes that are not cleaned up on failure or cancel

## Validate Request And Payload Accuracy

For each important API call, DB write, or event payload:

1. Locate the real payload assembly in code.
2. Map every critical field to its exact source variable.
3. Check type and format from real formatting/parsing logic, not guesses.
4. Compare semantically similar fields to ensure they are not silently merged.
5. Confirm whether the value belongs in header, query, body, params, message metadata, or record columns.

When docs, schemas, spreadsheets, or contracts exist, compare:

- field name
- required vs optional
- type
- format
- constant values
- enum meaning
- location in request or payload

## Judge Patch Safety

When reviewing a patch, ask:

1. Did it fix only the intended semantic bug?
2. Did it move persistence earlier or later than before?
3. Did it alter cancel, retry, refresh, resume, timeout, or failure paths?
4. Did it add a new rejection/throw/early-return path without updating callers?
5. Does it preserve original control flow for unaffected branches?
6. Did it change which source of truth a later step reads from?

Prefer the smallest fix that restores correct semantics without widening behavior changes.

## Review Heuristics

Strong signals of risk:

- one field name reused for multiple concepts
- local fix correct at one call site but not at later consumers
- store/cache writes happening before downstream success is confirmed
- mixed use of canonical id and display id
- stale state surviving cancel/retry/failure
- hidden aliasing through fallback expressions or object spreading
- backend and frontend disagreeing on field semantics
- queue/event consumers assuming a payload shape not guaranteed by the producer

## Findings First

When producing a review, findings come first and are ordered by severity.

Each finding should include:

- severity
- exact file and tight line reference
- entry path, branch, or scenario that triggers it
- why the resulting data becomes inaccurate, stale, inconsistent, or semantically wrong
- whether the risk is wrong request data, dirty persisted state, stale read, branch regression, or downstream contract breakage

After findings, provide a short flow summary only if it helps explain the issue set.

## Output Patterns

Use this skill for outputs such as:

- code review focused on data correctness
- end-to-end flow reconstruction
- branch-by-branch state accuracy audit
- minimal-change and no-regression review
- API/payload provenance checks across multiple layers
- audits of persistence timing and rollback safety

## Anti-Patterns

- Do not judge a field only by its interface name.
- Do not stop tracing after the first correct local use.
- Do not assume a later overwrite makes earlier wrong writes harmless.
- Do not ignore cancel, retry, refresh, resume, or failure branches.
- Do not accept fallback expressions as safe without checking semantic equivalence.
- Do not review only one layer when the bug is about cross-layer drift.
- Do not summarize architecture before identifying concrete correctness risks.
