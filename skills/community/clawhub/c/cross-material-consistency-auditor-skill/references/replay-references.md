# Replay References (Anonymized Regression Patterns)

These are anonymized inconsistency patterns distilled from real audit incidents.
Use them to verify the skill still catches each pattern class after any modification.
No external files are required — each case below is self-contained.

## Pattern classes for regression testing

### Pattern 1: Achievement-wording escalation (P0)

Two materials describe the same milestone with different strength:
Material A says "paper accepted by a top conference"; Material B says
"technical achievement selected by a top conference". Verify the audit flags
the wording mismatch as P0 and proposes one unified wording.

### Pattern 2: Source conflation (P0)

One sentence merges data points from two different research firms as if from
a single source. Verify the audit flags the citation-integrity violation.

### Pattern 3: Quantitative claim drift (P1)

Material A: "utilization reaches 100%"; Material B: "utilization approaches
100%". Verify the audit flags the reached-vs-approached drift and requires a
single canonical figure with qualifier.

### Pattern 4: Feature-ownership mismatch (P1)

The same capability is attributed to product X in one draft and product Y in
the companion press release. Verify the audit flags ownership conflict.

### Pattern 5: Promised-section omission (P1)

The press release promises a section (e.g. open ecosystem) that the long-form
article never delivers. Verify cross-material completeness checking catches it.

### Pattern 6: Cross-language annotation asymmetry (P1)

The source annotation is stronger/more hedged in one language version than the
other. Verify bilingual pairs are compared claim-by-claim, not just structurally.

### Pattern 7: Caption vs body terminology mismatch (P1)

A figure caption uses an older term while the revised body uses a new term.
Verify captions/alt-text are included in the comparison scope.

### Pattern 8: Series-level fact drift (P0)

Across a multi-article series, the same case study appears with different
numbers or mixed attributions (e.g. two universities' data merged). Verify
series mode reproduces per-claim drift detection.

## Acceptance rule

A replay against at least two pattern classes must reproduce:

- The P0 mismatch type.
- The recommended unified wording.
- P0 flagged to block publication.
- No original file modified.
