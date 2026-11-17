# Evaluation — Knowing Whether A Change Helped

An agent without an eval set has one measurement: complaints. This page is how to build the set, size it, score it, and gate releases on it.

**Before any prompt, tool or model change**, read `evals/<agent>.md` and the last rows of `eval-runs/<year>.md` (via `## Boxes` in `~/Clawic/data/agents/memory.md`). A change proposed without the current baseline in hand cannot be evaluated afterwards, because there is nothing to compare to.

**Contents:** [What to score](#what-to-score) · [Building the set](#building-the-set) · [Sizing](#sizing-how-many-cases-how-many-runs) · [Scoring](#scoring-methods) · [Judges](#llm-judges-where-they-work) · [The gate](#the-regression-gate) · [Online](#online-measurement) · [Metrics](#metrics-worth-tracking)

## What To Score

Three layers, and skipping the middle one is the usual mistake.

| Layer | Question | How |
|---|---|---|
| **Outcome** | Did the task get done correctly? | Assertions on the final state or answer |
| **Trajectory** | Did it get there the right way? | Expected tools called, in an acceptable order, without forbidden ones |
| **Cost of getting there** | What did it spend? | Turns, tokens, wall clock, money per case |

A right answer reached by a lucky guess and one reached by calling the tool look identical at the outcome layer. Score trajectory or you will ship an agent that passes evals and fails the day a tool's data changes.

Forbidden-tool assertions matter as much as expected ones: an injection case passes only if the exfiltration tool was **not** called (`security.md`).

## Building The Set

- **Start from real traffic, not imagination.** Twenty sampled transcripts produce a better first set than a brainstorm, because they contain the phrasings you would never invent.
- **Every diagnosed failure becomes a case in the same turn** (`debugging.md`). This is the mechanism that stops regressions, and it is the only one that costs nothing.
- Cover deliberately: happy path · ambiguous input · missing information · tool failure · empty result · out-of-scope request · escalation-worthy case · injection attempt · multi-step case that needs a plan · a case with two valid answers.
- Tag every case (`happy-path`, `injection`, `regression`, `tool-failure`) so you can report per-tag pass rates. A flat 0.91 hides a 0.4 on the injection tag.
- Keep cases small and independent. A case that depends on the previous one cannot be run `n` times or in parallel.
- Freeze the expected values. If a case's expectation is edited to match new behavior, it stopped being a test — record such edits explicitly as a set version bump.

## Sizing: How Many Cases, How Many Runs

- Agents are nondeterministic: **`n` runs per case**, scored as a pass rate. `n = 5` is a workable default; `n = 1` cannot distinguish a fixed bug from a lucky run.
- Resolution: the 95% confidence half-width on a proportion is at most about `1/√N` where `N` is total runs. So `N = 100` resolves ±10 points, `N = 400` resolves ±5, `N = 1,000` resolves ±3. **A 3-point improvement is not visible in a 100-run eval** — that is the arithmetic behind most "the change did nothing" arguments.
- Zero failures is not zero risk: the rule of three puts the 95% upper bound at `3/N`. Zero injection failures in 50 attempts still permits a true rate near 6%; to claim under 1% you need roughly 300 clean attempts.
- Comparing two variants needs the same cases, the same `n`, and the same fixtures. Different sets produce numbers that cannot be subtracted.
- Cost the run before promising a cadence: `cases × n × median_cost_per_case`. A 64-case set at `n = 5` and 0.012 USD is under 4 USD — cheap enough to run weekly, which is the point of keeping cases small.

## Scoring Methods

| Method | Use for | Cost | Watch out |
|---|---|---|---|
| Exact / schema assertion | Ids, structured output, tool sequences, forbidden tools | Free | Brittle on free text |
| Substring or regex must-contain / must-not-contain | Key facts present, banned phrases absent | Free | Passes on the right words in the wrong sentence |
| Deterministic checker | Code runs, SQL returns the right rows, file has the right shape | Free after writing it | Only exists where the domain has a verifier |
| Human review | Taste, tone, subtle correctness | Expensive, slow | The ceiling everything else is calibrated against |
| LLM judge | Free text at scale, when a rubric exists | Cheap per case, needs validation | Agrees with itself, not necessarily with you (→ next section) |

Prefer the cheapest method that can fail for the right reason. Most agent cases can be scored deterministically because the interesting assertion is about tools and state, not prose.

## LLM Judges, Where They Work

- A judge is a measurement instrument: **validate it against human labels before trusting it**, on a sample of cases you have labelled by hand, and report that agreement next to every score it produces.
- Give it a rubric with anchored levels and a reference answer where one exists. Reference-free scoring on open-ended output is the weakest configuration there is.
- Force a decision shape: a score plus the specific evidence for it. "Good, 4/5" is unauditable.
- Known biases to design against: position (order the two candidates both ways), verbosity (longer looks better), and self-preference. Randomize and average.
- Re-validate the judge whenever the judge model changes — it is part of the release bundle too (SKILL.md Rule 8).

## The Regression Gate

With `eval_gate: true`, a prompt, tool or model change is presented as blocked until it has been measured:

1. Record the baseline: pass rate, trajectory pass rate, median cost, p95 latency, per-tag rates, with the set version and `n`.
2. Apply the change. Re-run the identical set.
3. Ship if overall pass rate does not drop, no tag drops by more than the resolution of the run, and cost and latency stay inside their budgets.
4. Write the row to `eval-runs/<year>.md` with what changed — both runs, not only the good one.
5. A change that improves overall while dropping the injection or escalation tag is a rejection, not a trade-off.

## Online Measurement

Offline sets are stale the moment traffic shifts. Three cheap online signals:

- **End-reason distribution.** A rising share of `max_turns`, `budget` or `error` is a regression that no offline set caught (`debugging.md`).
- **Escalation and reopen rates.** Escalations that a human immediately reverses mean the trigger is wrong; resolved tasks that come back mean the outcome check is too weak (`human-in-the-loop.md`).
- **Sampled transcript review**, a fixed number per week, scored against the same rubric as the offline set. Every failure found becomes a case.

Shadow-run a candidate on real inputs without acting on its output when the stakes justify it: same traffic, no side effects, compare trajectories.

## Metrics Worth Tracking

| Metric | Definition | Why it earns its place |
|---|---|---|
| Pass rate | Passing runs / total runs, per tag | The headline, meaningless without `n` and the set version |
| Trajectory pass rate | Runs with the expected tool path | Catches right answers reached wrongly |
| Median and p95 cost | Per task type | The average hides the tail that pays the bill (`cost.md`) |
| Median and p95 latency | Per task type | p95 is what users experience as "broken" |
| Turns per task | Median | Rising turns means the plan degraded before quality did |
| End-reason mix | Share of each reason | The earliest online regression signal |
| Escalation rate and reversal rate | Both, together | One alone is uninterpretable |

**After every eval run**, write the row to `~/Clawic/data/agents/eval-runs/<year>.md` — date, agent, set version, `n`, pass rate, trajectory pass rate, median cost, p95 latency, model bundle, what changed — and add any new case to `evals/<agent>.md`, in the same turn (`memory-template.md`). Runs kept in a terminal scrollback cannot answer "when did this get worse", which is the only question anyone asks later.
