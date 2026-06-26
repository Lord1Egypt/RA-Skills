# AWP Validation Rules -- R1 through R24

Use this checklist to validate AWP workflow compliance. All rules are mandatory unless noted.

## Naming and Identity

- [ ] **R1:** `workflow.name` in the manifest MUST exactly match the workflow directory name.
- [ ] **R2:** All agent IDs (the `name` field in graph entries and agent configs) MUST be `snake_case` -- lowercase letters, digits, and underscores only. No hyphens, spaces, or uppercase.

## Agent Implementation (Recommended for Python)

- [ ] **R3 (recommended for Python):** Every `agent.py` SHOULD define a class named `Agent` that extends `AWPAgent` (from `awp.agent`).
- [ ] **R4 (recommended for Python):** The `Agent.name` property MUST return the exact same string as the agent's ID in the graph. For example, if the graph entry is `name: data_processor`, then `Agent.name` must return `"data_processor"`.

## Directory Structure

- [ ] **R5:** Every agent listed in the graph MUST have a corresponding directory at `agents/{agent_id}/`.
- [ ] **R6:** Every agent directory MUST contain both `agent.awp.yaml` and `agent.py`.
- [ ] **R7:** Every agent MUST have a system prompt at `workflow/instructions/SYSTEM_PROMPT.md`.
- [ ] **R8:** Every agent MUST have an intro prompt at `workflow/prompt/00_INTRO.md`.
- [ ] **R9:** Every agent MUST have an output schema at `workflow/output_schema/output_schema.json`.
- [ ] **R10:** Every agent MUST have field descriptions at `workflow/output_schema_desc/output_schema_desc.json`.

## Graph Integrity

- [ ] **R11:** `depends_on` entries MUST only reference agent names that are defined in the same workflow graph. No forward references to agents in other workflows.
- [ ] **R12:** The agent graph MUST be a directed acyclic graph (DAG). Circular dependencies are not allowed. If A depends on B, B must not depend on A (directly or transitively).

## Data Contract

- [ ] **R13:** Every field listed in `share_output` MUST appear as a property in the agent's `output_schema.json`. If an agent shares `[summary, findings, confidence]`, all three must be defined in the schema.
- [ ] **R14:** Tool names listed in `tools.allowed` MUST reference tools that are registered in the MCP registry. Built-in tools: `web.search`, `http.request`, `file.read`, `file.write`, `file.list`, `shell.execute`, `agent.send_message`, `agent.list_messages`, `memory.write`, `memory.read`, `memory.search`, `memory.curate`, `arithmetic.add`, `arithmetic.subtract`, `arithmetic.multiply`, `arithmetic.divide`.
- [ ] **R15:** If `tools.execute` is `false`, then `tools.allowed` MUST be an empty list or omitted entirely. An agent cannot have allowed tools without tool execution enabled.

## Configuration Values

- [ ] **R16:** `execution.mode` MUST be one of: `sequential`, `parallel`, `conditional`. No other values are accepted.

## Output Schema

- [ ] **R17:** Every `output_schema.json` MUST include a `confidence` property of type `number` with `minimum: 0.0` and `maximum: 1.0`. This field MUST also be listed in `required`.
- [ ] **R18:** Every `output_schema.json` MUST be valid JSON Schema draft-07 (indicated by `"$schema": "http://json-schema.org/draft-07/schema#"`) and MUST have `"type": "object"` at the root level.

## Code Mode & Sandbox (R19-R24)

- [ ] **R19:** If `capabilities.codemode.enabled` is `true`, then `capabilities.tools.enabled` MUST be `true`. Code Mode generates an SDK from the allowed tools.
- [ ] **R20:** If `capabilities.codemode.enabled` is `true`, then `capabilities.sandbox.type` MUST be set and MUST NOT be `"none"`. Agent-generated code MUST run in a sandbox.
- [ ] **R21:** `capabilities.codemode.language` MUST be one of: `"typescript"`, `"python"`, `"javascript"`.
- [ ] **R22:** If `capabilities.codemode.sdk_surface.mode` is `"explicit"`, then `capabilities.codemode.sdk_surface.include` MUST contain at least one tool FQN.
- [ ] **R23:** Every entry in `capabilities.codemode.sdk_surface.exclude` MUST match at least one tool in `capabilities.tools.allowed`.
- [ ] **R24:** If `capabilities.sandbox.type` is `"isolate"`, the `capabilities.sandbox.network` section MUST be present with at least `network.enabled` defined.
