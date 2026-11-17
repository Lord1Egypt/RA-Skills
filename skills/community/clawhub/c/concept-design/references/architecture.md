# Engineering architecture

Rule semantics follow Meng and Jackson. Default to an in-process modular monolith with language-native source roots. Confirm and document the scope of exceptions to these boundaries.

## Directories and naming

```text
<source root>/
  entry/<business module>/          # inbound protocols and outbound adapters
  compositions/<business group>/
    SYNCS.md
    <Action>UseCase                 # public entry rule
    <Action>On<Event>               # follow-up event rule
  concepts/<concept>/               # dedicated source package or module per concept
    CONCEPT.md
    api/                            # public commands, queries, and value types
    application/                    # action/query implementations and inner ports
    domain/                         # state, invariants, behavior, repository contracts
    adapters/                       # port implementations, persistence, concept wiring
  bootstrap/                        # final wiring and startup
```

- Keep layer names fixed. Use lowercase singular business directories, match group names to spec directories, and reuse the same business word stem. Join Java package words, as in `operatorsession`. Use singular type subjects and plural list operations and collections, as in `ReadBookingsUseCase` and `bookings`.
- Keep composition groups free of nested domain layers. Rules may share a source module or build unit. Functional implementations preserve roles and visibility.
- Wire Java/Spring components as needed in `<Concept>Configuration` under concept `adapters/`, `<BusinessScope>Configuration` in the composition group, and `<Application>Configuration` under `bootstrap/`. Bind values in `<Capability>Properties` at the consumer boundary. Use native equivalents in other languages.

## Layer responsibilities and dependencies

- **Inbound adapter → public `<Action>UseCase` → concept API.** Entry handles protocol parsing, format validation, trusted context, and response conversion. Fold forwarding-only Facades into the use case entry. Outbound adapters implement composition ports.
- **Independent concepts.** Each owns its state and invariants. Forbid dependencies, calls, and state reads between concepts, and dependencies on entry, composition, or bootstrap. Use type parameters or opaque IDs for external identities.
- **Concept internals.** Keep `api` and `domain` independent of other layers. `application` depends on `api`, `domain`, and inner ports. `adapters` implement ports. Repositories persist aggregates and query ports read projections. Define one port per responsibility.
- **Composition coordinates.** Access concepts through their APIs and depend on required inner ports. Forbid dependencies on entry or bootstrap. Keep business branches, authorization rechecks, transactions, and failure policy in rules. Helpers reuse computations or execution mechanisms without calling rules. Composition may keep execution records. Concepts own business facts.
- **Technology boundaries.** Keep protocol, framework, and persistence types out of business contracts and `api/application/domain`. Wiring constructs and injects components. Business code avoids container lookups. Technical libraries neither depend on nor coordinate business code.

## Synchronization boundaries

The inbound adapter establishes or passes the root action completion and its flow. Give each rule one named implementation. Each public use case implements one entry rule. Match completions in `when`, evaluate optional `where`, and invoke actions in `then`. Same-transaction follow-up rules may use internal methods. Use `<Action>On<Event>` for rules shared across entries, independently scheduled, or independently recovered. Follow-up rules fire on their own matching completions. Apply the contract and [execution and recovery](execution.md) for transactions, causality, atomic claims, and recovery.

## Specification ownership

Keep specifications beside implementations. Before modules exist, use the corresponding `concepts/<concept>/` or `compositions/<business group>/` under `docs/prd/`. Index authoritative specifications in the overall PRD and link acceptance to contracts or scenarios. Obtain authorization before moving confirmed locations.

Declare instances, type bindings, and shared entry contracts once. Repeated includes resolve to the same instance. Map each `SYNCS.md` rule to its use case, internal method, or event handler. Use the same rule identity across specifications, tests, and runtime records. Preserve persisted identities and trigger, transaction, failure, and retry semantics during migration. `// flow:` only groups documentation.

## Review and verification

Run checks on actual sources, build units, and configurations in normal checks or CI. Verify layout, naming, module discovery, rule mappings, and dependency graphs. Check visibility, cycles, type leaks, and adapter wiring. Fail violations with their locations and report missed coverage or unresolved dependencies as gaps. Behavior-test triggers, transactions, failures, retries, and concurrency.
