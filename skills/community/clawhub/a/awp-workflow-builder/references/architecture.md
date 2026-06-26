# AWP Architecture Overview

## Protocol Structure

AWP workflows are defined by two YAML documents and supporting files:

```
workflow.awp.yaml          -- Manifest (Layer 0) + global config
agents/{id}/agent.awp.yaml -- Agent Identity (Layer 1) + capabilities
```

## 7-Layer Model

```
Layer 6: OBSERVABILITY     -- Metrics, traces, health-checks, audit logs
Layer 5: ORCHESTRATION     -- DAG topology, execution modes, loops, conditions
Layer 4: MEMORY & STATE    -- State model, persistence, memory tiers, output contracts
Layer 3: COMMUNICATION     -- Message Bus, channels, message envelope, patterns
Layer 2: CAPABILITIES      -- Tools (MCP), skills, data sources, sandbox
Layer 1: AGENT IDENTITY    -- Name, role, LLM config, prompt, output schema
Layer 0: MANIFEST          -- Workflow metadata, version, dependencies, runtime
```

## Data Flow

```
User Task
    |
    v
Orchestrator reads workflow.awp.yaml
    |
    v
Topological sort of orchestration.graph
    |
    v
For each execution batch (parallel where possible):
    |
    +---> Agent.run(task, state)
    |       1. Load agent.awp.yaml + workflow artifacts
    |       2. Run preprocessor (if enabled)
    |       3. Inject memory (MEMORY.md) into prompt
    |       4. Collect inter-agent messages
    |       5. Gather previous agent outputs (via share_input)
    |       6. Call LLM with tools
    |       7. Parse response against output.contract
    |       8. Update state[agent_id] = parsed_result
    |       9. Write to daily log (if memory enabled)
    |
    v
Next batch (agents whose dependencies are satisfied)
    |
    v
Final state contains all agent outputs
```

## File Structure

```
{workflow-name}/
├── workflow.awp.yaml               -- Manifest
├── agents/
│   └── {agent_id}/
│       ├── agent.awp.yaml          -- Agent config
│       ├── agent.py                -- Agent class (Python ref impl)
│       └── workflow/
│           ├── instructions/
│           │   └── SYSTEM_PROMPT.md
│           ├── prompt/
│           │   └── 00_INTRO.md
│           ├── output_schema/
│           │   └── output_schema.json
│           ├── output_schema_desc/
│           │   └── output_schema_desc.json
│           ├── skills/             -- Agent-specific skills (optional)
│           └── preprocessor/       -- Data preprocessing (optional)
├── mcp/                            -- Custom MCP tools (optional)
├── skills/                         -- Project-level skills (optional)
├── workspace/                      -- Memory (created at runtime)
│   ├── MEMORY.md                   -- Long-term memory
│   └── memory/                     -- Daily logs
└── data/                           -- Input/output/state (optional)
```

## Key Concepts

### Output Contract

The `output.contract` in `agent.awp.yaml` is the single source of truth for what an agent produces. From it:

- `output_schema.json` is generated (JSON Schema draft-07)
- `output_schema_desc.json` is generated (field descriptions)
- `share_input` references are validated (R8)
- The `confidence` field is mandatory (R17)

### State Sharing

Agents share data through the state dictionary:

1. Agent A declares fields with `shareable: true` in its output.contract
2. Agent B lists `share_input: {agent_a: [field1, field2]}` in the graph
3. At runtime, Agent B receives Agent A's shareable outputs in its context

### Tool Calling

AWP uses MCP-compatible tool calling:

1. Agent's LLM returns tool call requests
2. Runtime executes tools via the tool registry
3. Tool results (standard format: `{ok, status, data, error, log}`) are fed back
4. LLM continues with tool results in context
5. This loops until the LLM produces a final response

### Memory Tiers

| Tier | Storage | Purpose | Persistence |
|------|---------|---------|-------------|
| Long-term | MEMORY.md | Curated facts, preferences | Permanent |
| Working | memory/YYYY-MM-DD.md | Daily agent logs | 30-90 days |
| Episodic | agent_outputs/*.json | Agent output history | 30 days |
| Semantic | Vector DB | Embedding-based search | Configurable |

### Compliance Levels

| Level | Name | Core Requirement |
|-------|------|-----------------|
| L0 | AWP/Core | Manifest + 1 Agent + Output Contract |
| L1 | AWP/Composable | L0 + DAG + State Sharing |
| L2 | AWP/Communicative | L1 + Message Bus |
| L3 | AWP/Memorable | L1 + Memory (2+ tiers) |
| L4 | AWP/Observable | L1 + Tracing + Metrics + Audit |
| L5 | AWP/Enterprise | L0-L4 + Security + Circuit Breaker |
