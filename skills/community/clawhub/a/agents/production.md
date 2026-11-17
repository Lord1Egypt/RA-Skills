# Production — Shipping And Operating An Agent

Scope: releasing, running, and being on call for an agent that real people or real systems depend on. Deployment shape follows `runtime_target`.

**Before any release or rollback**, read `deploys/<year>.md` (the bundle you would roll back to lives there and nowhere else), the agent's `specs/<agent>.md`, and the last row of `eval-runs/<year>.md` — via `## Boxes` in `~/Clawic/data/agents/memory.md`. **Check `## Due`** against today's date and state any overdue eval regression, red-team pass, cost review or model re-bid in one line.

## The Release Bundle

An agent release is not a code deploy. Ship and record all of it (SKILL.md Rule 8):

| Component | Recorded as | Why it belongs |
|---|---|---|
| Prompt | Version tag plus content hash | The most frequently changed component |
| Model | Provider id **and dated snapshot** | An unpinned alias moves with no deploy on your side |
| Tool schemas | Hash of the serialized schema set | A description edit changes behavior invisibly |
| Framework and libraries | Pinned versions | Defaults change in minor releases |
| Config | The values actually live, not the defaults | `max_turns`, autonomy, budgets alter behavior |
| Eval run | Date, set version, `n`, pass rate | Ties this bundle to evidence |

A rollback target that is missing any component is a guess. Never deploy an agent whose model is a floating alias — pin the snapshot and treat a model bump as its own release with its own eval run.

## Rollout

- **Shadow** first where stakes justify it: real inputs, no side effects, compare trajectories against the current version.
- **Canary** by percentage of traffic or by a low-stakes segment. Watch four numbers: end-reason mix, escalation rate, cost per task, p95 latency. Quality complaints arrive days after these move.
- **Hold** the canary for at least one full traffic cycle — a weekday-only sample misses the weekend shape entirely.
- **Roll back the bundle, not the prompt.** Reverting one component while another moved is a new, untested combination.
- Migrations that change memory or state format need a plan for in-flight tasks: drain, or make the new version read the old format.

## Concurrency, Timeouts And Backpressure

- Three timeouts, nested, each strictly below the next: tool call < model turn < whole task < the caller's own timeout. Any inversion turns a slow tool into a mystery hang.
- Bound concurrency by whichever is smallest: provider tokens-per-minute, the slowest downstream service's rate limit, and your worker count. **Tokens per minute is usually binding for agents**, because every turn re-sends the transcript (`cost.md`).
- Queue in front of workers so overload becomes latency rather than errors, and cap the queue so it becomes rejection rather than an unbounded backlog.
- Provider 429s get exponential backoff with jitter and a task-level retry budget; without jitter, every worker retries in lockstep and reproduces the overload (`implementation.md`).
- `runtime_target: serverless` forces externalized state and makes cold starts part of p95; long tasks need the async pattern — accept, return a job id, poll or callback.

## Reliability Numbers That Matter

- End-to-end success is `p^n` (SKILL.md Rule 3). Publish the step count with the promise, or the promise is unfalsifiable.
- Checkpoint after every irreversible action so a crash resumes rather than repeats (`architecture.md`).
- Degrade in a defined order when a dependency fails: retry → fall back to a smaller tier or a cached answer → return a partial result with its reason → escalate. Silent full failure is the only unacceptable option.
- Every fallback path needs its own eval cases; the untested fallback is the one that runs during the incident.

## What To Monitor

| Signal | Alert on | What it usually means |
|---|---|---|
| End-reason mix | Rising `max_turns`, `budget`, `error` | A behavior regression before anyone complains |
| Cost per task type | Median or p95 above budget | Turn growth, bigger tool results, or a cache break (`cost.md`) |
| p95 latency | Above the interactive threshold | Retry storms, serial tool chains, a fallback on the hot path |
| Escalation rate, and reversal rate | Either moving sharply | Triggers wrong in one direction or the other (`human-in-the-loop.md`) |
| Tool error rate by tool | Any tool's rate rising | A dependency degrading, seen first through the agent |
| Approval queue age | Backlog growing | The human gate is now the bottleneck |
| Cache hit rate | Falling to near zero | A volatile line entered the prefix |

Traces are the flight recorder: model snapshot, prompt version, per-turn tool and arguments hash, tokens, latency, end reason (`implementation.md`). Sample transcripts continuously; metrics tell you something changed, transcripts tell you what.

## The Kill Switch

- A single flag that stops the agent taking actions, separate from stopping the service — degraded-but-answering is usually better than gone.
- Tier-scoped: disable irreversible and external tools while leaving read tools live. Most incidents need the writes stopped, not the whole product.
- Test it on a schedule. An untested kill switch is discovered to be broken at the worst possible moment.
- Pair it with a documented "what to tell users" line, so nobody improvises that sentence during an incident.

## On-Call Runbook Contents

For each agent, one page, readable by someone who did not build it: what it does and what it can touch · where the traces are · how to read the end-reason mix · the kill switch and its scope · the current bundle and the previous one · the three failures that have happened before and their fixes · who owns escalation, by contacts key.

## Cadences

Every recurring item below is a row in the `## Due` table of `~/Clawic/data/agents/memory.md` with its last-run date: eval regression run · red-team pass (`security.md`) · cost review per task type · model re-bid · sampled transcript review · kill-switch test · dependency and framework version review. A maintenance schedule with no recorded last run gets skipped for two quarters and nobody notices until an incident does.

**On every release or rollback**, write the row to `~/Clawic/data/agents/deploys/<year>.md` with the full bundle and the result, update the agent's row in `## Agents`, and record the run in `eval-runs/<year>.md` — all in the same turn (`memory-template.md`). Write the on-call runbook to `~/Clawic/data/agents/artifacts/runbook-<agent>.md` with its `## Boxes` line the first time someone is on call for it.
