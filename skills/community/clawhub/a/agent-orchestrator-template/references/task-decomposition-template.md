# Task Decomposition Template

Use this template whenever a single request is too large or too tangled to hand off in one go. A clear decomposition keeps each sub-task bounded, documents dependencies, and highlights what can safely run in parallel.

## Decomposition Steps

1. **State the headline goal.** Rephrase the request in a single sentence that captures the final result the user expects.
2. **Break the goal into sub-goals.** Each sub-goal should map to a single task type or supporting activity (for example, exploratory analysis, implementation, verification, or operation).
3. **Document dependencies.** Note which sub-goals must finish before others start and whether a dependency only needs a partial artifact (draft notes, test results, triage decisions).
4. **Declare owned scope.** For every sub-task, specify exactly what the agent owns (files, modules, data sources, APIs, etc.) and what it must not touch.
5. **Mark parallel eligibility.** Identify when tasks are independent enough to run concurrently using the criteria in the parallel-dispatch rules.
6. **Define integration checkpoints.** Explain how outputs will be merged, who validates them, and what handoffs happen between sub-agents.

## Sub-task Worksheet

Use this table to make decomposition explicit before dispatching any sub-agents.

| Sub-task | Task type | Dependencies | Owned scope | Forbidden scope | Parallel eligible? | Integration note |
|----------|-----------|--------------|-------------|------------------|-------------------|
| Example: Investigate failing retry tests | explore | none | `src/retry/*` and `tests/retry/*` read-only | production config files | yes, read-only | pass stack trace + failure steps to implement task |

### Worksheet Guidance
- **Dependencies:** List prior sub-tasks or artifacts. If the dependency is just knowledge (for instance, “needs summary from explore task”), note that explicitly so the implementer knows what to wait for.
- **Owned scope:** This must include the exact files, services, or knowledge domains the agent can touch. Narrow ranges reduce conflict.
- **Forbidden scope:** Name the overlapping areas another agent will own or areas too risky for the current task.
- **Parallel eligibility:** Only mark “yes” when write scopes do not overlap, dependency results are read-only, and integration costs stay manageable.
- **Integration note:** Clarify how results are merged or how the next sub-task is triggered. This helps the main agent grasp acceptance requirements later.

## Example Decomposition

- Goal: Deliver a production-ready retry fix with documentation and verification.
- Sub-tasks:
  1. **Explore:** Inspect retry logic, gather failing test output, and sketch minimal fix scope. Owned scope: `src/retry/*` plus test logs. Parallel eligible: yes (read-only).
  2. **Implement:** Apply the fix to retry logic and add retry coverage. Owned scope: `src/retry/*` write, `tests/retry/*` adjustments. Depends on explore notes. Parallel eligible: no, waits for explore output.
  3. **Verify:** Run retry regression tests and confirm failure disappears. Owned scope: testing harness, CI summary. Depends on implement. Parallel eligible: no (needs updated code).

This structured decomposition keeps each agent accountable, highlights integration points, and clarifies when the orchestrator should wait or dispatch concurrently.
