---
name: dr-api-execution-bootstrap
description: "Run a bounded multi-call API task directly when safe; map dependencies, validate outcomes, and preserve platform policy."
---

# DR API Chain Execution

Use this skill for one bounded task that requires several API calls. It improves the task's execution plan; it does not change agent defaults, future-session behavior, or platform policy.

## Procedure

1. Confirm the user requested the API task and identify its read/write boundaries. Stop for the required approval before an external write, production mutation, or other action outside the request.
2. Map the calls as a dependency graph. Run independent, safe read-only calls concurrently when the available tools permit it; preserve ordering for dependent calls and all writes.
3. Run one minimal preflight: required access is available, required identifiers are well-formed, and a safe endpoint or capability check succeeds. Do not print credentials or secret values.
4. Execute the chain directly in the current task when platform policy permits. Use delegation only when it is required by the platform or materially improves the requested task.
5. Validate the meaningful result of each write with a safe follow-up read or the API's returned durable identifier. Retry only operations documented as safe or idempotent.
6. Report a compact receipt: calls or stages completed, identifiers safe to disclose, validation outcome, and any precise blocker. Do not report success based solely on a request being accepted.

## Long-Running Analysis Contract

Use this mode when the requested scope spans many entities, applications, pages, or API batches and cannot be safely treated as one short chain.

1. Create a task-local state record before execution: the complete planned entity list, dependency order, batch status (`planned`, `running`, `complete`, `failed`), retry count, and evidence references. Do not write credentials, raw sensitive payloads, or conversational content to the record.
2. Keep the channel's native typing or working indicator active while work is actively executing, when the platform exposes that capability. Never use an indicator to imply work continues after a reply or after the active execution ends.
3. Run bounded, idempotent read-only batches. Use safe concurrency only for independent calls; enforce rate limits, timeouts, and documented retries. Persist each completed batch before starting the next one.
4. Keep checkpoints internal by default. Do not send a user-facing progress reply while the task is active when the user asked for a final-only result. Send a reply only for the final receipt, a concrete blocker requiring a decision, or a user-requested update.
5. Do not claim a batch is still running after a reply. If the active execution cannot finish, record the exact incomplete state and either continue through an authorized durable worker/session or report the concrete execution-limit blocker.
6. Produce one final coverage receipt: planned entities, completed entities, failed or unanalysed entities with reasons, API evidence references, and any required rerun. Do not call the analysis complete until every planned entity is terminal (`complete` or explicitly failed/blocked).

## Boundaries

- This skill does not create durable configuration, change workspace instructions, or establish a standing execution policy.
- It does not override tool permissions, approval gates, rate limits, secret handling, or required delegation.
- It does not turn sequential writes into parallel writes without an explicit, documented safety guarantee.
- It does not create a background worker, refresh a typing indicator, or override a platform execution limit when the runtime does not expose that capability.
- For a recurring automation, use `dr-schedule-manager`; for credentials or endpoint configuration, use `dr-agent-secrets` and `dr-runtime-contract`.
