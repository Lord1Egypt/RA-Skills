# Functorial Data Model (FDM)

## Source

Authors: Brendan Fong, David I. Spivak — *Seven Sketches in Compositionality*, Ch. 3.
Src: `sources/cat/7sk_bbdd.md`

## What Is a Database

A database = system of interlocking tables. Data integration accounts for 40% of IT budgets (2008 study). Category theory provides mathematical approach for translating between different organizational forms (data migration).

**Business rules** expressed as path equalities:
- Department.Secr.WorksIn = Department (secretary works in their department)
- Employee.Mngr.WorksIn = Employee.WorksIn (manager works in employee's department)

Schema diagram: nodes = tables (ID columns); arrows = non-ID columns (pointing direction of reference). Internal references = foreign keys (renameable consistently); external references = strings (not renameable).

## Category

**Def 3.6 (Category C)** — Specify: (1) collection Ob(C) of objects; (2) for every c,d: set C(c,d) of morphisms; (3) for every c: identity morphism id_c ∈ C(c,c); (4) for f: c→d and g: d→e: composite f ; g ∈ C(c,e). Conditions: (a) Unitality: id_c ; f = f and f ; id_d = f. (b) Associativity: (f ; g) ; h = f ; (g ; h).

**Def 3.7 (Free category)** — For graph G=(V,A,s,t): Free(G) has objects = V and morphisms = paths c→d. Identity = trivial path; composition = path concatenation.

## Functors, Natural Transformations, Databases

**Def 3.35 (Functor F: C → D)** — (i) for every c ∈ Ob(C): F(c) ∈ Ob(D); (ii) for every f: c₁→c₂: F(f): F(c₁)→F(c₂). Properties: (a) F(id_c) = id_{F(c)}; (b) F(f ; g) = F(f) ; F(g).

**Schema** = finitely presented category C (objects = entities; morphisms = relations/attributes; equations = path constraints).

**Def 3.44 (C-instance)** — Functor I: C → **Set**. I(A) = set of records; I(f): I(A) → I(B) implements FK or functional attribute.

**Def 3.49 (Natural transformation α: F ⇒ G)** — (F,G: C → D). For each c ∈ C: α_c: F(c) → G(c) in D. Naturality: F(f) ; α_d = α_c ; G(f) for every f: c→d. α is natural isomorphism if each α_c is isomorphism.

**Def 3.54 (Functor category D^C)** — Objects = functors F: C → D; morphisms = natural transformations α: F ⇒ G.

### FDM-FUNCTOR-CATEGORY

**Def 3.60 (Instance homomorphism)** — Natural transformation α: I ⇒ J between C-instances. C-Inst := **Set**^C.

## Adjunctions and Data Migration

**Def 3.68 (Pullback Δ_F)** — Given F: C → D and I: D → **Set**: Δ_F(I) = F ; I: C → **Set**. For α: I ⇒ J: α_F: F ; I ⇒ F ; J. Functor Δ_F: D-Inst → C-Inst.

**Def 3.70 (Adjunction)** — L: C → D left adjoint to R: D → C: for any c ∈ C and d ∈ D, C(c, R(d)) ≅ D(L(c), d) naturally in c and d.

**Adjunction chain**: Σ_F ⊣ Δ_F ⊣ Π_F.

## Migration Operators

### MIGRATION-DELTA

**Δ_F (Pullback)** — Δ_F(J) = J ∘ F. Reindexes data from target D to source C. SQL analog: column renaming, SELECT with alias. Guarantees: no information loss.

Procedure: (1) identify F: Source_Schema → Target_Schema; (2) for each A in Source, Δ_F(J)(A) := J(F(A)); (3) for each f: A→B, Δ_F(J)(f) := J(F(f)); (4) composition preserved by functoriality.

**Σ_F (Left Pushforward)** — Left adjoint of Δ_F; migrates via colimits. SQL analog: UNION, INSERT INTO SELECT, aggregations. Σ_F(I)(B) := colim_{A∈F⁻¹(B)} I(A). May lose information via co-identifications. Always document information lost.

**Π_F (Right Pushforward)** — Right adjoint of Δ_F; migrates via limits. SQL analog: JOIN, WHERE, cartesian products. Π_F(I)(B) := lim_{A∈F⁻¹(B)} I(A). Discards records not satisfying all conditions.

Decision guide: Δ = rename/restructure, same cardinality; Σ = merge/aggregate/generalize (accepts loss); Π = restrict/filter/specialize (accepts discards).

## Limits

**Def 3.79 (Terminal object Z)** — ∀ C ∈ C, ∃! C → Z. SQL: SELECT 1, constants.

**Prop 3.84** — All terminal objects isomorphic.

**Def 3.86 (Product X × Y)** — With projections p_X: X×Y→X, p_Y: X×Y→Y. Universal: for any C with f: C→X and g: C→Y, ∃! ⟨f,g⟩: C→X×Y. SQL: cartesian JOIN.

**Thm 3.95 (Finite limits in Set)** — For J presented by finite graph (V,A,s,t) with V = {v₁,...,vₙ} and D: J → **Set**:

lim D := {(d₁,...,dₙ) | dᵢ ∈ D(vᵢ) and ∀ a: vᵢ→vⱼ in A, D(a)(dᵢ) = dⱼ}

with projections pᵢ(d₁,...,dₙ) := dᵢ. This is a limit of D. Explains Π-operations as limits of diagrams.

**Pullback A ×_C B** — Limit of f: A→C, g: B→C. SQL: JOIN ON shared_key.

**Equalizer eq(f,g)** — Subobject where f = g. SQL: WHERE f(x) = g(x).

## Colimits

**Initial object 0** — ∀ C: ∃! 0 → C. SQL: empty tables, WHERE FALSE.

**Coproduct A+B** — With injections i₁, i₂. SQL: UNION ALL.

**Pushout A ⊔_C B** — Pasting A and B identifying common part C. SQL: UNION + PK reconciliation. Use: schema merge, incremental normalization.

**Coequalizer** — Quotient by equivalence relation from parallel morphisms. SQL: GROUP BY, DISTINCT.

## Advanced Concepts

**Yoneda Lemma** — For any A ∈ C: Nat(Hom(A,−), F) ≅ F(A) naturally in A. Interpretation: an object is fully determined by how others map to it. Application: entity defined by its incoming FKs; type defined by functions producing it.

**Slice category C/X** — Objects = morphisms f: A→X; morphisms = commuting triangles. Use: model relative instances, contextualized data, entities depending on a base context.

**Kan extension (basic)** — (Lan_F G)(d) = colim_{c: F(c)→d} G(c). Σ_F = special case with G = instance I.
XRef: `urn:fxsl:kb:algebraic-databases#KAN-EXTENSION`

## Operational Principles

**Diagram commutes** — Model coherent iff all relevant diagrams commute. Procedure: identify all parallel paths A→B; compute composition of each; verify path₁ = path₂; mismatch → structural inconsistency.

**Universal property** — Prefer universal constructions (limits/colimits) over ad-hoc solutions. Unique up to isomorphism; canonical and robust designs.

**Yoneda interface** — Design by interface: component defined by how it interacts, not by implementation. Consequence of Yoneda applied to software architecture.
