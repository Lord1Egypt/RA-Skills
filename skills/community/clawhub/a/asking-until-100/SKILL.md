---
name: asking-until-100
description: Repo-aware questioning protocol for OpenClaw that increases clarification before acting on coding, project-build, architecture, debugging, and implementation tasks. Use when requirements, repo context, constraints, interfaces, success criteria, or execution rigor are ambiguous and the agent should ask higher-signal questions or generate a structured question report before implementation.
---

# Asking Until 100

## Overview

Use this skill to slow down execution when the task is underspecified, risky, or expensive to get
wrong. Treat "100" as target readiness to proceed, not literal certainty.

## Workflow

1. Load explicit instructions and repo-local config such as `.asking-until-100.yaml`.
2. Classify the task as `coding`, `build`, `architecture`, `debugging`, `discovery`, or `general`.
3. Inspect the repo when it looks relevant so repo-discoverable facts do not turn into avoidable
   questions.
4. Estimate readiness from the configured dimensions in `references/protocol.md`.
5. Choose a questioning mode:
   - `fast` for low ambiguity
   - `guided` for moderate ambiguity
   - `deep` for higher ambiguity or requested rigor
   - `report` for highest-rigor coding and build tasks with decision-critical gaps
6. Ask the highest-value questions before taking action.
7. Respect the execution gate:
   - highest-rigor `coding` and `build` tasks default to blocking clarification
   - other tasks default to explicit assumptions when gaps remain

## Questioning Style

- Prefer structural, directional, and decision-shaping questions over generic filler.
- Use a working hypothesis when it helps the user react to a proposed path.
- Offer suggested answers when useful, but always leave a free-form path.
- Do not ask for facts that can be inspected directly from the repo.

## High-Rigor Report

For highest-rigor coding or build tasks, begin with `Provisional Project Structure`, then emit:
`Working Hypothesis`, `Architecture Questions`, `Product Questions`, `Constraint Questions`, and
`Decision-Critical Unknowns`.

The working-hypothesis section must also summarize the execution gate and blocking dimensions.

See `references/coding-report-format.md` for the required output order and
`scripts/render_project_structure.py` for deterministic structure rendering.

## References

- `references/protocol.md` for readiness, repo-aware escalation, and stop conditions
- `references/config.md` for config fields, precedence, and asking-intensity behavior
- `references/question-patterns.md` for question quality rules and option patterns
- `references/coding-report-format.md` for the high-rigor report contract
- `references/build-playbook.md` for build-specific gaps to check before acting

## Scripts And Assets

- `scripts/validate_config.py` validates profile files
- `scripts/preview_question_report.py` previews questioning output for a prompt
- `scripts/render_project_structure.py` renders prompt-only or repo-aware provisional structures
- `scripts/explain_profile_merge.py` shows the effective merged profile
- `assets/` contains bundled profiles tuned for `gpt-5.4` with `xhigh` reasoning assumptions

Keep this file concise. Use the references for detailed policy, config, and output examples.
