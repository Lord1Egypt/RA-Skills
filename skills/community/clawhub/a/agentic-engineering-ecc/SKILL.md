---
name: agentic-engineering-ecc
description: "Workflow pattern for AI-assisted engineering using eval-first execution, task decomposition, and cost-aware model routing. Trigger phrases: agentic engineering, eval-first workflow, decompose tasks, model routing, cost discipline, task completion criteria."
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":[],"env":[]},"os":["linux","darwin","win32"]}}
---

# Agentic Engineering

Operate as an agentic engineer using eval-first execution, decomposition, and cost-aware model routing. Adapted from everything-claude-code by @affaan-m (MIT).

## Quick Start

1. **Define completion criteria** — write acceptance criteria and success metrics before execution
2. **Create baseline evals** — write capability and regression tests that capture current state
3. **Decompose work** — break into 15-minute units, each independently verifiable with a single dominant risk
4. **Route models by complexity** — Haiku for narrow tasks, Sonnet for implementation, Opus for architecture
5. **Run post-implementation evals** — measure deltas, confirm no regressions

## Key Concepts

- **Eval-first execution:** Run tests before coding; measure against known baseline; catch regressions early
- **15-minute unit rule:** Each task should have one clear risk, one verifiable outcome, be completable in ~15 minutes
- **Model tier matching:** Complexity determines model — don't overpay for simple tasks, don't underpay for hard ones
- **Review focus:** Prioritize invariants, error boundaries, security, coupling — not style (automation handles that)
- **Session strategy:** Continue for coupled units; reset after major phase transitions; compact at milestones

## Common Usage

**Setting up eval-first for a feature:**
```
1. Define acceptance criteria (user-facing behavior)
2. Write capability eval (can the system do the required task?)
3. Write regression eval (does existing functionality still work?)
4. Execute feature implementation with model routing
5. Re-run evals, compare deltas
6. Document any new risks discovered during review
```

**Model routing example:**
- Haiku: boilerplate generation, narrow edits, classification
- Sonnet: feature implementation, small refactors, test writing
- Opus: multi-file changes, root-cause analysis, architecture decisions

**Cost discipline:**
Track per task: model tier, token estimate, retries, wall-clock time, success/failure. Escalate model tier only when lower tier fails with clear reasoning gap, not on uncertainty.

## References

- `references/eval-patterns.md` — detailed eval-first loop patterns
- `references/decomposition-rules.md` — 15-minute unit principle and task breakdown examples
- `references/review-checklist.md` — what to focus on in code review (invariants, boundaries, security, coupling)
