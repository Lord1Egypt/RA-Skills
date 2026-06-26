---
name: cli-anything-openclaw
description: Adapt HKUDS CLI-Anything for OpenClaw workflows. Use when the user wants to build, refine, test, or validate an agent-native CLI harness for a GUI application or source repository inside OpenClaw, mentions CLI-Anything, or asks to apply the CLI-Anything methodology on a local path or GitHub repo.
---

Use this skill as an OpenClaw-native bridge to the upstream CLI-Anything methodology.

## What this skill is

This skill packages the core CLI-Anything methodology in a portable form for OpenClaw users.

Use it when the user wants to:
- analyze whether a software project is a good fit for an agent-friendly CLI harness
- design command groups and workflow structure for a GUI application or repo
- refine an existing harness
- validate packaging, tests, and CLI entry points using CLI-Anything-style thinking

## Inputs

Accept either:
- a local source path
- a GitHub repository URL

Derive the software name from the local directory name if needed.

## Required references

Read these in order:

1. `references/harness.md` — core methodology and workflow
2. `references/codex-skill.md` — condensed Codex-oriented rules
3. Relevant command references as needed:
   - `references/cli-anything.md`
   - `references/cli-anything-refine.md`
   - `references/cli-anything-validate.md`
   - `references/cli-anything-test.md`
   - `references/cli-anything-list.md`

## Preferred workflow

1. Acquire source locally if needed.
2. Analyze architecture, backend surfaces, data model, and current automation affordances.
3. Decide whether the project is a good fit for an agent-native CLI harness.
4. If building:
   - propose command groups
   - propose state model
   - propose `agent-harness/` layout
5. If refining:
   - inventory current commands and tests
   - identify gaps
   - prioritize high-impact additions
6. If validating:
   - check packaging, CLI namespace, tests, and JSON output expectations
7. Always report:
   - files changed or proposed
   - commands run
   - risks / limitations
   - next best step

## Important constraints

- Treat this as a methodology skill, not as a promise that a harness already exists.
- Prefer wrapping real software backends rather than reimplementing behavior.
- Plan tests before writing them.
- Keep outputs concrete and actionable.
