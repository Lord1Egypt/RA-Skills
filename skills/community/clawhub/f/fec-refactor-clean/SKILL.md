---
name: fec-refactor-clean
description: Use when safely removing dead frontend code, unused exports, stale components, obsolete routes, unused dependencies, or cleanup targets found by tools such as knip, depcheck, ts-prune, TypeScript, ESLint, or manual review. Do not use for feature rewrites that change behavior; Chinese triggers include dead code, clean up unused, refactor clean, dependency cleanup, delete useless code.
---

# Refactoring and cleaning

## Purpose

Identify and clean up unused front-end code under validation protection, reducing technical debt while avoiding accidentally deleting dynamic references, routing entries, configuration files, and runtime conventions.

## Procedure

1. Establish a baseline first: run or confirm the current status of lint, type-check, test, and build.
2. Collect candidates:
   - Prioritize the use of existing tools in the warehouse, such as knip, depcheck, ts-prune, eslint, and TypeScript.
   - When tools are not available, use `rg` to check references, exports, routes, registration points and document entries.
3. Classification by risk:
   - SAFE: test fixtures, unreferenced tool functions, explicitly unexported private components.
   - CAUTION: Shared components, feature entries, style files, Storybook stories.
   - DANGER: routing, configuration, package scripts, runtime templates, dynamic import, plug-in metadata.
   - UPGRADE: Expired dependencies, duplicate dependencies, unused dependencies and security alarms will be evaluated first for dependency upgrade or dependency cleanup, and will not be mixed with dead code deletion.
4. Only SAFE items are automatically processed; CAUTION and DANGER need to output suggestions and evidence and are not deleted directly.
5. Run the affected verification command after each batch cleanup.
6. If the verification fails, stop expanding the cleaning scope and locate the batch first.
7. Conduct behavioral equivalence review after cleaning: public APIs, routes, commands, templates, metadata, documentation examples, and report outputs can still be referenced.
8. Sort technical debt: Prioritize projects that have verification protection, affect development efficiency, or block upgrades; only output suggestions for large-scale rewrites with low evidence.

## Frontend-Specific Checks

- Check JSX/template strings, route configuration, barrel export, Storybook, tests, documentation examples and dynamic component registration.
- Style files need to check className, CSS Modules, Tailwind safelist, global selectors and theme variables.
- Dependency cleanup checks build plugins, runtime templates, CLI scripts, monorepo subpackages, and peer dependencies.

## Constraints

- Does not change user-visible behavior.
- Do not remove public APIs, routes, templates, or configurations that cannot be proven referenceless.
- No "one big delete" replacement for verifiable small batch cleanups.
- Don't mix formatting, renaming or schema rewriting into dead code cleanup.
- No evidence that "no one seems to be using it" is needed; there must be search, tool output, type error disappearance, or test protection.
- Don’t disguise major dependency version upgrades as cleanup; upgrade risks, release notes, and lockfile changes should be offloaded to the dependency upgrade workflow.

## Detailed reference

When writing a cleanup report, load [references/report-template.md](references/report-template.md).

## Expected Output

- Clean reports are saved as `reports/refactor-clean-YYYY-MM-DD-HHmmss.md`.
- After the code is cleaned, the relevant verification commands pass, or the cause of the blocking is clearly stated.
## Structural Refactoring Boundary

This workflow owns proven dead/unused code. When code is live but structurally difficult—long functions, ownership problems, mutable/derived data, conditionals, API shape, or hierarchy design—route it to structural refactoring instead of deleting or rewriting it under cleanup.
