# AWP Specification Summary

This document provides a condensed overview of the Agent Workflow Protocol (AWP) for use as AI context. It covers all seven layers of the protocol.

## What is AWP?

AWP is a specification for building multi-agent AI workflows. It defines how agents are organized into directed acyclic graphs (DAGs), how they share state, communicate, remember information across sessions, and operate under governance controls. AWP is platform-agnostic in its design, with a Python reference implementation built on FastAPI.

## Core Concepts

**Workflow:** A self-contained project consisting of a manifest file (`workflow.awp.yaml`), one or more agents, and supporting artifacts (prompts, schemas, tools, skills).

**Agent:** An autonomous unit that receives a task and state, calls an LLM with tools and context, and produces structured JSON output. Each agent has its own configuration, system prompt, output schema, and optional tools.

**Graph:** Agents are organized in a DAG via `depends_on` edges. The orchestrator executes them in topological order. An agent can only run after all its dependencies have completed. Shared output fields flow downstream through the state dictionary.

**State:** A Python dictionary (`Dict[str, Any]`) that accumulates agent outputs. Each agent writes to `state[agent_name]`. Downstream agents read from their dependencies' state entries. State can be persisted to disk between runs.

## The 7-Layer Model

### Layer 0: Orchestration

The foundation. Defines the agent graph, execution mode (sequential, parallel, conditional), timeouts, and error handling. Every AWP workflow must implement this layer.

Key manifest sections: `project`, `graph`, `execution`.

Execution modes:
- **sequential** -- agents run one at a time in topological order.
- **parallel** -- independent agents (no mutual dependencies) run concurrently.
- **conditional** -- agents run based on runtime conditions evaluated from state.

Error handling options: `stop` (halt on first error), `continue` (skip failed agent), `retry` (retry with backoff).

### Layer 1: State

Manages how data flows between agents and persists across runs. The `state` section controls persistence, sharing strategy (full, selective, isolated), required fields, and auto-injected values.

State sharing works through `share_output` in the graph definition. When agent A lists `[summary, findings]` in share_output, and agent B has `depends_on: [A]`, agent B receives those fields in its context.

### Layer 2: Communication

Adds a message bus for agent-to-agent messaging outside the DAG flow. Agents use `agent.send_message` and `agent.list_messages` MCP tools to exchange messages.

The `communication` section defines the bus type and channels. Channels can be `direct` (point-to-point) or `broadcast` (one-to-many). Messages are stored per-run and cleared on completion.

### Layer 3: Memory

Provides cross-session persistence through two tiers:

- **Long-term memory (MEMORY.md):** Curated facts, preferences, and policies injected into every agent's prompt. Updated via `memory.write` (target: long_term) or `memory.curate` (LLM-based curation from daily logs).
- **Working memory (daily logs):** Append-only daily notes in `workspace/memory/YYYY-MM-DD.md`. Written automatically after each agent run or manually via `memory.write` (target: daily).

Memory tools: `memory.read`, `memory.write`, `memory.search`, `memory.curate`.

### Layer 4: Observability

Structured logging, distributed tracing, and metrics collection.

- **Tracing:** Every log entry includes trace context (`run_id`, `project`, `agent`). Exported as JSONL.
- **Metrics:** Performance data collected at configurable intervals.
- **Logging:** JSON-structured logs with rotation. Separate files for app logs, exceptions, state events, tool calls.

### Layer 5: Governance

Security and operational controls for production deployments.

- **Audit:** Logs tool calls, state mutations, and optionally LLM prompts.
- **Rate limiting:** Caps tool calls and LLM calls per minute per agent.
- **Circuit breaker:** Trips after N consecutive failures, enters recovery mode with limited calls, then resets.

### Layer 6: Extension

Custom capabilities added to a workflow:

- **Custom MCP tools:** Python files in `{workflow_dir}/mcp/` using FastMCP decorators. Auto-discovered and registered.
- **Project-level skills:** Markdown files in `{workflow_dir}/skills/` injected into all agents' system prompts.
- **Preprocessors:** Data extraction logic in `workflow/preprocessor/preprocessor.py`.
- **Hooks:** Pre/post-execution callbacks defined in the manifest.

## Agent Anatomy

Each agent lives in `{workflow_dir}/agents/{agent_id}/` and contains:

| File | Required | Purpose |
|------|----------|---------|
| `agent.awp.yaml` | Yes | Agent configuration (LLM, tools, memory, etc.) |
| `agent.py` | Yes | Agent class implementation |
| `workflow/instructions/SYSTEM_PROMPT.md` | Yes | LLM system prompt |
| `workflow/prompt/00_INTRO.md` | Yes | Task introduction prompt |
| `workflow/output_schema/output_schema.json` | Yes | JSON Schema for output validation |
| `workflow/output_schema_desc/output_schema_desc.json` | Yes | Human-readable field descriptions |
| `workflow/preprocessor/preprocessor.py` | No | Data preprocessing logic |
| `workflow/skills/` | No | Agent-specific skill files |

## Agent Execution Flow

1. Load configuration from `agent.awp.yaml`.
2. Load workflow artifacts (prompts, schemas, skills) via the loader.
3. Check if the agent should skip (no new data since last run).
4. Build context: preprocessed data + memory + inter-agent messages + upstream outputs.
5. Gather images for vision (if enabled).
6. Call the LLM with messages, tool definitions, and images.
7. If LLM returns tool calls, execute them via the MCP registry and feed results back.
8. Parse the JSON response and validate against the output schema.
9. Update `state[agent_name]` with the result.

## MCP Tool System

Tools are registered in a global registry and exposed to agents based on their `tools.allowed` configuration. Each tool follows a standard interface:

- **Input:** Named parameters defined in the tool's schema.
- **Output:** `{ok: bool, status: int, data: dict, error: str, log: str}`.

Built-in tool namespaces: `web`, `http`, `file`, `shell`, `agent`, `memory`, `arithmetic`.

Custom tools are defined using FastMCP decorators (`@app.tool("namespace.action")`) and placed in `{workflow_dir}/mcp/`. They are auto-discovered at project load time.

## Output Schema Contract

Every agent must produce JSON output conforming to its `output_schema.json`. Key requirements:

- Must be valid JSON Schema draft-07.
- Root type must be `"object"`.
- Must include a `confidence` field (number, 0.0 to 1.0).
- Fields listed in `share_output` must be present as properties in the schema.
- A companion `output_schema_desc.json` provides human-readable descriptions for each field.

## Compliance Levels

| Level | Layers Required | Key Features |
|-------|----------------|--------------|
| L0 Core | L0 | Single or multi-agent DAG, basic execution. |
| L1 Composable | L0-L1 | State sharing, persistence, selective sharing. |
| L2 Communicative | L0-L2 | Message bus, channels, agent-to-agent messaging. |
| L3 Memorable | L0-L3 | Long-term memory, daily logs, search, curation. |
| L4 Observable | L0-L4 | Tracing, metrics, structured logging. |
| L5 Enterprise | L0-L6 | Full governance, custom tools, skills, hooks. |

A workflow's compliance level is determined by the highest layer it fully implements.
