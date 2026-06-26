# AgentMemory Deep Analysis

## Snapshot

- Upstream: `rohitg00/agentmemory`, package `@agentmemory/agentmemory` version `0.9.22` (verified May 28, 2026).
- Purpose: persistent cross-agent memory for coding agents through a local REST server, MCP shim, hooks, skills, and first-party adapters.
- Runtime: Node 20+, `iii-sdk 0.11.2`, local state through iii/SQLite-style primitives. No external database is required for the default path.
- Main ports: REST/MCP HTTP on `3111`, stream on `3112`, viewer on `3113`, iii engine bridge on `49134`.

## Architecture

AgentMemory has three distinct integration layers:

1. Server: `agentmemory` starts the worker, REST API, viewer, and iii function registrations.
2. MCP shim: `agentmemory mcp` or `@agentmemory/mcp` proxies to the server via `AGENTMEMORY_URL`; if the server is unreachable, it falls back to a limited local InMemoryKV tool set.
3. Agent hooks/plugins: Codex, Claude Code, OpenCode, and OpenClaw adapters capture session events and optionally inject retrieved context.

The full MCP surface is available only in proxy mode with a live server. Fallback mode supports a small set such as `memory_save`, `memory_recall`, `memory_smart_search`, `memory_sessions`, and `memory_governance_delete`.

## Codex Surface

The Codex adapter writes `[mcp_servers.agentmemory]` in `~/.codex/config.toml`. `agentmemory connect codex --with-hooks` also writes `~/.codex/hooks.json` with absolute paths to bundled hook scripts. That hook fallback exists because Codex Desktop may not dispatch plugin-local hooks reliably; MCP can still work without it.

The Codex plugin ships:

- MCP server registration.
- Hooks: `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PreCompact`, `Stop`.
- Skills: `remember`, `recall`, `session-history`, `forget`, `recap`, `handoff`, `commit-context`, `commit-history`.

## OpenClaw Surface

The OpenClaw integration is a memory plugin plus MCP recipe. The plugin:

- Registers a memory capability when the host exposes `api.registerMemoryCapability`.
- Uses `before_agent_start` to recall relevant memory and prepend context.
- Uses `agent_end` to observe successful conversation turns.
- Guards bearer-token use over plaintext non-loopback HTTP, warning once or throwing when `AGENTMEMORY_REQUIRE_HTTPS=1`.

OpenClaw may warn that the plugin uses legacy hook names. Treat that as a compatibility warning unless current OpenClaw has a newer memory capability contract to target.

## Configuration Knobs

- `AGENTMEMORY_URL`: REST base URL, default `http://localhost:3111`.
- `AGENTMEMORY_SECRET`: optional bearer token. Never print it.
- `AGENTMEMORY_REQUIRE_HTTPS=1`: refuse to send a bearer over non-loopback HTTP.
- `AGENTMEMORY_TOOLS=all|core`: server-side visible tool set; default is all in v0.9.22.
- `AGENT_ID`: tags writes in multi-agent setups.
- `AGENTMEMORY_AGENT_SCOPE=isolated`: filters recall/session APIs by `AGENT_ID`.
- `AGENTMEMORY_AUTO_COMPRESS=true`: opt-in LLM summaries; costs tokens.
- `AGENTMEMORY_INJECT_CONTEXT=true`: opt-in hook context injection; costs session tokens.
- `AGENTMEMORY_FORCE_PROXY=1`: skip MCP livez probe when the route is known reachable but probes fail.
- `AGENTMEMORY_PROBE_TIMEOUT_MS`: raise MCP probe timeout for slow remote routes.

## Quality Assessment

Strong points:

- Broad agent support through MCP, REST, hooks, and plugins.
- Good operational tooling: `status`, `doctor`, `demo`, `connect`, `remove`, `import-jsonl`.
- Good privacy controls for delete and bearer-token transport.
- Clear fallback behavior for MCP-only hosts.

Risks to manage:

- `npx` can stall or cache stale package versions; prefer a stable local binary for configs.
- Plugin/hook paths can become stale after package upgrades.
- Sandbox/container localhost routing can silently point at the wrong network namespace.
- Remote HTTP with `AGENTMEMORY_SECRET` leaks bearer tokens unless blocked.
- MCP fallback mode can look "working" while missing most tools.
- OpenClaw plugin docs in upstream can lag current OpenClaw plugin compatibility warnings.
