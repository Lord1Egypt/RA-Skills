---
name: evolution-analyzer
description: Analyze EvoMap evolution history to detect stagnation patterns and recommend focused next innovation actions from local evolution artifacts.
---

# Evolution Analyzer

Analyzes local `memory/evolution/` artifacts and suggests whether to continue, pivot, or reduce scope for the next cycle.

## When to Use

- After repeated similar signals such as `empty_cycle_loop_detected` or `stable_success_plateau`
- Before deciding to innovate versus optimize
- During heartbeat checks to assess evolution health trends

## Usage

```bash
node skills/evolution-analyzer/index.js
```

## Output

Returns JSON with:

- `totalCycles`
- `lastCycleId`
- `recentFailures`
- `recommendations`

## Notes

- Read-only analysis; does not modify evolution state
- Use `evolution-dashboard` for broader metrics; use this for actionable next-step recommendations
