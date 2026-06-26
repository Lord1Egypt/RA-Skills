# Asana Task Guide — Task Manifest Format

The engineer produces a Task Manifest after the Implementation Plan is finalized. The PM uses this manifest to create the Asana board. The engineer does not create Asana tasks directly — this document is the handoff artifact.

## Task Manifest Structure

The manifest is a structured list organized by role. Each task maps directly to the PM's Asana task format (SRS ID, complexity, effort, acceptance criteria, dependencies).

---

## Task Entry Format

For each task:

```
Task ID: [ROLE]-TASK-[NNN] (e.g., FE-TASK-001, BE-TASK-001, DB-TASK-001, QA-TASK-001)
Title: [concise task title — verb + noun, e.g., "Implement user registration form"]
Assigned Role: FE Dev | BE Dev | DB / BE Dev | QA Engineer
SRS Requirement(s): [SRS-XXX, SRS-YYY]
Spec Section: [FE-001, BE-003, DB-002 — the Implementation Plan section this task implements]
Complexity: Low | Medium | High
Effort: [story points] ([hours] hours)
Sprint/Phase: [which development phase this belongs to]

Description:
  [2-4 sentences describing what this task accomplishes. Reference the spec section for full detail.]

Acceptance Criteria:
  - [ ] [criterion 1 — matches the spec's acceptance criteria]
  - [ ] [criterion 2]
  - [ ] [criterion 3]

Dependencies:
  - Blocked by: [ROLE-TASK-NNN — task(s) that must complete before this one can start]
  - Blocks: [ROLE-TASK-NNN — task(s) that cannot start until this one completes]
```

## Organizing by Role

Group tasks under role headers so the PM can assign them in bulk:

### Database Tasks
DB tasks generally come first — schema must exist before BE can build on it.

### Backend Tasks
BE tasks follow DB tasks. Group by feature area, not by endpoint.

### Frontend Tasks
FE tasks can begin in parallel (scaffolding, routing, static components) but API-dependent work follows BE tasks.

### QA Tasks
QA tasks map to features, not to individual FE/BE tasks. QA tests the integrated feature, not isolated endpoints or components.

### Engineering Tasks
Tasks the engineer owns (rare — usually just "Code Review" and "Produce Implementation Plan"):

```
ENG-TASK-001: Produce Engineering Design & Implementation Plan
Assigned Role: Project Engineer
SRS Requirement(s): All
Complexity: High
Effort: [estimate based on project scope]
Dependencies: Blocked by PM completion of SRS sign-off
```

## Dependency Identification Rules

Use these patterns to identify dependencies (aligned with the PM's dependency framework):

1. **Schema before service:** Any BE task that reads/writes a table depends on the DB task that creates/modifies that table.
2. **Service before consumer:** Any FE task that calls an API endpoint depends on the BE task that implements that endpoint.
3. **Auth before protected:** Any task involving protected resources depends on the auth implementation task.
4. **Core before extension:** Base CRUD depends on table creation. Advanced business logic depends on base CRUD.
5. **Integration before consumption:** Third-party integration setup must precede any task that uses that integration.

## Task Sizing Guidance

Aim for tasks that are completable in 1-3 days. If a task estimates at 8+ story points or 2+ days, consider splitting it:

- Split by sub-feature (e.g., "User CRUD" → "Create user endpoint" + "List users endpoint" + "Update user endpoint")
- Split by layer if a single feature spans FE+BE (each gets its own task)
- Never split artificially — a task should be a coherent unit of work

## Manifest Summary

At the end of the manifest, provide a summary the PM can use for sprint planning:

```
Total Tasks: [count]
  FE: [count] ([total story points] points, [total hours] hours)
  BE: [count] ([total story points] points, [total hours] hours)
  DB: [count] ([total story points] points, [total hours] hours)
  QA: [count] ([total story points] points, [total hours] hours)
  ENG: [count] ([total story points] points, [total hours] hours)

Critical Path: [list the sequence of dependent tasks that determines minimum project duration]
Parallelizable: [which role tracks can run simultaneously]
Recommended Sprint Breakdown: [if applicable — which tasks fit in sprint 1 vs. 2 vs. 3]
```
