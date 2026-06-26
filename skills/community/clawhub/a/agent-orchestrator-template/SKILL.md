---
name: Agent Orchestrator Template
description: A skill for main agents that need bounded delegation, safe parallel dispatch, and independent acceptance across multiple specialists.
---

# Agent Orchestrator Template

A framework for main agents that coordinate specialized sub-agents instead of trying to execute every part of a task alone.

## Core Philosophy

**The main agent is an orchestrator, not a dump pipe.**

Its job is to:

1. Classify the request
2. Decide whether to keep it local or dispatch it
3. Send a bounded task contract to the right sub-agent
4. Coordinate parallel work only when safe
5. Verify outputs before presenting one clean answer

Sub-agents execute scoped work. The main agent owns correctness.

## OpenClaw Local Compatibility

This skill is written to fit the current local OpenClaw profile instead of overriding it.

Respect these existing limits:

- Allowed sub-agents: `codex`, `invest`, `content`, `knowledge`, `community`
- ACP dispatch: enabled
- Default ACP agent: `codex`
- Maximum concurrent sub-agents: `2`

Do not invent agent ids that are not already allowed by the local OpenClaw config. If a task does not clearly map to one of the allowed agents, keep it local.

If you need more agent kinds than the local five, extend the registry at the routing config level instead of altering this skill’s description. The `agents` block now supported in the routing schema lets you declare agent metadata (id, description, capabilities) and refer to those ids via `preferred_agent`/`fallback_agent`. The current OpenClaw profile in `references/openclaw-playbook.md` is a runnable example, but you can register additional agents (ops-specialist, researcher, etc.) in `examples/custom-agent-registry.yaml` without touching the local workspace constraints.

## OpenClaw Routing Map

Use these mappings before introducing any custom routing logic:

| Task Type + Domain | OpenClaw Agent | Notes |
|---------|-----------|------|
| `explore + code` | `codex` | Use for bounded codebase investigation and root-cause analysis. |
| `implement + code` | `codex` | Default coding path. Main agent still owns acceptance. |
| `verify + code` | `main` first, `codex` only if needed | Keep final verification local unless a bounded reviewer pass is useful. |
| `operate + knowledge` | `knowledge` | Archiving, note organization, knowledge-base updates. |
| `explore + knowledge` | `knowledge` | Search, retrieval, note inspection, archive lookup. |
| `implement + content` | `content` | Drafting, rewriting, title/outline/content generation. |
| `operate + community` | `community` | Posting, replying, engagement, community-side actions. |
| `explore + invest` | `invest` | Market/stock/fundamental analysis. |
| `operate + invest` | `invest` | Watchlist, simulated trading, structured finance workflows. |
| ambiguous or tightly coupled work | `main` | Keep local until boundaries are explicit. |

## Orchestration Lifecycle

```text
1. Receive task
2. Check no-spawn rules
3. Classify task type and domain
4. Decide local vs delegated execution
5. Write task contract
6. Dispatch one or more sub-agents
7. Track status
8. Verify outputs
9. Resolve gaps or conflicts
10. Synthesize final answer
```

## Task Model

This template uses two routing dimensions.

### 1. Task Type

Task type describes **what kind of work is being requested**:

- `explore` — investigate, inspect, analyze, answer bounded questions
- `implement` — write or modify code/content/configuration
- `verify` — test, validate, review, compare, check constraints
- `operate` — perform external actions, archive, publish, update systems

### 2. Domain

Domain describes **what area the task belongs to**:

- `code`
- `knowledge`
- `content`
- `community`
- `invest`

The orchestrator should classify both. "Fix this bug" is not only `code`; it is usually `implement + code`, and may need `explore + code` first.

## Local vs Delegated Execution

Do not spawn by default. Spawn when delegation materially improves quality, speed, or isolation.

### Keep It Local When

- The task is a simple direct question
- The work is blocking the next immediate step
- The task is too coupled to current reasoning context
- Dispatch overhead is higher than doing it directly
- The user explicitly wants the current agent to do it

### Delegate When

- The work is bounded and well-defined
- The task can run in parallel with other work
- A sub-agent is a better fit for the task type
- A scoped implementation can be isolated safely
- Verification can remain with the main agent

## No-Spawn Rules

Check these before any routing logic.

Typical no-spawn rules:

- "What is X" or simple factual questions -> answer directly
- "你自己来" / "你直接做" -> keep local
- Tight blocking work needed for the next action -> keep local
- Highly coupled edits with unclear boundaries -> keep local first

## Dispatch Rules

### Rule 1: Route by task type first

Choose the right execution pattern before choosing a domain.

Examples:

- `explore + code` -> `codex`
- `implement + code` -> `codex`
- `verify + code` -> `main` first
- `operate + knowledge` -> `knowledge`

### Rule 2: Always send a task contract

Never dispatch vague instructions like "go handle this".

Every delegated task should include:

- goal
- expected output
- owned files or owned scope
- forbidden files or forbidden scope
- blocking vs sidecar status
- verification method

See **[references/task-contract-template.md](references/task-contract-template.md)**.

### Rule 3: Parallelize only when safe

Parallel work is useful only when tasks do not collide.

Good candidates:

- multiple read-only exploration tasks
- implementation tasks with disjoint write scopes
- verification running while non-overlapping implementation continues
- at most `2` concurrent sub-agents in the current OpenClaw profile

Bad candidates:

- two agents editing the same files
- tasks whose outputs must be known before the next step
- work that depends on hidden shared context

See **[references/parallel-dispatch-rules.md](references/parallel-dispatch-rules.md)**.

## Status Model

Track delegated work explicitly.

Recommended statuses:

- `pending`
- `in_progress`
- `blocked`
- `needs_review`
- `completed`
- `abandoned`

This makes recovery decisions concrete. A blocked task is different from a completed task with review gaps.

## Acceptance Workflow

Sub-agent output is not complete until the main agent verifies it.

Verify:

1. Was the right skill or workflow used?
2. Did the agent stay inside its task boundary?
3. Is the output materially complete?
4. Did it produce the expected artifact or result?
5. Is there any conflict with other agent outputs?
6. Has the claimed verification actually been run?

See **[references/acceptance-patterns.md](references/acceptance-patterns.md)**.

## Recovery Workflow

When delegated work fails:

1. Diagnose the exact failure point
2. Decide whether the main agent can fill the gap
3. Re-route only if another agent is a better fit
4. Update routing rules if the misroute was systematic
5. Keep ownership of the final answer

`resume-orchestration.py` runs on a persisted state file and replays in-progress work. It reuses the existing `dispatch_id`/`bundle_dir`, polls the adapters, and finalizes tasks marked `dispatched` or `running` without dispatching new bundles. Use `scripts/state-store.py update-resume` to inspect or repair resume metadata before calling the resume script, including `max_attempts`, `retryable_failure_codes`, and `next_retry_after`.

For operator visibility, `watch-state.py` prints a current snapshot of each task's `status`, `attempt_count`, `last_dispatch_status`, and scheduled retry timestamp without replaying hook logs.

## Recommended References

- **[references/routing-template.md](references/routing-template.md)** — dual-axis routing model and config schema
- **[references/openclaw-playbook.md](references/openclaw-playbook.md)** — concrete OpenClaw local routing and dispatch examples
- **[references/task-contract-template.md](references/task-contract-template.md)** — required task contract fields
- **[references/parallel-dispatch-rules.md](references/parallel-dispatch-rules.md)** — when parallel dispatch is safe
- **[references/acceptance-patterns.md](references/acceptance-patterns.md)** — boundary, verification, and synthesis checks

## OpenClaw Starter Pattern

For the current local OpenClaw setup, use this compact decision sequence:

```text
1. If the task is simple, blocking, or tightly coupled -> keep it in main
2. If it is code exploration or implementation -> route to codex
3. If it is note/archive/knowledge work -> route to knowledge
4. If it is writing/drafting -> route to content
5. If it is community action -> route to community
6. If it is market/investment analysis -> route to invest
7. Never exceed 2 concurrent sub-agents
8. Main agent always verifies and synthesizes the final answer
```

## Key Reminders

1. Route by task type before domain, then map to an allowed OpenClaw agent id
2. Keep blocking or tightly coupled work local
3. Dispatch bounded tasks, not vague requests
4. Never exceed the local sub-agent concurrency limit of `2`
5. Verify sub-agent claims independently
6. Synthesize one final answer instead of forwarding fragments
