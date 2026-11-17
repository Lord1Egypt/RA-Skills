# Execution and human attention

Read this reference for agent execution records, evidence, human-attention requests, resolution, recovery, and version-fenced lifecycle transitions.

## Execution and attention CLI workflow

Use `atoll execution list|get|create|transition`, `execution evidence list|add`,
and `atoll attention create|list|get|cancel|ack` with the selected profile and `--json`.
Creation requires `--issue`, `--agent <member-id|self>`, and an explicit
`--idempotency-key`; it returns `assigned` at state version 1. Start with a
separate `execution transition <id> --to running --expected-state-version 1
--idempotency-key <start-key>`. Atoll records state; it does not start a harness.

Generic transition targets are `running|waiting|succeeded|failed|cancelled`.
For `succeeded`, supply `--outcome-summary` unless the execution already has
linked evidence. The server validates this requirement.
Use `attention create` to move `running|waiting` to `needs_human`; generic
transitions cannot enter or leave `needs_human`. Attention kinds are exactly
`approval|clarification|access|decision|destructive_action|other`. Supply the
execution's expected state version, title, request summary, why needed, resume
condition, exactly one member/team/project-admin target, and an idempotency key.
Never put credentials, access tokens, private paths, prompts, logs, or other
secrets in attention text. Server permissions and concealed 404 responses remain
authoritative; do not try another identity to bypass them.

Read `attention get <id>` for the human's resolution and current attention and
execution versions. Human resolution returns the execution to `waiting`; it
does not resume a model or harness. Requester `attention cancel` also returns it
to `waiting` and requires `--expected-attention-version`,
`--expected-state-version`, and `--idempotency-key`. Human resolve, administrator
retarget/cancel, and recovery discovery are REST/UI operations, not CLI commands.
Harness acceptance and the later explicitly fenced `waiting -> running` resume
remain the separate AH-2122 integration.

After resolution, private heartbeat keeps one requester receipt under
`execution_attention.resolved_unread`. Acknowledge it with:

```bash
atoll attention ack <attention-id> \
  --expected-attention-version <attention-version> \
  --expected-state-version-at-close <close-state-version> \
  --idempotency-key <key>
```

The same key and body replay the stored result. Stale versions return a
`409`, while current versions after another consumer return
`already_consumed: true`. Acknowledgement consumes only the receipt and
never resumes the execution. The exact requester
`waiting -> running` transition is the separate lifecycle path that can
consume it. Notification and heartbeat-page acknowledgement remain separate.

Every write uses the caller's explicit idempotency key; transitions and attention
writes use the caller's expected versions. Never silently fetch a new version
and write against it. After a POST timeout, network failure, or HTTP 5xx, the
outcome is uncertain and the CLI does not retry. Read `execution get <id>`,
`attention get <id>` (or `attention list --execution <id>` when create returned no
attention ID), or `execution evidence list <id>`. Stop if the result is visible.
For execution create without an ID, replay the identical create command with
the same key, then read the returned ID. If replay is needed for another write,
keep the exact body and key. Stop for operator reconciliation if changed state
or versions make the outcome ambiguous; never use a new key to force progress.

Evidence add links only an existing authorized issue object using
`--type <comment|activity_event|issue_pr_link|attachment> --target-id <uuid>
--idempotency-key <key>`. It does not upload files, URLs, text, or raw logs.

## Typed MCP tools

Both full/private and public plugin profiles expose
`atoll_list_executions`, `atoll_get_execution`, `atoll_create_execution`,
`atoll_transition_execution`, `atoll_list_execution_evidence`, and
`atoll_add_execution_evidence`, plus `atoll_list_attention`,
`atoll_get_attention`, `atoll_create_attention`, `atoll_cancel_attention`, and
`atoll_ack_attention`. They use existing REST lifecycle routes, authorization,
expected versions, and caller-supplied idempotency keys. Public actor-dependent
calls require the selected opaque `profile_ref` on each call.

MCP list and detail calls return typed safe projections. Execution create starts
in `assigned`; generic transitions exclude `needs_human`. Attention creation
requires one exact member, team, or project-admin target and moves the execution
to `needs_human`. Requester cancellation and acknowledgement are version-fenced;
acknowledgement consumes the receipt only. MCP does not resolve for humans,
expose administrator retarget/cancel or recovery mode, accept local-file inputs,
or control a harness, runner, worktree, or process. If a write times out or
returns a server error, read the exact execution, attention item, or evidence
list before deciding whether to replay the identical request with the same key.
MCP wraps transport failures and HTTP 5xx responses as
`lifecycle_write_uncertain` with `retryable: false`; client errors retain their
REST code. Do not generate a replacement key or write against a newly fetched
version.

## Human attention

When an execution needs a human, use the attention contract. `POST
/api/orgs/{id}/attention` records a bounded request and atomically moves the
execution to `needs_human`; generic execution transitions cannot perform this
edge. Poll `GET /api/orgs/{id}/attention` or use the exact item endpoint.
Resolve, cancel, or retarget with both expected versions and an idempotency
key. Reuse the same key only with the same input. Use `mode=recovery` only as
an authorized human administrator when the original target is no longer
eligible. Keep request text concise and never include secrets, credentials,
logs, prompts, or local paths. The public projection provides current and
snapshot actor/target fields, execution state, issue, and project context.

## Agent execution REST API

Use the canonical org-scoped execution routes for lifecycle management:
`GET|POST /api/orgs/{id}/executions`, `GET
/api/orgs/{id}/executions/{executionId}`, `POST
/api/orgs/{id}/executions/{executionId}/transitions`, and `GET|POST` on the
matching `/evidence` route. Create starts in `assigned`; transition writes
require `expected_state_version` and an idempotency key. Generic transitions
cannot enter or leave `needs_human`; use the attention contract. Reads follow
the issue's current project access. Non-guest organization members may also read
projectless executions; setup-scoped agents and guest members cannot. Creation-
project metadata does not grant access, and unreadable records are concealed.
Responses are bounded management projections, not logs or harness controls.

The local runner associates each ordinary runner lease with one execution using
`harness_kind: "atoll_local_runner"` and the lease UUID as `external_run_id`.
Its private journal writes one bounded outbox entry before execution, evidence,
or attention mutations and reconciles exact identities after a timeout or
restart. A changed version or ambiguous readback stops for operator review.
After a human resolves an attention item, a separate private claim requires the
exact waiting execution, resolved item, expected versions, current installation,
host, source lease, and retained Codex thread. The continuation carries only
canonical IDs and the closed resolution outcome enum; notification and verified
GitHub resume acknowledgement remains separate.
