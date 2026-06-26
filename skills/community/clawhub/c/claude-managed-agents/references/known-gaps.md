# Known gaps and assumptions

## Dependency assumptions

- Python 3 is required.
- The helper works without the Anthropic Python SDK for CRUD via HTTP fallback.
- Streaming currently uses direct SSE over HTTP, even when the SDK is installed.
- `ant` is optional and only needed for the secondary CLI path.

## Files API

This skill now includes helpers for upload, list, download, and delete, plus session resource add, list, and delete flows.

It still does **not** expose every possible file metadata or pagination abstraction from the platform. For unusual edge cases, use raw API calls or extend the helper further.

Also, uploaded source files can legitimately return `downloadable: false`. The helper supports `file download`, but operators should expect it to work primarily for downloadable artifacts rather than arbitrary source uploads.

## Vault management

This skill supports passing `vault_ids` at session creation time.

It does **not** create or manage vault resources directly.

## Custom tools

Custom tool definitions are supported at the agent level.
Custom tool result handling is supported at the session event level.

The helper intentionally does not execute any custom tool logic itself. That execution belongs to the surrounding application or operator flow.

## Callable agents and multi-agent preview

The CLI accepts raw JSON for `callable_agents`, but research-preview orchestration flows are not deeply abstracted yet. Use raw JSON payloads for advanced experiments.

## Delete vs archive

The helper now supports agent delete in addition to archive/delete flows for environments and sessions.

The platform docs describe both archive and delete for environments and sessions. In practice, archive can fail if a session is still running, while delete may still succeed. Prefer archive when the resource is idle, or delete when using disposable smoke fixtures that are still active and must be torn down.
