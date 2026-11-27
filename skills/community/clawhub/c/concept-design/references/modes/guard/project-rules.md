# Align project rules

Compare confirmed contracts, actual code, and [engineering architecture](../../architecture.md) to align the project's `CLAUDE.md` or equivalent rule file. Report conflicts before updating relevant rules. Do not treat existing code as the contract or change contracts to conceal defects.

Replace repetition with the short principles below; preserve unrelated rules and open decisions. Link each rule to its project authority and actual check without copying specification or engineering-architecture bodies.

```markdown
1. Organize engineering code by six top-level responsibilities: modules, usecases, adapters (inbound/outbound/readviews), infrastructure, contracts, and bootstrap; create directories as needed. Retain concept and synchronization terms in design and explicitly map them to module and use case implementations.
2. Business modules implement only this product's independent business concepts, reusing mature capabilities through ports and adapters rather than new business modules; each module owns its state and invariants; forbid dependencies, calls, and state reads between business modules. External access uses api only; keep protocol, framework, and persistence types out of api/application/domain.
3. Use cases implement synchronization rules. inbound establishes or passes the root action completion and its flow, then calls the public <Action>UseCase directly. Give each rule one named implementation that executes through module APIs according to when/where/then; follow-up rules fire on their own matching completions.
4. Dependencies point toward business internals. Use cases do not depend on adapters; consumers own ports and their result and failure types; adapter branches do not depend on one another. contracts contains only shared vocabulary, exchange formats, and their own invariants, with no dependencies on other application top-level packages; infrastructure does not depend on business modules, usecases, contracts, adapters, or bootstrap; bootstrap only wires.
5. Implement CONCEPT.md/SYNCS.md; confirm contracts before behavior changes. Preserve rule-to-implementation mappings, persisted identities, and existing failure and retry semantics. Check listener IDs and in-flight recovery when applicable; distinguish business redelivery from contract-permitted technical retries.
6. Architecture checks cover actual sources and use violating fixtures to prove constraints. Behavior tests cover contracts and execution boundaries. Fix code on failure and never report unverified work as passed.
```

Use the project engineering dependency table as the authority for dependencies and read/write scope; report conflicts with generated rules first. Adapt names and check entry points to the project language and confirmed exceptions. Include the optional jobs convention only after project opt-in, preserving specific exceptions. List naming, migration, or cross-application contract details the project needs as its own rules. Verify alignment with all three sources; report unresolved conflicts and unexecuted checks.
