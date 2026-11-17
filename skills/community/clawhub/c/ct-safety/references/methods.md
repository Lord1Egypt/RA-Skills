# Methods — Disproportionality & Scoring (agent-facing)

This file documents the statistical methods used by `ct-safety`. It is the technical
reference for the `## Methods` section of SKILL.md. All formulas and thresholds are
preserved here so SKILL.md can stay concise.

## 1. The 2×2 contingency table

For a drug–event pair, build the table from FAERS counts:

| | Event (E) | Not-E (¬E) | Row |
|---|---|---|---|
| Drug (D) | a | b | a+b |
| Not-D (¬D) | c | d | c+d |

- **a** = reports with both drug D and event E
- **b** = reports with D but not E
- **c** = reports with E but not D
- **d** = reports with neither
- `drug_total = a+b`, `event_total = a+c`, `grand_total = a+b+c+d`
- `b = drug_total − a`, `c = event_total − a`, `d = grand_total − a − b − c`

## 2. Four disproportionality measures

### PRR (Proportional Reporting Ratio)
```
PRR  = (a / (a+b)) / (c / (c+d))
χ²   = (a − E[a])² / E[a]   (1-df chi-square vs expected under independence)
PRR  p-value = 1-df χ² upper tail via math.erfc (pure stdlib, no scipy)
```
**Signal rule:** PRR ≥ 2 **and** χ² ≥ 4.

### ROR (Reporting Odds Ratio)
```
ROR  = (a·d) / (b·c)
```
**Signal rule:** ROR lower 95% CI > 1.
The 95% CI is computed by the standard log-method:
`exp( ln(ROR) ± 1.96·sqrt(1/a + 1/b + 1/c + 1/d) )`.

### IC (Information Component, UMC/VigiBase)
```
IC   = log₂( (a+0.5) / expected ) ,  expected = (a+b)(a+c)/grand_total
```
**Signal rule:** IC lower 95% CI > 0.

### EBGM (Empirical Bayes Geometric Mean, FDA MGPS / DuMouchel 1999)
Bayesian gamma-Poisson shrinkage mixture.
- **EBGM** = posterior mean (shrunken estimate).
- **EB05 / EB95** = 2.5% / 97.5% posterior quantiles.
- Implemented in `ebgm.py` as regularized lower incomplete gamma via Numerical
  Recipes series / continued-fraction (pure stdlib, no scipy).
- Computed from **raw counts**, independent of the Haldane correction.
- **Signal rule:** EB05 ≥ 2.

> Note: IC is the UMC/VigiBase Information Component — it is **not** EBGM.
> True FDA EBGM is implemented in `ebgm.py`.

## 3. Continuity correction & zero guards

- **Haldane-Anscombe correction** (`continuity=True`, default since v0.1.9): add
  `+0.5` to every cell of the sparse 2×2 before computing ratios.
- **Structural-zero guard (`a == 0`)**: when the drug–event pair is never reported
  together, `compute()` returns a **conservative null** —
  `signal_overall=False`, all four sub-method flags `False`, with an explicit `note`
  — **regardless of `continuity`**. (EBGM correctly returns ~1 / no signal.)
- **Negative-cell guard (cell < 0)**: invalid negative counts also return the
  conservative null (no `OverflowError`/`NaN`, no crash), mirroring the `a==0` guard.

## 4. Multi-event FDR control — Benjamini-Hochberg

- `benjamini_hochberg()` applied to the R13 multi-event sweep and the R5 competitor
  benchmark, surfacing `fdr_q` / `fdr_signal` in the Markdown tables.
- PRR p-value (1-df χ² upper tail via `math.erfc`) feeds the correction.
- Purpose: curb false discovery under multiple testing.

## 5. PT → SOC organ grouping

- `disproportionality.map_soc()` maps high-frequency MedDRA PTs to System Organ
  Class (SOC), with an `"Unmapped"` fallback for unknown terms.
- Curated, **non-certified** dictionary (readability use only; MedDRA-licensed
  lookup recommended for full coverage).
- **Substring fallback fix (v0.1.14):** substring matching applies only to
  multi-word dictionary keys, longest-match-first, explicitly excluding generic
  words (`PAIN`, `KIDNEY`, …) from hijacking compound PTs
  (e.g. `CHEST PAIN` → explicit `Cardiac` entry, no longer `General`).
- SOC column is added to all event tables (single-event, top-events, R13, R5).

## 6. Multi-drug adjusted ROR (aROR) — `--compare-drugs`

Implemented in `adjust_ror.py`:
- `adjusted_ror_aggregate()` — focal vs pooled reference, Haldane fallback for sparse.
- `mantel_haenszel_or()` — stratified pooled OR (aggregate MH level).
- `logistic_irls()` with **Firth penalization** — individual-level hook for
  patient-level rows (available when patient data is supplied).

First drug on the CLI = focal; remaining = reference pool. Requires `--event`.

## 7. Temporal anomaly detection — `--trend`

Implemented in `time_series.py`:
- `fetch_monthly_series()` — one openFDA `receivedate` count facet (rate-limit friendly).
- `to_quarterly()` — monthly → quarterly buckets.
- `detect_anomaly()` — **CUSUM + rolling-Z + changepoint**, pure stdlib.
Catches Weber-effect upticks that a pooled estimate smooths over. Requires `--event`.

## 8. Safety Signal Score (0–100) & Evidence Tier (T1–T4) — `--with-fda-label`

Implemented in `signal_score.py`. Composites up to five sources into a transparent
score and evidence tier:

| Component | Source |
|---|---|
| FAERS disproportionality | ROR / PRR / IC + FDR |
| FDA Label | labeled vs unlabeled (`check_event()`: unlabeled = higher priority) |
| China PV | cdr-adr.org.cn qualitative corroboration |
| Temporal trend | `#5 --trend` |
| Control validation | `#6 --validate-controls` |

- **Score range:** 0–100. All component **weights centralized in `signal_score.WEIGHTS`** (auditable).
- **`controls` component (v0.1.14):** `safety_signal_score()` takes `control_pair`;
  if the queried (drug,event) is itself a `CONTROL_DRUGS` anchor, it is scored by
  whether the pipeline's measured signal matches the known expectation (match=10,
  mismatch=0) — no extra network call.
- **Evidence tiers:**
  - **T1 — Strong**
  - **T2 — Moderate**
  - **T3 — Weak**
  - **T4 — Indeterminate**
- Default (without `--with-fda-label`) = FAERS × CN-PV dual-source; with
  `--with-fda-label` the FDA Label 3rd source is enabled.
- Exposed in the single-event report as a dedicated "综合安全信号评分与证据分级"
  section: 0–100 score + T1–T4 + each component.
