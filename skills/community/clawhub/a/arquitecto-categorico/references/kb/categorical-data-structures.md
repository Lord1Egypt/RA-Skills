# Categorical Data Structures

Patterson, E., Lynch, O., & Fairbanks, J. (2022). Categorical Data Structures for Technical Computing. Applied Category Theory to generate data structures automatically from formal specifications. Addresses fundamental disconnect between rigorous mathematical models and ad-hoc software implementations.

Enabling technologies: GATs (Generalized Algebraic Theories), C-Sets (sets indexed by a category), ACSets (Attributed C-Sets), Catlab.jl.

## Core Definitions

**C-Set.** Given schema (small category) C, a database is a functor X: C → Set.
- For each object c in C: X(c) = set of instances (rows in a table).
- For each morphism f: c → d: X(f): X(c) → X(d) = function (foreign key column).

**ACSet (Attributed C-Set).** Extension of C-Set for concrete data (numbers, strings). Functor X: S → Set where attribute objects map to fixed data types (e.g., ℝ, String). Handled formally via comma categories or indexing over a base type category.

**GAT (Generalized Algebraic Theory).** Dependent type system for defining categories, functors, and more complex structures.

**Schema presentation.** Schema C is finitely presented by generators (objects and morphisms) and equations (axioms). Separation of Syntax/Semantics: GAT defines syntax (C); models of the theory (functors to Set) are the semantics (data).

**Migration operators** induced by a functor F: C → D between schemas:

| Operator | Definition | Analogy |
|----------|-----------|---------|
| Δ_F (pullback) | Precomposition with F; brings data from D to C | —  |
| Σ_F (left pushforward) | Adds/unions structures (C to D) | UNION or generalization |
| Π_F (right pushforward) | Products (C to D) | JOIN or MATCH |

**Gluing.** Combination of partial models via colimits (pushouts) in the category of C-Sets, guaranteeing correct fusion of references.

## DIK Hierarchy — Categorical Data Structures

**Data = database instance.**
- Definition: instance of a database conforming to a schema.
- C-Set model: functor X: C → Set, X(c) = rows, X(f) = foreign key.
- ACSet extension: attribute objects map to fixed data types.
- In this paradigm, data are not passive records but functors.

**Information = formal structure specification.**
- Definition: formal specification of data structure and algebraic constraints.
- GAT model: finitely presented schema C (generators + equations).
- Enables multiple implementations (in-memory, SQL, graphs) by changing target category or functor implementation.
- Schema is a first-class mathematical object.

**Knowledge = functorial transformations.**
- Definition: functorial operations for translating data between schemas and combining datasets.
- Given F: C → D, three adjoint operations on C-Sets: Δ_F, Σ_F, Π_F.
- Gluing via pushouts for combining partial models.

**Modeling = explicit executable workflow in Catlab.jl.**
1. Define domain: write GAT or category presentation (objects and morphisms).
2. Generate code: Julia macros convert specification into optimized data types (structs) and indexed access methods.
3. Generic manipulation: universal categorical API (limit, colimit, functor) decouples algorithm from data structure.

## Catlab.jl Schema Example

```julia
@present TheoryGraph(FreeSchema) begin
  V::Ob
  E::Ob
  src::Hom(E,V)
  tgt::Hom(E,V)
end
```

## Properties and Consequences

- Interoperability: C-Sets give different domains (graphs, Petri nets, meshes) a common language.
- Correctness: data migrations mathematically guarantee structure preservation, eliminating entire classes of ETL errors.
- Efficiency: code generation allows high-level abstractions to compete in performance with manual implementations.
- Foundation for systems where Action (Fukada) and Structure (Patterson) coexist rigorously.
