# Multi-Agent — Coordination, Handoffs, And Why It Usually Costs More

The decision to split is SKILL.md Rule 1. This page is what to do once splitting is genuinely justified, and how to tell that it was not.

**Before designing a topology**, read `## Agents` in `~/Clawic/data/agents/memory.md` and the spec of every agent involved (`specs/<agent>.md` via `## Boxes`). A handoff contract written against an imagined tool list is the most common source of coordination bugs.

## The Split Test

Split only when two roles need **different tool sets** or **different trust levels**. Concretely, one of these is true:

- One role must be read-only while the other writes or spends (a researcher and an executor).
- One role runs on a small cheap model at high volume and the other on a frontier model rarely (a triager and a resolver).
- One role handles untrusted content and must never hold the credentials the other holds (`security.md`).
- The roles run at genuinely different times or on different schedules and share nothing but a queue.

Not a reason to split: different topics, different tone, "specialization" as an intuition, or a diagram that looks like an org chart. Those are sections of one system prompt.

## Topologies

| Topology | Shape | Works for | Fails when |
|---|---|---|---|
| **Router** | Classifier → one specialist | Many task types, one door | The misroute is silent; add a "none of these" branch and log it |
| **Orchestrator-worker** | One planner, `k` workers, results merged | Breadth-first read-only work: research, comparison, wide search | Workers edit shared state, or the merge step re-reads everything and costs more than the parallelism saved |
| **Sequential pipeline** | A → B → C, each a stage | Stages with clean, typed outputs (extract → validate → write) | Any stage needs context a previous stage discarded |
| **Critic loop** | Producer + reviewer, bounded rounds | Output with a checkable rubric | The reviewer has no rubric — then it is two opinions and a coin flip |
| **Blackboard / shared state** | Agents read and write one document | Human-in-the-loop workspaces | Two agents write concurrently; last write wins and nobody notices |

Cost shape: a fan-out of `k` workers costs about `k×` the tokens of doing it once and finishes with the **slowest** branch. It buys breadth, not latency, and never on a serial dependency.

## The Handoff Contract

Every edge between agents is an interface. Write it before writing either side:

1. **Input schema** — the exact fields the receiver needs. If you cannot state it in one line, this is not a boundary (Rule 1).
2. **Output schema** — typed, bounded in size, with an explicit failure shape. `{status: ok|failed|partial, result, reason}` beats free text every time.
3. **What the receiver may NOT do** — its tool tier ceiling, in the schema's own terms.
4. **Who owns the retry** — the caller, always. A sub-agent that retries itself and then the caller retries too produces `n²` attempts.
5. **Context passed, and context deliberately not passed** — written into each agent's `specs/<agent>.md` alongside its tool table. Context fragmentation is the failure mode of multi-agent systems: the receiver acts confidently on a subset it does not know is a subset.

## Context Fragmentation, The Real Failure

The orchestrator knows why. The worker knows how. The failures live in between:

- The worker asks a clarifying question the orchestrator cannot answer, because the user is not in that conversation.
- Two workers make locally correct, mutually incompatible choices — different formats, different assumptions, both defensible.
- The merge step cannot tell a confident wrong answer from a confident right one, because it did not see either trajectory.

Mitigations that actually work: pass the **goal and the constraints verbatim**, not a paraphrase; require every worker to return its assumptions as a field; and make the merger able to reject and re-dispatch a single worker instead of re-running the fan-out.

## Sub-Agent As Tool

The cleanest way to nest agents: expose the sub-agent as a tool with a schema, a tier, and a bounded result (`tools.md`).

- It gets the caller's turn cap divided, not the caller's cap again. `child_max_turns ≤ parent_max_turns / expected_child_calls`, or one child eats the whole budget.
- It returns a summary sized for the caller's window, never its transcript. A sub-agent that returns everything it read has moved the context problem, not solved it.
- Depth two, at most. A grandchild agent's failure reaches the user as "something went wrong" with no trajectory anyone can read.
- Its cost counts against the parent's `cost_ceiling_per_task_usd`. Budgets that do not propagate are not budgets.

## Failure Modes Specific To Multi-Agent

| Symptom | Cause | Fix |
|---|---|---|
| Total cost several times the single-agent baseline for the same quality | Each hop re-establishes context; the merge re-reads everything | Measure both against the same eval set before keeping the split |
| Workers return incompatible formats | Output schema is prose, not a schema | Typed output with a validator at the edge |
| The orchestrator loops re-dispatching the same worker | The worker's failure is indistinguishable from a bad result | Explicit `status: failed` with a reason (`tools.md`) |
| One worker hangs and the whole task hangs | No per-child deadline | Child deadline strictly below the parent's remaining budget; treat a timeout as `partial` |
| Quality drops after adding a reviewer | The reviewer has no rubric and rewrites to taste | Give the reviewer the eval rubric, or delete it |
| A worker performs a write the orchestrator did not intend | Tier ceiling never enforced at the child | Enforce tier in code at the child's tool layer, not in the parent's prompt (SKILL.md Rule 6) |

## Before Keeping A Split

Run the same eval set against the single-agent version and the split version, `n` runs each (`evaluation.md`), and compare four numbers: pass rate, trajectory pass rate, median cost, p95 latency. A split that does not win on at least one and tie on the rest is an architecture that costs more and is harder to debug.

**Write the outcome** to `~/Clawic/data/agents/artifacts/decision-<topic>.md` with both sets of numbers and the date, add its `## Boxes` line, and update each agent's row in `## Agents` and its `specs/<agent>.md` in the same turn (`memory-template.md`). Every team re-argues the multi-agent question; the ones with a measured artifact re-argue it once.
