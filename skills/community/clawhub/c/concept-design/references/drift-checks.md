# Drift and severity

Compare confirmed contracts with implementation without repairs. Establish versions and coverage, then read specifications, PRD/staged indexes, rules, code, schemas/migrations, and tests. Verify search results against definitions; assess parent-specification coverage by content. Missing or unscanned code stays unverified. See [specification notation](spec-notation.md) for syntax and behavior.

## Classification

| Evidence | Default |
| --- | --- |
| Undeclared public action, changed signature/result, observable new state, undocumented contract parameter | Medium |
| Declared action absent from all relevant implementations | High |
| Core definition semantically depends on another concept | Medium |
| Private access, direct concept calls, shared mutable state, excluded action reachable | High |
| OP lacks representative test | Verification gap; risk-based |
| Recorded gap resolved by implementation | Low |
| Undocumented rule / declared rule removed | Medium / High |
| Changed trigger | Medium |
| Changed binding/effect, undeclared participant, bad matching/correlation/cardinality, missing required response, illegal joint effects, forbidden replay, misplaced invariant | High |
| Scenario shows missing coordination, lost control, distorted purpose, or independent business lifecycle in coordination state | Medium |
| Required progress or authorization consistency fails | Impact-based |
| Every supported entry proven unable to trigger a rule | Low |
| PIPELINE missing stage/source or changed data contract | Medium |
| PIPELINE contradictory invariant/private access | High |
| Existing map contradicts rules | Medium |
| Unresolved action/query/signature/result/type binding | Verification gap; grade by impact once a violation is established |
| Internal concept lacks specification/index explanation | Medium |

Check pipeline order, contracts, triggers, quality, and public interfaces.
Check rule cases, query cardinality, arguments, correlation, failure, replay, and loops.
Resolve external-entry signatures; Requesting needs no synthetic CONCEPT.
A sync diagram may live in the overall PRD alone.

Check [engineering architecture](architecture.md#review-and-verification) separately, including when behavior specifications are missing.

## Judgment and report

Undeclared behavior against a partial model is a coverage gap unless an applicable contract or explicit exclusion proves drift.
Private helpers/caches, naming maps, behavior-preserving Result/async wrappers, and legacy headings alone are not drift.
Recorded exceptions retain their scope/consequences; documenting calls does not restore independence.

Critical requires authorization bypass, data destruction, or core unavailability evidence.
High means clear violation; Medium impactful omission; Low local maintenance.
Explain impact-based adjustments; Low counts alone do not raise severity.
Medium+ findings MUST cite current locations.
Merge shared root causes across paths.
Report scope/versions, measured counts, passed/found/unverified per category, contract/code locations, impact, and repair steps.
