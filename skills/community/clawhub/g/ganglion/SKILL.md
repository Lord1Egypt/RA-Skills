---
name: ganglion
description: "Use for every task involving this project. Covers running Ganglion, its CLI commands, HTTP bridge API, pipeline execution, knowledge queries, configuration, and operational workflows. Trigger phrases: 'run the pipeline', 'start the server', 'check status', 'query knowledge', 'configure', 'call the API', 'scaffold a project', 'check metrics', 'rollback', 'swap policy'."
homepage: https://github.com/TensorLink-AI/ganglion
metadata: {"openclaw": {"emoji": "📘", "requires": {"bins": ["python3", "ganglion"], "env": ["LLM_PROVIDER_API_KEY"]}, "always": true}}
---

# Ganglion — Operator's Manual

Ganglion is a domain-specific execution engine for Bittensor subnet mining. It provides a pipeline framework for orchestrating autonomous mining agents that search for optimal model configurations. It exposes a CLI, an HTTP bridge API, and a Python library. Ganglion is search infrastructure — it doesn't know what a good model looks like, it knows how to search for one.

## Quick Reference

```bash
# Scaffold a new project
ganglion init ./my-subnet --subnet sn9 --netuid 9

# Check state (local mode)
ganglion status ./my-subnet
ganglion tools ./my-subnet
ganglion agents ./my-subnet
ganglion knowledge ./my-subnet --capability training --max-entries 10
ganglion pipeline ./my-subnet

# Run (local mode)
ganglion run ./my-subnet
ganglion run ./my-subnet --stage plan
ganglion run ./my-subnet --overrides '{"target_metric":"accuracy"}'

# Start HTTP bridge (remote mode)
ganglion serve ./my-subnet --bot-id alpha --port 8899

# Check state (remote mode)
curl -s "$GANGLION_URL/v1/status" | jq .data
```

## Mode Detection

Ganglion supports two modes. **Always check which mode applies before running commands.**

- **Local mode**: No `GANGLION_URL` set, or `GANGLION_PROJECT` is set. Use `ganglion <command> <project_dir>` directly.
- **Remote mode**: `GANGLION_URL` is set. Use `curl` against the HTTP bridge.

```bash
if [ -n "$GANGLION_PROJECT" ] || [ -z "$GANGLION_URL" ]; then
  echo "local"
else
  echo "remote"
fi
```

## Response Format

All HTTP bridge endpoints (except health probes) return responses in a standard envelope:

- **Success**: `{"data": <payload>}` — use `jq .data` to extract
- **Error**: `{"detail": {"error": {"code": "ERROR_CODE", "message": "..."}}}`

Health probes (`/healthz`, `/readyz`) return raw JSON without the envelope.

Interactive API docs: `$GANGLION_URL/v1/docs` (Swagger UI).

> **Note:** Unversioned routes (e.g. `/status`) still work but are deprecated. Always use `/v1/`.

## How to Run

**Prerequisites:** Python >= 3.11, `LLM_PROVIDER_API_KEY` set (used by the LLM runtime).

**Install:** `pip install ganglion`

**Scaffold a project:**
```bash
ganglion init ./my-subnet --subnet sn9 --netuid 9
```
This creates `config.py`, `tools/`, `agents/`, and `skill/` in the target directory.

**Start in local mode:**
```bash
export GANGLION_PROJECT=./my-subnet
ganglion status $GANGLION_PROJECT
```

**Start in remote mode:**
```bash
ganglion serve ./my-subnet --bot-id alpha --port 8899
export GANGLION_URL=http://127.0.0.1:8899
```

The project directory must contain a `config.py` that defines `subnet_config` (SubnetConfig) and `pipeline` (PipelineDef). See `{baseDir}/references/configuration.md` for full config details.

## Key Features

### Observe State
Query the current framework state — registered tools, agents, pipeline definition, knowledge, metrics, and run history. Local mode uses CLI commands; remote mode uses GET endpoints.

Full reference: `{baseDir}/references/commands.md`

### Execute Pipelines
Run the full pipeline or a single stage. The orchestrator executes stages in dependency order, applies retry policies, injects accumulated knowledge into agent prompts, and records outcomes.

```bash
# Local
ganglion run ./my-subnet
ganglion run ./my-subnet --stage plan

# Remote
curl -s -X POST "$GANGLION_URL/v1/run/pipeline" -H "Content-Type: application/json" -d '{}' | jq .data
curl -s -X POST "$GANGLION_URL/v1/run/stage/plan" -H "Content-Type: application/json" -d '{}' | jq .data
```

### Mutate at Runtime (Remote Only)
Register new tools, agents, and components; patch the pipeline; swap retry policies; update prompts. All mutations are validated, audited, and reversible.

```bash
# Register a tool
curl -s -X POST "$GANGLION_URL/v1/tools" -H "Content-Type: application/json" \
  -d '{"name":"my_tool","code":"<code>","category":"training"}' | jq .data

# Patch pipeline
curl -s -X PATCH "$GANGLION_URL/v1/pipeline" -H "Content-Type: application/json" \
  -d '{"operations":[{"op":"add_stage","stage":{"name":"validate","agent":"Validator","depends_on":["train"]}}]}' | jq .data
```

Pipeline operations: `add_stage`, `remove_stage`, `update_stage`. See `{baseDir}/references/commands.md` for all mutation endpoints.

### Knowledge Store
Cross-run strategic memory that compounds over time. Records patterns (what worked) and antipatterns (what failed), then automatically injects relevant history into agent prompts. Knowledge is queried by capability and filtered by bot_id for multi-bot setups.

```bash
# Local
ganglion knowledge ./my-subnet --bot-id alpha --capability training

# Remote
curl -s "$GANGLION_URL/v1/knowledge?capability=training&max_entries=10" | jq
```

### Rollback
Undo any mutation. Every mutation is recorded in an audit log with rollback data.

```bash
curl -s -X POST "$GANGLION_URL/v1/rollback/last" | jq
curl -s -X POST "$GANGLION_URL/v1/rollback/0" | jq    # undo ALL mutations
```

### Multi-Bot Workflows
Multiple OpenClaw sessions share a knowledge pool via `--bot-id`. Each bot's discoveries flow into the shared pool. Cooperation emerges from shared knowledge, not explicit coordination.

```bash
# Two local sessions
ganglion run ./my-subnet --bot-id alpha
ganglion run ./my-subnet --bot-id beta

# Two remote servers
ganglion serve ./my-subnet --bot-id alpha --port 8899
ganglion serve ./my-subnet --bot-id beta  --port 8900
```

### MCP Integration
Ganglion is a bidirectional MCP system: it can **consume** external MCP servers (client mode) and **expose** its own tools as an MCP server (server mode).

#### MCP Client Mode — Consuming External Tools
Connect to external MCP servers to add tools to the agent's repertoire. Tools from MCP servers appear as regular Ganglion tools with a configurable prefix.

```bash
# Static: add to config.py
# from ganglion.mcp.config import MCPClientConfig
# mcp_clients = [MCPClientConfig(name="weather", transport="stdio", command=["python", "-m", "weather_server"])]

# Dynamic: add at runtime via API
curl -s -X POST "$GANGLION_URL/v1/mcp/servers" -H "Content-Type: application/json" \
  -d '{"name":"weather","transport":"stdio","command":["python","-m","weather_server"]}' | jq .data

# Check connected MCP servers
curl -s "$GANGLION_URL/v1/mcp" | jq .data

# Disconnect / Reconnect
curl -s -X DELETE "$GANGLION_URL/v1/mcp/servers/weather" | jq .data
curl -s -X POST "$GANGLION_URL/v1/mcp/servers/weather/reconnect" | jq .data
```

MCPClientConfig options: `name`, `transport` (stdio|sse), `command` (for stdio), `url` (for sse), `env`, `tool_prefix`, `category`, `timeout` (default 30s).

#### MCP Server Mode — Exposing Ganglion Tools
Run Ganglion as an MCP server so external agents (Claude Code, Claude Desktop, OpenClaw) can call Ganglion tools directly.

```bash
# stdio transport (Claude Desktop / Claude Code)
ganglion mcp-serve ./my-subnet --transport stdio

# SSE transport (HTTP-based clients)
ganglion mcp-serve ./my-subnet --transport sse --mcp-port 8900

# Multi-role with access control
ganglion mcp-serve ./my-subnet --roles ./roles.json
```

**Claude Code integration:** This repo includes `.mcp.json` which auto-configures Claude Code to connect to Ganglion's MCP server via stdio. Claude Code will see all Ganglion tools natively in its tool palette.

#### Exposed MCP Tools (31 total)

**Observation (11)** — read-only state queries:
`ganglion_get_status`, `ganglion_get_pipeline`, `ganglion_get_tools`, `ganglion_get_agents`, `ganglion_get_runs`, `ganglion_get_metrics`, `ganglion_get_leaderboard`, `ganglion_get_knowledge`, `ganglion_get_source`, `ganglion_get_components`, `ganglion_get_mcp_status`

**Mutation (6)** — write operations:
`ganglion_write_tool`, `ganglion_write_agent`, `ganglion_write_component`, `ganglion_write_prompt`, `ganglion_patch_pipeline`, `ganglion_swap_policy`

**Execution (3)** — run operations:
`ganglion_run_pipeline`, `ganglion_run_stage`, `ganglion_run_experiment`

**Admin (5)** — rollback and MCP management:
`ganglion_rollback_last`, `ganglion_rollback_to`, `ganglion_connect_mcp`, `ganglion_disconnect_mcp`, `ganglion_reconnect_mcp`

**Compute (6)** — infrastructure tools:
`compute_status`, `compute_jobs`, `compute_job_detail`, `compute_routes`, `write_dockerfile`, `build_image`

#### Multi-Role MCP Serving
Run one process with multiple MCP server instances, each with different access levels and auth tokens.

```json
// roles.json
[
  {"name": "admin",    "categories": null,                        "token": "admin-xyz",    "port": 8901},
  {"name": "worker",   "categories": ["observation","execution"], "token": "worker-abc",   "port": 8902},
  {"name": "observer", "categories": ["observation"],             "token": "observer-def", "port": 8903}
]
```

Roles filter tools by category. `null` categories = access to all tools. Each role gets a separate port and bearer token for SSE transport. At most one role can use stdio transport.

#### Per-Bot Usage Tracking
When running with `--roles`, a shared `UsageTracker` records per-bot tool calls (tool name, success/failure, timestamp, duration) to `.ganglion/usage.db`. Query via `/usage` endpoint on any SSE role.

#### Connecting Other Agents to Ganglion's MCP Server
OpenClaw and other LLM agents can start Ganglion's MCP server for themselves or for other agents to connect to. Use SSE transport for generic MCP clients that don't support stdio.

```bash
# Start Ganglion MCP server with SSE transport (any MCP client can connect)
ganglion mcp-serve ./my-subnet --transport sse --mcp-port 8900

# SSE endpoints exposed:
#   GET  http://127.0.0.1:8900/sse         — SSE stream (tool list + results)
#   POST http://127.0.0.1:8900/messages     — send tool calls
#   GET  http://127.0.0.1:8900/usage        — usage stats (if tracking enabled)
#   GET  http://127.0.0.1:8900/usage?bot_id=alpha — per-bot stats

# With auth (multi-role), include bearer token:
#   curl -H "Authorization: Bearer worker-abc" http://127.0.0.1:8902/sse
```

**For OpenClaw:** OpenClaw reads skills and invokes commands via bash/curl — it doesn't connect to MCP natively. To give OpenClaw access to Ganglion tools, use the CLI (local mode) or HTTP bridge (remote mode) documented above. OpenClaw can also *start* an MCP server so that other MCP-capable agents (Claude Desktop, Cursor, etc.) can connect:

```bash
# OpenClaw starts the MCP server for other agents
ganglion mcp-serve ./my-subnet --transport sse --mcp-port 8900
```

**For generic MCP clients (Cursor, Windsurf, custom):** Point your client's MCP config at the SSE endpoint:
- Server URL: `http://127.0.0.1:8900/sse`
- Messages endpoint: `http://127.0.0.1:8900/messages`
- Transport: SSE
- Auth: Bearer token (if using roles)

## Common Workflows

See `{baseDir}/examples/common-workflows.md` for full step-by-step guides.

1. **First run**: `ganglion init` → edit `config.py` → `ganglion run`
2. **Iterative mining**: check status → review knowledge → run pipeline → check metrics → repeat
3. **Dynamic mutation**: observe tools/agents → register new tool via API → patch pipeline → run
4. **Multi-bot setup**: start multiple servers with different `--bot-id` values on the same project
5. **MCP integration**: connect external tool servers → tools appear in registry → agents can use them

## When Things Go Wrong

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `FileNotFoundError: No config.py` | Wrong project path | Verify path contains `config.py` |
| `LLM_PROVIDER_API_KEY` errors | Missing or invalid API key | `export LLM_PROVIDER_API_KEY=sk-...` |
| `ConcurrentMutationError` | Mutating during a pipeline run | Wait for the run to finish |
| `PipelineValidationError` | Invalid pipeline DAG (cycles, missing deps) | Check `ganglion pipeline` output |
| Agent stuck / max turns reached | Agent cannot make progress | Review knowledge, swap retry policy, adjust prompts |

Full troubleshooting: `{baseDir}/references/troubleshooting.md`

## Retry Policies

Four built-in policies control how stages retry on failure:
- **NoRetry** — single attempt
- **FixedRetry** — retry N times (default: 3)
- **EscalatingRetry** — increase temperature per attempt, optional stall detection
- **ModelEscalationRetry** — climb a model cost ladder (cheap → expensive)

Three presets: `SN50_PRESET` (escalating + stall detection), `SIMPLE_PRESET` (fixed), `AGGRESSIVE_PRESET` (model escalation).

## Additional Resources

- Full CLI & API reference: `{baseDir}/references/commands.md`
- Configuration guide: `{baseDir}/references/configuration.md`
- Operational procedures: `{baseDir}/references/operations.md`
- Troubleshooting: `{baseDir}/references/troubleshooting.md`
- Workflow examples: `{baseDir}/examples/common-workflows.md`
- Sample API requests: `{baseDir}/examples/sample-requests.md`
- Health check script: `{baseDir}/scripts/healthcheck.sh`
