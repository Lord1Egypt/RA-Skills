# Knowledge Base as Category

## KB Category Definition

Ctx: The Knowledge Base as a well-formed category with global invariants.
XRef: `urn:fxsl:kb:seven-sketches`
Notes: under current KORA governance, artifact identity is derived from filesystem + valid manifests, while the catalog is only a generated resolver. In this corpus, only `XRef` is materially encoded today; stronger relation kinds require a normalized relation block before they become auditable.

**KB** = category where Ob(KB) = artifacts and Hom(KB) = materially encoded relations plus explicitly normalized future relation edges.

Objects: each Markdown artifact under `KNOWLEDGE/fxsl/cat/` with valid front matter (`urn`, `version`, `status`, etc.). The generated catalog may be checked afterward as a derivative index, but it is not the source of truth.

Identity: each artifact has trivial self-reference morphism.

Composition: if A XRef→ B and B XRef→ C, path A → B → C exists. Today this composition is only guaranteed over materialized `XRef` edges.

## Morphism Types

| Type | Direction | Materialization | Semantics |
|---|---|---|---|
| XRef | A → B | Materialized today via `XRef:` lines | A cites/uses B; weak dependency |
| requires | A → B | Deferred until normalized relation block exists | A cannot function without B; strict dependency |
| refines | A → B | Deferred until normalized relation block exists | A more specific; faithful functor F: Cat(A) → Cat(B) exists |
| generalizes | A → B | Deferred until normalized relation block exists | A = colimit of family including B |
| equivalent_to | A ↔ B | Deferred until normalized relation block exists | Functors F: A→B, G: B→A with GF ≅ id, FG ≅ id |

## Global Invariants (Active)

**KB-INV-NO-DANGLING** (Severity: HIGH) — No dangling `XRef` references. ∀ `XRef` in artifact A: target(`XRef`) ∈ Ob(KB) ∨ target is resolvable external URN. Procedure: scan filesystem artifacts, extract `XRef`, resolve URNs via the current index/catalog or known external targets, and verify `#fragment` anchors when present.

**KB-INV-FILESYSTEM-MANIFEST-COMPLETE** (Severity: MEDIUM) — ∀ artifact in `KNOWLEDGE/fxsl/cat/`: valid front matter exists and the artifact is indexable. Procedure: list all Markdown artifacts in `KNOWLEDGE/fxsl/cat/`, parse manifests, verify required metadata, then compare against a freshly regenerated catalog only as a derivative consistency check.

**KB-INV-URN-UNIQUE** (Severity: CRITICAL) — ∀ URN u: |{A ∈ KB : urn(A) = u}| = 1. Procedure: extract URNs directly from manifests in the filesystem and detect duplicates.

**KB-INV-VERSION-DECLARED** (Severity: HIGH) — ∀ A ∈ KB: `version` is explicit in front matter and follows SemVer. Procedure: parse `version` from metadata, validate syntax, and compare derivative registries only after reindex when needed.

**KB-INV-RELATION-SCHEMA-GATED** (Severity: HIGH) — Invariants over `requires`, `refines`, `generalizes` and `equivalent_to` are `DEFERRED` until a normalized relation block exists in each artifact. Procedure: if the relation schema is absent, emit `DEFERRED` instead of `PASS`/`FAIL`.

## Deferred Invariants (Require Normalized Relation Metadata)

**KB-INV-NO-BAD-CYCLES** (Severity: MEDIUM) — No refinement cycles without declared equivalence. If A refines B and B refines A -> A equivalent_to B must be declared. Procedure: once relation blocks exist, build directed graph of `refines`; detect cycles; for each cycle verify `equivalent_to`.

**KB-INV-REQUIRES-ACYCLIC** (Severity: CRITICAL) — `requires` graph is acyclic (DAG). No chain A requires B requires ... requires A. Procedure: once relation blocks exist, build directed graph of `requires`; run DFS or Kahn cycle detection; any cycle -> CRITICAL.

## Universal Constructions in KB

**KB-PUSHOUT-MERGE** — Merge of two artifacts with common base = pushout.

```
     C (base)
    / \
   A   B
    \ /
     D = A ⊔_C B (merge)
```

Use: merge of partial knowledge on same base domain. Ex: C = seven_sketches; A = algebraic_databases; B = cql_data_integration; D = unified_algebraic_integration.

**KB-PULLBACK-COMMONALITY** — Common knowledge between two artifacts = pullback.

```
 D = A ×_C B (pullback)
    / \
   A   B
    \ /
     C
```

Use: identify conceptual overlap between artifacts.

**KB-COLIMIT-SYNTHESIS** — Synthesize artifact from multiple sources = colimit. Given diagram D: J → KB, colim(D) = synthesis unifying all respecting relations. Use: cognitive_toolkit is (conceptually) colimit of artifacts it synthesizes.

## Global Audit Procedure

Steps:
1. Inventory: list all artifacts in `KNOWLEDGE/fxsl/cat/**/*.md` directly from the filesystem and parse manifests.
2. Verify KB-INV-FILESYSTEM-MANIFEST-COMPLETE.
3. Verify KB-INV-URN-UNIQUE.
4. Verify KB-INV-VERSION-DECLARED.
5. Rebuild or reconcile the catalog only as a derivative consistency check when the audit requires resolver parity.
6. Build the active KB graph: nodes = artifacts; edges = materialized `XRef`.
7. Verify KB-INV-NO-DANGLING over the active graph.
8. If normalized relation blocks exist, extend the graph with `requires`, `refines`, `generalizes`, `equivalent_to` and activate the deferred invariants; otherwise report them as `DEFERRED`.
9. Individual artifact audit (`AUDIT-PROC-FULL` per artifact).
10. Generate global report, explicitly separating active checks from deferred ones.

Output format:

```
## Global KB Audit Report

### 1. Inventory
- Total artifacts: N
- In catalog: N
- Orphans: 0

### 2. Global Invariants
| Invariant | State | Details |
|-----------|-------|---------|
| NO-DANGLING | ✓/✗ | ... |
| FILESYSTEM-MANIFEST-COMPLETE | ✓/✗ | ... |
| URN-UNIQUE | ✓/✗ | ... |
| VERSION-DECLARED | ✓/✗ | ... |
| NO-BAD-CYCLES | ACTIVE/DEFERRED | ... |
| REQUIRES-ACYCLIC | ACTIVE/DEFERRED | ... |

### 3. KB Graph
- Nodes: N artifacts
- XRef edges: M
- Deferred relation edges: K
- Density: X%

### 4. Issues by Artifact
| Artifact | CRITICAL | HIGH | MEDIUM | LOW |
|----------|----------|------|--------|-----|

### 5. Global Proposals
[List of KB-level improvements]
```
