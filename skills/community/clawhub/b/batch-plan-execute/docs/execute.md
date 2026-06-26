# Autonomous Execute Mode

Use this document only after the user explicitly starts execution in the current turn.

Do not infer execution permission from review approval, `LGTM`, `OK`, `继续`, or other non-execution acknowledgements.

## Execution Gate

Execution is allowed only when the user explicitly asks to start implementation, for example:

- `开始执行`
- `按这个方案实现`
- `去改代码`
- `直接落地`
- `implement now`
- `apply the plan`

If the signal is weaker than that, stay in planning behavior.

## Inputs

Resolve execution targets in this order:

1. an explicit plan file path
2. an explicit `plans/` directory
3. the latest plan lineage next to the referenced requirement source

Use the latest reviewed artifact for each selected module lineage.

Fail immediately if the latest artifact still contains unresolved HTML review comments.

## Grounding Pass

Before spawning execution subagents:

- inspect the affected code areas again
- confirm write boundaries
- confirm shared interfaces, schemas, migrations, and utilities
- confirm dependency layering
- confirm which modules are safe to run in parallel

Do not skip this pass just because plan mode already happened. Execution ownership must still match the live repository state.

## Worker Dispatch

Prefer implementation-oriented subagents for execution work.

Each execution subagent must receive:

- the exact module plan body
- the dependency layer for that module
- the upstream modules that must already be complete
- the shared-change ownership boundaries
- the file or subsystem write scope it owns
- the instruction that it is not alone in the codebase and must not revert unrelated edits
- the instruction to implement, validate locally when possible, and report changed files

Use these rules:

- Dispatch execution subagents in dependency-layer order.
- Within a ready layer, parallelize only modules that do not share ownership of the same schema, interface, migration, utility, or infrastructure change.
- If a shared change is needed by multiple modules, give it one owner execution subagent and make other execution subagents depend on that result.
- If an execution subagent uncovers that its plan is no longer valid against the repository, stop the affected branch and escalate to the main agent instead of freelancing a new plan.

## Main-Agent Responsibilities

The main agent owns:

- execution-subagent selection and dispatch order
- shared-change ownership decisions
- integration of execution-subagent results
- conflict resolution
- final verification

Use these rules:

- Review execution-subagent outputs before advancing downstream layers.
- Do not let downstream work continue if an upstream layer failed validation.
- Preserve user changes and unrelated repo edits.
- Let exceptions and test failures surface. Do not add fallback logic unless the plan explicitly requires it.

## Verification

Run validation in this order:

1. the narrowest module-specific checks that prove the implemented change works
2. broader checks for the touched area
3. final integrated repo checks when the change surface warrants it

Prefer the repository's existing test, lint, typecheck, build, or other validation commands as appropriate for the touched scope.

If only a subset of checks is relevant, run that narrower scope first and still report what broader validation remains unrun.

## Completion Criteria

Execution is complete only when:

- every selected module in the ready scope is implemented
- required validations for those modules pass
- downstream dependencies, if any, have either completed or been explicitly deferred by plan
- the final report names the changed areas, validations run, and any remaining blockers
