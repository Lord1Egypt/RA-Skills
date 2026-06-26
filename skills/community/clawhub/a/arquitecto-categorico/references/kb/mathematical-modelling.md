# Mathematical Modelling via Category Theory

## Source

Src: `sources/cat/Mathematical modelling by help of cate.md`
XRef: `urn:fxsl:kb:mbse-consistency#MBSE-INJECTION-POSET`, `urn:fxsl:kb:seven-sketches#FDM-FUNCTOR-CATEGORY`

Notes: Model Poset = instance of injection order in MBSE; category of models analogous to instance category [C, Set] of FDM; model coupling uses products/coproducts as limits/colimits.

## Category Theory Foundations

**Def 2.1 (Category)** — Objects A,B,C,...; arrows f,g,h,... with dom(f), cod(f); composition g ∘ f: A → C for f: A → B, g: B → C; identity 1_A: A → A. Axioms: associativity h ∘ (g ∘ f) = (h ∘ g) ∘ f; unit f ∘ 1_A = f = 1_B ∘ f.

**Def 2.2 (Rel)** — Objects = sets; morphisms = binary relations f ⊆ A × B. Identity on A = {(a,a) | a ∈ A}.

**Def 2.3 (Discrete category)** — Every arrow is an identity.

**Def 2.4 (Functor)** — F: C → D. Objects A ↦ F(A); arrows f: A → B ↦ F(f): F(A) → F(B). Preserves F(1_A) = 1_{F(A)}; F(g ∘ f) = F(g) ∘ F(f).

**Def 2.5 (Natural transformation)** — ϑ: F → G (F,G: C → D). Family (ϑ_C: F(C) → G(C))_{C∈C} with naturality square: ϑ_{C'} ∘ F(f) = G(f) ∘ ϑ_C for every f: C → C'.

**Def 2.6 (Product C×D)** — Objects (C,D); arrows (f,g): (C,D) → (C',D'); composed componentwise.

**Def 2.7 (Functor category)** — B^C = Funct(C,B): objects = functors T: C → B; morphisms = natural transformations.

**Def 2.8 (Initial/terminal)** — 0 initial: ∃! 0 → C for any C. 1 terminal: ∃! C → 1 for any C.

**Prop 2.1** — Initial (terminal) objects unique up to isomorphism.

**Def 2.9 (Subcategory)** — S ⊆ C closed under domain/codomain, identities, composition. Full if all arrows between S-objects are in S.

**Def 2.10 (Comma category)** — (T ↓ S): objects ⟨e,d,f⟩ with f: T(e) → S(d); arrows ⟨k,h⟩ making diagram commute.

**Def 2.11 (Universal arrow)** — Pair ⟨r,u⟩ with r∈D and u: c → S(r) such that for any f: c → S(d), ∃! f': r → d with S(f') ∘ u = f.

**Def 2.12 (Equalizer)** — Of parallel f,g: A → B: object E, arrow e: E → A with f ∘ e = g ∘ e, universal.

## Categories of Mathematical Models

**Def 2.13 (Category of models)** — Model_1: objects = finite non-empty assumption sets Set_A; morphisms = relations between sets; S: Set_A → A maps assumptions to model formulation; all objects act in same physical dimension.

### MM-COMPLEXITY-ORDER

**Def 2.14 (Complexity order)** — A has higher complexity than B iff Set_A ⊂ Set_B but Set_B ⊄ Set_A. Equal complexity iff Set_A = Set_B.

**Def 2.15 (Total/partial order)** — If Set_{A_1} ⊂ Set_{A_2} ⊂ ... ⊂ Set_{A_n} and union = Set_{A_n}: totally ordered. Otherwise: partially ordered.

**Cor 2.1** — In totally ordered Model_1 with n objects: unique most complex (Set_{A_1} ⊂ Set_{A_i} ∀i) and unique simplest (Set_{A_n} = ∪_j Set_{A_j}).

**Prop 2.2** — For partially ordered Model_1: one of (1) neither extreme exists; (2) most complex exists, simplest does not; (3) simplest exists, most complex does not; (4) both exist.

**Thm 2.1** — If most complex Set_{A_1} and simplest Set_{A_n} coexist: Model_1 is totally ordered or contains ≥2 totally ordered subcategories.

**Thm 2.2** — Every partially ordered category of mathematical models contains ≥1 totally ordered subcategory.

**Def 2.16 (Convertible models)** — Two formulations B_1, B_2 associated to Set_{A_1} via functors F,G connected by natural transformation ϑ: F ⇒ G. B_1 and B_2 are convertible.

**Cor 2.2** — Convertible models have the same complexity.

## Coupled Models

**Def 2.17/2.18 (ModCoup_{i,j})** — Product category Model_i × Model_j with projections π_1, π_2. Coupled object: Set_{i,j} := ⟨Set_i ∪ Set_j, Set_Coup^{i,j}⟩ where Set_Coup^{i,j} = coupling conditions.

**Prop 2.3** — Set_{i,j} := T(Set_i) ∪ F(Set_j) = ⟨Set_i ∪ Set_j, Set_Coup^i ∪ Set_Coup^j⟩. Either both Set_Coup^i, Set_Coup^j non-empty, or exactly one.

**Def 2.19 (ModCoup_{i,i})** — Coproduct Model_i + Model_i. Objects via disjoint unions; coupling conditions Set_Coup^{i,i} ≠ ∅.

**Def 2.20 (Complexity of coupled models)** — A has higher base complexity than B if Set_A ⊂ Set_B; higher coupling complexity if Set_Coup^A ⊂ Set_Coup^B; higher total if both.

**Thm 2.3** — If most complex and simplest objects coexist in base or coupling: ModCoup_{i,j} is totally ordered in that sense.

**Thm 2.4** — Every partially ordered category of coupled models contains ≥1 totally ordered subcategory.

**Def 2.23 (Convertible coupled models)** — Two formulations B1, B2 of same Set_A convertible if ∃ natural transformation linking F(Set_A) and G(Set_A).

**Cor 2.5** — Convertible coupled models have same complexity.

## Abstract Constructions

**Def 2.28 (Functor categories of formalisations)** — Model^F = Funct(Model, Model^F); ModCoup^F = Funct(ModCoup, ModCoup^F). Structure preserved under different derivation methods.

**Def 2.29 (Comma category for coupling)** — (T ↓ S) with T: Model_i → ModCoup_{i,j}, S: Model_j → ModCoup_{i,j}. Objects ⟨Set_i, Set_j, f⟩ collect all ways to build coupled models.

**Cor 2.6** — Universal arrow from Model to Model^F exists if Model is totally ordered.

**Cor 2.7** — Universal arrow from Model_i or Model_j to ModCoup_{i,j} exists if Model_i or Model_j totally ordered.

## Engineering Definitions

**Def 2.30** — Mathematical model = set of basic assumptions + formulation + derivation.
**Def 2.31** — Complexity = range of phenomena describable.
**Def 2.32** — Convertibility = same assumptions, different formulations. Complexity unchanged.
**Def 2.33** — Coupled model = union of models + coupling conditions (more than mere union of equations).
**Def 2.34** — Coupling = mapping increasing complexity (adds phenomena).

## Reference Equations

Beam theories: ρF d²u/dt² + EI_y d⁴u/dx⁴ = 0 (Euler-Bernoulli; Rayleigh/Timoshenko variants).
Heat equation: cρ dθ/dt − λΔθ = 0.
Elasticity (Lamé): μΔu + (λ+μ)grad(div u) + ρK = 0.
Coupled thermoelasticity: μΔu + (λ+2μ)grad(div u) − (3λ+2μ)α_T grad Θ + F − ρü = 0, plus coupled heat-type equation.

Signal: S α = ℝ^{n+1} → α. Differential operators: D_i^s := ∂^s/∂ξ_i^s; div: SR n(α^n, α); grad: SR n(α, α^n).

## Completeness and Reducibility

**Def 2.39** — Set_A complete w.r.t. Set'_A if Set_A ⊂ Set'_A; write A | Set'_A.

**Def 2.41 (Reducible)** — Set_A complete w.r.t. Set'_A is reducible if ∃ simpler object still complete w.r.t. Set'_A. Reduction: Set_A →^{Set'_A} Set_B.

**Def 2.42 (Extendable)** — Set_A extendable if ∃ more complex object still complete w.r.t. Set'_A.

**Def 2.43 (Minimal/Maximal)** — Complete Set_A: minimal if irreducible; maximal if not-extendable.

**Prop 2.6 (Consistency of coupling)** — Coupling of models consistent iff squares in diagram commute for all pairs of objects and morphisms.
