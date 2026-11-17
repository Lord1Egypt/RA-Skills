---
name: fec-code-review
description: Use when the user asks for general frontend code review, PR review, merge-readiness assessment, architecture maintainability, type-safety, rendering/state risks, style consistency, testability gaps, or a cross-cutting review summary. Delegate deep security, accessibility, E2E, or performance investigations to their specialized skills; Chinese triggers include code review, code review, review.
---

# Front-end code review

## Review modes and coverage

User-specified scope takes precedence over the default. Use the following three review modes:

- **Change review**: only when recent changes, current edits, staged changes, a PR or a commit are explicitly requested or clearly established by the active task, review those changes and necessary context. For local changes, inspect staged and unstaged diffs and relevant untracked project files within the requested scope; a staged-only request reviews only staged changes. If there are no changes, report that there is nothing to review; do not switch to recent commits or expand scope automatically.
- **Targeted review**: when files or directories are specified, inventory and review existing code in that scope, including unchanged code; no Git diff is required.
- **Project review (default)**: when no scope or change context is specified, or when the entire project is requested, inventory project-owned frontend code, related tests, configuration and dependency declarations, then review in module batches, including unchanged code; no Git diff is required.

Select scope before collecting diffs. A file/directory alone means full review of that scope; a path combined with an explicit change request restricts incremental review to that path. An unqualified invocation defaults to project review even if Git changes exist. At review start, state the selected mode and target scope. When automatically delegating review after edits, pass the current change scope explicitly; do not trigger project review merely because the reviewer was called.

Exclude dependency directories, build outputs, caches, generated files and third-party code by default, and record exclusions. Keep the frontend responsibility boundary; this is not a backend audit. A nonexistent target or a scope with no relevant files must be reported explicitly, not replaced with another scope.

Merge findings with the same root cause across batches. Report **review mode, target scope, reviewed files/modules, exclusions, unreviewed files/modules, completion status and verification commands/results**. If context or execution limits prevent completion, mark the review partial and list remaining modules; never claim complete project coverage. Reading callers for context or running project-wide lint/typecheck does not count as manual review of those files.

Change reviews retain merge recommendations. Targeted and project reviews use a risk assessment (Low / Medium / High, with blocking findings), not a claim of merge readiness. Preserve severity levels, evidence requirements and report filenames. Output reports only unless repairs are explicitly requested.

## Purpose

Review the front-end code quality from 8 dimensions including architecture, type safety, accessibility, style consistency, performance and testability, and output a graded review report.

## Procedure

1. Read the project facts first: package scripts, frameworks, directory conventions, recent diffs, existing tests and related rules.
2. Find problems based on risk, rather than picking styles based on personal preference; each finding must be able to point to specific files, line numbers, and user impacts.
3. Use five axes to converge conclusions: correctness, maintainability, type/interface, user experience, and verification coverage.
4. Only preliminary screening will be done for deep water areas such as safety, accessibility, E2E, and performance; diversion will be clearly defined when special investigation is needed.
5. During multi-dimensional review, first split according to responsibilities, and then merge similar findings; only one main finding for the same root cause of the same file is retained to avoid repeated noise.
6. List blocking issues first in the report, then recommendations; do not write firm conclusions on issues without evidence.

## Multi-dimensional review arrangement

When changes span multiple quality dimensions, organize them according to "main review + special diversion" instead of having all dimensions repeatedly check the same code.

| Dimension | Trigger condition | Diversion boundary |
| ------------------- | ---------------------------------------------------- | ------------------------------------ |
| TypeScript Projects and Type Contracts | DTOs, generics, public types, type guards, `any`, assertions, tsconfig | In-depth type modeling and TS configuration handed over to the TypeScript process |
| State management | State attribution, global store, URL state, derived state, cross-page synchronization | State selection and migration are handed over to the state management special process |
| Security | User input, HTML rendering, token, upload, third-party script | Vulnerability level analysis is handed over to the security-specific process |
| Accessibility | Pop-up windows, menus, forms, keyboard operations, focus management | WCAG scrutinizes the special accessibility process |
| Performance | Large lists, heavy dependencies, repeated requests, long tasks, package sizes | Handle performance evidence and budget to the performance-specific process |
| E2E | Key user path, login status, payment, cross-page process | Browser use cases and traces are handed over to E2E special process |

Discover merge rules:

- When the same root cause appears in multiple dimensions, only the highest severity level is retained and the related dimensions are listed in `Dimension`.
- Repeated patterns in multiple places in the same file are merged into one pattern-level discovery, and representative locations are listed.
- Questions with insufficient confidence are placed in Open Questions and will not be upgraded to blocked items.
- Format issues that can be stably captured by automation are handed over to lint/format and are not discovered by human reviewers.

## Review dimensions

1. Architecture

- Is the component boundary clear?
- Whether display logic and business logic are separated
- Is there a reusable abstraction?
- Whether there is a God component

2. Type safety

- Whether there is unnecessary `any`
- Is the props type clear?
- Is the return value of hooks/composables stable?
- Whether the API contract has type constraints where feasible

3. Rendering and status

- Is there unnecessary repeated rendering?
- Is the use of key stable?
- Whether the deducible state is stored repeatedly
- Is the local state coupled too deeply?
- Whether the global store only saves client state that is truly shared across borders
- Whether the boundaries between URL state, server state, form state and browser persistence are clear

4. Style

- Whether the magic number is still used when there is already a Token
- Whether the class name is consistent with the warehouse convention
- Is responsive processing clear?
- Are multiple style systems being mixed unnecessarily?

5. Accessibility

- Is the semantic structure reasonable?
- Whether label and aria are used correctly when needed
- Whether to support keyboard operation
- Is the focus management of floating layers and menus correct?

6. Maintainability

- Is the component/page file size reasonable (it should be within **300 lines**; if it exceeds **500 lines** or is too complex, it must be split. See "Component file size" in the shared React/Vue rules)
- Is the naming quality good?
- Is there any repetitive logic that should be extracted
- Whether there is dead code, outdated comments or temporary hacks
- Whether the business status, type, and identification use bare numbers/naked strings (should be aligned with `templates/shared/rules/fec-typescript.md` "Magic Number / Magic String is prohibited")

7. Test

- Is critical test coverage missing?
- Is there a fragile selector or unstable test mode?

8. Security

- No obvious XSS risks (dangerouslySetInnerHTML/v-html must be reviewed)
- No sensitive information hardcoded
- Direct rendering without unvalidated user input

9. Performance and experience evidence

- Whether to introduce heavy dependencies on the first screen, repeated requests, large list rendering or long tasks
- Whether the status of loading, empty, error, disabled, focus, etc. is complete
- Whether the responsive layout has verifiable breakpoints and text overflow protection

10. Must-check items (blocking merge)

- [ ] TypeScript complete type, no `any`
- [ ] No guardless assertions for external input, DTO, and public type boundaries
- [ ] No XSS risk
- [ ] No sensitive information hardcoded
- [ ] Core logic has unit tests

11. Quality items (suggested modifications)

- [ ] The size of the component file complies with the agreement (within about 300 lines is preferred; if it exceeds 500 lines or is highly complex, the sub-components/Hooks/Composables/utils have been disassembled)
- [ ] No duplicate code (DRY principle)
- [ ] No unused imports

12. Normative items (style suggestions)

- [ ] clear naming semantics
- [ ] comments cover complex logic

## Detailed reference

When writing a code review report, load [references/report-template.md](references/report-template.md). Findings must be specific and actionable; don't write general recommendations such as "optimize performance" without pointing out specific code patterns.

## Constraints

- Do not write personal style preferences as blocking issues; blocking items must have clear evidence of user impact, runtime risk, security risk, or maintenance cost.
- Do not give findings without file locations and supporting evidence; a diff is required only for change review.
- In-depth security, accessibility, E2E and performance issues are only screened initially; when an evidence chain is needed, they will be diverted to special skills.
- Do not report multiple reports for the same root cause; merge them into one representative finding and list the scope of impact.
- Format issues that are stably covered by automated tools are handed over to lint/format and are not discovered by human reviewers.

## Expected Output

- Grading review report (CRITICAL / HIGH / MEDIUM / LOW)
- Each problem is associated with a specific file and line number, with suggestions for repairing it.
- It is not recommended to merge the blocking item (CRITICAL) until it is repaired
- The review report is saved as `reports/code-review-YYYY-MM-DD-HHmmss.md`
- Multi-dimensional reviews should consolidate duplicate findings and explain which special capabilities have been diverted to
- Label uncertain items with required verification commands or supplementary context, and do not write guesses into facts
## Refactoring Boundary

A general review may flag maintainability evidence, but dedicated smell diagnosis or a behavior-preserving refactoring plan owns deeper structural analysis. Review should not silently execute structural changes; it can recommend diagnosis/planning when a finding needs systematic transformation.
