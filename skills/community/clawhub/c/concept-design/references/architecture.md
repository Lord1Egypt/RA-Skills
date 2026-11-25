# Engineering architecture

Concept and synchronization semantics follow Meng and Jackson; the engineering names and layout below are conventions of this skill. Default to an in-process modular monolith with language-native source roots. Confirm and document the scope of exceptions to the responsibility and dependency boundaries below.

## Principles

- **Modules implement independent concepts.** Each business module owns its state and invariants. Forbid dependencies, calls, and state reads between business modules; use type parameters or opaque IDs for external identities.
- **Use cases implement compositions and synchronizations.** Keep business branches, authorization rechecks, transactions, and failure policy in rules; module-local constraints remain in their module.
- **Dependencies point toward business internals.** Source dependencies follow `inbound → usecases → modules/api`; outbound interaction follows `usecases → consumer-owned ports ← outbound/readviews`.
- **Technical mechanisms do not decide business policy.** Keep protocol, framework, and persistence types out of business layers. Only wiring constructs and injects components; business code avoids container lookups.
- **Each definition has one authority.** Declare specifications, instances and type bindings, and rule identities once; engineering renames preserve the model and behavior.

## Design and engineering terms

| Design term | Engineering expression | Responsibility |
| --- | --- | --- |
| Concept | Business module at `modules/<business name>` | Independently own state, actions, and invariants |
| Concept composition | Use case group at `usecases/<business group>` | Organize application-specific coordination across modules |
| Synchronization rule | Named use case, internal method, or event handler | Implement a `when/where/then` causal rule |

Specifications retain concepts, compositions, synchronization rules, and `CONCEPT.md/SYNCS.md`. `modules` denotes business modules, not every technical module discovered by a framework; separate build or deployment units are not required.

## Directories and naming

Use the following six top-level responsibilities as the default layout, creating directories as needed; keep concepts and compositions directly visible.

```text
<source root>/
  modules/<business name>/          # dedicated business source package or module per concept
    CONCEPT.md                     # when colocating specifications
    api/                           # in-process public commands, queries, and value types
    application/                   # action/query implementations and inner ports
    domain/                        # state, invariants, behavior, repository contracts
    persistence/                   # storage implementations and storage codecs
    security/                      # module-specific security implementations, as needed
  usecases/<business group>/
    SYNCS.md                       # when colocating specifications
    <Action>UseCase                # public entry rule
    <Action>On<Event>              # follow-up event rule
    ports/                         # consumer-owned ports, results, and failure types, as needed
  adapters/
    inbound/<business group>/      # HTTP, protocols, events, and business scheduling triggers
    outbound/<capability>/         # external system integrations
    readviews/                     # owner-published and authorized cross-application views, as needed
  infrastructure/                  # application-local general technical mechanisms
  contracts/                       # vocabulary and exchange formats shared across application layers, as needed
  bootstrap/                       # final wiring and startup
```

- Use these engineering names in new projects. In existing projects, record design-to-implementation mappings before authorized responsibility-based moves.
- Use lowercase singular business directories and fixed collection or role names. Reuse business word stems between modules and their concepts, and between use case groups and their compositions; module and use case groups need not share names. Use singular type subjects and plural list operations and collections, as in `ReadBookingsUseCase` and `bookings`.
- Keep use case groups free of nested domain layers; limit `support` to internal collaborators of its group. Name other module-local technical implementations by their actual responsibilities and create them as needed. Rules may share a source module or build unit; functional implementations preserve roles and visibility.
- Directory groups are not build, deployment, or framework modules; explicitly register and check nested boundaries.
- Wire components in the language's native form: module wiring stays at the module root, a use case group binds only its own components and ports, and wiring across roles or adapter branches belongs in `bootstrap`. See [Java/Spring conventions](architecture-java.md) for naming and optional checks.

## Layer responsibilities and dependencies

| Boundary | Allowed dependencies |
| --- | --- |
| `contracts` | Its own types, standard library, and necessary value-type annotations; no other application top-level package, runtime framework, or I/O |
| `infrastructure` | Technical mechanisms and libraries; no business modules, use cases, business vocabulary, adapters, or wiring |
| Module business internals | This module's inner layers and `contracts`; explicitly allowlist exceptions for pure technical value types |
| Module technical implementations such as `persistence/security` | This module's inner layers, `contracts`, and required technical mechanisms and frameworks; no other business module, use case, or top-level adapter |
| `usecases` | Public module `api`, its own ports, `contracts`, and necessary technical mechanisms; no `adapters`, module internals, or wiring |
| `adapters/inbound` | Public use cases and their input/output types, `contracts`, and technical mechanisms; initiate business actions and queries through use cases |
| `adapters/outbound`, `adapters/readviews` | Public consumer-owned ports, required public value types, `contracts`, and technical mechanisms; no business use case entry calls |
| `bootstrap` | Configurations, factories, and implementations needed for wiring; no business decisions or business state |

- **Module internals.** Keep `api` and `domain` independent of other module layers; `application` depends on `api/domain` and inner ports. Repositories persist aggregates and query ports read projections. Define one port per responsibility.
- **Ports.** Consumers own ports and their required result and failure types; assign shared ports an explicit owner in the same layer. Local DTOs and utilities also stay with their actual consumers.
- **Adapters.** `adapters` only groups directories; declare separate boundaries for `inbound/outbound/readviews` and forbid all six source-dependency directions between them.

Place responsibilities by actual behavior, splitting framework integration classes accordingly:

| Responsibility | Owner |
| --- | --- |
| Protocols, format validation, trusted context, and response conversion; business scheduling triggers, business event entry points, and business authentication filters | `adapters/inbound` |
| External protocol implementations | `adapters/outbound` |
| Implementations of consumer-owned read ports; access only owner-published and authorized views, and distinguish no match from a read failure | `adapters/readviews` |
| Cross-module business policy; cross-module business redelivery conditions, backoff, and coordination | `usecases` |
| Module-local business policy, business redelivery, and module-specific protection implementations | Owning module |
| Storage implementations, storage codecs, and pure storage lifecycle maintenance | Module `persistence` |
| Stable identifiers, immutable value types, exchange formats, and their own invariants; no business facts | `contracts` |
| General cryptography, rate limiting, audit writing, and Web mechanisms | `infrastructure` |
| Contract-permitted technical retries, such as connection retries | Owning adapter or technical mechanism |

Business redelivery and technical retries both follow the [execution contract](architecture-execution.md) for idempotency, retry limits, and failure results; technical retry does not independently authorize repeated effects.

## Synchronization boundaries

The inbound adapter establishes or passes the root action completion and its flow. Give each rule one named implementation; each public use case implements one entry rule: match completions in `when`, evaluate optional `where`, and invoke actions in `then`. Same-transaction follow-up rules may use internal methods. Use `<Action>On<Event>` for rules shared across entries, independently scheduled, or independently recovered; they fire on their own matching completions.

Helpers reuse computations or execution mechanisms without calling rules; fold forwarding-only Facades into the use case entry. Composition may keep execution records; concepts own business facts. Apply the contract and [execution and recovery](architecture-execution.md) for transactions, causality, atomic claims, and recovery.

## Specification ownership

Specifications may sit beside implementations as `CONCEPT.md` in a business module and `SYNCS.md` in a use case group; retain existing separate design directories. Before modules exist, use the corresponding `concepts/<concept>/` or `compositions/<business group>/` under `docs/prd/`. For separate layouts, explicitly maintain the following mappings; retain design-defined concept names, instances and type bindings, and rule identities:

```text
<design root>/concepts/<concept>/CONCEPT.md → <source root>/modules/<business name>/
<design root>/compositions/<business group>/SYNCS.md → <source root>/usecases/<business group>/
```

Index authoritative specifications in the overall PRD and link acceptance to contracts or scenarios. Maintain each specification body in one place without duplicating it between colocated and separate layouts. Obtain authorization before moving confirmed locations.

Declare instances, type bindings, and shared entry contracts once. Repeated includes resolve to the same instance. Map each `SYNCS.md` rule to its use case, internal method, or event handler. Use the same rule identity across specifications, tests, and runtime records. `// flow:` only groups documentation.

## Review and verification

- **Check the actual project.** Run checks on actual sources, build units, and configurations in normal checks or CI. Verify layout, naming, module discovery, design-to-implementation mappings, and dependency graphs. Check visibility, cycles, type leaks, and adapter wiring. Checkers explicitly distinguish design and source paths.
- **Violations must fail.** Fail violations with their locations and report missed coverage or unresolved dependencies as gaps. Verify nested boundaries and actual class matching; use violating fixtures to prove that all six adapter dependency directions and other forbidden dependencies fail. Acyclicity or empty matches alone are not evidence of independence.
- **Verify behavior separately.** Behavior-test triggers, transactions, failures, retries, and concurrency.
- **Verify cross-application formats independently.** Check fields, types, required/nullable values, and serialized representations against fixed-version contract fixtures; tests do not read another application's source.

Run engineering moves under [migration and compatibility](architecture-execution.md#compatibility).
