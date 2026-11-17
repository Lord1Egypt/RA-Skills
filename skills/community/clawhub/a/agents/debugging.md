# Debugging — Symptom To Cause

Agent bugs are rarely "the model is bad". They are a tool that returned nothing useful, a context that lost the instruction, a cap that tripped silently, or a version that moved. Work the chain.

**Before diagnosing**, read `## Incidents` in `~/Clawic/data/agents/memory.md` (this failure may already have a cause and a fix), the agent's `specs/<agent>.md`, and its runbook in `artifacts/` if `## Boxes` names one.

## The Five-Minute Triage

Ask these in order; each one eliminates a whole class:

1. **What was the end reason?** `done` · `max_turns` · `budget` · `timeout` · `error` · `escalated`. Different reasons are different bugs, and this field alone splits the search space (SKILL.md Rule 9).
2. **Did the model see it?** Dump the exact rendered context of the failing turn. Half of "the agent ignored X" is X not being in the window.
3. **Did the tool return what you think?** Call it directly with the same arguments. The trace shows what the tool said, not what it meant.
4. **Did anything move?** Model snapshot, prompt version, tool schema, framework version, config — compare against the last known-good release row in `deploys/<year>.md` (Rule 8).
5. **Is it reproducible?** Run the same input `n` times. A 3-in-10 failure and a 10-in-10 failure are different investigations (`evaluation.md`).

## Symptom Table

| Symptom | Most likely cause | First move |
|---|---|---|
| Same tool, same arguments, repeatedly | The result never reached the transcript, or it never changes state | Assert the result is appended; add loop detection and inject an observation, not a silent break (`implementation.md`) |
| Alternates between two tools forever | Neither result satisfies the stop condition, which is unstated | Define `done` in checkable terms (`architecture.md`) |
| Invents arguments | Missing `enum`, ambiguous parameter name, or no format in the description | Tighten the schema; validate and return the reason (`tools.md`) |
| Picks the wrong tool consistently | Two descriptions are interchangeable | Merge, or add the discriminator sentence to both (`tools.md`) |
| Claims it did something it did not | No tool call was made; the model narrated the action | Gate completion on the observed side effect, never on the text |
| Follows instructions early, drifts later | Middle-of-context decay, or compaction dropped the rules | Re-anchor after compaction; preserve rules verbatim (`context.md`) |
| Re-asks a question already answered | The answer lived only in a compacted turn | Promote answered facts into the state block (`context.md`) |
| Duplicate side effect after a crash or retry | No idempotency key, or the ledger is written after the call | Reserve the key before the side effect (`implementation.md`) |
| Works in dev, fails in production | Prompt version, model snapshot, tool schema or config differs | Diff the release bundle, not the code (Rule 8) |
| Was fine last week, worse today, no deploy | An unpinned model alias moved | Pin the dated snapshot, then re-run the eval to quantify the gap |
| Cost per task jumped, no code change | Transcript growth, a tool returning bigger results, a cache miss, a retry storm | Cost decomposition in `cost.md` |
| p95 latency several times the median | Retries with backoff, a serial tool chain, or a fallback model on the slow path | Latency decomposition in `production.md` |
| Escalates everything, or nothing | Triggers are vague, or a confidence signal nobody calibrated | Observable triggers (`human-in-the-loop.md`) |
| Eval passes, users complain | The eval set does not resemble traffic | Rebuild cases from sampled real transcripts (`evaluation.md`) |
| Sub-agent output the parent cannot use | The handoff contract is prose | Typed output with a failure shape (`multi-agent.md`) |
| Behaves differently for one user only | Their memory store holds a stale or contradictory fact | Inspect the injected state for that user (`memory-design.md`) |
| Anything else | Reproduce with the smallest loop that shows it — one tool, one turn, fixed inputs — then re-add pieces until it breaks | The piece that breaks it names the subsystem |

## Reading A Trace

Fields worth having, in the order you will use them: `end_reason` → `turn` count → per-turn `tool`, `args_hash`, `result_bytes`, `latency_ms` → `tokens_in` / `cached_in` → `model` snapshot and `prompt_version`.

- **Repeated `args_hash`** is a loop, immediately visible without reading any text.
- **`result_bytes` spiking** on one turn explains a cost jump and a later drift in the same run.
- **`cached_in` collapsing to zero** means something volatile entered the prefix (`cost.md`).
- **`latency_ms` clustered at a round number** is a timeout, not a slow service.
- A trace without `model` and `prompt_version` cannot answer "was it always like this", which is the question you will actually have.

## Reproducing Nondeterminism

- Fix everything you can: temperature, seed if the provider offers one, tool results (replay recorded fixtures), and the timestamp the prompt sees.
- With tool results replayed and the prompt fixed, remaining variance is the model. With them live, you are also testing your dependencies — decide which experiment you are running.
- Report failures as rates over `n` runs. "It failed" is not a bug report for a nondeterministic system.
- Bisect on the bundle, one component at a time: old prompt with new model, new prompt with old model. Two runs answer what a week of reading cannot.

## When The Model Really Is The Problem

Only after the four checks above. Signals that it is genuinely a capability limit rather than a harness bug:

- The failure survives with the tool results replayed, the instruction at the end of the prompt, and the task reduced to one turn.
- A larger tier succeeds on the same fixed inputs where the current one fails, repeatedly.
- The task requires holding more simultaneous constraints than the output ever satisfies at once — that is a decomposition problem, and the fix is fewer things per turn (`architecture.md`), not a bigger prompt.

**When a cause is found**, write one dated line in `## Incidents` of `~/Clawic/data/agents/memory.md` ending in what changed, and add the failing input as a case in `evals/<agent>.md` in the same turn. The second occurrence of the same failure earns a runbook at `~/Clawic/data/agents/artifacts/runbook-<symptom>.md` with its `## Boxes` line (`memory-template.md`). A cause found and not written is a cause found twice.
