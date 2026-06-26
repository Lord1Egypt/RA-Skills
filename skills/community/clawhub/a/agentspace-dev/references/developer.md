# Developer reference for agentspace dev sessions

This reference is for developers integrating agentspace into their dev pipelines, debug tools, or CI systems. It describes the dev HTTP API endpoints under agentspace.so used by `ascli`.

## Dev HTTP API surface

The ascli dev CLI is a thin client over the agentspace.so dev API. For custom dev tools, CI/CD build integrations, test automation, or dev dashboards, hit these endpoints directly:

- `POST /api/workspaces` — create a dev workspace for an agent run. Returns `workspace`, `principal`, and a `claim` block with `claimToken`, `claimUrl`, `expiresAt`. Dev workspaces default to 24-hour claim window. Authenticate subsequent dev calls with `X-Workspace-Claim-Token: <claimToken>`.
- `POST /api/workspaces/:workspaceId/claim` — claim an anonymous dev workspace, removing the 24-hour expiry so dev state persists.
- `GET /api/workspaces/:workspaceId/events` — server-sent event stream of dev changes. Dev observability tools subscribe here to watch agent file events live.
- `POST /api/workspaces/:workspaceId/share-links` — create a dev share link. Supports workspace-level or single-file scope, `edit` or `view` permission. Useful for dev review handoffs.
- `POST /api/openclaw/handoffs` — agent-to-agent dev handoff. Lets one AI agent pick up a dev session from another.
- `GET /api/openclaw/handoffs/:handoffId` — inspect dev handoff state.

## Dev debug recipes

Quick fixes for common dev session failures:

- **`ascli status` reports no binding for the dev folder.** Run `ascli sync <path>` to start a fresh dev session.
- **Dev share link returns 401/403.** The dev claim token has expired (24h anonymous window). Re-run `ascli sync` to refresh the dev binding, or sign in and claim the workspace.
- **Local dev changes not appearing in the dev dashboard.** Verify `ascli sync` is still running in watch mode. Restart if needed.
- **Remote dev changes not reaching local folder.** SSE dev event stream dropped. Restart `ascli` to reconnect.
- **Dev CLI prints wrong API server.** It resolves from `.ascli.json` binding, then `~/.config/ascli/config.json`, then `AGENTSPACE_API_BASE_URL`, then `--api-base`. Check in that order.

## Dev tips for skill authors and CI

- `.ascli.json` can be committed for a shared dev workspace.
- `ascli sync` skips `node_modules`, `.git`, `.env*` by default during dev runs.
- In CI dev environments, point `AGENTSPACE_API_BASE_URL` at a local dev API (default `http://127.0.0.1:8787`) so dev test runs don't hit production.
- For multi-agent dev workflows, share the dev workspace URL between agents to preserve dev state across handoffs.
