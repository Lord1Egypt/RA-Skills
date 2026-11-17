# Execution, recovery, and migration

Define business behavior in the [specification notation](spec-notation.md). This document adds engineering guarantees: implementations must preserve contracts under the declared concurrency, failure, and recovery conditions.

## Execution constraints

Record concept-local requirements in `CONCEPT.md` and cross-concept requirements in `SYNCS.md`; an annotation is sufficient. Link each requirement to an action or rule and state **permitted behavior, required outcomes, assumptions, and acceptance checks**. Cover applicable completion, order, correlation, repetition, failure, timing, and recovery policies. Mark unknowns `open` and irrelevant items `not applicable`.

## Execution checks

- **Define completion.** Invocations request execution; completions record declared results; occurrence identity connects them. Equal arguments do not identify one execution. Define asynchronous completion explicitly; acceptance or enqueueing does not complete later work.
- **Preserve causality.** A flow contains a root occurrence and its descendants. `then` calls and completions retain it; `when` matches only its records. Correlate repeated attempts by occurrence or cause and specify all matches or one attempt. Read persistent facts through `where`; connect delayed callbacks through entry/correlation protocols. `// flow:` is only a label.
- **Declare outcome policies.** Match errors separately from `valid: false`; map rule-handled exceptions to declared cases. Zero bindings emit no calls; multiple bindings emit calls per row. Specify required zero-match responses, candidate selection, failure handling, and loop controls. Later failures preserve existing completions.
- **Keep checks consistent with effects.** Validate input and identity across trust boundaries; format validation does not replace authorization. Authorize the actual resource and operation before protected effects, keeping authorization valid through those effects; check invariants atomically within actions.
- **Deduplicate firings.** Derive identity from occurrence tuples and binding rows; claim atomically before calling. Preserve legitimate repeats and prevent forbidden duplicates. Later-valid queries need an explicit reevaluation trigger and a policy for new bindings.

Implement named rules as functions or objects in composition. Ordinary calls, listeners, and Promise chains follow the same principles. Memory may suffice without restart recovery; otherwise apply the protocol below.

## Atomicity and recovery

A database transaction covers participating stores, not external effects. Cross-concept transactions require both compatible contracts and participating stores.

When restart recovery is required, close each crash window:

| Crash window | Required guarantee |
| --- | --- |
| State committed, completion not recorded | Commit state and completion/outbox atomically, or reconcile explicitly so required work is not silently lost. |
| Firing claimed, calls not dispatched | Atomically save the claim and pending calls, retaining completion identities, flow, rule identity/version, bindings, and causes. |
| Target committed, acknowledgement absent | Use stable invocation identity and receiver deduplication, or declared reconciliation. A processed marker alone does not guarantee exactly-once effects. |
| External effect performed, later work fails | Apply equivalent idempotency checks to external effects and retain completed actions. Compensation need not restore the original state. |

Bound retries or define controlled continuation, and expose exhaustion. The [login example](spec-examples.md#external-identity-login) shows partial completion: an error response does not undo existing identity or profile updates.

## Compatibility

Before changing state, identities, interfaces, or rules, inspect stored data, deployed callers, pending calls, and historical completions. Determine required migration, backfill, old/new compatibility, and rollback or roll-forward. Version rules or drain affected work if replay would reinterpret old records. Renaming code does not change stored identities; verify whether code-only moves need migration.

## Checks

Verify applicable cases: success/refusal, zero/many bindings, equal-valued repeats, cross-flow records, concurrent reevaluation, state changes between query and write, the crash windows above, redelivery, in-flight migration, and retry exhaustion. Link evidence to actual effects, occurrences, causes, and contracts; leave unexecuted checks unverified.
