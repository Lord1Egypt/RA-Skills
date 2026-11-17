# Refactor Planning Reference

Use before implementation in `fix` and `refactor` modes, and whenever a finding recommends meaningful structural change.

## Required Plan Sections

- objective
- findings addressed
- non-goals
- behavior to preserve
- files likely to change
- proposed steps
- tests to add/update
- migration or compatibility concerns
- rollback plan
- risks and mitigations

## Approval Boundary

When the current user request only asked for analysis or planning, stop after writing `refactoring-plan.md` and ask for approval before editing source code.

When the user explicitly asked to implement a fix/refactor, still create the plan first, then implement according to the plan in the same turn if feasible.

## Refactor Types

- Local extraction: method/function/component extraction.
- Boundary cleanup: move business rules from controllers/views/routes into services/domain helpers.
- Dependency inversion: introduce an interface/port only when tests or architecture require it.
- Pattern adoption: introduce a design pattern only after applying `rules/overengineering.md`.
- Data migration: plan compatibility, backfill, rollout, and rollback.

## Implementation Discipline

Keep changes behavior-preserving unless the user asked for behavior changes. Add tests around current behavior before risky refactors when coverage is thin.
