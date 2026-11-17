# Long Operations

Load this reference for Deep Research, video, music, and future asynchronous generation.

## Default Behavior

Start long work asynchronously and return an opaque handle immediately.

The model must not depend on implicit MCP connection state. Every later action accepts the explicit `operation_id`.

Target lifecycle:

```text
start -> operation_id
status(operation_id)
result(operation_id)
cancel(operation_id)
```

The operation's initial modality-specific tool—`gemini_research`, `gemini_generate_video`, or `gemini_generate_music`—performs `start`.

Dedicated primary surfaces expose:

```text
gemini_get_operation_status
gemini_get_operation_result
gemini_cancel_operation
```

The legacy low-token compatibility server exposes:

```text
operation(action="status"|"result"|"cancel", operation_id=...)
```

Do not add an unbounded agent-facing operation list to assist/create surfaces. A paginated diagnostics list may exist only in the account/maintenance surface.

## Local Persistence

Use a local SQLite database. It is local product state, not a cloud service.

Recommended tables:

```text
operations
cleanup_jobs
```

Operation rows may contain only recovery metadata:

```text
operation_id
operation_type
provider_operation_id
upstream_chat_id
state
created_at
updated_at
expires_at
attempt_count
error_code
verification_status
artifact_id
artifact_uri or artifact_path
```

Do not persist:

```text
Cookies
prompts
chat text
research report text
raw Gemini responses
generated file bytes
```

Default operation retention is seven days unless a workflow explicitly requires a shorter lifetime.

## Handles

Operation IDs must be:

- opaque;
- high-entropy;
- stable across process restarts;
- independent of connection/session identity;
- rejected cleanly when unknown or expired.

Always preserve provider/research/chat identifiers in structured results when observed.

## States

Use a stable state set:

```text
queued
running
completed
timed_out
cancel_requested
cancelled
failed
expired
```

`timed_out` means one wait ended; it does not prove the upstream job stopped.

`cancel_requested` means cooperative cancellation was requested.

Only report `cancelled` when the observable contract supports that terminal state. If the upstream work completes before cancellation takes effect, preserve the observed terminal result.

## Idempotency

- `status` is read-only and idempotent.
- `result` is read-only and idempotent.
- repeated `cancel` calls must not create additional upstream work;
- retries must reuse the same operation handle whenever continuation is possible;
- never start a new operation automatically because a status request failed.

## Current Compatibility Runtime

Until the SQLite OperationService is implemented:

1. start Deep Research with `wait_for_completion=false`;
2. preserve `upstream_operation_id` and `upstream_chat_id`;
3. preserve queued/running/timed-out state;
4. avoid duplicate starts;
5. use retained chat/report actions for recovery where available;
6. state clearly when restart-safe recovery is not yet implemented.
