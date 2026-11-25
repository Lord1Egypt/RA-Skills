# Model criteria

Judge whether a concept qualifies, a composition fits, and a subset is usable. Judge against requirements and counterexamples, not form, rule counts, or flow length. See the [specification notation](spec-notation.md).

## Concepts

A concept is **user-facing**, **semantic**, and **independently understandable**, with **behavior** serving a clear **purpose**. API programmers are users too; semantics includes abstract **static structures** and **dynamic behavior**.

Being **purposive** means serving a purpose that users understand and that brings value by itself. Being **end-to-end** means providing the functionality needed to fulfill that purpose: authentication cannot stop at registration. If the **operational principle** only describes how an action updates state, something is missing.

**Familiarity** lets users draw on prior experience, while allowing new concepts. **Reusability** often follows from **independence**, **purpose**, and complete functionality; prior instances of reuse are not required. **Most designs adapt, extend, and combine existing design ideas.**

These eight [criteria from Jackson](https://essenceofsoftware.com/tutorials/concept-basics/criteria/) identify concepts. Classes, interface widgets, features, and individual user stories do not qualify merely by their form.

## Composition

**Concepts define local behavior; synchronizations define coordination.** Composition may restrict behavior but must preserve participating contracts.

| Problem in a scenario | Adjustment |
| --- | --- |
| Required coordination is absent | Tighten synchronization. |
| Automation removes needed manual control | Loosen synchronization or allow configuration. |
| Composition distorts a concept's purpose | Recheck boundaries and contracts. |

Coordination actions such as access and notify also need contracts. Logs and queues qualify only with independent purposes and complete behavior.

## Diagram

Use one node per rule: all `when` inputs are conjunctive, `where` reads are separate, and all `then` targets remain visible without implied order. Simplified arrows must retain rule names and conjunctions; see the [diagram contract](tool-diagram.md). Loops must terminate or continue under control; engineering cutoffs must be observable.

## Product subsets

An intrinsic dependency embeds another concept's definition; replace it with a type parameter or external coordination. An extrinsic dependency comes from product requirements: `A → B` means retaining A requires B in this product. Code coupling or type binding alone does not establish that requirement.

A product subset S must be dependency-closed: **if A ∈ S and A → B, then B ∈ S**. Include or exclude cycle members together. Closure is necessary, not sufficient: the subset also needs a purpose, usable entries, valid remaining rules, and resources. Express product dependencies separately from synchronization diagrams.
