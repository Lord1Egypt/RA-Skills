# Harness Engineering Framework

Harness Engineering = infrastructure for making AI agents reliable in production.

Core metaphor: AI Agent = SOTA model (wild horse) + Harness (control system) = thoroughbred

## Table of Contents

1. [R.E.S.T. Model](#rest-model)
2. [PPAF Agent Loop](#ppaf-agent-loop)
3. [Harness as REPL Container](#harness-as-repl-container)
4. [Three Core Constraints](#three-core-constraints)
5. [Six Design Principles](#six-design-principles)
6. [Planning Patterns](#planning-patterns)
7. [Agent Maturity Matrix](#agent-maturity-matrix)
8. [Key Metrics](#key-metrics)

---

## R.E.S.T. Model

Agent quality targets:

### Reliability
- Failure recovery from checkpoints
- Operation idempotency for safe retries
- Behavioral consistency under same inputs

### Efficiency
- Resource control (token consumption, API calls, compute time)
- Low-latency response in interactive scenarios
- High throughput in batch processing

### Security
- Least privilege for current subtask
- Sandbox execution for untrusted code
- Input/output filtering (injection prevention, PII protection)

### Traceability
- Full-chain tracing from request to result
- Decision explainability (tool selection rationale)
- State auditability at any historical point

## PPAF Agent Loop

Agent behavior is a continuous four-phase cycle:

1. **Perception** — Sense world state (user input, tool results, history, task progress)
2. **Planning** — Update goals, decompose tasks, select next action
3. **Action** — Execute internal ops (update memory) or external ops (call tools, send reply)
4. **Feedback/Reflection** — Observe results, adjust strategy

## Harness as REPL Container

### Read (Context Manager)
- Translate external world + internal memory into structured Prompt
- Manage information injection boundaries (where RAG results enter Prompt)
- Apply reduction rules when token budget is tight

### Eval (Call Interceptor)
- Capture LLM function calling intent
- Route to correct tool executor
- Monitor execution: timeout, resource quota, error capture

### Print (Feedback Assembler)
- Capture tool execution results
- Assemble structured observations
- Re-inject into context for next reflection

### Loop
- Continue until goal reached or termination condition triggered

## Three Core Constraints

1. **Token window is finite** — Must compress infinite state into limited context
2. **LLM output is non-deterministic** — Must handle malformed outputs gracefully
3. **State must be external** — LLM is stateless CPU; all persistence in Harness-controlled storage

## Six Design Principles

1. **Design for Failure** — Anomalies are normal; all components need fault tolerance
2. **Contract-First** — All interactions defined by machine-readable schemas
3. **Secure by Default** — Least privilege, zero trust, defense in depth
4. **Decision vs. Execution Separation** — "What to do" decoupled from "how to do it"
5. **Everything is Measurable** — Every behavior, decision, resource consumption tracked
6. **Data-driven Evolution** — Every run is a learning opportunity

## Planning Patterns

| Pattern | Complexity | Use Case |
|---------|-----------|----------|
| Single-step React | Low | Simple Q&A, single tool call |
| Plan-and-Execute | Medium | Most enterprise scenarios (default) |
| Replan on Exception | Medium | Structured plan + exception-triggered replanning |
| Multi-Agent Collaboration | High | Open, long-running, multi-domain tasks |

Default recommendation: Plan-and-Execute with replan-on-exception overlay.

## Agent Maturity Matrix

| | Low Context Efficiency (Manual) | High Context Efficiency (Automated) |
|---|---|---|
| **Reactive** | Q3: Basic chatbots, simple tools | Q4: Integrated copilots |
| **Proactive** | Q2: Research agents, planning tools | Q1: Full autonomous growth systems |

Goal: Move from Q3/Q4 toward Q1 through mature Harness engineering.

## Key Metrics

- Task Success Rate
- Instruction Following Rate
- Tool Use Effectiveness
- End-to-end Latency
- Average Token Consumption
- Policy Denial Rate
