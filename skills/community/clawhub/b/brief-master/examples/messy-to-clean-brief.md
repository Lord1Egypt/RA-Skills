# Messy Request To Clean Brief

Brief Master exists for the moment before Proof Loop: the user knows what hurts, but the task is still too vague to hand to an agent safely.

## Messy Request

```text
The German translation thing is still broken. Can you get an agent to fix it properly? It timed out last time and I do not want another half-fix.
```

## Clean Agent Brief

```markdown
## Task
Fix German prompt translation persistence so translated form schemas are populated reliably.

## Inputs
- Repo: `/workspace/app`
- Start with `apps/server/src/prompts/translation.service.ts`
- Read the existing translation timeout issue and latest failing test output first.

## Acceptance Criteria
AC1: All 50 German prompt rows have `formSchemaTranslated` populated after running the translation endpoint.
Verify: run `pnpm test:server translation` and inspect the seeded German prompt rows.

AC2: The translation job handles provider timeout without leaving partial NULL state.
Verify: use the existing timeout fixture or add one focused test if missing.

AC3: Existing English prompt behaviour is unchanged.
Verify: run the current prompt service tests.

## Constraints
- Do not change the public API response shape.
- Do not rewrite unrelated prompt storage code.
- Keep the fix small enough for focused review.

## Non-goals
- No new translation provider.
- No UI work.
- No broad prompt model migration.

## Verification
Run the focused server tests first. If they pass, run the broader prompt test suite. Record command output in the task evidence.
```

## What Changed

The cleaned brief turns a complaint into something an agent can execute:

- one task
- known starting files
- explicit acceptance criteria
- constraints and non-goals
- verification commands
- evidence expectations

That is the handoff point where Proof Loop can freeze the spec and make completion auditable.
