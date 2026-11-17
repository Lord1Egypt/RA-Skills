# Verification Workflow

## Task Card

Before editing, record objective, authorized scope, directly related files, risks, verification level, and completion conditions. Group related adjustments before implementation to avoid repeated scans and full-suite runs.

Use a linear path: locate once, edit as a group, verify by risk, record the stage, then stop or hand off. Do not repeatedly rescan the repository or rerun successful checks after every small edit.

## Context and Output Budgets

Set explicit project limits for initial files, default file ranges, command output, visual evidence, and handoff summaries. Prefer targeted search and concise success output. On failure, rerun only the failed check unless new evidence invalidates earlier results.

## Verification Levels

### L1: Low Risk

For prose, documentation, or narrow presentation changes: inspect the diff, run the relevant documentation validator, and inspect only affected visuals when appearance changed.

### L2: Module Risk

For one feature, parser, lifecycle, or behavior: run focused tests and add type or build checks when crossing a compile or bundle boundary.

### L3: High Risk or Release Boundary

For cross-module changes, dependencies, security boundaries, protected code, or a formal release: run the full test suite, lint, build, relevant guards, documentation checks, and targeted desktop/mobile review when applicable. Creating a commit does not by itself raise L1 or L2 work to L3.

## Automated Documentation Checks

A validator accepts explicit paths and optional configuration. Check frontmatter; one H1 and no heading jumps; configured numbered sections; unique identifiers across active and archived logs; exact active index/detail agreement; prefix, type, and label consistency; type-specific required fields; end time and evidence for completed records; release copy for candidates; document update time; and configured active-record or context-budget limits.

The validator reads only specified files, emits actionable diagnostics, and never modifies documentation.

## Repository Integration

Compose documentation validation with existing pre-commit guards. Do not replace protected-code, secret, private-research, or build-leak checks. Inspect staged paths before committing so fixtures, generated outputs, and private materials remain excluded.
