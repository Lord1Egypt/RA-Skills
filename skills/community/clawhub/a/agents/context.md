# Context — Budgeting The Only Thing The Model Can See

The model is stateless. Everything it appears to know is in this turn's context, and everything in this turn's context was paid for. What *persists* between tasks is `memory-design.md`; this page is what goes into the window right now.

**Before diagnosing drift or a window overflow**, read `## Stack` in `~/Clawic/data/agents/memory.md` (window size, model tier, compaction settings in force) and the agent's `specs/<agent>.md` for its tool count — the fixed prefix is usually the part nobody measured.

## The Budget

```
window = system_prompt + tool_schemas + injected_state + transcript + tool_results + reserved_output
```

- Reserve the output first, not last. An agent that dies on the final turn because there was no room to answer has been working for free.
- The **fixed prefix** (`system_prompt + tool_schemas`) is paid on every turn: across `T` turns it costs `T × prefix`. Trimming 1,000 tokens from the prefix of a 20-turn task saves 20,000 input tokens per run.
- Measure the four parts once, per agent, and write them into `## Stack`. "We don't know what fills the window" is the state most agents are in when their bill is questioned.

## Placement Beats Volume

- The beginning and the end of the context get followed most reliably; instructions buried in the middle of a long transcript get followed least. This is why an agent "forgets its instructions" at turn 30 with the same prompt that worked at turn 3.
- Re-anchor after every compaction: the operative instructions go back in at the end, not only at the top.
- Order the prefix from most stable to most volatile — system prompt, tool schemas, then anything per-turn. Caching depends on this exact ordering (`cost.md`).
- Put the task restatement immediately before the model's turn, not at the top of a 40k-token transcript.

## Compaction

Compaction is the trade of fidelity for room, and it is where agents silently lose the plot.

- **Trigger** at a fraction of the window, not at overflow — roughly 70-80% used. Compacting at 100% means the compaction call itself has no room.
- **Preserve verbatim**, always: the original goal, hard constraints, the current plan, decisions already made, and the results of side effects already committed. Everything else is summarizable.
- **Summarize** the middle, keep the last few turns raw. The most recent turns are the ones the next decision depends on.
- **Never summarize a tool result you may need exactly** — an id, a diff, a number. Move it to a state block that survives compaction untouched.
- Each compaction is lossy and they compound: after three, the agent is working from a summary of a summary. Track compaction count in the trace, and treat "compacted three times" as a signal to checkpoint and restart with a fresh goal (`architecture.md`).

## What Goes Where

| Content | Home | Why |
|---|---|---|
| Role, rules, output contract | System prompt | Stable, cacheable, followed best at the top |
| Tool schemas | Tool block | Paid every turn — the reason to keep the set small (`tools.md`) |
| Current goal and constraints | A state block re-emitted every turn, or the end of the prompt | Survives compaction, resists middle-of-context decay |
| Committed side effects and ids | State block | Losing these causes duplicate actions after compaction |
| Conversation | Transcript, compacted | The part that grows |
| Big documents | A handle plus an excerpt, fetched on demand | One document must not evict the task (`tools.md`) |
| Facts about the user or account | Injected state, from your own store | Retrieval is for the long tail, state for what must be right (`memory-design.md`) |

## Retrieval Inside The Loop

- Retrieve **per turn on demand**, not everything up front. Preloaded context is paid on every subsequent turn whether it was relevant or not.
- Retrieved passages are untrusted content: label them as data, and they get no instruction authority (SKILL.md Rule 6).
- Keep the retrieved block small and cite the source id, so a wrong answer can be traced to the passage that caused it. Retrieval quality itself is `rag`.
- Do not re-retrieve the same passage every turn. Retrieve once, promote it into the state block, and let the transcript refer to it.

## Symptoms And Causes

| Symptom | Cause | Fix |
|---|---|---|
| Follows instructions early, ignores them late | Instructions in the middle of a long context; compaction dropped them | Re-anchor at the end each turn; preserve rules verbatim through compaction |
| Repeats a question already answered | The answer was compacted away, or lived only in a tool result | Promote answered facts into the state block |
| Duplicates a completed side effect | Committed-actions list was summarized | Keep side effects verbatim; checkpoint (`architecture.md`) |
| Window overflow on the last turn | No output reservation | Reserve output tokens in the budget |
| Costs jumped with no code change | A tool started returning larger results, so every later turn re-sends them | Cap result size at the tool boundary (`tools.md`) |
| Cache hit rate collapsed | Something volatile moved into the prefix — a timestamp, shuffled tools, per-turn memory injection | Volatile content last (`cost.md`) |
| Answers contradict earlier turns | Two versions of a fact coexist — one retrieved, one in state | State wins on conflict, and the retrieved copy is dropped |

## Long-Running Sessions

- Set a **session horizon**, not just a turn cap: after `n` compactions or a wall-clock limit, checkpoint and start a fresh context from the checkpoint. Fresh contexts outperform thrice-summarized ones on the same task.
- Externalize the artifact. An agent writing a long document should write to a file through a tool and re-read the sections it needs, so the document is not carried in the transcript.
- Keep a running "decisions so far" block, appended in one line per decision. It is the cheapest thing that survives compaction and prevents the agent from re-deciding.

**When a compaction strategy, a window budget or a state-block layout is settled**, write it into the agent's `specs/<agent>.md` under the memory policy, and record the measured prefix size in `## Stack` of `~/Clawic/data/agents/memory.md`, in the same turn (`memory-template.md`). A context budget that lives only in someone's head is re-derived, wrongly, at the next cost review.
