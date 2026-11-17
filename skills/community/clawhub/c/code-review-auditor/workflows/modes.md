# Mode Workflows

## complete

Use for broad review requests. Inspect architecture, dependencies, tests, configuration, and representative flows. Produce all category reports, even when some contain no findings.

## diff / changed

Use repository diff commands to identify changed files. Review changed code plus nearby callers, tests, schemas, routes, message contracts, and configuration needed to understand behavior. Avoid turning a diff review into a full audit unless the changed code exposes a larger root cause.

## security

Prioritize exploitability and data exposure. Check trust boundaries, input sources, authorization, authentication, secrets, logs, crypto, dependencies, and deployment-relevant config. Use high confidence language only when exploit path is clear.

## architecture

Map modules, dependency direction, framework boundaries, persistence boundaries, messaging boundaries, and domain/application/infrastructure responsibilities. Prefer diagrams in prose or Mermaid only when it clarifies the output.

## smells

Focus on local maintainability and defect risk. Avoid reporting minor style nits unless they materially affect comprehension or correctness.

## patterns

Look for repeated branching, duplicated construction, adapter leakage, lifecycle state rules, duplicated predicates, and behavior families. Recommend patterns only after applying `rules/overengineering.md`.

## performance

Look for hot paths from routes, consumers, jobs, queries, loops, IO, and rendering. Tie findings to input size, data volume, concurrency, latency, or throughput assumptions.

## tests

Assess whether important behavior can be changed safely. Favor tests around business behavior, security boundaries, data access, message contracts, and integration seams.

## hotspots

Rank files/modules using available evidence:

- changed lines and churn
- complexity and nesting
- dependency fan-in/fan-out
- number and severity of findings
- lack of tests
- production criticality
- security or data sensitivity

## explain

Explain the findings and tradeoffs in plain language. Do not implement changes.

## fix

Create `refactoring-plan.md` with a narrow implementation plan, tests, rollback notes, and files likely to change. Implement only after explicit approval or when the user has already asked for implementation.

## refactor

Create `refactoring-plan.md` focused on behavior-preserving changes. Include invariants, test strategy, staged commits, and migration risk. Implement only after explicit approval or when already requested.

## challenge

Act as a skeptical reviewer. Identify hidden risks, missed cases, weak assumptions, overengineering, operational burden, and simpler alternatives.
