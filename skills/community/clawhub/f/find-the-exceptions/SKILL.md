---
name: find-the-exceptions
description: >
  Part of the Overpowered skill suite.
  Pressure-test a rule, decision table, SOP, requirement, or business process by finding edge cases and alternative branches that would break a happy-path specification. Use before automation or formalization when hidden exceptions could change behavior; focus on material exceptions, not imaginative trivia.
metadata:
  suite: overpowered
  suite_url: https://github.com/raguets/overpowered
  level: "2-process"
  version: "0.1.0"
---

# Overpowered / Find the Exceptions

## Core rule

**A process is not executable until its material non-happy paths are either defined or explicitly unknown.**

## Procedure

1. State the current happy-path rule/process in precise terms.
2. Identify its decision variables: amount, role, state, timing, availability, jurisdiction, data quality, dependencies, etc.
3. Generate candidate exceptions using these lenses:
   - boundaries: exactly at thresholds, empty/zero/max values;
   - missing/invalid/duplicate inputs;
   - timing: late, early, concurrent, reordered events;
   - authority: absence, delegation, multiple approvers;
   - lifecycle: cancellation, amendment, retry, rollback;
   - scope: internal/external, special category, jurisdiction;
   - dependency failure: unavailable system/source/person;
   - conflicting rules or precedents.
4. Filter to exceptions that can materially change the outcome.
5. Resolve discoverable facts from available artifacts before asking the user.
6. Convert resolved branches into a decision table/state model.
7. Mark unresolved branches `UNKNOWN`; do not invent policy.

## Output contract

```text
Condition | Expected path | Exception path | Status | Evidence / decision needed
```

End with:

- newly discovered rules;
- unresolved branches that block automation;
- edge cases that are safe to defer.

## Deep reference

Read `references/exception-lenses.md` for complex processes or when the first pass does not expose enough material branches.

## Interaction rule

When user input is required, ask one high-value question at a time. Prefer a recommended/default answer when there is enough context to propose one.

## Gotchas

- Do not confuse brainstorming bizarre scenarios with finding material exceptions.
- Do not ask humans for facts the environment can provide.
- Exact-threshold behavior is a common source of automation bugs; make it explicit.
- Exceptions can modify data shape, authority, timing, or failure recovery—not only business rules.

## Stop condition

Stop when material branches are defined, deliberately deferred, or explicitly unknown with an owner for resolution.
