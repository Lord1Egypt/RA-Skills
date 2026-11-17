# Build

Inputs: confirmed specifications, project conventions, scoped source/manifests/tests.
A review/plan MUST NOT edit files.

1. Identify scoped actions, queries, result cases, invariants, rules, execution constraints, and extra observable behavior.
2. Before editing, compare the source tree, build manifests, and confirmed persistence conventions against the [architecture constraints](../references/architecture.md).
3. Implement or refactor within scope while preserving confirmed behavior and stable identities.
   Update moved specifications, exports, dependencies, and PRD indexes.
4. Use [execution and recovery](../references/execution.md) for rule execution and applicable migration.
5. Run affected concept, composition, protocol, assembly, and architecture checks.
   Verify contract items, OPs, and application scenarios separately.

Resolve known contract/architecture violations within authorized scope.
