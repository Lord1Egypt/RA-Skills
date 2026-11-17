---
name: dry-run
description: >
  Part of the Overpowered skill suite.
  Simulate a workflow, migration, bulk update, automation, or other side-effecting operation before committing changes. Use when effects are broad, costly, irreversible, externally visible, or difficult to audit; skip when the action is trivially reversible and low risk.
metadata:
  suite: overpowered
  suite_url: https://github.com/raguets/overpowered
  level: "0-primitive"
  version: "0.1.0"
---

# Overpowered / Dry Run

## Core rule

**Preview the consequences before committing side effects when the cost of being wrong is material.**

## Procedure

1. Identify the intended action and all externally visible side effects.
2. Define a simulation mode that uses representative inputs but blocks or redirects side effects.
3. Produce a change plan or predicted outcome:
   - records/files/messages affected;
   - decisions the workflow would make;
   - exceptions and failures;
   - human gates triggered.
4. Compare the simulated result with invariants and acceptance criteria.
5. If material surprises appear, stop and revise before live execution.
6. Preserve the dry-run report as evidence for approval when useful.

## Output contract

```text
Dry-run scope
Predicted changes
Exceptions
Human gates triggered
Invariant checks
Go / No-go recommendation
```

## Gotchas

- A dry run that still sends real emails or writes production data is not a dry run.
- Use representative edge cases, not only the happy path.
- Do not confuse “no error” with “correct effect.” Check business invariants.
- State any side effects that cannot be simulated faithfully.

## Stop condition

Stop when predicted effects are explicit enough to approve, revise, or reject live execution.
