# AWP Compliance Levels -- Quick Reference

## L0 Core

**Layers:** L0 (Orchestration)
**Minimum requirements:**
- `workflow.awp.yaml` with project, graph, execution, state, logging, settings sections.
- At least one agent in the graph.
- Each agent has: agent.awp.yaml, agent.py, SYSTEM_PROMPT.md, 00_INTRO.md, output_schema.json, output_schema_desc.json.
- Output schema includes confidence field.
- No tools, memory, or communication required.

**Use when:** You need a simple single-agent or basic multi-agent workflow with no cross-session state.

---

## L1 Composable

**Layers:** L0 + L1 (State)
**Additional requirements beyond L0:**
- Multiple agents with `depends_on` edges forming a DAG.
- `share_output` fields defined and matching output schema properties.
- `state.persist: true` with a persist path.
- `state.sharing_strategy` explicitly set (full, selective, or isolated).

**Use when:** You need a multi-step pipeline where agents build on each other's output.

---

## L2 Communicative

**Layers:** L0-L2 (Communication)
**Additional requirements beyond L1:**
- `communication` section in workflow manifest with bus configuration.
- At least one channel defined.
- At least one agent with `agent.send_message` or `agent.list_messages` in tools.allowed.

**Use when:** Agents need to exchange information outside the DAG structure (e.g., requests, alerts, feedback).

---

## L3 Memorable

**Layers:** L0-L3 (Memory)
**Additional requirements beyond L2 (communication optional):**
- `memory` section in workflow manifest with at least one tier enabled.
- At least one agent with `memory.enabled: true` in agent config.
- Memory tools (`memory.read`, `memory.write`, `memory.search`) in at least one agent's allowed tools.

**Use when:** The workflow benefits from recalling information across sessions (e.g., iterative research, learning from past runs).

---

## L4 Observable

**Layers:** L0-L4 (Observability)
**Additional requirements beyond L3 (memory optional):**
- `observability` section in workflow manifest.
- Tracing enabled with export format specified.
- Metrics collection enabled with export path.
- Structured logging enabled with JSON format and trace context.

**Use when:** You need production-grade monitoring, debugging, and performance tracking.

---

## L5 Enterprise

**Layers:** L0-L6 (All layers)
**Additional requirements beyond L4:**
- `security` section in workflow manifest.
- Audit logging enabled for tool calls and state mutations.
- Rate limiting configured with per-minute caps.
- Circuit breaker configured with failure threshold and recovery timeout.
- All lower layers fully implemented.

**Use when:** Production deployment requiring governance, audit trails, fault tolerance, and operational controls.

---

## Compliance Determination

A workflow's compliance level is the highest level for which ALL requirements are met. Partial implementation of a higher level does not count. For example, a workflow with L0 + L1 + L3 (but no L2 communication) is L1 Composable, not L3 Memorable, because L2 is skipped.

Exception: L2 (Communication) and L3 (Memory) can be implemented independently. A workflow with L0 + L1 + L3 is L3 if L2 features are genuinely not needed.
