---
name: "batch_migration_orchestrator"
description: "Use when the user wants a large, mechanical change split into many independent units and executed in parallel with isolated workers and PRs."
---


# Batch Migration Orchestrator

Use this skill for sweeping refactors, migrations, bulk renames, or repetitive codebase-wide edits.

## Goal
Turn one large request into a safe parallel rollout with independent units, validation, and mergeable outputs.

## Workflow
1. Inspect the repo to find every affected area, convention, and dependency.
2. Split the change into independent units by module, directory, or subsystem.
3. Define an end-to-end verification recipe for each unit.
4. Launch workers in parallel only when their write scopes do not overlap.
5. Track completion, collect PRs or patches, and summarize failures.

## Guardrails
- Do not parallelize tightly coupled work.
- Do not let workers edit the same files.
- Require each worker to validate its own unit.
- Prefer worktree or isolated branch execution when git is available.

## Inputs
- Migration target
- Scope boundaries
- Verification method
- Branch/PR expectations

## Example Requests
- Migrate this monorepo from Jest to Vitest in parallel.
- Split this bulk API rename into independently shippable work units.

## Inputs
- Migration goal
- Affected modules or directories
- Verification expectations
- Branch or PR policy

## Outputs
- Work decomposition plan
- Parallel worker prompts
- Status tracking summary
- PR or patch rollup

## Success Criteria
- Every unit has a clear scope.
- No worker write conflicts exist.
- Each unit includes verification.

## Non-Goals
- One-off tiny edits
- Tightly coupled refactors that must land as one patch

## Source Provenance
Derived from Claude Code bundled skill logic in `src/skills/bundled/batch.ts`.
