# Design

1. Establish the beneficiary, application purpose, scope, current behavior, and required results.
   Inspect existing entries, state ownership, failures, and tests when available.
   Retain required security, timing, and reliability bounds.
2. Propose concepts and scenarios in the [decision record](../decision-records.md).
3. Apply all eight [concept criteria](../model-criteria.md#concepts).
   Write contracts in the [specification notation](../spec-notation.md) with their [execution constraints](../architecture-execution.md#execution-constraints); read the matching scenario in the [examples](../spec-examples.md) when a model is needed.
4. Design rules and check [composition and subsets](../model-criteria.md#composition).
5. When engineering design is in scope, map entries, rule implementations, and concept boundaries using the [engineering architecture](../architecture.md), with dependency checks; for Java/Spring projects, also read the [Java/Spring conventions](../architecture-java.md).

Deliver concept contracts, rules, their diagram, exclusions, and open decisions.
Required responses MUST cover declared success and refusal cases.
Explain the model using the [reading version](../spec-reading.md) by default; expand precision as needed.
