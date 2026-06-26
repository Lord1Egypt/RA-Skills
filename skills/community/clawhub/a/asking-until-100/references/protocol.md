# Readiness Protocol

## Purpose

Use a visible readiness heuristic instead of claiming hidden certainty. The goal is to decide when
to ask more questions, when to block execution, and when to proceed with explicit assumptions.

## Inputs

- the current user request
- explicit rigor instructions from the user
- repo-local config such as `.asking-until-100.yaml`
- task-specific overrides from the selected profile
- repo context discovered from the current workspace when it looks relevant

## Canonical readiness dimensions

Check these dimensions before acting:

- goal and success criteria
- repo or project state
- architecture, boundaries, interfaces, dependencies, and data flow
- runtime, environment, package manager, deploy target, CI provider, and rollback context
- constraints, tradeoffs, scale, secrets, and timeline pressure
- evidence quality for debugging or build failure claims

## Mode selection

- `fast`: low uncertainty, low rigor, low consequence
- `guided`: moderate ambiguity or one important missing dimension
- `deep`: multiple missing dimensions or explicit high-rigor intent
- `report`: highest-rigor coding or build work where structure and sequencing are still decision
  critical

## Repo-aware rules

- Inspect the repo before asking about facts that are likely discoverable locally.
- Count repo-derived runtime, package manager, CI, deploy, and structural signals toward readiness.
- When repo signals are weak or the task is clearly greenfield, fall back to prompt-only inference.

## Execution gates

- `block`: stay in clarification/planning mode until the blocking dimensions are answered.
- `assumptions`: proceed only with explicit assumptions when the question budget or user intent
  allows it.
- `ask`: surface the remaining gaps and ask the user whether to continue.

Default policy:

- highest-rigor `coding` and `build` tasks => `block`
- everything else => `assumptions`

## Stop conditions

Proceed when:

- readiness is at or above the configured target, or
- the active gate allows progress with explicit assumptions, or
- the user explicitly authorizes continued work despite unresolved gaps

Do not claim full understanding when major dimensions remain unknown.
