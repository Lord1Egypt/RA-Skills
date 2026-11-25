# Drift and severity

Compare confirmed contracts with implementation without repairs. Establish versions and coverage, then read specifications, PRD/staged indexes, rules, code, schemas/migrations, and tests. Verify search results against definitions; assess parent-specification coverage by content. Missing or unscanned code stays unverified. See [specification notation](../../spec-notation.md) for syntax and behavior.

## Severity

Critical requires authorization bypass, data destruction, or core unavailability evidence. High means clear violation; Medium impactful omission; Low local maintenance. Explain impact-based adjustments; Low counts alone do not raise severity.

## Classification

| Scope | Evidence | Default |
| --- | --- | --- |
| Concept | Undeclared public action, changed signature/result, observable new state, undocumented contract parameter | Medium |
| Concept | Core definition semantically depends on another concept; internal concept lacks specification/index explanation | Medium |
| Concept | Declared action absent from all relevant implementations | High |
| Concept | Private access, direct concept calls, shared mutable state, excluded action reachable | High |
| Synchronization | Undocumented rule; changed trigger | Medium |
| Synchronization | Scenario shows missing coordination, lost control, distorted purpose, or independent business lifecycle in coordination state | Medium |
| Synchronization | Declared rule removed | High |
| Synchronization | Changed binding/effect, undeclared participant, bad matching/correlation/cardinality, missing required response, illegal joint effects, forbidden replay, misplaced invariant | High |
| Synchronization | Required progress or authorization consistency fails | Impact-based |
| Synchronization | Every supported entry proven unable to trigger a rule | Low |
| Pipeline | PIPELINE missing stage/source or changed data contract | Medium |
| Pipeline | PIPELINE contradictory invariant/private access | High |
| Diagram | Existing map contradicts rules | Medium |
| Verification | OP lacks representative test | Verification gap; risk-based |
| Verification | Unresolved action/query/signature/result/type binding | Verification gap; grade by impact once a violation is established |
| Maintenance | Recorded gap resolved by implementation | Low |

Check each area:

- **Rules**: cases, query cardinality, arguments, correlation, failure, replay, and loops.
- **Pipelines**: order, contracts, triggers, quality, and public interfaces.
- **Entries**: resolve external-entry signatures; Requesting needs no synthetic CONCEPT. A sync diagram may live in the overall PRD alone.
- **Engineering**: check [engineering architecture](../../architecture.md#review-and-verification) separately, including when behavior specifications are missing.

## Judgment and report

- Undeclared behavior against a partial model is a coverage gap unless an applicable contract or explicit exclusion proves drift.
- Private helpers/caches, naming maps, behavior-preserving Result/async wrappers, and legacy headings alone are not drift.
- Recorded exceptions retain their scope/consequences; documenting calls does not restore independence.
- Medium+ findings MUST cite current locations; merge shared root causes across paths.

Report scope/versions, measured counts, passed/found/unverified per category, contract/code locations, impact, and repair steps.
