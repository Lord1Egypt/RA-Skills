---
name: project-quality-governance
description: Create, audit, or refactor authoritative technical specifications, issue and improvement logs, risk-based verification workflows, and automated documentation checks. Use when an engineering repository needs durable quality governance, structured history, task-routed documentation, or consistency validation. Do not use for ordinary product copy, unstructured personal notes, or documentation unrelated to engineering quality governance.
---

# Project Quality Governance

Build a governance system that is authoritative, searchable, minimally repetitive, cost-aware, and safe to evolve.

## Workflow

1. Inspect the repository before proposing changes. Locate existing contributor instructions, technical specifications, change logs, validation scripts, package commands, hooks, and ignored private areas.
2. Establish the authority order: current user direction, invariant safety rules, verified code and tests, then historical plans.
3. Make the smallest compatible structural change. Preserve useful headings, identifiers, links, and user history; correct facts instead of rewriting history.
4. Establish one lightweight default entrypoint. Route ordinary tasks from it to only the relevant specification section, implementation file, and focused test.
5. Put invariant rules and a task-to-section reading map at the top of the authoritative specification. Keep one H1 and a stable H2/H3 hierarchy.
6. Define explicit context and output budgets. Prefer targeted search, bounded file ranges, concise command summaries, and one grouped verification pass.
7. Separate current rules, verified implementation facts, historical plans, and private experiments.
8. Keep an active status index for unresolved and recent records; move older completed history into searchable archives without deleting it.
9. Add a read-only validator for structure, identifiers, archive uniqueness, budgets, evidence, and time consistency. Integrate it without weakening existing protections.
10. Verify proportionally: L1 for low-risk changes, L2 for one module or behavior, and L3 only for cross-module work, dependency or security boundaries, protected code, or formal release. A commit alone must not raise the level.
11. Report the resulting structure, checks run, unresolved items, and next precise entry point.

## Reference Routing

- Read [references/technical-spec-architecture.md](references/technical-spec-architecture.md) for authoritative specification structure.
- Read [references/issue-and-improvement-log.md](references/issue-and-improvement-log.md) for schemas, indexes, templates, corrections, and release-note candidates.
- Read [references/verification-workflow.md](references/verification-workflow.md) for validation depth, automated checks, and commit preparation.
- Use `scripts/validate-quality-docs.mjs` only after adapting its explicit configuration to the repository's schema.

## Guardrails

- Match the repository's language unless the user requests another language.
- Do not overwrite contributor history or turn unknown facts into invented precision.
- Do not introduce product rules, dependencies, services, or new scope merely to complete documentation.
- Do not read private research or secrets unless the current task explicitly requires it and access is authorized.
- Keep validators diagnostic-only; they must not rewrite documents.
- Preserve existing pre-commit and security guards; add checks compositionally.
- Treat numeric context budgets as repository policy, not universal defaults. Derive or confirm them before enforcing limits.

## Completion Criteria

- The authoritative document exposes invariant rules and task routing before details.
- Heading levels are stable and navigable.
- The status index and detailed records agree exactly.
- Active and archived records are unique, bounded, and discoverable without loading full history.
- Defects and improvements have distinct schemas, explicit evidence, and honest historical gaps.
- Automated checks are reproducible and proportional verification has been performed.
- No private research, secrets, build outputs, or repository-specific material has leaked into reusable artifacts.
