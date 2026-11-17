---
name: assumption-audit
description: >
  Part of the Overpowered skill suite.
  Expose material assumptions, hidden premises, and unresolved unknowns in a plan, analysis, design, or decision. Use before committing to work when an incorrect assumption could change the approach; avoid turning trivial low-impact unknowns into bureaucracy.
metadata:
  suite: overpowered
  suite_url: https://github.com/raguets/overpowered
  level: "0-primitive"
  version: "0.1.0"
---

# Overpowered / Assumption Audit

## Core rule

**Treat assumptions as manageable risk, not invisible context.**

## Procedure

1. Read the proposed plan, analysis, or decision.
2. Extract only assumptions that could materially change the result.
3. Classify each as:
   - **verified fact**;
   - **reasonable working assumption**;
   - **testable unknown**;
   - **decision still required**.
4. For each material assumption, state what would change if it were false.
5. Resolve cheap, discoverable facts using available tools instead of asking the user.
6. Escalate only decisions, unavailable knowledge, or genuinely ambiguous intent.

## Output contract

```text
Assumption | Status | Why it matters | Cheapest resolution
```

End with the smallest set of unresolved assumptions that must be addressed before the next irreversible step.

## Gotchas

- Do not list generic project risks just to make the table longer.
- “Likely” is not “verified.”
- If a tool or artifact can cheaply answer the question, inspect it before asking a human.
- Not every unknown must be resolved before progress; focus on decision-changing unknowns.

## Stop condition

Stop when the remaining unresolved assumptions are either explicitly accepted or must be resolved before the next material action.
