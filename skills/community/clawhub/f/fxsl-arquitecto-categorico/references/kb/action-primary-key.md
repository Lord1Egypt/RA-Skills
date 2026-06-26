# Action as Primary Key

Fukada, S. (2024). Action is the primary key: a categorical framework for episode description and logical reasoning.

Central thesis: the action is not an attribute of a state or transition — it is the primary key that indexes and structures episodic memory.

## Core Definitions

**World as category C.** Rich structure resides in morphisms (actions); objects (states) are secondary or inferred from the action network.

**Database functor.** Schema S = finitely presented category. Instance: functor I: S → Set. For each object X in S, I(X) = set of data instances.

**Grothendieck construction.** Transition Data → Info modeled by the category of elements ∫I (Grothendieck construction), where individual data items are "glued" following the schema structure. Formula: Info ≅ ∫I →π S.

**Knowledge via internal logic.** Modeled by the internal logic of the category (typically a Topos or regular category). Inference = composition of morphisms: if f: A → B and g: B → C, then g ∘ f: A → C is derived.

**Constraints.** Expressed as limits (pullbacks, equalizers) that must commute; business rules as commutative diagrams for every valid instance.

## DIK Hierarchy — Categorical Reinterpretation

| Level | Definition | Categorical model |
|-------|-----------|-------------------|
| Data | Raw observations and discrete events; set of atomic recorded facts | Discrete category D or terminal objects in an instance category |
| Information | Data + relations (structure); the "how" data relates | Schema S + Grothendieck construction: Info ≅ ∫I →π S |
| Knowledge | Information + rules/logic (semantics); reasoning, inference, validation | Internal logic of category (Topos / regular category) + limit constraints |

## Action as Primary Key — Episode Modeling

**Category of actions A.** Objects = world states or contexts; morphisms = actions that transform one context into another.

**Indexing functor.** Action as indexing entity: indexing functor Idx: E → A, where E = category of episodes. Each episode maps to a canonical action.

**Episode compositionality.** If episode E1 ends in a state that begins E2, they compose: E1 ; E2. Enables construction of complex episodes (stories, processes) from atomic actions, preserving logical structure.

## Conclusions

- Rigor: eliminates ambiguity in what constitutes an episode.
- Interoperability: modeling Data, Info, and Knowledge as categorical structures (functors, schemas, logic) facilitates integration with other knowledge systems.
- Reasoning: primary key structure on the action enables efficient queries and robust logical deductions about agent behavior.
- Formal basis for episodic memory systems in advanced cognitive architectures.
