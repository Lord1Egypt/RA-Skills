# Task Contract Template

Every delegated task should be issued with a task contract. This is the minimum structure needed to keep multi-agent work bounded and reviewable.

## Required Fields

- `goal`
- `task_type`
- `domain`
- `expected_output`
- `owned_scope`
- `forbidden_scope`
- `blocking_status`
- `verification_method`

## Related Runtime Fields

These are not part of the contract itself, but operators usually inspect them alongside task contracts during execution:

- `status`
- `verification_status`
- `acceptance_result`
- `attempt_count`
- `last_dispatch_status`
- `next_retry_after`

## Minimal Contract

```text
Goal: [what the sub-agent should accomplish]
Task type: [explore / implement / verify / operate]
Domain: [code / knowledge / content / ...]
Expected output: [file, summary, diff, checklist, review note]
Owned scope: [files, modules, system area, external target]
Forbidden scope: [areas it must not change]
Blocking status: [blocking / sidecar]
Verification method: [exact check or evidence required]
```

## Recommended Extended Contract

```text
Goal: Investigate why the retry flow fails on timeout and identify the minimal fix scope.
Task type: explore
Domain: code
Expected output: Root-cause summary with affected files and proposed fix scope.
Owned scope: Read-only inspection of src/retry/* and tests/retry/*.
Forbidden scope: Do not edit files. Do not inspect unrelated modules unless required to confirm the cause.
Blocking status: blocking
Verification method: Findings must cite the inspected files and explain why the bug occurs.
```

## Contract Rules

1. `goal` must be concrete
2. `expected_output` must be reviewable
3. `owned_scope` must be narrow enough to check
4. `forbidden_scope` should name likely collision zones
5. `blocking_status` tells the orchestrator whether waiting is justified
6. `verification_method` must be something the main agent can confirm

## Scope Design Guidance

For read-only work:

- use module or file inspection boundaries
- forbid edits explicitly

For implementation work:

- assign a disjoint write set where possible
- name tests or checks that prove the change

For external operations:

- define the target system or path exactly
- define what counts as success

## Anti-Patterns

Do not dispatch contracts like:

```text
Go fix this.
Look into it.
Handle the content task.
Do whatever is needed.
```

These are not contracts. They prevent clear ownership and make acceptance weak.

## Main-Agent Review Questions

Before dispatching, ask:

1. Can I tell what success looks like?
2. Can I tell what the agent is allowed to touch?
3. Can I verify the result independently?
4. Is this task small enough to delegate safely?

If any answer is "no", rewrite the contract before dispatch.
