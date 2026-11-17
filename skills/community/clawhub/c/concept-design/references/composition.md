# Concept Composition

**Concepts define local behavior; synchronizations define coordination.** Composition may restrict behavior but must preserve participating contracts; see the [specification notation](spec-notation.md).

| Problem in a scenario | Adjustment |
| --- | --- |
| Required coordination is absent | Tighten synchronization. |
| Automation removes needed manual control | Loosen synchronization or allow configuration. |
| Composition distorts a concept's purpose | Recheck boundaries and contracts. |

Judge against requirements and counterexamples, not rule counts or flow length. Coordination actions such as access and notify also need contracts. Logs and queues qualify only with independent purposes and complete behavior.

## Diagram

Use one node per rule: all `when` inputs are conjunctive, `where` reads are separate, and all `then` targets remain visible without implied order. Simplified arrows must retain rule names and conjunctions; see the [diagram contract](diagram-contract.md). Loops must terminate or continue under control; engineering cutoffs must be observable.

## Product subsets

An intrinsic dependency embeds another concept's definition; replace it with a type parameter or external coordination. An extrinsic dependency comes from product requirements: `A → B` means retaining A requires B in this product. Code coupling or type binding alone does not establish that requirement.

A product subset S must be dependency-closed: **if A ∈ S and A → B, then B ∈ S**. Include or exclude cycle members together. Closure is necessary, not sufficient: the subset also needs a purpose, usable entries, valid remaining rules, and resources. Express product dependencies separately from synchronization diagrams.
