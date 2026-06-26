# Categorical Systems Theory

Work-in-progress book developing categorical systems theory: applying category-theoretic ideas to general systems theory. A system interacts with its environment through a specified interface; from the environment's view, only the interface matters. Systems interact via composable interfaces.

Key concerns: modularity (how to build larger systems from smaller ones); compositionality (facts about composite systems calculable from components and wiring). Uses standard category theory, indexed categories, and double categories; leads to a theorem about representable lax doubly indexed functors.

## Foundational Definitions

**Cartesian category.** Category C with all finite products and a terminal object. Functor F: C → D is cartesian if it preserves products and terminal objects.

**Dynamical system.** States (how things can be) + dynamics (how things change given how they are, potentially depending on inputs/parameters).

**Systems theory.** Particular way to answer: what is a state; how outputs vary with state; what inputs exist and how they depend on state; what changes are possible; how states change (deterministically, stochastically, etc.); how changes depend on inputs.

## Deterministic and Differential Systems

**Deterministic system S.** Consists of:
- State_S: set of states
- Out_S: set of output values (exposed variables)
- In_S: set of input values (parameters)
- expose_S: State_S → Out_S
- update_S: State_S × In_S → State_S (next state)

Interpretable in any cartesian category C.

**Closed system.** No inputs and no outputs: In_S and Out_S are singletons.

**Examples:**
- Clock: State = {1,...,12}, Out = {1,...,12}, In = {*}, expose = id, update(t,*) = tick(t).
- SIR discrete: State = triples (s,i,r) ∈ ℝ³, parameters (α,β); update_SIR((s,i,r),(α,β)) = (s - α·s·i, i + α·s·i - β·i, r + β·i).

**Differential system S** (first-order, ordinary). State_S = ℝ^n, In_S = ℝ^m, Out_S = ℝ^k; update_S: ℝ^n × ℝ^m → ℝ^n encoding d s/dt = update_S(s,i); expose_S: ℝ^n → ℝ^k. Euc = category of objects ℝ^n and smooth maps; cartesian with ℝ^n × ℝ^m = ℝ^{n+m}. Note: right-hand ℝ^n in differential systems is a tangent space, not a next state.

## Lens Theory

**Lens in cartesian category C.** Pass-forward map f: A^+ → B^+ and pass-back map f^♯: A^+ × B^- → A^-.

**Lens composition.** (f^♯,f): (A^-,A^+) → (B^-,B^+) with (g^♯,g): (B^-,B^+) → (C^-,C^+):
- pass-forward: g ∘ f
- pass-back: (a^+,c^-) ↦ f^♯(a^+, g^♯(f(a^+), c^-))

**Lens_C.** Category with objects = pairs (A^-,A^+); morphisms = lenses. Every cartesian functor F: C → D induces a functor Lens_C → Lens_D preserving parallel products.

**Deterministic systems as lenses.** A deterministic system = lens of the form (update_S, expose_S): State_S ↔ (In_S, Out_S). Differential systems = lenses in Euc with the same shape.

**Lens types by effect monad:**

| Type | update signature | Monad | Use |
|------|-----------------|-------|-----|
| Deterministic | S×I→S | Identity | pure deterministic systems |
| Possibilistic | S×I→P(S) | Powerset | non-determinism, multiple futures |
| Stochastic | S×I→D(S) | Distribution | probabilistic models |
| Cost | S×I→(S,Cost) | Writer | logging or accumulated costs |

## Wiring Diagrams

### WIRING-DEF

**Arity.** Free cartesian category on one object X. Objects = X^I for finite sets I; morphisms = reindexing maps derived from functions f*: X^I → X^J for f: J → I. Arity ≅ FinSet^op.

**WD (Wiring Diagrams).** WD := Lens_Arity. Monoidal structure via parallel products. For object C in cartesian category C, unique (up to iso) cartesian functor ev_C: Arity → C sends X to C; any wiring diagram interpreted as a lens in C.

**Typed wiring diagrams.** Family C(-): T → C in cartesian C → strong monoidal functor ev_C: WD_T → Lens_C.

**Wiring diagram components:**
- Inner boxes: component systems (lenses, coalgebras, services).
- Outer box: interface of composite system.
- Wires: input→output connections between boxes.

**Procedure for wiring diagram construction:**
1. List all components with interface types (inputs, outputs).
2. Draw each component as a box with ports.
3. Connect outputs to inputs respecting types.
4. Verify no cycles without delay (or model delay explicitly).
5. Define external interface: which inputs/outputs are exposed.
6. Result = morphism in the wiring diagram category.

**Lawvere theory L.** Single-sorted: cartesian category + bijective-on-objects functor Arity → L. Models of L in cartesian C = cartesian functors L → C. WD_L := Lens_L (wiring diagrams with operations from L).

## Non-Deterministic and Monadic Systems

**Commutative monad (M, η) on cartesian C.** Assignment MA to every A; map η_A: A → MA; for every f: A → MB a lift f^M: MA → MB; satisfying unit/identity/composition laws. Commutative if ∃ σ: MA × MB → M(A × B) making commutativity diagrams commute.

**Powerset P.** Commutative monad on Set: η_A(a) = {a}; f^P(X) = ⋃_{x∈X} f(x); σ_{A,B}(X,Y) = {(a,b) | a∈X, b∈Y}.

**Distribution D.** D(A) = finitely supported probability distributions on A. Stochastic map f: A → D(B): each a ↦ distribution on B. D is commutative monad: η_A(a) = Dirac delta; f^D pushes forward by summation; σ forms product measure of independent distributions.

**Kleisli category Kl(M).** Objects = objects of C; morphisms f: A ~> B given by A → MB in C; identity = η_A; composition f;g = f (g)^M.

**M-system S.** State_S, Out_S, In_S, expose_S, Kleisli map update_S: State_S × In_S → M(State_S).

**Monad catalog:**

| Monad | Effect | Kleisli morphism |
|-------|--------|-----------------|
| Maybe | partial failure | A → Maybe B |
| List | non-determinism | A → [B] |
| Distribution | probability | A → D(B) |
| State S | mutable state | A → S → (B,S) |
| Writer W | logging/trace | A → (B,W) |

**Kleisli composition procedure:**
1. Choose monad M by dominant effect (Maybe, List, State, etc.).
2. Express each pipeline step as f: A→M(B).
3. Compose using bind (>>=): f >=> g = λa. (f a) >>= g.
4. Composition automatically handles the effect (failure, non-det, state).

```
-- Pipeline with Maybe (can fail):
parseUser :: String → Maybe User
validateAge :: User → Maybe User
saveUser :: User → Maybe UserId
pipeline = parseUser >=> validateAge >=> saveUser
-- If any step fails, entire pipeline returns Nothing.
```

## Generalized Lens Construction

**Indexed category A: C^op → Cat.** Assigns category A(C) to each C, plus functorial reindexing.

**Grothendieck construction ∫_{C:C} A(C).** Objects = pairs (C,A) with A ∈ A(C); morphisms from C and reindexing in A.

**Ctx_C** (for object C in cartesian C). Objects = objects of C; morphisms f: X ⇒ Y = maps C × X → Y; composition uses diagonal Δ and projection π_2.

**Lens_C as Grothendieck.** Lens_C = ∫_C Ctx_C^op.

**A-lenses.** For indexed A: C^op → Cat: Lens_A = ∫_C A(C)^op.

**M-lenses.** Ctx_C^M (biKleisli of C×- and M): morphisms f: X ⇒ Y given by C × X → MY; identity = π_2;η; composition uses Δ; (C×f); λ; Mg; μ. Category of M-lenses: Lens_C^M = ∫_C (Ctx_C^M)^op. M-lens: pass-forward f: A^+ → B^+ and pass-back f^#: A^+ × B^- → M(A^-).

## Behavior Analysis

**Trajectory.** Sequence of states generated by system dynamics; used to analyze temporal evolution.

**Steady state.** s such that update(s, i) = s for some input regime; identifies stable configurations.

**Periodic orbit.** State sequence repeating after a finite number of steps; models cycles in dynamical systems.
