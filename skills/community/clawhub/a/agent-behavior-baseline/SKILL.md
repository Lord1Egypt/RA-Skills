---
name: agent-behavior-baseline
description: "Establish an observable baseline for an AI agent before changing it: a minimal SQLite trace store, a fixed eval suite with stable IDs, real-task wiring, a memory retrieval baseline, and an adherence eval with constraint cards. Use when adding observability, measuring whether a change improved behaviour, or deciding between an index and a knowledge graph. Tool-agnostic; stdlib only."
license: MIT
---

# Agent Behavior Baseline

Without a baseline, every change is judged by impression. This skill builds the smallest measurement set that can answer “did it get better?”, and it separates the two things that are constantly confused: **environment smoke** and **model quality**.

> Developed through agent operation and corrected against real failures, not hand-authored as a prompt template.

## Applicability

**Use for**
- Before changing a system prompt, rule file, tool policy, or retrieval setup.
- When someone asks “is the agent still working correctly?” and there is no data.
- When deciding whether to add a knowledge graph, a new index, or more tools.

**Do not use for**
- Benchmarking across models. This is a local regression baseline, not a leaderboard.
- Proving safety. Adherence checks reduce uncertainty; they do not certify.
- Short-lived experiments where no baseline will be used again.

## Boundary

Required: local execution, file system access, Python standard library.

Known limits:
- A pass on an environment check says nothing about answer quality. Label every result as `smoke` or `quality`.
- Fixed suites overfit: once checks are added to fix failures, the suite measures itself. Keep original IDs stable and add new ones separately.
- Memory retrieval baselines measure top-k hit, not answer correctness.
- Adherence samples under 10 are anecdotes, not statistics.

## Step 1 — Trace store

One table, stdlib only:

```
task_id TEXT PRIMARY KEY, type TEXT, source TEXT, started_at TEXT,
duration_ms INTEGER, tools TEXT, retries INTEGER,
tokens_in INTEGER, tokens_out INTEGER, outcome TEXT,
error_class TEXT, artifact TEXT, notes TEXT, constraint_fail INTEGER DEFAULT 0
```

`scripts/trace_store.py init | add | summary --since N`.

**Completion criterion:** a row exists for the run you just did, and `summary` can aggregate by type.

## Step 2 — Fixed eval suite

Put checks in `state/evals/tasks.json`. Each has an `id`, `name`, `kind` (`file_exists` or `command`), and either `path` or `cmd` with optional `expect_contains`.

Rules:
- Mix kinds; a suite of only file checks measures installation, not behaviour.
- IDs are permanent. Fixing a stale check means updating its expectation, not deleting the ID.
- A failing check is a finding. Do not relabel it as “known”.

**Completion criterion:** pass count, failed IDs, and duration reported for every run.

## Step 3 — Wire one real task

- Wrap one high-frequency task (a scheduled job, a watchdog) with the tracer.
- The wrapper must emit nothing on success; otherwise every run looks like an alert.
- Verify the wrapper: run it against a no-op and confirm zero bytes of output.

**Completion criterion:** one scheduled task produces a trace row without producing output.

## Step 4 — Memory retrieval baseline

Choose 10 real queries spanning rules, versions, configuration, recent reports, and procedures. Run each, take top 3, and judge hit / partial / miss by hand.

If misses cluster on coverage (a path is not indexed), fix coverage first. Only if misses cluster on relationships or time should you consider a graph or entity index.

**Completion criterion:** 10 judged queries and one decision: coverage fix, index card, or graph evaluation.

## Step 5 — Adherence eval

Turn each critical rule into a constraint card: trigger, must, must-not, failure criterion, source. Then define tasks that exercise them.

- Record `constraint_fail` per run.
- Rules must exist in the prompt or system context; a constraint only present in the eval file is invisible to the agent and the test is invalid.
- Destructive or outbound tests run in a mock or sandbox, never against real targets.
- Report x/y over repeated samples. One pass is not a fix.

**Completion criterion:** at least 10 samples, per-task PASS/FAIL/PARTIAL, and invalid tests counted separately.

## Step 6 — Change log

Every measurement change gets a line: item, path, purpose, rollback command, review date. If nothing was added, write “no new dependencies”.

**Completion criterion:** rollback is possible without reconstructing from memory.

## Decision rules

- Memory baseline ≥ 8/10 → do not build a knowledge graph.
- Failures concentrated in coverage → add paths or index cards, then re-run.
- Only persistent relationship/time failures justify evaluating a graph.
- A single passing sample never justifies “fixed”.

## Discipline

- Separate smoke from quality in every report. Merging them is the most common way a dashboard lies.
- Keep the baseline frozen; do not tune checks to current output.
- Report the denominator. “3 failures” means nothing without “out of 20”.

## Final self-check

1. Trace row written and aggregation works.
2. Eval suite has mixed kinds and stable IDs.
3. One real task is wrapped and silent on success.
4. Memory baseline has 10 judged queries and a decision.
5. Adherence eval has ≥10 samples, with invalid tests separated.
6. Every result labelled `smoke` or `quality`.
