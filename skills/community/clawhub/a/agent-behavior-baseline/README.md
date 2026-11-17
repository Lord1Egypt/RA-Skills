# agent-behavior-baseline

An AgentSkill for answering “did the agent get better?” with data instead of impression.

It builds the smallest set of measurements that survives a change: a trace table, a fixed eval suite, one wired real task, a memory retrieval baseline, and an adherence eval. It also enforces the distinction that most dashboards blur: **environment smoke is not model quality**.

It is a small engineering idea, published in case it is useful. No product, no service, stdlib only. Developed through agent operation and corrected against real failures, not hand-authored as a prompt template.

## The three ideas

1. **Two classes of data.** `smoke` says the environment is wired; `quality` says the agent behaves. Every result carries one label, and no report merges them.
2. **Stable IDs, frozen baseline.** Checks may be fixed, but their IDs stay. Otherwise a suite that keeps “passing” is measuring its own edits.
3. **Denominators, not anecdotes.** Hits are reported over a base, and a single pass never means fixed — especially for destructive or outbound behaviour, which must be tested in a mock.

## Quickstart

```
python3 scripts/trace_store.py init
python3 scripts/eval_suite.py --tasks examples/tasks.json
python3 scripts/trace_store.py summary --since 7
```

`trace_store.py` is a one-table SQLite store with `add` and `summary` by type. `eval_suite.py` runs file and command checks, writes `last-run.json`, and records a trace row when a trace DB is configured.

## What it does not do

- It does not benchmark models against each other.
- It does not prove safety. Adherence checks reduce uncertainty; they do not certify.
- It does not measure answer quality from an environment check. A passing `file_exists` is not a correct answer.
- Samples under 10 are anecdotes; the skill says so rather than reporting a rate.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | Six steps: trace, suite, real task, memory baseline, adherence, change log. |
| `references/adherence-eval.md` | Constraint cards, sampling, mock rules, invalid-test accounting. |
| `scripts/trace_store.py` | Minimal SQLite trace store. |
| `scripts/eval_suite.py` | Fixed-suite runner with trace integration. |
| `examples/tasks.json` | Five-check sample covering both task kinds. |

## License

MIT. Use it, fork it, rewrite it.
