---
name: automate-this
description: >
  Part of the Overpowered skill suite.
  Transform a described human/business process into an executable automation design by separating deterministic steps, agentic reasoning, existing systems, and human gates; define triggers, data, decisions, exceptions, controls, and verification. Use when the goal is to automate a process, not merely understand it or interview the user about it.
metadata:
  suite: overpowered
  suite_url: https://github.com/raguets/overpowered
  level: "2-process"
  version: "0.1.0"
---

# Overpowered / Automate This

## Core rule

**Automate the process with the simplest reliable mechanism for each step. Do not use an agent where deterministic code, rules, or an existing system is better.**

## Inputs

Accept rough descriptions, SOPs, screenshots, forms, emails, spreadsheets, workflow diagrams, or existing automation artifacts.

## Procedure

1. **Define outcome and trigger.** What starts the process and what observable result ends it?
2. **Map the current flow.** Inputs → steps → decisions → outputs → actors/systems.
3. **Expose exceptions.** Invoke/apply `find-the-exceptions` when branches are incomplete.
4. **Classify every step** with one preferred implementation:
   - deterministic code/rules;
   - database/query;
   - existing application/workflow capability;
   - agentic reasoning;
   - human gate;
   - manual-only / not automatable yet.
5. **Define interfaces.** Inputs, outputs, schemas, side effects, required tools/permissions.
6. **Design human gates.** Use `human-gates` for authority, accountability, ambiguity, or risk.
7. **Define failure behavior.** Retry, timeout, partial success, rollback, idempotency, escalation.
8. **Define observability.** Logs, evidence, run status, audit trail, key metrics.
9. **Define completion criteria.** What proves the workflow achieved the business outcome?
10. **Recommend a dry run** when side effects or scale make it prudent.

## Output contract

```text
Objective
Trigger
Inputs

Step | Purpose | Implementation | Input | Output | Failure path | Human gate

Decision rules
Exceptions / unknowns
Systems and permissions
Observability
Completion criteria
Rollout / dry-run plan
```

When useful, add Mermaid or BPMN-like pseudocode, but the execution table remains authoritative.

## Deep reference

Read `references/implementation-modes.md` when step classification is ambiguous or the design is drifting toward agentic complexity by default.

## Architecture rule

Do not begin by choosing “single agent vs multi-agent.” First classify the work. Agent topology follows from the required reasoning, isolation, concurrency, and permissions.

## Gotchas

- “AI everywhere” is an anti-pattern.
- Do not automate an ambiguous policy; resolve or gate it.
- Do not preserve manual copy/paste steps unless there is a real constraint.
- A human approval without defined trigger/evidence/outcomes is not an implementation.
- Include recovery and idempotency for workflows that can partially execute.

## Composition

- Missing organization knowledge → `know-enough`.
- Historical process examples → `find-precedent`.
- Hidden branches → `find-the-exceptions`.
- Human authority → `human-gates`.
- Risky rollout → `dry-run`.
- Final acceptance → `completion-audit`.

## Stop condition

Stop when every material process step has a chosen implementation mode, interfaces, exception/failure behavior, ownership, and completion evidence.
