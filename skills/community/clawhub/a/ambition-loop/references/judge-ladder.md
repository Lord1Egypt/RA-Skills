# External judge ladder

Use the highest rung you can reach. Rungs 1–4 count as outside judges. Rung 5 is a last resort and must be labelled. Rung 6 is never evidence.

| Rung | Judge | Examples |
|---|---|---|
| 1 | **Reality / outcome** | Production metric after rollout, A/B test, real user behaviour, the system staying crash-free over N days |
| 2 | **Runnable check on unseen data** | Held-out or future data for predictions, a fresh benchmark run, a reproduction on a clean machine, fuzzing |
| 3 | **Deterministic tool** | Test suite, type checker, linter, compiler, proof checker, schema validator, profiler or Lighthouse numbers, accounting reconciliation |
| 4 | **Independent reviewer** | A domain expert, a blind evaluator, a separate model instance with no shared context grading against a rubric written *before* the work |
| 5 | **Structured self-check (weak)** | A checklist run against the output. Label it `WEAK` and pair it with what a real judge would be |
| 6 | **Opinion (not allowed)** | "Looks good", "should work", the model's confidence |

## Picking the pass line
- Write the pass line **before** doing the work: a number, a threshold, or a binary result.
- For predictions, fix the train/test split first. Do not tune on the test set.
- For performance, say how it was measured (cold or warm, device, percentile).
- For writing and decks, use a reviewer rubric that checks whether the reader can state the decision and the cause in a sentence, along with any factual claims that can be checked against sources.

## By domain (starting points)
- **Code:** tests (add failing ones first), CI, benchmarks, reproductions on all target OSes, static analysis.
- **Data / analytics:** reproducing from raw data, held-out validation, backtests, reconciling against source-of-truth totals.
- **Performance:** profiler traces, p50 and p95 under fixed load, Lighthouse or WebPageTest.
- **Research / writing:** citations verified against primary sources, a blind reviewer against a rubric, fact checks.
- **Business decisions:** a backtest on history ("would this have caught it sooner?"), a parallel run beside the current process.
- **Design:** usability test tasks, accessibility checkers, measured contrast and performance.
