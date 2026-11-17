# Behavior-Preserving Refactoring

Behavior-preserving frontend refactoring orchestration with evidence, risk classification, diff budgets, step verification, rollback, and proof reporting.

## Skill

- ID: `fec-refactoring`
- Category: `review-quality`
- Version: `2.9.0`
- Source: `skills/fec-refactoring/SKILL.md`

## Description

Use when restructuring existing frontend code while preserving observable behavior, including responsibility extraction, module movement, conditional simplification, API cleanup, or data organization. Do not use for new feature behavior, behavior-changing bug fixes, dependency or framework migrations, or proven dead-code cleanup.

## Usage

Install or import this package with any skill runtime that understands the standard `SKILL.md` layout. The canonical source remains the Frontend Craft repository.

## Packaged Files

- [references/principles.md](references/principles.md)
- [references/refactoring-vs-feature-change.md](references/refactoring-vs-feature-change.md)
- [references/when-to-refactor.md](references/when-to-refactor.md)
- [references/workflow.md](references/workflow.md)

## Optional Related Packages

- `@bovinphang/fec-code-smells`
- `@bovinphang/fec-refactoring-catalog`
- `@bovinphang/fec-refactoring-validation`
- `@bovinphang/fec-refactor-clean`
- `@bovinphang/fec-code-review`
- `@bovinphang/fec-tdd-workflow`
- `@bovinphang/fec-debug-framework`
- `@bovinphang/fec-validation-fix`
- `@bovinphang/fec-testing-strategy`

## License

MIT
