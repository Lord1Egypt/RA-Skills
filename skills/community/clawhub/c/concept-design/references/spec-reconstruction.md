# Reconstruct specifications

Reconstruct an evidenced candidate baseline from actual code, then establish which consumers may rely on it. Observed behavior does not automatically become a requirement: distinguish **observations, inferred purpose, known defects, desired repairs, and confirmed requirements**, with evidence and confirmation status for each.

## Concept

Inspect exports, callers, persistence, result cases, invariants, and tests. Record types, cardinalities, initial state, action results, and queries using the [specification notation](spec-notation.md). Omit private helpers and caches without observable effects. List required synchronizations separately; record coupling as a defect, not a permitted concept dependency.

## Synchronization

Trace application purposes and scenarios through handlers, registrations, mediators, and adapters to public actions; map implementations using [engineering architecture](architecture.md). Transcribing direct calls or private SQL does not make valid rules. Put pure data transformation in [PIPELINE](pipeline-spec.md).

Check entry completions, result cases, bindings, calls, and request/object/occurrence correlation. All groups reference one application-level instance, type, and entry declaration; repeated includes create no new instances.

Complete reconstruction covers:

- All includes, signatures, and call arguments; zero/many query behavior and request isolation.
- Response, retry, compensation, or ignore policies for every reachable result; unsupported policies remain open.
- Partial completion, replay, and loops. Loops terminate or continue under explicit control; depth caps are optional.
- Evidenced [execution constraints](execution.md#execution-constraints) and diagrams preserving conjunctions, multiple targets, and query reads.

Report rule count, scenario coverage, boundary findings, and unknowns, identifying candidate claims that still need confirmation.
