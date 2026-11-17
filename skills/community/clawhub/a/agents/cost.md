# Cost — Token Economics Of A Loop

Prices and cache windows change; the arithmetic does not. Verify current per-token prices and cache behavior against the provider's page before quoting money, and quote every figure with its date.

**Before answering any cost question**, read `## Cost` in `~/Clawic/data/agents/memory.md` — or `cost-log.md` if `## Boxes` points there — plus `## Agents` for the model bundle in force. A current number with no prior measurement is not an answer, it is an anecdote.

## Where The Money Actually Goes

```
cost_per_task = Σ_turns ( input_tokens × input_price + output_tokens × output_price ) + tool-side API costs
input_tokens(turn t) ≈ prefix + transcript_so_far          # prefix = system prompt + tool schemas
total_input(T turns) ≈ T × prefix + d × T(T−1)/2           # d = tokens added per turn
```

Three consequences worth internalizing:

1. **Transcript cost is quadratic in turns.** Doubling turns roughly quadruples the growing part. A task that drifts from 5 turns to 15 does not cost 3× more; it costs closer to 9× on that component.
2. **The prefix is paid `T` times.** A 4,000-token prefix over 20 turns is 80,000 input tokens before any conversation. Cutting tools is a cost fix (`tools.md`).
3. **Input dominates output for most agents.** Optimizing the reply length while re-sending a growing transcript every turn is fixing the small term.

## Diagnosing A Cost Jump

In order — the first two explain most cases:

1. **Turns per task.** Pull median turns before and after. A rise means a behavior change: a tool started failing, a stop condition got vaguer, retries began (`debugging.md`).
2. **Tokens per turn.** A tool that started returning bigger results raises every subsequent turn in the same task, permanently (`tools.md`).
3. **Cache hit rate.** `cached_in / tokens_in` collapsing to zero means something volatile entered the prefix.
4. **Model bundle.** An alias moved, or a fallback path is being taken more often (SKILL.md Rule 8).
5. **Traffic mix.** Same cost per task, more of the expensive task type. Report cost per task *type*, never one blended average.

Split the answer into one-time versus run-rate: a batch job that ran once is an incident; a raised floor compounds every month until someone fixes it.

## Prompt Caching, The Largest Single Lever

Caching bills the reused prefix at a discount and only helps when the prefix is byte-identical from the start.

- **Order the prompt most-stable to most-volatile**: system prompt → tool schemas → static context → retrieved memory → transcript. Anything mutable early invalidates everything after it.
- Classic invalidators: a timestamp or "today is" line at the top, tool schemas emitted in a non-deterministic order, per-turn injected memory placed before the transcript, a user id interpolated into the system prompt.
- Caches expire on a provider-defined window; a long human pause mid-conversation means the next turn pays full price. Bursty traffic benefits least.
- Verify the hit rate in the trace (`cached_in`), not in the design. A cache you believe in and never measured is usually broken by one line.

## Model Routing

Route only after the loop is efficient — routing a wasteful loop just buys a discount on waste.

- Two tiers beat five. A small model for classification, extraction, routing and summarization; the main tier for the loop; a frontier tier only where a measured quality gap exists.
- **Break-even for a cascade**: escalating a fraction `f` of traffic costs `small + f × large` versus `large` alone. It pays only while `small + f × large < large`, i.e. `f < 1 − small/large` — and misclassification eats the margin, because a wrong route pays both.
- Routing adds serial latency on escalation: you pay the small model's time *plus* the large one's. On interactive paths this can worsen p95 even as cost falls (`production.md`).
- Sub-tasks are the safest routing surface: summarize with the small tier inside a loop that runs on the main tier. No classifier needed, no misroute possible.
- Re-check the choice on a cadence — put "model re-bid" in the `## Due` table. Tier prices and capabilities move faster than most configs.

## Reducing Cost Without Losing Quality

Ordered by savings per hour of work:

| Move | Mechanism | Watch |
|---|---|---|
| Cut turns | Better stop condition, fewer unnecessary tool calls, a plan instead of exploration | Quadratic term shrinks fastest |
| Fix the prefix for caching | Reorder, freeze tool order, move volatile content last | Verify with `cached_in` |
| Truncate tool results at the boundary | Stops one big result costing on every later turn | Return a handle instead (`tools.md`) |
| Trim the tool set | Every schema is paid every turn | Also improves selection accuracy |
| Compact earlier | Bounds transcript growth | Lossy; preserve the state block (`context.md`) |
| Small tier for sub-tasks | Summaries, classification, extraction | Measure the quality delta on the eval set |
| Cap retries per task | Retry storms are invisible in the median and obvious in the p95 | `implementation.md` |
| Batch offline work | Providers commonly discount asynchronous batch processing | Only for work with no latency requirement |
| Shorter outputs | Output price is usually the higher per-token rate | The smaller term for most agents |

## Budgets And Enforcement

- `cost_ceiling_per_task_usd` is enforced inside the loop, checked before each turn (`implementation.md`). A budget checked at the end is a report.
- Set a per-user or per-tenant daily ceiling as well: a single pathological input should not be able to spend the month.
- Alert on **cost per task by type**, not total spend. Total spend rises with success; cost per task rising is the regression.
- Fan-out multiplies by `k` (`multi-agent.md`). Any parallel design states its `k` and its worst-case cost before it ships.
- Quote the monthly number with a task-volume assumption written next to it: `median_cost × tasks_per_month`, plus the p95 tail for the pessimistic case.

## Measuring Properly

- Per task type, not blended. Report **median and p95** — the average is dragged by the tail and describes no real task.
- Sample size for a cost claim is the same problem as an eval claim: enough runs that the median is stable (`evaluation.md`).
- Include tool-side costs: search APIs, databases, third-party calls. An agent whose model cost is 0.01 USD and whose search calls are 0.05 USD has a search problem, not a model problem.
- Attribute by task type in the trace itself, or you will be reconstructing it from timestamps later.

**After any cost measurement or optimization**, write the row to `## Cost` in `~/Clawic/data/agents/memory.md` — task type, agent, median, p95, median turns, the date measured, and the currency — overwriting the existing row for that task type rather than adding a second one. An optimization also earns its line in `## Cost Changes` of `cost-log.md` once that section has split out (`memory-template.md`). Record the cost review's run date in `## Due`; a review with no last-run date gets skipped for a quarter and nobody notices.
