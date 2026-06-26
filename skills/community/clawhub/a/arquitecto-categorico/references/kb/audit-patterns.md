# Categorical Audit Patterns

Formal patterns for auditing, diagnosing, and improving DIK artifacts using categorical criteria. Sources: Seven Sketches (Fong, Spivak) — path equality, FDM; Categorical Data Integration (Brown, Spivak, Wisnesky) — integrity by construction; Coalgebra for the Working Software Engineer (Barbosa) — bisimulation as behavioral equivalence criterion; MBSE + Cat (S2ML) — catmodels, binary consistency, injections.

## DIK Classification of Artifacts

| Level | Definition | Examples |
|-------|-----------|---------|
| DATA | Instance I: S → Set over schema S. Values, rows, records, observations. Functor assigning sets to objects and functions to morphisms. | SQL table, JSON document, CSV file |
| INFORMATION | Schema S (finitely presented category). Objects = entities/types; morphisms = relations/attributes; path equations = business constraints. | DDL SQL, JSON Schema, GraphQL Schema, KORA Markdown artifact with frontmatter |
| KNOWLEDGE | Transformations, migrations, abstract models. Functors between categories, adjunctions (Δ/Σ/Π), Kan extensions, behaviors (coalgebras), inference rules. | Migration functor F: S → T, agent spec, KORA artifact with explicit procedure |

Audit focus per level: DATA → referential integrity, completeness, schema consistency. INFORMATION → structural coherence, commutativity, completeness of relations. KNOWLEDGE → functoriality, structure preservation, validity of adjunctions, and explicit operational criteria when the artifact claims executable guidance.

## Audit Dimensions

### Structural (AUDIT-DIM-STRUCTURAL)

| Check | Definition | Severity | Procedure |
|-------|-----------|----------|-----------|
| CHECK-IDENTITY | Each object has identity morphism? | CRITICAL | List all objects; verify id_A: A → A for each A |
| CHECK-COMPOSITION | Morphisms compose correctly? | CRITICAL | For f: A→B, g: B→C verify g∘f: A→C; verify cod(f)=dom(g) |
| CHECK-ASSOCIATIVITY | (h∘g)∘f = h∘(g∘f)? | CRITICAL | — |
| CHECK-PATH-EQUALITY | Declared parallel paths commute? | HIGH | For each equation path₁=path₂: verify I(path₁)=I(path₂) for every instance I. Ex: Employee.Mngr.WorksIn = Employee.WorksIn |

### Referential (AUDIT-DIM-REFERENTIAL)

| Check | Definition | Severity |
|-------|-----------|----------|
| CHECK-REF-INTERNAL | Ref: targets exist in same document? | HIGH |
| CHECK-XREF-EXTERNAL | XRef: targets are resolvable URNs? If #ID, verify it exists in target. | HIGH |
| CHECK-FOREIGN-KEY | For each morphism f: A→B, every v ∈ I(A) has I(f)(v) ∈ I(B). | CRITICAL |

### Completeness (AUDIT-DIM-COMPLETENESS)

| Check | Level | Severity |
|-------|-------|----------|
| CHECK-DATA-COMPLETE | Instance I defined for all objects in schema? | MEDIUM |
| CHECK-INFO-COMPLETE | Schema has explicit objects, morphisms, and equations? | MEDIUM |
| CHECK-KNOWLEDGE-OPERATIONALITY | If the artifact claims executable guidance, are the operational criteria or procedures explicit? | LOW |

### Quality (AUDIT-DIM-QUALITY)

| Check | Definition | Severity |
|-------|-----------|----------|
| CHECK-UNIVERSAL-CONSTRUCTION | Universal constructions used where applicable? | LOW |
| CHECK-FUNCTORIALITY | Transformations preserve structure? | MEDIUM |
| CHECK-BEHAVIORAL-EQUIVALENCE | Equivalent states identified via bisimulation? | LOW |

### Migration (AUDIT-DIM-MIGRATION)

| Check | Definition | Severity | Procedure |
|-------|-----------|----------|-----------|
| CHECK-MIGRATION-FUNCTOR | F: S→T well-defined? | HIGH | Verify F(id_A)=id_{F(A)} and F(g∘f)=F(g)∘F(f) |
| CHECK-MIGRATION-SQUARE | Migration square commutes? | HIGH | Given F: S→T, I: S→Set, J: T→Set — verify J ∘ F = α ∘ I (naturally) |
| CHECK-CONSTRAINT-PRESERVATION | Migration preserves required constraints? | HIGH | — |

### Behavioral (AUDIT-DIM-BEHAVIORAL)

| Check | Definition | Severity | Procedure |
|-------|-----------|----------|-----------|
| CHECK-INTERFACE-CONFORMANCE | System implements declared interface functor F? | HIGH | — |
| CHECK-BISIMULATION | Declared equivalent components are bisimilar? | MEDIUM | Identify c₁: U₁→F(U₁), c₂: U₂→F(U₂); verify bisimulation R ⊆ U₁×U₂; or verify beh(u₁)=beh(u₂) in final coalgebra |
| CHECK-ACTION-INDEX | Episodes have action as primary key? | LOW | — |

## Problem Patterns and Improvements

| Pattern | Symptom | Proposal | Justification |
|---------|---------|----------|---------------|
| PATTERN-BROKEN-DIAGRAM | Parallel paths do not commute | Add path equation or correct morphisms | Commutativity is a categorical coherence requirement |
| PATTERN-ORPHAN-OBJECT | Object without morphisms (except identity) | Connect to graph or remove if redundant | — |
| PATTERN-DANGLING-REFERENCE | Ref/XRef points to nonexistent | Correct reference or create target | — |
| PATTERN-MISSING-OPERATIONALITY | Artifact claims execution or auditability but omits explicit procedure/criteria | Add procedure, decision criteria, or executable checklist | Actionable knowledge requires operational closure when execution is claimed |
| PATTERN-SEMVER-INVALID | Version missing or not valid SemVer | Declare explicit SemVer in metadata | Corpus metadata separates persistent URN identity from mutable versioning |
| PATTERN-AD-HOC-CONSTRUCTION | Ad-hoc construction where universal exists | Use corresponding limit/colimit | — |
| PATTERN-NON-FUNCTORIAL-MIGRATION | Migration does not preserve composition | Redefine as valid functor or use Σ/Δ/Π | — |
| PATTERN-REDUNDANT-BISIMILAR | Bisimilar components treated as distinct | Identify via unique morphism to final coalgebra | — |

## Full Audit Procedure

**Step 1 — DIK Classification.**
a) Determine level: DATA | INFORMATION | KNOWLEDGE.
b) Identify type: SCHEMA | INSTANCE | ARTIFACT | MODEL | AGENT.
c) Record URN and domain.

**Step 2 — Structural Audit (AUDIT-DIM-STRUCTURAL).**
Execute CHECK-IDENTITY, CHECK-COMPOSITION, CHECK-ASSOCIATIVITY, CHECK-PATH-EQUALITY. Record CRITICAL issues.

**Step 3 — Referential Audit (AUDIT-DIM-REFERENTIAL).**
Execute CHECK-REF-INTERNAL, CHECK-XREF-EXTERNAL. If instance: CHECK-FOREIGN-KEY. Record HIGH issues.

**Step 4 — Completeness Audit (AUDIT-DIM-COMPLETENESS).**
Execute level-appropriate check (DATA/INFO/KNOWLEDGE). Record MEDIUM issues.

**Step 5 — Quality Audit (AUDIT-DIM-QUALITY).**
Execute CHECK-UNIVERSAL-CONSTRUCTION, CHECK-FUNCTORIALITY, CHECK-BEHAVIORAL-EQUIVALENCE if applicable. Record LOW issues.

**Step 6 — Migration Audit (if applicable) (AUDIT-DIM-MIGRATION).**
Execute CHECK-MIGRATION-FUNCTOR, CHECK-MIGRATION-SQUARE, CHECK-CONSTRAINT-PRESERVATION.

**Step 7 — Behavioral Audit (if applicable) (AUDIT-DIM-BEHAVIORAL).**
Execute CHECK-INTERFACE-CONFORMANCE, CHECK-BISIMULATION, CHECK-ACTION-INDEX for episodes.

**Step 8 — Report Generation.**
a) Consolidate issues by severity.
b) Associate improvement PATTERN to each issue.
c) Generate proposals with categorical justification.

## Audit Report Format

```
## DIK Audit Report

### 1. Classification
- DIK Level: [DATA | INFORMATION | KNOWLEDGE]
- Type: [SCHEMA | INSTANCE | ARTIFACT | MODEL | AGENT]
- URN: [urn if applicable]

### 2. Diagnostic Summary
| Dimension      | Status | Issues       |
|----------------|--------|--------------|
| Structural     | ✓/✗   | n CRITICAL   |
| Referential    | ✓/✗   | n HIGH       |
| Completeness   | ✓/✗   | n MEDIUM     |
| Quality        | ✓/✗   | n LOW        |
| Migrations     | ✓/✗/NA| ...          |
| Behavior       | ✓/✗/NA| ...          |

### 3. Detected Issues
| # | Severity | Dimension | Description | Location |

### 4. Improvement Proposals
| # | Issue | Pattern | Proposal | Justification |

### 5. Next Steps
[Prioritized list]
```
