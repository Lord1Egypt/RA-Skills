# Review

MUST remain read-only.
Without code, review design only; without specifications, limit conclusions to evidenced code properties.
Record scope, versions, contract confirmation/coverage, and unknowns before judging differences.

1. Apply [qualification criteria](../references/concept-criteria.md) to the actual user, including API programmers.
2. With code, check [engineering architecture](../references/architecture.md#review-and-verification). With applicable behavior contracts, also apply [drift checks and severity](../references/drift-checks.md).
3. Trace required success and refusal through rules and actual composition/adapters.
   Compare matching, binding sources/cardinality, occurrence/object/request isolation, and outcomes against the [execution constraints and shared checks](../references/execution.md#execution-constraints).
4. Check joint effects for hidden ordering, misplaced invariant checks, stale authorization, and forbidden replay effects.
   Check the [recovery protocol](../references/execution.md#atomicity-and-recovery) against declared recovery requirements.
5. Check required progress, loops, missing coordination, lost user control, and distorted concept purpose against concrete scenarios.
   Coordination state with independent business purpose/lifecycle may require a concept.
6. For each requested subset, check requirement-backed dependencies, entries, rules, resources, and build support.
   Reconcile references and diagrams; merge common root causes.

Under/over-sync and failed purpose fulfillment need counterexamples.
A rule is dead only after every supported entry is inspected.
An acyclic occurrence graph does not prove termination.
A type cycle, missing depth cap, long flow, dispersed rules, background work without HTTP response, or durable log alone is not a defect.
Results may respond, retry, compensate, or be intentionally ignored under their contract; no separate error rule per output is required.

Report purpose fulfillment, independence, composition, engineering architecture, behavioral drift, and requested subsets separately.
Each finding states scenario, current evidence, failed contract/assumption, impact, and repair.
