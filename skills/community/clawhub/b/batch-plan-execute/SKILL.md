---
name: batch-plan-execute
description: Use when the user wants AI to turn a requirement text, requirement document, and existing reviewed plan files into dependency-ordered implementation plans and, only after an explicit execution command, implement those plans with subagents in parallel where safe and in sequence where required.
---

# Batch Plan Execute

Use this skill when the task is to create, revise, retire, execute, or inspect module plans based on a requirement source and the current `plans/` directory state.

This skill has two explicit modes:

- `plan`: generate or revise implementation-ready plans
- `execute`: implement already-reviewed plans

Do not enter `execute` mode unless the user explicitly starts execution in the current turn.

## What This Skill Does

- Accepts requirement text from chat, a requirement file such as `requirements.md`, or an existing plan file or `plans/` directory.
- Reconstructs the current planning state from the latest requirement source, existing plan files, and a hidden state file.
- Detects mixed changes per module: new requirements, changed requirements, removed requirements, and review notes.
- Builds dependency-aware module or workstream plans that reflect parallelizable and serial work.
- Executes approved plans with implementation subagents only after an explicit execution command from the user.

## Input Handling

Choose the primary input in this order:

1. An explicit plan file path or `plans/` directory path mentioned by the user.
2. An explicit requirement file path mentioned by the user.
3. A file or document already attached in the task context.
4. The requirement text written directly in the chat.

Use these rules:

- If a plan file path is provided, treat that plan lineage as the primary starting point and inspect the sibling `plans/` directory.
- If a `plans/` directory path is provided, inspect only plan files and the state file inside that directory.
- If a requirement file path is provided, read it directly and treat it as the latest requirement source.
- If the input is raw chat text, treat the full user text as the latest requirement source.
- If both a requirement source and a `plans/` directory are available, always use both.
- Match the final plan language and the execution-progress language to the dominant language of the latest requirement source unless the user explicitly asks for translation.

Fail immediately if any referenced file or directory does not exist or is not readable.

## Execution Gate

Default to `plan` mode.

Enter `execute` mode only when the user explicitly issues an execution command in the current turn.

Examples that DO enter `execute` mode:

- `开始执行`
- `按这个方案实现`
- `去改代码`
- `直接落地`
- `implement now`
- `apply the plan`

Examples that DO NOT enter `execute` mode:

- `LGTM`
- `OK`
- `继续`
- `按这个方向`
- `review 过了`
- any approval that confirms the plan but does not explicitly ask to start implementation

Use these rules:

- Review approval is not execution approval.
- If the user is ambiguous, stay in `plan` mode and either refine the execution plan or ask for a clearer execution command.
- Never infer execution intent from momentum, optimism, or lack of objections.

## Output Location And Naming

Write plan files into a `plans/` directory:

- If the source is a requirement file, use a `plans/` folder next to that file.
- If the source is a plan file or `plans/` directory, keep writing into that same `plans/` directory.
- If the source is raw chat text, use `<cwd>/plans/`.

Create the `plans/` directory if it does not exist.

Base plan files use this format:

- `<module-slug>.md`

Revision plan files use this format:

- `<module-slug>.rev-<n>.md`

The hidden state file must be:

- `.batch-plan-state.json`

Use these naming rules:

- `new-plan` may create a base file if the module has no prior lineage.
- `revise-plan` and `obsolete-plan` must always write a new `rev` file.
- `no-op` must not write a new plan file.
- Do not overwrite an existing file silently.
- Plan slugs should follow implementation ownership, not requirement heading text, when the two differ.

## State File

Maintain `plans/.batch-plan-state.json` as the planning baseline.

The state file must contain at least:

- `requirement_source`
- `requirement_hash`
- `run_at`
- `modules`

Each module state object must contain at least:

- `slug`
- `title`
- `status`
- `source_excerpt_hash`
- `body_hash_without_heading`
- `latest_plan_file`
- `latest_rev`
- `last_action`

Status values must be explicit:

- `active`
- `obsolete`

Use these rules:

- The state file describes planning lineage only.
- Do not treat the state file as permission to execute.
- If the state file is missing, bootstrap from the latest requirement source and the existing plan files instead of failing.

## Plan Mode

Use [docs/plan.md](./docs/plan.md) as the detailed plan-writing contract.

### Module Extraction

Default to splitting by implementation units and dependency boundaries, not by repository package structure and not mechanically by requirement headings.

Before extracting modules or computing any requirement hashes, preprocess the latest requirement source by removing HTML comments outside fenced code blocks.

Use these rules:

- Treat commented requirement content as nonexistent.
- Start from requirement sections only as an extraction aid, not as the final module boundary.
- Treat meta sections such as background, goals, scope, non-goals, assumptions, rollout, acceptance criteria, and non-functional requirements as global constraints, not standalone modules.
- Merge requirement slices that land on the same implementation path, shared code surface, or same owner-level deliverable.
- Split a section only when it clearly describes independent deliverables or a strict implementation sequence such as foundation work before feature work.
- Prefer module boundaries that match functional ownership, shared interface ownership, migration boundaries, or deployment boundaries.
- Do not create overlapping modules that both own the same shared change.
- Fail loudly if no implementation-bearing modules can be extracted or if shared ownership cannot be assigned clearly.

If the source is plain text with no reliable headings:

- derive a concise module list from the requirement content
- use feature boundaries, workflows, deliverables, and prerequisite relationships as module names
- avoid generic module names like `misc`, `other`, or `supporting-work`

### Dependency And Parallelism Modeling

After extracting candidate modules, derive an explicit dependency graph before classification or subagent spawning.

Use these rules:

- Classify each module as `foundation`, `feature`, or `follow-on`.
- Record `depends_on`, `blocks`, `parallelizable_with`, and `shared_change_owner`.
- Prefer parallel modules only when they do not require the same shared code ownership in the same phase.
- Prefer serial sequencing when one module changes contracts, schemas, migrations, or shared utilities that another module consumes.
- If the implementation is `A then B`, model that directly instead of forcing both into one peer list.
- Do not infer fake parallelism. Sequence conservatively if safe ordering is unclear.

### Review Detection And Lineage

Review detection is only meaningful inside `plans/*.md`.

Use these rules:

- Treat any HTML comment outside fenced code blocks as a review note.
- If review content in user comments conflicts with the original requirement document, treat the review content as the latest authoritative instruction.
- Do not preserve HTML comments in final plan output.
- Resolve the latest lineage artifact by highest `rev`, otherwise latest base file.
- Prefer slug matches first.
- Allow rename matching only for safe one-to-one matches on `body_hash_without_heading`.
- If rename matching is ambiguous, do not guess.

### Mixed-Mode Classification

Determine action per module, not once for the whole run.

Classify each module into exactly one action:

- `new-plan`
- `revise-plan`
- `obsolete-plan`
- `no-op`

Use these defaults:

- Merge requirement changes and review notes into one `revise-plan`.
- Generate an `obsolete-plan` revision instead of silently dropping removed modules.
- When no requirement source is available, allow review-driven revisions only.
- Comment-only edits in the requirement source must not trigger `revise-plan`.

### Plan Subagents

Spawn one planning subagent per affected module after locking the module list, dependency graph, and action.

Use these rules:

- Prefer read-only analysis subagents for planning work.
- Use a general-purpose subagent only if a dedicated read-only analysis role is unavailable and the subagent can still stay read-only.
- Planning subagents must not edit files.
- Run planning subagents in parallel only within the same dependency layer.
- Ask each planning subagent to return affected code areas, interfaces, dependencies, parallelism notes, risks, tests, and explicit assumptions.

### Plan Assembly

The main agent owns final plan quality, plan file output, and state file updates.

Use these rules:

- Resolve cross-module dependencies so terminology and shared changes stay consistent.
- Confirm one clear owner for each shared interface, schema, migration, or infrastructure change.
- Order final module output according to dependency layers rather than requirement heading order.
- State explicitly when a module is blocked by another module or can run in parallel after prerequisites.
- Refresh `plans/.batch-plan-state.json` only after all affected modules are processed.

## Execute Mode

Use [docs/execute.md](./docs/execute.md) as the detailed execution contract.

Enter this mode only after the explicit execution gate is satisfied.

### Execution Preconditions

Fail immediately if any of these is true:

- no target plan file or `plans/` directory can be resolved
- the latest target plan artifact still contains unresolved review comments
- the repository cannot be grounded enough to assign write ownership safely
- shared-change ownership is ambiguous
- dependency cycles cannot be justified as a merged module

### Execution Behavior

Use these rules:

- Execute the latest reviewed artifact for each selected module lineage.
- Respect the dependency graph produced in plan mode or reconstruct it from the latest plan set before dispatch.
- Use implementation subagents for code changes.
- Give each implementation subagent a clear write scope and ownership boundary.
- Do not let two implementation subagents own the same shared interface, schema, migration, or infrastructure change in the same layer.
- Run implementation subagents in parallel only inside the same ready dependency layer.
- Hold downstream layers until upstream validation succeeds.
- Let failures surface. Do not add fallback logic unless the plan explicitly requires it.

### Execution Verification

The main agent owns final verification and integration.

Use these rules:

- Run the narrowest useful validation first, then broader repo checks if the change surface warrants it.
- Prefer the repository's existing validation commands for the affected scope and the final integrated output.
- Report failures with the exact blocking module or layer.
- Do not mark execution complete while required validations are still failing.

## Failure Rules

Stop and report the problem instead of generating weak output when:

- the requirement file, plan file, or plans directory is missing or unreadable
- module extraction fails for a required requirement source
- a plan would be mostly speculation with no meaningful codebase tie-in
- multiple latest lineage candidates exist for one module and the ordering cannot be resolved safely
- rename matching is ambiguous and cannot be reduced to a safe one-to-one mapping
- shared changes or dependency ownership cannot be assigned to one clear module or workstream
- the dependency graph contains cycles that cannot be justified as a single merged module
- the state file exists but is malformed and cannot be safely reconstructed from visible artifacts

Do not emit empty plan files, summary-only files, or a single aggregate plan when the task requires per-module outputs.
