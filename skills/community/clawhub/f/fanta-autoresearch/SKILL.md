---
name: autoresearch
description: "Autonomous goal-directed iteration for optimization and improvement tasks. Use when you need to systematically improve a metric, optimize a system, or iteratively refine something. Triggers on phrases like 'autoresearch', 'autonomous loop', 'iterate until', 'improve X', 'optimize Y', or when user wants to run multiple iterations of make-change → verify → keep/revert cycles."
---

# Autoresearch Skill

Run autonomous iteration loops: **Goal → Metric → Loop (make change → verify → keep/revert → repeat)**.

## Core Protocol

```
SETUP:
1. Define GOAL (what to improve)
2. Define METRIC (how to measure success)
3. Define SCOPE (what can be modified)
4. Establish BASELINE (current metric value)

LOOP (forever or N iterations):
1. Review current state + history + results log
2. Pick next change (based on what worked, what failed, what's untried)
3. Make ONE focused change
4. Commit change (for rollback)
5. Run mechanical verification (tests, benchmarks, scores)
6. If improved → keep. If worse → revert. If error → fix or skip.
7. Log the result
8. Repeat until goal reached or max iterations
```

## Principles

1. **One change per iteration** — Atomic changes. If it breaks, you know why.
2. **Mechanical verification only** — No subjective "looks good." Use metrics.
3. **Automatic rollback** — Failed changes revert instantly.
4. **Git is memory** — Each experiment is committed. Git revert preserves history.
5. **Simplicity wins** — Equal results + less code = KEEP

## Quick Start

```
Goal: Improve memory search Top-1 hit rate from 65% to 75%
Metric: Benchmark score (openclaw cron runs --id <job-id> --limit 1)
Scope: ~/.openclaw/workspace/MEMORY.md, ~/.openclaw/openclaw.json
Max Iterations: 5
```

Then run the loop manually or spawn a subagent to execute it.

## Usage Patterns

### Pattern 1: Manual Loop (Interactive)

For simple tasks, run the loop yourself:

```
Iteration 1:
  - Change: [describe what you'll change]
  - Verify: [run verification]
  - Result: [keep/revert + reason]
  - Log entry
```

### Pattern 2: Spawn Subagent (Autonomous)

For longer tasks, spawn a subagent with the loop instructions:

```
sessions_spawn with:
  - task: Full autoresearch loop specification
  - timeoutSeconds: 600 (10 min per iteration)
  - mode: run (one-shot) or session (persistent)
```

### Pattern 3: Background Process

For very long loops, use exec with background continuation:

```
exec with:
  - command: The optimization script
  - background: true
  - yieldMs: 60000 (check every minute)
```

## Verification Commands

| Domain | Verify Command |
|--------|----------------|
| Memory search | `openclaw cron runs --id <job-id> --limit 1` |
| Tests | `npm test`, `pytest`, `cargo test` |
| Build | `npm run build`, `cargo build` |
| Lint | `eslint .`, `ruff check .` |
| Benchmarks | `npm run bench`, custom benchmark script |
| Coverage | `npm test -- --coverage` |

## Logging Format

Track iterations in TSV format:

```
iteration	change	metric_before	metric_after	delta	status	description
0	baseline	65.0	65.0	0.0	baseline	initial state
1	lowered minScore	65.0	70.0	+5.0	keep	improved retrieval
2	tried larger model	70.0	68.0	-2.0	revert	worse, reverted
3	added corpus entry	70.0	72.0	+2.0	keep	filled gap
```

## Subagent Template

When spawning a subagent for autoresearch, use this template:

```markdown
GOAL: [what to improve]
METRIC: [how to measure]
VERIFICATION: [command to run]
SCOPE: [files that can be modified]
MAX_ITERATIONS: [number]

CONSTRAINTS:
- [resource limits]
- [safety rules]
- [reversibility requirements]

APPROACH:
1. Establish baseline
2. For each iteration:
   a. Identify next change
   b. Make ONE atomic change
   c. Run verification
   d. Compare to baseline
   e. Keep if improved, revert if worse
   f. Log result
3. Report final results
```

## Common Patterns

### Improving Benchmark Scores

```
Goal: Improve benchmark score
Metric: Benchmark output
Changes: Config tweaks, corpus improvements, model changes
Iterations: 5-10
```

### Fixing Tests

```
Goal: All tests passing
Metric: Test count failing
Changes: Fix one test at a time
Iterations: Until zero failures
```

### Reducing Bundle Size

```
Goal: Bundle < 100KB
Metric: Build output size
Changes: Remove dependencies, tree-shake, minify
Iterations: Until target met
```

### Increasing Coverage

```
Goal: Coverage > 80%
Metric: Coverage percentage
Changes: Add tests for uncovered lines
Iterations: Until target met
```

## Failure Handling

| Failure | Response |
|---------|----------|
| Syntax error | Fix immediately, don't count as iteration |
| Runtime error | Attempt fix (max 3 tries), then move on |
| Resource exhaustion | Revert, try smaller variant |
| Timeout | Revert, simplify approach |
| External dependency failed | Skip, log, try different approach |

## Stopping Conditions

- Goal metric reached
- Max iterations hit
- No improvement for 3 consecutive iterations
- User interrupt (Ctrl+C or `/stop`)

## References

For advanced patterns, see:
- [references/workflows.md](references/workflows.md) — Multi-step workflows
- [references/metrics.md](references/metrics.md) — Common metric patterns