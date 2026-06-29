# Bootstrap Protocol

Use this when a project has no usable `Docs/` loop state.

## Cold Start Decision

If `Docs/` is missing or both `Docs/TARGET.md` and `Docs/ACCEPTANCE.md` are missing:

1. Do not start coding.
2. Inspect lightweight project context, such as README, package manifests, route names, app name, or user request.
3. Draft a target summary and acceptance contract.
4. Ask the user to confirm or correct the target when the goal is not already explicit.
5. Create `Docs/` files only after the target is clear enough to avoid wasted work.

The agent may create provisional files without a separate confirmation only when all items below are true:

- The user goal can be restated as one sentence.
- A runnable verification command or documentation-only verification method is discoverable.
- No hard-stop risk is present.
- The user's original request includes explicit acceptance criteria, evidence expectations, a failure example, or an implied completion condition that is safe to infer, such as "fix bug X" meaning "X no longer reproduces."

If any item is missing, mark bootstrap as `needs confirmation` and ask the user before implementation. Provisional targets must start with:

```markdown
Status: Provisional
```

Confirmed targets must start with:

```markdown
Status: Confirmed
```

Record provisional assumptions in `Docs/EVALUATION.md`.

## Existing Docs Migration

If the project already has `Docs/` from another workflow, do not rebuild it.

1. If `Docs/TARGET.md` exists but `Docs/ACCEPTANCE.md` is missing, derive a first acceptance contract from `TARGET.md` and mark uncertain items under `Manual Confirmation Needed`.
2. If legacy aliases exist, read them once and migrate to canonical names: `PROJECT_TARGET.md` -> `TARGET.md`, `PROJECT_STATUS.md` -> `STATUS.md`, `COMPLETED_JOBS.md` -> `COMPLETED.md`, `PENDING_JOBS.md` -> `PENDING.md`, `NEXT_STEPS.md` or `SCHEDULE.md` -> `NEXT_ACTIONS.md`.
3. Preserve existing `Docs/COMPLETED.md` or migrated completed-work history.
4. Create missing `LOOP_CONFIG.md`, `STOP_RULES.md`, `EVALUATION.md`, and `LOOP_RUNS.jsonl` with conservative defaults.
5. Record the migration decision in `Docs/EVALUATION.md`.

## File Creation Order

Create files in this order:

1. `Docs/TARGET.md`
2. `Docs/ACCEPTANCE.md`
3. `Docs/LOOP_CONFIG.md`
4. `Docs/STOP_RULES.md`
5. `Docs/STATUS.md`
6. `Docs/PENDING.md`
7. `Docs/NEXT_ACTIONS.md`
8. `Docs/EVALUATION.md`
9. `Docs/LOOP_RUNS.jsonl`
10. `Docs/COMPLETED.md`

Minimum first-loop files are `TARGET.md`, `ACCEPTANCE.md`, `LOOP_CONFIG.md`, `STATUS.md`, `PENDING.md`, and `NEXT_ACTIONS.md`. `STOP_RULES.md`, `EVALUATION.md`, `LOOP_RUNS.jsonl`, and `COMPLETED.md` should still be created before the first loop ends.

Create `Docs/HANDOFF.md` only when a standalone handoff is needed.

## Bootstrap Questions

Ask only what is needed to write `TARGET.md` and `ACCEPTANCE.md`, in this order:

```text
- What is the user goal?
- What must be true for this to be complete?
- What is out of scope?
- What evidence should prove completion?
- What would count as failure?
```

Minimum ask rule:

- If the goal cannot be restated in one sentence, ask for the goal.
- If no explicit or safely implied completion condition exists, ask what must be true for completion.
- If the request could affect data, permissions, external accounts, or existing behavior, ask for non-goals or boundaries.
- If failure would be ambiguous, ask for one failure example.

## Bootstrap Output

After bootstrap, report:

```text
Bootstrap complete / needs confirmation
- Target:
- Success criteria:
- Non-goals:
- Verification plan:
- First next action:
```

Do not proceed to implementation until `TARGET.md` and `ACCEPTANCE.md` are present and not contradictory.

## First Loop Action Template

Use this when creating the first `Docs/NEXT_ACTIONS.md`:

```markdown
# Next Actions

## Immediate Next Action
1. Reproduce or inspect the smallest path that proves the target, then make the minimal safe change and run the core verification command.

## Stop/Resume Notes
- Stop state: Continue
- Resume command or entry point: Use Agent Loop Engineering from Docs/NEXT_ACTIONS.md
- Needed human input: None unless a hard stop appears
```

For documentation-only or skill-only projects, replace "run the core verification command" with "run structural validation and review the changed documentation paths."

Examples:

- Bug fix: `Reproduce bug X with the smallest command or flow, inspect the failing path, make the minimal fix, then run the core verification and the reproduction scenario.`
- New feature: `Identify the narrowest acceptance item, implement only that slice, then run automatic verification plus one functional scenario.`
- Documentation or skill-only: `Validate required files and schema, review the changed references for consistency, and record review evidence in ACCEPTANCE.md.`
