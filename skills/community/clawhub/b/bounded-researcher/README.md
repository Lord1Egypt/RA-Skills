# bounded-researcher

`bounded-researcher` is an OpenClaw skill for software-agent research tasks that must stay narrow, evidence-first, and implementation-oriented.

It is designed for teams where:
- a supervisor owns decisions
- a researcher should reduce uncertainty without taking architecture ownership
- cheaper research models need strong behavioral constraints

## Best For

- codebase triage
- bug localization
- validation runs
- evidence summaries
- narrow precedent or documentation checks

## Not For

- writing production code
- making final architecture decisions
- broad open-ended exploration with no bounded next step

## Core Guarantees

- separates facts from inference
- stops at the next bounded step
- attributes external claims
- marks unsupported license claims as `license unverified`
- escalates instead of improvising when scope expands

## Files

- `SKILL.md`: skill instructions
- `manifest.yaml`: package metadata
