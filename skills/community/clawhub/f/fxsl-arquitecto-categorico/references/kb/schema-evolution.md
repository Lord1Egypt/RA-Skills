# Schema Evolution and Behavioral Audit

## Overview

Ctx: Auditing migrations, versions, and behavior over time.
XRef: `urn:fxsl:kb:seven-sketches#MIGRATION-DELTA`, `urn:fxsl:kb:coalgebras#BISIMULATION`, `urn:fxsl:kb:cql-data-integration#CQL-PROVENANCE`, `urn:fxsl:kb:constraint-logic#CL-MIGRATION-AUDIT`

Extends audit from static snapshots to temporal processes and dynamic behaviors.

## Version Category

**Ver** = category: objects = versions; morphisms = migrations.

- Objects: v1.0.0, v1.1.0, v2.0.0, ...
- Morphisms: upgrade: v_n → v_{n+1}; downgrade: v_{n+1} → v_n (if exists)
- Identity: no-op migration on each version
- Composition: upgrade_{n,n+1} ; upgrade_{n+1,n+2} = upgrade_{n,n+2}
- Properties: Ver typically a preorder (at most one morphism between versions); if upgrades and downgrades compatible → partial groupoid

**Schema functor F: Ver → Cat** — assigns each version its schema. F(v_n) = S_n; F(upgrade) = migration functor F_{n,n+1}: S_n → S_{n+1}.

Example: F(v1.0.0) = S₁ with {Employee, Department}; F(v1.1.0) = S₂ with {Employee, Department, Project}; F(upgrade_{1.0→1.1}) = inclusion S₁ ↪ S₂.

**Instance fibration** — for each version v, instance category Inst(F(v)). Migration upgrade_{n,n+1} induces functors Δ/Σ/Π between instance categories.

```
Inst(S₁) --Σ_F--> Inst(S₂)
    |                   |
    v                   v
 v1.0.0 --upgrade--> v1.1.0
```

## Migration Chain Audit

**Migration chain** — sequence v₁ → v₂ → ... → vₙ.

Audit goals: (1) each migration is functorial; (2) composition preserves critical invariants; (3) detect cumulative information/constraint loss.

**Procedure**:
1. Inventory: list versions v₁,...,vₙ and migrations m₁: v₁→v₂, ..., m_{n-1}: v_{n-1}→vₙ.
2. Individual migration audit: for each mᵢ verify functor validity (preserves id, composition); identify operator (Δ,Σ,Π or combination); apply CL-MIGRATION-AUDIT for constraints; record preserved vs. lost constraints.
3. Composition audit: compute m = m_{n-1} ∘ ... ∘ m₁; verify m: S₁ → Sₙ valid functor; compare constraints T₁ vs. Tₙ; identify chain-lost constraints.
4. Provenance analysis: trace data in Sₙ to origin in S₁; detect orphaned data (no clear origin).
5. Invariant analysis: identify critical invariants (must-preserve constraints); verify preservation across full chain; critical invariant lost → CRITICAL severity.
6. Report: migration map; constraints preserved vs. lost per migration; critical invariants final state; improvement recommendations.

**Technical debt detection** — Symptoms: schema violates prior version constraints; ad-hoc non-functorial migrations; important constraints progressively lost; migrated data no longer satisfies original invariants. Procedure: load constraints from v₁; load current instance I in vₙ; verify original constraints on current data; difference = accumulated categorical debt; propose refactoring plan.

## Behavioral Audit

**Coalgebra** — c: U → F(U): U = state space; F = interface functor; c assigns each state its observable behavior.
XRef: `urn:fxsl:kb:coalgebras#COALGEBRA-DEF`

**Bisimulation audit** — comparing behavioral equivalence between system versions:
1. Model versions as coalgebras: (U₁, c₁: U₁ → F(U₁)) and (U₂, c₂: U₂ → F(U₂)); verify same interface functor F.
2. Verify bisimulation: find relation R ⊆ U₁ × U₂ such that (u₁,u₂) ∈ R implies: output(c₁(u₁)) = output(c₂(u₂)); if u₁ transitions to u₁', ∃ u₂' with u₂ transitions to u₂' and (u₁',u₂') ∈ R. Alternative: verify via final coalgebra beh₁(u₁) = beh₂(u₂).
3. Analyze differences: identify diverging states; identify input sequences producing different outputs; classify: intentional change vs. regression.
4. Report: bisimilar? Yes/No; divergence points; recommendation: document change or fix regression.

**Action audit** — auditing logs/episodes using action as primary key:
1. Verify episodic structure: each episode has indexing action; action = morphism in domain category; no orphaned episodes.
2. Verify compositionality: if episode E₁ followed by E₂, composition of actions recorded?; action sequences form paths in category.
3. Verify temporal consistency: actions respect temporal order; no time-travel (effects before causes).
4. Verify constraints on actions: actions satisfy declared preconditions?; results satisfy postconditions?
5. Report: episode-by-action coverage; temporal anomalies; pre/postcondition violations.

## Categorical Provenance

**Provenance** — given datum d in instance J: T → **Set**, provenance(d) = set of data in I: S → **Set** that contributed to d via migration F: S → T.
XRef: `urn:fxsl:kb:cql-data-integration#CQL-PROVENANCE`

**Provenance audit**:
1. Completeness: for each d in target, provenance defined? If not → WARN: datum without provenance.
2. Correctness: if provenance(d) = {s₁,...,sₖ}, applying migration to sᵢ produces d?
3. Minimality: provenance includes only necessary data? Unnecessary items → inefficiency (not error).
4. Transitivity: for migration chains, provenance transitive through v₁→v₂→v₃?
5. Report: provenance coverage; data without origin; inconsistencies.

## Full Temporal Audit Procedure

Scope determination:
- Schema evolution? → Migration chain audit + debt detection.
- Behavior? → Bisimulation audit (version comparison) or action audit (logs).
- Provenance? → Provenance audit.
- Combined? → Execute all applicable.

Output format:

```
## Temporal/Behavioral Audit Report

### 1. Scope
- Schema evolution: ✓/✗
- Behavior: ✓/✗
- Provenance: ✓/✗

### 2. Evolution (if applicable)
| Version | Constraints | Preserved | Lost |
|---------|-------------|-----------|------|

### 3. Behavior (if applicable)
| System A | System B | Bisimilar | Divergences |
|----------|----------|-----------|-------------|

### 4. Provenance (if applicable)
| Coverage | No origin | Inconsistencies |
|----------|-----------|-----------------|

### 5. Issues and Proposals
[Consolidated list]
```
