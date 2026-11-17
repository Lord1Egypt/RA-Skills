# Coherence Function — Minimum Viable Spec (MVS-1)

**Provenance:** Drafted in chat with DeepSeek, 2026-10-15. NOT filed to the mesh, NOT claimed as agent work, NO PoWP.
**Status:** DRAFT — passing P1–P6 is necessary but not sufficient for PROMOTED. Promoted findings stay at 0.
If used in the mesh, file as **[proposal]**, attribute "drafted in chat".
Until someone checks it on a frozen corpus, it is "just a well-specified HOLD."

## Scope

Δ(a,b) → [0,1] over artifacts from the same declared type space T.
"Coherence" is NOT truth / quality / correctness — it is agreement on the declared comparison surface.

**Hard constraints:**
- **C1** — Every call specifies a versioned comparison surface S. Δ without S must **raise**, not default.
- **C2** — Direction is fixed once; flipping between call sites is non-conforming.

## The six properties (all must pass on the frozen corpus; failing any one = VETO on promotion, not a downgrade)

- **P1 — Totality on declared inputs.** Measures: does Δ return a defined scalar for every (a,b,S) with a,b∈T(S)?
  Pass: 100% of corpus pairs return a float in [0,1]; no raise/NaN/None.
  Fail: any raise/NaN/null/out-of-range on valid input. "A function that can't be called is not a function."
- **P2 — Identity / reflexivity.** Measures: does an artifact cohere perfectly with itself?
  Pass: Δ(a,a)=1.0 **exactly** (bit-identical float, not ≈) for every corpus artifact.
  Fail: <1.0 or varies across invocations. Non-deterministic fields (e.g. timestamps on S) must be canonicalized first; canonicalization is part of the function.
- **P3 — Symmetry.** Measures: order-independence.
  Pass: Δ(a,b)=Δ(b,a) exactly on all corpus pairs.
  Fail: asymmetry beyond a documented per-field tolerance of 0 — no default tolerance; inherently directional fields must be excluded from S and handled by a separate directional function.
- **P4 — Declared-surface locality (no ghost signal).** Measures: does Δ depend only on fields in S?
  Pass: perturb any off-surface field (metadata, whitespace, key ordering, receipt hash, agent ID) → Δ bit-identical, for 100% of corpus pairs across all off-surface fields.
  Fail: any off-surface field changes Δ → VETO. "The most common silent failure."
- **P5 — Monotone response to declared disagreement.** Measures: does Δ decrease monotonically as declared-surface disagreement increases?
  Pass: Δ(a,p₀(a)) ≥ Δ(a,p₁(a)) ≥ … ≥ Δ(a,pₙ(a)) for ordered strictly-increasing-disagreement perturbations, with **at least one strict inequality per artifact** (catches the constant-function trap).
  Fail: any inversion or flat response across strictly-disagreeing perturbations.
- **P6 — Calibration against the declared band boundaries.** Measures: do the §3 thresholds actually separate the corpus as claimed?
  Pass (on frozen, hand-labeled corpus, ≥2 independent labelers, labels COHERENT/PARTIAL/INCOHERENT):
  ≥95% COHERENT pairs score ≥0.70; ≥95% INCOHERENT score <0.25; no PARTIAL pair scores 1.0;
  false-ALLOW rate ≤1%; false-VETO rate ≤1%.
  Fail: any missed — "a function that passes P1–P5 but fails P6 is well-behaved and miscalibrated, which is exactly the state the HOLD was meant to prevent." Failing P6 returns to HOLD (VETO on promotion).

Why six and not more: each is independently falsifiable on the corpus and maps to a named real failure; "adding properties without a corpus test is the aspirational move this spec rejects."

## Δ direction convention

Δ is **SIMILARITY, not distance.**
Δ_S(a,b) = 1 − D_S(a,b)/D_max(S), where D_S(a,b) = Σ w_f·d_f(a_f,b_f), w_f≥0, Σw_f=1, weights versioned as part of S, D_max(S)=1 by normalization so Δ_S=1−D_S.

Consequences: Δ=1 ⟺ D=0 (perfect agreement); Δ=0 ⟺ D=1 (max disagreement); Δ is NOT a probability; Δ not comparable across different S (ledger entries must carry S and version); if you want distance, call D_S directly — bands are defined on Δ.

Per-field distance table (required):
- boolean/enum: 0-if-equal-else-1
- bounded numeric: min(1,|x−y|/range_f)
- identifier/hash strings: byte-equal-or-1 (no fuzzy matching)
- prose: 1−(edit_similarity/max_len) on declared normalized form
- set: Jaccard (both-empty→0, one-empty→1)
- ordered list: normalized Kendall-tau
- absent required field → 1

## Bands

- **ALLOW** Δ≥0.70 (may proceed to independent replay + adversarial review; NOT promotion)
- **AMBER** 0.70>Δ≥0.25 (proceed only with written disagreement inventory; blocked from promotion until resolved or superseded)
- **VETO** Δ<0.25 (reject; file as negative result)
- Boundary convention: exactly 0.70→ALLOW; exactly 0.25→AMBER.

## Stub vectors (S_example: fields {status: enum, value: numeric(range=100), ref: hash-string}, weights {0.5,0.3,0.2})

- ALLOW: a={status:"ready",value:40,ref:"sha256:aaaa…"}, b={status:"ready",value:46,ref:"sha256:aaaa…"} → D=0.018, Δ=0.982. Also: d_value=0.60 → Δ=0.82 exactly stub.
- AMBER: a={status:"ready",value:40,ref:"sha256:aaaa…"}, b={status:"ready",value:90,ref:"sha256:bbbb…"} → D=0.35, Δ=0.65; exact-0.55 variant: d_value=1.0→D=0.50→Δ=0.50. Mandatory edge: d_ref=0, d_value=1.0 → Δ=0.70 boundary test.
- VETO: a={status:"ready",value:40,ref:"sha256:aaaa…"}, b={status:"withdrawn",value:95,ref:"sha256:bbbb…"} → D=0.865, Δ=0.135.
- Mandatory boundary stubs: Δ=0.70→ALLOW; Δ=0.25→AMBER; Δ=0.2499…→VETO; Δ(a,a)=1.0→P2; off-surface perturbation→bit-identical→P4.

## Frozen test corpus

≥500 artifact pairs, ≥200 hand-labeled by ≥2 independent labelers (disagreement resolved by written rule), hash-pinned BEFORE P6 runs (re-labeling after seeing scores invalidates P6); includes adversarial cases: near-duplicates differing only off-surface (P4), constant-output traps (P5), direction-flip traps (P3), boundary pairs (P6). ≥20% of labeled pairs held out from weight tuning (calibration leakage). Corpus+labels are part of the promotion receipt; corpus change voids the promotion → back to HOLD.

## Ten failure modes

1. Direction flip (distance in one path, similarity in another — prevented by §2 convention + P3 + boundary stubs).
2. Ghost signal (off-surface fields move Δ — most common silent failure — P2+P4+perturbation stubs).
3. Constant function (caught by P5 strict-inequality + corpus).
4. Threshold-by-vibes (bands tuned to look good, then corpus relabeled — P6 frozen-corpus + labeler independence).
5. Fuzzy-string creep (identifiers/hashes "forgiven" — §2.1 table: byte-equal or 1).
6. Undefined surface (Δ called without S or stale S — C1 raise + S on every receipt).
7. NaN/None smuggling (P1 + absent-field rule).
8. Asymmetric prose normalization (P3 + declared normalization).
9. Calibration leakage (frozen corpus + hold-out).
10. Band-boundary ambiguity (§3 convention + boundary stubs).

## Implementation checklist

Declare S (fields, types, weights, normalization, d_f per field, version); implement D_S and Δ_S=1−D_S; raise on missing S/unknown type/weight-sum≠1/out-of-range; canonicalize non-deterministic fields; pin frozen corpus hash; run P1–P6 and boundary/off-surface stubs recording pass/fail with corpus hash and code hash in the receipt; emit receipt with S version, code hash, corpus hash, P1–P6 results, stubs, labeler rule — no receipt → no promotion.

Non-goals: truth, causal validity, semantic equivalence beyond declared S, cross-S comparability, agent intent.
