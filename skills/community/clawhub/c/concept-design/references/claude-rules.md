# Align CLAUDE.md

Compare confirmed contracts, actual code, and [engineering architecture](architecture.md); report conflicts before updating relevant rules. Do not treat existing code as the contract or change contracts to conceal defects.
Replace repetition with the short principles below; preserve unrelated rules and open decisions. Link each rule to its project authority and actual check without copying specification bodies.

```markdown
1. Fix directories to entry/<module>, compositions/<group>, concepts/<concept>, bootstrap. Use lowercase singular business directories, match groups to specifications, and assign concept responsibilities to api/application/domain/adapters.
2. Inbound adapters establish or pass the declared root action completion and its flow, then call the public <Action>UseCase directly. The use case executes one entry synchronization rule through concept APIs according to when/where/then. Fold forwarding-only Facades into the use case. Independent rules connect through action completions. Helpers supply computations or execution mechanisms only.
3. Concepts own their state and invariants; forbid dependencies, calls, and state reads between concepts. Business access uses api only; assembly uses dedicated entries. application depends on api/domain and inner ports; adapters implement ports. api/domain do not depend on other concept layers; keep these business layers framework-free.
4. Implement CONCEPT.md/SYNCS.md; confirm contracts before behavior changes. Give each synchronization rule one named implementation. Follow-up rules fire on their own matching completions. Pluralize lists and collections by meaning. Preserve rule-to-implementation mappings, persisted identities, and existing failure and retry semantics.
5. Architecture checks cover directories, naming, dependencies, visibility, and rule mappings; behavior tests cover contracts and execution boundaries. Fix code on failure; never report unverified work as passed.
```

Adapt names and check entry points to the project language and confirmed exceptions. Verify alignment with all three sources; report unresolved conflicts and unexecuted checks.
