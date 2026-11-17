# Architecture — Loop Shapes And Topologies

Choosing the shape of the loop before writing it. Coordination between several agents has its own page (`multi-agent.md`); what persists has `memory-design.md`.

**Before proposing a shape**, read `## Agents` and `## Stack` in `~/Clawic/data/agents/memory.md`, and the spec of any agent you are about to change if `## Boxes` points at one. Proposing a topology for an agent that already exists in a different one is how a rewrite gets sold as a fix.

## The Only Loop

```
while not done and turns < max_turns and spend < budget and clock < deadline:
    decision = model(context)           # context = system prompt + tools + transcript + injected state
    if decision.tool_calls: observe(execute(decision.tool_calls))
    else: done = True
```

Everything below is a variation on what goes into `context`, who decides `done`, and what happens between turns. If a proposed architecture cannot be described as a change to those three, it is a diagram, not a design.

## Shapes, And What Each Buys

| Shape | The loop | Buys | Costs | Pick it when |
|---|---|---|---|---|
| **Single-turn with tools** | One model call, tools resolved, one answer | Latency, predictable cost, trivial to eval | No recovery from a bad tool result | The task is a lookup and a rewrite |
| **ReAct / interleaved** | Think → act → observe, repeated | Visible reasoning, recovers mid-task, debuggable | Output tokens every turn, drifts on long runs | General assistants, research, anything a human will read the trace of |
| **Plan then execute** | Plan once, execute steps, replan on failure | The plan is inspectable and approvable before spend | A stale plan executes confidently into a changed world | Multi-step work with real side effects, or where a human approves the plan |
| **State machine / graph** | Explicit nodes and transitions; the model fills nodes | Deterministic control flow, resumable, testable per node | Rigid — new cases need new edges | Known workflows with branches: onboarding, triage, refunds |
| **Reflexion / critic** | Produce, critique, revise, bounded by attempts | Quality on generative tasks with a checkable rubric | 2-3× the tokens per output | Writing, code, anything with a validator |
| **Router** | Classify, then hand to a specialized prompt or agent | Cheap specialization without coordination | A misroute is invisible and terminal | Many task types with one entry point |

Default: **ReAct with a hard cap** for open-ended work, **state machine** the moment the same workflow runs a hundred times a day. The migration between them is the normal life cycle of an agent, not an admission of error.

## The Termination Question

More agents fail on "when do I stop" than on "what do I do next".

- **Model-declared done** — the model stops calling tools. Cheap, and wrong whenever the model believes it finished. Always pair with a verification step for anything with a side effect.
- **Verified done** — a checker (a test, a schema, a second call, an observable side effect) says the goal is met. The only form of `done` worth trusting for write-tier work.
- **Budget done** — a cap tripped (SKILL.md Rule 2). Must return the partial result *and* the reason, so the caller can resume rather than restart.
- **Escalated done** — a human owns it now (`human-in-the-loop.md`).

The trace stores which of the four ended every run; that field is the first thing you will want during an incident (SKILL.md Rule 9).

## Planning: How Far Ahead Is Worth It

- Plan length should track how stable the world is. If a step's result routinely changes the next step, a 7-step plan is 6 steps of fiction — plan 2 and replan.
- Replanning is not free: it re-reads the transcript and re-emits the plan. Bound it — replan at most `ceil(max_turns / 5)` times, then escalate rather than spiral.
- The strongest cheap planning move is decomposition into steps with **independent verifiers**. A step you cannot check is a step you cannot retry intelligently.
- Reliability math decides depth (SKILL.md Rule 3): at 95% per step, a 5-step plan lands ~77% of the time, a 15-step plan ~46%. Long plans need checkpoints, not optimism.

## Checkpoints And Resumability

- A checkpoint is the smallest state that lets a new process continue: goal, completed steps with their results, current step, and the side effects already committed.
- Checkpoint **after every irreversible action**, before anything else — the failure you cannot afford is redoing a payment because the process died after the charge and before the log.
- Store checkpoints outside the process (`runtime_target: serverless` makes this mandatory; containers make it merely wise). Keyed by task id, so a retry resumes instead of duplicating.
- Resume needs an idempotency contract with every write tool (`tools.md`), or resumption is just a second execution.

## Agent, Workflow, Or Neither

The most valuable architectural answer is often "this does not need an agent".

| Signal | Build |
|---|---|
| The steps are always the same, in the same order | A script that calls a model at one step |
| The path branches on a small closed set of conditions | A workflow with model-filled nodes |
| The path depends on what earlier results turn out to be | An agent loop |
| The task is one transformation of one input | A single model call, no loop |

An agent buys the freedom to choose the next step. If nothing chooses, you paid the loop's cost — latency, nondeterminism, token growth — for nothing.

## Interfaces With The Rest Of The System

- **Synchronous request/response** — cap the whole run below the caller's timeout, and stream progress or the user assumes it hung.
- **Queue worker** — natural fit: retries, concurrency and backpressure come from the queue. Requires idempotency because the queue will redeliver (`production.md`).
- **Scheduled** — the run has no human present, so `autonomy_level` matters more and escalation must reach someone asynchronously.
- **Embedded in another agent** — it is a tool from the caller's side; give it a tool schema, a tier and a bounded result (`multi-agent.md`).

**When a shape is chosen against a real alternative**, write the decision to `~/Clawic/data/agents/artifacts/decision-<topic>.md` — the shape, what was rejected, the measurement that decided it, and what would justify revisiting — plus its `## Boxes` line, in the same turn (`memory-template.md`). Architecture arguments recur every quarter; the ones with a written measurement recur once.
