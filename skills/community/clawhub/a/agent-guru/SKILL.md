---
name: production-agent-design
description: Use when building, designing, or reviewing a multi-agent system for production — routing agents, orchestrating subagents, guarding tools with permissions, managing memory and context windows, adding observability and cost tracking, handling errors, or setting up session persistence.
compatibility: Designed for agentic frameworks (LangGraph, Strands, or similar). Examples use LangGraph. pip install langgraph langgraph-supervisor.
metadata:
  version: "1.0"
---

# Production Agent Design

## Core Principle

> **The LLM is the reasoning engine. Your code is the execution engine. The loop is the contract between them.**

Every production concern — safety, cost, retries, logging, permissions — lives in the harness, not the prompt. A prompt that says "be careful with deletions" is a suggestion. A `GuardedToolNode` that intercepts `delete_*` calls is a guarantee.

## When to Use This Skill

- Designing a new multi-agent system from scratch
- Adding safety, cost controls, or observability to an existing agent
- Debugging runaway cost, infinite loops, or context window exhaustion
- Choosing between single-agent vs multi-agent topology
- Implementing human-in-the-loop (HITL) for irreversible actions
- Setting up session persistence and resumption

## Architecture at a Glance

```
INGRESS (HTTP / CLI / Webhook / Schedule)
    │
ROUTER LAYER          — classify intent, dispatch cheaply
    │
ORCHESTRATOR          — decompose tasks, delegate to specialists
    ├── Agent A (scoped tools)
    └── Agent B (scoped tools)
         │
TOOL LAYER            — validate schema → check permission → execute → truncate
         │
CROSS-CUTTING CONCERNS
    ├── MEMORY         (short-term / working / long-term)
    ├── OBSERVABILITY  (traces, cost, session replay)
    └── RESILIENCE     (retry, circuit breaker, loop guard)
         │
PERSISTENCE           — checkpoints (Redis / Postgres) + audit log
```

## Single Agent vs Multi-Agent

```
Task scoped to ONE domain?
  YES → Single ReAct agent with appropriate tools
  NO  → Independent subtasks?
          YES → Parallel multi-agent (supervisor + specialists)
          NO  → Sequential / hierarchical orchestrator
                  │
              Any irreversible step requiring human review?
                YES → Plan-then-execute with HITL interrupt
                NO  → Orchestrator with auto-delegation
```

**Rule:** Start with a single agent. Add multi-agent complexity only when you hit a concrete limit — context window size, tool set sprawl, latency, or accuracy.

## Framework Selection

| Need | Use |
|------|-----|
| Complex branching, HITL, durable persistence, fine-grained control | **LangGraph** |
| Simple loop, minimal boilerplate, rapid prototype, leaf agents | **Strands** |
| Orchestration graph + simple leaf agents | **LangGraph + Strands hybrid** |

## Reference Files

Load these **on demand** using the triggers listed below. Do not load all of them upfront.

| File | Load when... |
|------|-------------|
| [references/router-layer.md](references/router-layer.md) | Designing intent routing, building a classifier node, handling misrouting |
| [references/orchestrator-layer.md](references/orchestrator-layer.md) | Decomposing tasks, spawning subagents, implementing plan-then-execute |
| [references/tool-safety-layer.md](references/tool-safety-layer.md) | Designing tools, adding permission rules, implementing HITL or killswitch |
| [references/memory-layer.md](references/memory-layer.md) | Context window approaching limit, adding long-term memory, injecting project context |
| [references/observability-layer.md](references/observability-layer.md) | Adding tracing, tracking token cost, debugging agent behavior, setting up alerts |
| [references/resilience-layer.md](references/resilience-layer.md) | Adding retry logic, circuit breakers, preventing infinite loops |
| [references/persistence-layer.md](references/persistence-layer.md) | Choosing a checkpointer, implementing session resume, session branching |
| [references/production-checklist.md](references/production-checklist.md) | Before deploying to production — full ~40-point readiness checklist |

## Quick Reference

| Pattern | Key implementation | Reference |
|---------|--------------------|-----------|
| Intent routing | `conditional_edges` + confidence threshold | `router-layer.md` |
| Scoped subagents | `create_react_agent` with tool subset | `orchestrator-layer.md` |
| Plan-then-execute | Two nodes, read-only tools in plan phase | `orchestrator-layer.md` |
| Tool schema | `args_schema=PydanticModel` on `@tool` | `tool-safety-layer.md` |
| Permission guard | `GuardedToolNode` with `PermissionRule` list | `tool-safety-layer.md` |
| HITL interrupt | `interrupt()` + `Command(resume=...)` | `tool-safety-layer.md` |
| Runtime concurrency | `is_concurrency_safe(input)` per tool call | `tool-safety-layer.md` |
| Abort hierarchy | Query-level abort + sibling-level child abort | `tool-safety-layer.md` |
| Tiered compaction | budget → snip → microcompact → autocompact | `memory-layer.md` |
| Auto-compaction | Summarization node at 80% context | `memory-layer.md` |
| Context injection | `AGENT.md` loaded into system prompt | `memory-layer.md` |
| Full trace | `BaseCallbackHandler` + structured events | `observability-layer.md` |
| Cost tracking | Per-turn token accounting in callback | `observability-layer.md` |
| Config snapshot | Freeze all feature flags at query entry | `observability-layer.md` |
| Diminishing returns | Track token deltas; stop if delta < 500 × 2 | `resilience-layer.md` |
| Output limit escalation | Escalate to 64k tokens before compaction | `resilience-layer.md` |
| Streaming cleanup | Tombstone partial messages on fallback | `resilience-layer.md` |
| Error-as-observation | `try/except` → `ToolMessage` | `resilience-layer.md` |
| Circuit breaker | State machine wrapping tool fn | `resilience-layer.md` |
| Session resume | Checkpointer + stable `thread_id` | `persistence-layer.md` |

## Gotchas

- **Safety rules must be code, not prompts.** A prompt saying "don't delete production data" is not a safety control.
- **Never dump the full parent message history into a subagent.** Pass only the specific task and relevant data — context pollution degrades performance and wastes tokens.
- **`InMemorySaver` is for development only.** Use Redis or Postgres checkpointers in production.
- **`interrupt()` pauses the graph.** Resume it by calling `graph.invoke(Command(resume=...), config=config)` — forgetting this leaves the agent stuck.
- **Tool result truncation is mandatory.** Large tool outputs (file reads, search results) will exhaust the context window if not truncated before returning.
- **Always set `max_iterations`.** Without a loop guard, a miscalibrated agent runs indefinitely and incurs unbounded cost.
- **Apply compaction in tiers.** Budget tool results → snip → microcompact → autocompact. Jumping straight to full summarization wastes tokens when a cheaper step would suffice.
- **Track diminishing returns, not just token budget.** An agent can burn through its iteration budget producing nearly empty continuations. Stop when the last 2 deltas are both below ~500 tokens.
- **Snapshot config at query entry.** Never re-read feature flags or env vars mid-turn — a remote config change during a 30-second response causes inconsistent behavior within a single turn.
- **Concurrency safety must be checked at runtime.** Schema metadata cannot determine if a bash command is safe — inspect the actual input string at call time. Fail conservatively (serial) if parsing fails.
