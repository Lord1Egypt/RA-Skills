# Architecture Review

## architecture_inventory
Planner, router, specialist executor, memory store, and approval gate.

## failure_mode_map
- Router sends vague tasks to the wrong specialist.
- Shared memory leaks stale context into new runs.
- Approval happens after expensive tool calls.

## architecture_test_plan
- Test ambiguous routing.
- Test stale memory.
- Test tool outage recovery.
- Test human approval before side effects.

## optimization_roadmap
1. Tighten router intent categories.
2. Separate short-term from persistent memory.
3. Move approval gate earlier for side-effectful actions.

## measurement_plan
Track routing accuracy, retry rate, human intervention rate, and cost per successful run.

## architecture_recommendation
iterate
