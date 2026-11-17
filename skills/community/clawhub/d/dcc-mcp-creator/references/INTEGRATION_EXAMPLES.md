## Example: New Nuke Adapter

When asked to create a Nuke MCP adapter, start by mapping the host lifecycle:
how Python is loaded, how the UI/main thread must be entered, what headless
mode is available, how plugins are installed, and which operations should be
bundled as default skills. Then scaffold the adapter around core primitives:

- `DccServerBase` for MCP/HTTP and skill catalog behavior.
- `DccServerOptions.from_env("NUKE")` or an adapter-specific equivalent for env-driven configuration.
- `HostExecutionBridge` plus a Nuke dispatcher for all Nuke API calls.
- Core project, readiness, resource, diagnostics, and gateway helpers before adapter-local glue.
- `dcc-mcp-skills-creator` for the first `nuke-*` skill packages.

## Example: Private Non-DCC Service

When asked to expose an internal asset, render-farm, review, or production
service, stay in the supplied private project and start with
[`examples/remote-server`](https://github.com/dcc-mcp/dcc-mcp-core/tree/main/examples/remote-server). It is a standalone
service despite the historical directory name: it binds to loopback for local
development, discovers a bundled example Skill, and needs no DCC process or GitHub
repository.

- Use a stable custom identifier such as `studio-assets`; do not pretend it is
  Maya or another cataloged DCC.
- Pass `instance_type="standalone"`, leave `dcc_pid` unset, and use inline
  execution unless a real external host boundary exists.
- Validate the Skill, start the service, then exercise `tools/list`,
  `tools/call`, resources, and errors with the official open-source MCP
  Inspector before testing gateway discovery.
- Keep development on loopback. Intranet exposure requires operator-owned
  TLS, authentication, firewall policy, secret storage, and audit controls.
- Package through the owner's existing wheel, archive, container, Rez, or
  private registry workflow. Do not create or publish a public repository
  unless the user explicitly requests it.

## Cross-DCC Asset Sync

When an adapter publishes an evolving file to another local or remote DCC, use
Core's `AssetSyncRevision` and `FileAssetSyncStore` contract. Keep absolute
paths process-local: public tools accept a relative source name, while both the
source root and consumer destination root come from operator configuration.
Validate format and size before publishing, pass `expected_head_revision` for
optimistic conflict detection, and materialize only beneath the consumer-owned
root. The adapter owns its native import, canvas, refresh, or watch behavior;
Core owns only the path-free revision manifest, content-addressed object, and
conflict/materialization rules. See `docs/guide/asset-sync.md` and ADR-021.
