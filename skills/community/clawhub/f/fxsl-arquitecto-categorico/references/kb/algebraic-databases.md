# Algebraic Databases

Schultz, P., Spivak, D.I., Vasilakopoulou, C., Wisnesky, R. Extension of the set-valued functor model to incorporate multi-sorted algebraic theories; schemas, instances, change-of-schema functors, and queries packaged in a double categorical structure called a proarrow equipment.

## Core Structures

**Profunctor.** M: C ⇸ D = functor M: C^op × D → Set. Also called correspondences or distributors; viewed as bimodules or generalized relations. Composition: (M ⊗ N)(c,e) = ∫^{d∈D} M(c,d) × N(d,e). Morphism of profunctors φ: M ⇒ N = natural transformation respecting left and right actions. Bicategory of small categories, profunctors, and transformations = Prof.

**Bimodule.** Profunctor structured in the double category Data (schemas, mappings, modules). Encapsulates queries as composable entities.

**Proarrow equipment (framed bicategory).** Double category D with: objects and vertical morphisms forming D_0; horizontal 1-cells forming D_1 with functors L,R: D_1 → D_0; unit functor U: D_0 → D_1; composition ⊗: D_1 ×_{D_0} D_1 → D_1 subject to coherence. Frame functor (L,R): D_1 → D_0 × D_0 is a fibration. Prof is a proarrow equipment.

**Collages.** Equipment D has collages if every proarrow M: A ⇸ B has a universal cocone. In Prof: objects = Ob(C) ⊔ Ob(D); hom-sets defined piecewise by C(c,c'), D(d,d'), M(c,d). Prof has extensive collages.

## Algebraic Theories

**Multi-sorted algebraic theory.** Cartesian strict monoidal category T with set S_T of base sorts; monoid of objects free on S_T. Morphism of theories T → T': product-preserving functor sending base sorts to base sorts.

**Algebra over T.** Product-preserving functor T → Set. Category of algebras = T-Alg.

**Algebraic profunctor.** M: C ⇸ T is algebraic if M(c,-): T → Set preserves finite products for each c in C. Equivalently, M: T → Set^{C^op} factors through T-Alg.

**Left tensor.** For M: C ⇸ D and algebraic N: D ⇸ T, left tensor M ⊗ N: C ⇸ T = Λ_N ∘ M: C^op → T-Alg.

## Presentations and Syntax

**Algebraic signature Σ.** Set S_Σ of base sorts + set Φ_Σ of function symbols f: (s1,...,sn) → s'. Presentation (Σ,E) of theory T: signature Σ + equations E such that T ≅ Cxt_Σ / E.

**Category presentation.** Pair (G,E) where G is a graph (unary signature) and E is a set of unary equations. Category = Fr(G)/E.

## Algebraic Database Schemas

**Schema S over algebraic theory Type.** Pair (S_e, S_o): S_e = entity category; S_o: S_e ⇸ Type = observables profunctor (algebraic).

**Schema mapping F: S → T.** Functor F_e: S_e → T_e + 2-cell F_o: S_o ⇒ T_o ∘ F_e^{op} in Prof. Category of schemas = Schema.

## Instances and Migrations

**Instance on S = (S_e, S_o).** Functor I: S → Set whose restriction to Type is a Type-algebra. S-Inst = category of instances and natural transformations. S-Inst is equivalent to a category of algebras for some algebraic theory; has all small colimits.

**Three migration functors** for schema mapping F: S → T:

| Functor | Definition | Adjunction |
|---------|-----------|-----------|
| Δ_F (pullback) | Δ_F(I) = I ∘ F | right adjoint to Σ_F |
| Σ_F (left pushforward) | Σ_F(I) = ∫^{s ∈ S_e} I(s) · y(Fs) | left adjoint to Δ_F |
| Π_F (right pushforward) | Right Kan extension | right adjoint to Δ_F |

## Double Category Data

**Data.** Double category: objects = schemas; vertical morphisms = schema mappings; horizontal morphisms = bimodules; 2-cells = transformations respecting the type side. Composition M ⊗ N of bimodules M: R ⇸ S and N: S ⇸ T: M ⊗ N = Λ_N ∘ M. Data is an equipment.

## Queries and Uber-Queries

**Query Q on schema S.** FOR-WHERE-RETURN specification → schema R (one entity) + bimodule M: R ⇸ S. Evaluation on instance J: Γ_M(J).

**Query evaluation.** Γ_M(I) = ∫^c M(c,−) × I(c): applies profunctor M (uber-query) to concrete instance I.

**Query composition.** (M;N)(a,c) = ∫^b M(a,b) × N(b,c). Builds complex queries from simple composable blocks.

### UBER-QUERY

**Uber-query.** Bimodule N: L ⇸ S; more general query possibly returning multiple tables or referencing other queries.

## Theoretical Foundations

### KAN-EXTENSION

**Kan extensions.** Lan_F (left, generalizes Σ_F) and Ran_F (right, generalizes Π_F): best universal approximations to extending functors along F.

### KAN-LIFT

**Kan lift.** Inverse extension problem; requires functor to be fully faithful to preserve semantics.

**Yoneda embedding.** y: C → [C^op, Set], y(A) = Hom(−,A). Fully faithful: C embeds in presheaf category. A ≅ B in C iff y(A) ≅ y(B). Fundamentals interface design and query representation as presheaves.

## Implementation

Each finite presentation of categories or instances requires a decision procedure for the word problem, typically resolved by rewriting systems (Knuth-Bendix completion).

**Appendix: componentwise composition.** Composite M ⊗ N expressed via pushout in [R_e^op, Type-Alg]. Exponentiation N ◁ P described by pointwise pullbacks.

## Paper Contents

1. Introduction — 2. Profunctors and Proarrow Equipments — 3. Algebraic Theories — 4. Presentations and Syntax — 5. Algebraic Database Schemas — 6. Algebraic Database Instances — 7. The Fundamental Data Migration Functors — 8. The Double Category Data — 9. Queries and Uber-Queries — 10. Implementation — A. Componentwise Composition and Exponentiation in Data
