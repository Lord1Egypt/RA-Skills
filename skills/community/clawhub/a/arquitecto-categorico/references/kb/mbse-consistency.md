# MBSE Consistency via Category Theory

## Source

Src: `sources/cat/Category Theory for Consistency Betwee.md`
XRef: `urn:fxsl:kb:mathematical-modelling#MM-COMPLEXITY-ORDER`, `urn:fxsl:kb:categorical-systems-theory#WIRING-DEF`

Notes: Catblocks analogous to components in wiring diagrams; injection poset = instance of Model Poset from mathematical_modelling; binary consistency = type of pullback in category of Catmodels.

## Category Theory Foundations

**Def 1.1 (Category)** — C: class Ob(C) of objects; for x,y ∈ Ob(C), set Hom_C(x,y) of morphisms. Axioms: (1) composition g ∘ f ∈ Hom_C(x,z) for f ∈ Hom_C(x,y), g ∈ Hom_C(y,z); (2) associativity (h ∘ g) ∘ f = h ∘ (g ∘ f); (3) identity id_x: x → x for each x.

**Def 1.2 (Functor)** — F: C → D. F_Ob: Ob(C) → Ob(D); F_{x,y}: Hom_C(x,y) → Hom_D(F(x),F(y)). Axioms: F(id_x) = id_{F(x)}; F(g ∘ f) = F(g) ∘ F(f).

**Def 1.3 (Natural transformation)** — α: F ⇒ G (F,G: C → D). For each x ∈ Ob(C): α_x: F(x) → G(x) in D. Naturality: for f: x → y in C, G(f) ∘ α_x = α_y ∘ F(f).

$$\begin{array}{ccc} F(x) & \xrightarrow{F(f)} & F(y) \\ \downarrow{\alpha_x} & & \downarrow{\alpha_y} \\ G(x) & \xrightarrow{G(f)} & G(y) \end{array}$$

**Def 1.4 (Full/Faithful)** — F: C → D. Full: F_{x,y} surjective for all x,y. Faithful: F_{x,y} injective for all x,y.

**Def 1.5 (Equivalence of categories)** — C ≃ D: functors F: C → D, G: D → C with natural transformations α: Id_C ⇒ G ∘ F and β: Id_D ⇒ F ∘ G.

**Def 1.6 (Cone)** — Over diagram D in C: object Q + morphisms from Q to each object of D making triangles commute.

**Def 1.7 (Limit)** — Universal cone L: for any other cone Q, ∃! Q → L making all triangles commute.

**Def 1.8 (Pullback)** — Limit of diagram f: A → C, g: B → C. Pullback A ×_C B with universal property.

## S2ML+Cat Framework

**Def 4.1 (Catport)** — Given countable set of symbols P, Catport = category C_P where Ob(C_P) = singleton {p ∈ P} and only morphism = identity on p. Interpretation: atomic port/interface.

**Def 4.2 (Catconnection)** — Category C_C: Ob(C_C) = finite non-empty set of Catports; only morphisms = identities. Interpretation: abstract connection between ports.

**Def 4.3 (Catblock)** — Category C_B with finite objects ∈ {Catblocks, Catports, Catconnections} and morphisms capturing reference/containment. Conditions: for each Catconnection C ∈ Ob(C_B) with Catport P1 ∈ Ob(C): morphisms r_{P1,C}: P1 → C and r'_{P1,C}: C → P1 exist; for each Catblock B1 ∈ Ob(C_B), its Catconnections/Catports/Catblocks belong to Ob(C_B) with morphisms to B1; for each X ∈ Ob(B1), unique Catblock B' in C_B contains X.

**Prop 4.1** — A Catblock is a category. (Proof: verify identities, composition, associativity from discrete substructures and containment morphisms.)

**Def 4.4 (Catmodel)** — Category M: Ob(M) = finite set of {Catblocks, Catports, Catconnections}; unique root Catblock R ∈ Ob(M); for x,y ∈ Ob(R), Hom_M(x,y) = Hom_R(x,y); morphisms from R to each object; no extra morphisms beyond category axioms.

## Catmodel Relations

**Catmodel injection** — f: M → N preserving structure (blocks, ports, connections) injectively. M = structural submodel of N.

**Def 4.11 (Equivalence of Catmodels)** — A,B ∈ S2ML+Cat are equivalent if ∃ injections F: A → B and G: B → A.

**Thm 4.1** — Any Catmodel in S2ML+Cat associates bijectively to a model in standard S2ML quintuple (up to symbol choice). (Proof: construct F: S2ML → Catmodel and G: Catmodel → S2ML; show G ∘ F = id and F ∘ G = id modulo renaming.)

**Lem 4.1** — If injections F: M1 → M2 and G: M2 → M1 exist: R2 = F(R1) and R1 = G(R2) (roots map to roots).

**Lem 4.2** — Under same assumptions: Order(M1) = Order(M2).

**Lem 4.3** — Under same assumptions: for each i ∈ [0,k], M1 and M2 have same number of objects of order i; F_Ob and G_Ob preserve order.

**Lem 4.4** — Under same assumptions: image of Catconnection under F_Ob (and G_Ob) = Catconnection with same number of Catports.

**Thm 4.2 (Cantor-Bernstein for Catmodels)** — If injections F: A → B and G: B → A exist: ∃ injection G': B → A with G' ∘ F = id_A and F ∘ G' = id_B. (Proof: constructive, by strong induction on order using Lem 4.1–4.4; build piecewise inverse per Catblock/Catconnection.)

**Cor 4.1** — From Thm 4.2: F is equivalence of categories.

**Thm 4.3** — Equivalence of Catmodels is equivalence relation (reflexive: identity injection; symmetric: reverse injections; transitive: composition of injections).

**Def 4.12 (Injection relation)** — A injected into B: ∃ injection F: A → B.

**Thm 4.4 (Injection partial order)** — Injection relation = partial order over Catmodels (given equivalences). Reflexive: identity; antisymmetric: mutual injections → equivalence; transitive: composition of injections.

## Consistency Relations

**Def 4.13 (Binary consistency)** — A ~ B iff ∃ A', B' and injections f_A: A' → A, f_B: B' → B, F: A' → B', G: B' → A' with F ∘ G = id_{B'} and G ∘ F = id_{A'}.

**Prop 4.3** — ~_all (no additional restriction): any two Catmodels A,B satisfy A ~_all B. (Proof: trivial Catmodels A', B' with single root block; identity maps F,G.)

**Def 4.14 (Dictionary consistency)** — ~_dic: binary consistency relation identifying common skeleton in each model. Elements outside skeleton are "forgotten." Captures user-provided alignment (dictionary of matched elements).

**Prop 4.2** — S2ML+Cat is a category. Objects = Catmodels; morphisms = injections. Identities: trivial injections; composition: composition of injections is injection; associativity: standard.

## Binary Consistency Procedure

Inputs: Catmodel M (MBSE), Catmodel N (Safety).

1. List elements of M and N (blocks, ports, connections).
2. Identify common elements by name/type/semantics.
3. Construct candidate K with shared elements.
4. Verify K is valid Catmodel (root Catblock, closed connections).
5. Verify inclusions K → M and K → N preserve structure.
6. If K exists and non-trivial → M and N are consistent.
7. If K empty or trivial only → inconsistency.

Example: M = {Controller, Sensor, Actuator, ctrl_to_sensor, ctrl_to_act}; N = {Controller, SafetyMonitor, ctrl_to_monitor}; K = {Controller}; K→M: Controller ↦ Controller; K→N: Controller ↦ Controller. Result: consistent (share Controller as common interface).

## Injection Partial Order (Complexity)

### MBSE-INJECTION-POSET

Injection relation defines partial order on Catmodels: A ≤ B iff ∃ injection A → B. Organizes models in a lattice of refinements/abstractions. Allows comparison of structural complexity of different models of the same system.
