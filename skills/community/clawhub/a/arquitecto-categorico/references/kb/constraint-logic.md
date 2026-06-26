# Unified Constraint Logic

Unified constraint language for all KB artifacts. Fragment of regular logic expressible in categories. Sources: Seven Sketches (Fong, Spivak) — path equations, schemas as categories; CQL (Spivak, Wisnesky) — ologs, constraints as equations, static satisfaction; Sketches of an Elephant (Johnstone) — categorical sketches, regular logic.

## Constraint Language L_CT

**Sorts.** Objects of the category (types, entities).

**Terms.** Morphisms and their compositions (paths).

**Formulas:**

| ID | Form | Syntax | Semantics | Example |
|----|------|--------|-----------|---------|
| FORMULA-PATH-EQ | path₁ = path₂ | composition of morphisms | I(path₁)=I(path₂) for every instance I: S→Set | Employee.Mngr.WorksIn = Employee.WorksIn |
| FORMULA-EXISTENCE | ∃x. φ(x) | required limit exists | category has the required limit | ∃ pullback of A→C←B |
| FORMULA-UNIQUENESS | ∃!x. φ(x) | unique morphism satisfying condition | universal property of limits/colimits | ∃! f: X→A×B s.t. π₁∘f=g₁ ∧ π₂∘f=g₂ |
| FORMULA-INCLUSION | A ↪ B (monomorphism) | injective morphism | I(A) ⊆ I(B) via injective I(f) | Manager ↪ Employee |
| FORMULA-SURJECTION | A ↠ B (epimorphism) | surjective morphism | I(f): I(A) → I(B) surjective | Employee ↠ HasDepartment |

**Theory T = (S, Σ).** Schema S (category with objects and morphisms) + axiom set Σ of L_CT formulas.

## Theory Satisfaction

**I ⊨ T.** Instance I: S → Set satisfies theory T = (S, Σ) iff it satisfies all formulas in Σ.

**Satisfaction procedure:**
1. For each φ ∈ Σ:
   a) If φ is path₁=path₂: verify I(path₁)=I(path₂).
   b) If φ is ∃-formula: verify existence of required object.
   c) If φ is ↪ (mono): verify injectivity of I(f).
   d) If φ is ↠ (epi): verify surjectivity of I(f).
2. If all pass → I ⊨ T.
3. If any fails → I ⊭ T, report violated formula.

**Mod(T) = category of models of T.** Objects: instances I: S→Set with I ⊨ T. Morphisms: natural transformations α: I ⇒ J preserving T. Use: study the space of all valid instances of a schema with constraints.

## Constraint Contexts

**Database constraints (L_CT mapping):**

| SQL constraint | L_CT form |
|---------------|----------|
| PRIMARY KEY | jointly monic identifier family from entity to key-attribute product |
| FOREIGN KEY | morphism f: A→B with existence constraint in I(B) |
| UNIQUE | monomorphism into attribute space or jointly monic attribute family |
| NOT_NULL | total attribute into a non-null subtype / exclusion of optional null object |
| CHECK | path equation or inclusion into subobject |

Example: `FOREIGN KEY (dept_id) REFERENCES Department(id)` → WorksIn: Employee → Department with ∀e. WorksIn(e) ∈ I(Department).

**MBSE constraints (L_CT mapping):**
- Block composition: block diagram as category, composition = connection.
- Port compatibility: type equation on connected ports.
- Consistency: existence of pullback between models.

**KORA artifact constraints:**

| Constraint | L_CT |
|-----------|------|
| Ref_Valid | well-defined internal morphism |
| XRef_Resolves | external morphism with target in KB |
| Operationality_Explicit | if artifact claims executable guidance, procedure/criteria are explicit |
| Version_Declared | metadata.version exists and is valid SemVer |
| URN_Persistent | URN is stable artifact identity and remains version-free |

## Constraint Preservation by Migrations

**F: S→T preserves φ** if F(φ) is satisfiable in T.

| Preservation type | Definition | Use |
|-----------------|-----------|-----|
| Strict | I ⊨ φ ⟹ F*(I) ⊨ F(φ) for all I | Strong guarantee: constraint always maintained |
| Weak | ∃I such that F*(I) ⊨ F(φ) | At least some models preserve the constraint |

**Adjoint behavior with constraints (Δ/Σ/Π):**

| Operator | Constraint preservation | Reason |
|----------|------------------------|--------|
| Δ_F (pullback) | ALWAYS preserves path equations | Δ_F(I)(A)=I(F(A)); composition preserved |
| Σ_F (left pushforward) | NOT always | Uses colimits; may "collapse" distinctions |
| Π_F (right pushforward) | Preserves existence constraints | Uses limits; preserves universal properties. May empty sets if no compatible elements |

**Preservation verification procedure:**
1. Identify type of φ (path eq, mono, epi, existence).
2. Identify migration operator (Δ, Σ, Π).
3. Apply rules per table above.
4. Document which constraints are preserved and which are not.

## Migration Constraint Audit

### CL-MIGRATION-AUDIT

**Procedure:**
1. Extract source theory T_source = (S, Σ_S).
2. Extract target theory T_target = (T, Σ_T).
3. Identify migration functor F: S → T.
4. For each φ ∈ Σ_S:
   a) Compute F(φ) (image of constraint).
   b) Verify if F(φ) ∈ Σ_T or derivable from Σ_T.
   c) If not → WARN: constraint may be lost.
5. For each ψ ∈ Σ_T not coming from Σ_S:
   a) Verify if migration can satisfy ψ.
   b) If not → ERROR: migration violates target constraints.
6. Generate preservation report.

## Theory Audit

**Audit that an artifact defines a consistent theory:**
1. EXTRACTION: identify schema S; extract explicit constraints (path eq, FKs, etc.); extract implicit constraints (from KORA conventions); construct T = (S, Σ).
2. INTERNAL CONSISTENCY: verify Σ has no obvious contradictions (e.g., path₁=path₂ and path₁≠path₂ simultaneously); verify required limits exist in S.
3. SATISFIABILITY: verify at least one model I ⊨ T exists. If T only has empty models → WARN: possibly trivial theory.
4. COMPLETENESS: verify important constraints are declared (e.g., FKs have explicit existence constraint).
5. REPORT: extracted theory + consistency issues + completeness issues.

**Audit that an instance satisfies its theory:**
1. Load schema S and instance I.
2. Load theory T = (S, Σ).
3. For each φ ∈ Σ: evaluate I ⊨ φ; if fails: record violation with concrete data.
4. Generate satisfaction report.
