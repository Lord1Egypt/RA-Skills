## Failure Analysis and Bug Routing

Reproduce through `dcc-mcp` and keep one gateway session id. Run
`dcc-mcp-cli doctor`, then `dcc-mcp-cli stats --status failure --session-id
<session-id>`; preserve the failed call's `request_id`, trace/job ids, adapter
version, DCC version, readiness fields, and the smallest safe reproduction.
Use `/v1/debug/issue-reports/<request_id>` for the public-safe issue body and
review any `?mode=raw` export locally before sharing it.
The bundled error report binds persisted-job diagnostics to the exact current
instance key. If that database is absent, report persistence as unavailable;
never glob a sibling instance or fall back to another process's database.
It likewise binds rolling-log diagnostics to the current DCC process PID; if
that exact log is absent, report logging as unavailable instead of selecting a
same-DCC sibling log.

Report adapter-owned dispatch, host-thread, readiness, packaging, or install
bugs in the adapter repository. Escalate shared CLI, gateway, protocol, or core
contract failures to `dcc-mcp-core`. Tool schema/script/workflow defects belong
to the owning Skill and `dcc-mcp-skills-creator`. Record runtime feedback with
the gateway-owned `dcc-mcp-cli feedback` command so the report remains possible
after an adapter or DCC process exits; include the last known instance,
request, and job ids. Instance-level `dcc_feedback__report` is the live-adapter
Finding v1 entry point. Core must register it so runtime DCC/adapter/core/host
versions, OS, instance id, fingerprint, and conservative redaction status are
auto-filled; adapters must not accept agent claims for those fields or add an
adapter-specific action/local-success fallback. Open an external issue only
with user authorization.

Core persists accepted adapter reports under the shared registry and exposes
them through `dcc-mcp-cli feedback list|export` / `GET /admin/api/feedback`.
Adapters must use `DccServerBase`'s instance-owned `FeedbackStore`; do not add a
second adapter-local log, aggregation endpoint, or delete-then-copy rotation.
The gateway query is bounded, deduplicates by feedback id, and fails explicitly
when filesystem reads or scan limits prevent a complete result.
