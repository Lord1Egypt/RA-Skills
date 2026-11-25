# Java/Spring conventions

How Java/Spring projects apply the [engineering architecture](architecture.md); adopt as needed. Responsibility and dependency boundaries come from the engineering architecture; use native equivalents in other languages.

## Naming and wiring

- Join Java package words.
- Wire components explicitly as needed: put `<Business>Configuration` at the module root, limit `<BusinessScope>Configuration` in a use case group to its own components and ports, and put final wiring under `bootstrap/`. Wiring across roles or adapter branches belongs in `bootstrap`.
- Bind values in `<Capability>Properties` at the consumer boundary.

## Optional: centralized scheduled and event entry points

When a project centralizes scheduled and module-event entry points in `adapters/inbound/jobs`, declare the applicable sources and exceptions in project conventions and enable these architecture checks:

- `@Scheduled` and `@ApplicationModuleListener` appear only in that package and its descendants.
- `jobs` does not depend on other `inbound` subpackages such as `web`.

Check actual entry methods, composed annotations, and repeatable annotations; use passing and violating fixtures to verify matching and both constraints. Business jobs execute through use cases. Pure storage lifecycle maintenance may remain in storage under an explicit class- or method-level exception. If triggered centrally from `jobs`, use a declared purely technical maintenance port, record it in the project dependency table, and wire it through `bootstrap`; do not access storage internals or introduce a forwarding-only business use case. Without project opt-in, neither a `jobs` directory nor annotation-location checks are required.

## Listener migration

Apply [migration and compatibility](architecture-execution.md#compatibility) when moving module-event entry points:

- Check explicit or default listener IDs and pending publication records; default IDs may contain the declaring method's qualified name. Model rule identity is not framework listener identity.
- Preserve stable IDs or migrate stored records according to existing data. Verify that old records recover after restart without missed execution or extra duplicates.
- Annotation-location conventions do not require replacing listener annotations or changing transaction and asynchronous semantics; verify actual effects and applicable recovery behavior.
