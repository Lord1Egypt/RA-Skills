# Parallel Dispatch Rules

Parallel dispatch is valuable only when it reduces total time without creating coordination debt.

## Use Parallel Dispatch When

- tasks are independent
- write scopes do not overlap
- one task does not depend on another's result
- read-only exploration can run concurrently
- verification can run without blocking active implementation

## Avoid Parallel Dispatch When

- tasks edit the same file or module
- the next step depends on a result that is not yet known
- the work shares hidden context that is hard to specify
- the main agent would spend more time integrating than it saves

## Recommended Patterns

### Pattern 1: Parallel Exploration

Good for:

- separate codebase questions
- independent document lookups
- multiple bounded comparisons

Example:

```text
Task A: explore authentication flow in src/auth/*
Task B: explore session refresh flow in src/session/*
Main agent: compare findings and choose fix scope
```

### Pattern 2: Split Implementation By Ownership

Good for:

- disjoint files or modules
- clearly separated responsibilities

Example:

```text
Task A: worker owns src/ui/login.tsx
Task B: worker owns src/api/session.ts
Main agent: integrate and verify end-to-end behavior
```

### Pattern 3: Verification Alongside Sidecar Work

Good for:

- background review while a non-overlapping task continues
- read-only validation of earlier completed work

Example:

```text
Task A: worker updates docs/
Task B: explorer checks whether related examples still match the API
Main agent: accept or request repairs
```

## Required Checks Before Parallelizing

Check all of these:

- [ ] Are write sets disjoint?
- [ ] Can each task be explained without the other?
- [ ] Can the main agent integrate results cheaply?
- [ ] Is neither task on the immediate blocking path?
- [ ] Will total active sub-agents stay within the local runtime limit?

If any answer is "no", do not parallelize yet.

In the current local OpenClaw profile, keep concurrent sub-agents at or below `2`.

## Parallel Status Handling

Each parallel task should have its own status:

- `pending`
- `in_progress`
- `blocked`
- `needs_review`
- `completed`

The main agent should not treat "one task completed" as "all parallel work completed".

## Recovery Rules

If one parallel task fails:

1. keep successful task outputs isolated
2. decide whether the failed task should be retried, rerouted, or absorbed locally
3. re-check whether the remaining work is still worth running in parallel

## Common Failures

| Failure | Cause | Correction |
|---------|-------|-----------|
| merge conflict between workers | overlapping write scope | split by ownership earlier |
| idle waiting on a "parallel" task | hidden dependency | move dependency back to main path |
| duplicated investigation | vague exploration prompts | give different bounded questions |
| hard integration | contracts too broad | shrink task scope before dispatch |
