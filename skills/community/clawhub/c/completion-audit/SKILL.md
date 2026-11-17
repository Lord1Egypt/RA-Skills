---
name: completion-audit
description: >
  Part of the Overpowered skill suite.
  Independently determine whether a claimed task outcome is actually complete by reconstructing completion criteria and checking fresh evidence. Use before declaring work done, accepted, migrated, reconciled, fixed, or delivered; not as a general planning loop.
metadata:
  suite: overpowered
  suite_url: https://github.com/raguets/overpowered
  level: "0-primitive"
  version: "0.1.0"
---

# Overpowered / Completion Audit

## Core rule

**Activity is not completion. A completion claim is valid only when its material success criteria are supported by evidence.**

## Procedure

1. Restate the claimed outcome without trusting the worker's summary.
2. Derive observable completion criteria from the original objective, constraints, and acceptance conditions.
3. Identify the authoritative evidence for each criterion.
4. Inspect or run fresh checks when tools permit.
5. Grade each criterion:
   - **PROVEN** — sufficient evidence;
   - **NOT PROVEN** — evidence contradicts the claim or is missing;
   - **NOT APPLICABLE** — criterion does not apply, with reason.
6. Return the actual status. Do not soften `NOT PROVEN` into “probably done.”

## Output contract

```text
Claimed outcome: ...

Criterion | Evidence | Status
...

Verdict: PROVEN / NOT PROVEN
Remaining work or missing evidence: ...
```

## Independence rule

Prefer source artifacts, test outputs, database checks, logs, or direct observations over the executing agent's narrative.

## Gotchas

- Do not add arbitrary criteria that were never part of the objective or necessary invariants.
- A generated file existing is not proof that its contents are correct.
- A successful tool call is not proof that the desired business outcome occurred.
- If verification is impossible, say `NOT PROVEN`, not `FAILED`, unless evidence shows failure.

## Stop condition

Stop when every material criterion has an explicit status and the overall verdict follows from those statuses.
