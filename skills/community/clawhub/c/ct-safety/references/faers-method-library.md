# FAERS Method Library: Choosing Metrics, Comparators and Robustness Routes

> 中文摘要：FAERS 研究的方法选择库——信号指标（ROR/PRR/IC/EBGM）、比较器与范围方法、表征方法、稳健性方法各自的适用场景、替代方案与选择规则。配合 `faers-comparative-design.md` 使用。
>
> **Adapted from**: `active-comparator-single-soc-faers-safety-comparison` (references/method-library.md, study-patterns.md) — AIPOCH, MIT License
> **Source**: https://github.com/aipoch/medical-research-skills
> **Migrated**: 2026-08-04 (into ct-safety)

---

## 1. Signal-detection core

| Method | Primary use | Main alternative | Decision rule |
|---|---|---|---|
| **ROR** | Simple, interpretable disproportionality metric | PRR / IC / EBGM | Default for readable primary tables; ct-safety default |
| **PRR** | Regulatory-style screening companion | ROR | Secondary support when conventional MHRA-style thresholds are wanted (PRR ≥ 2, χ² ≥ 4, n ≥ 3) |
| **IC (BCPNN)** | Bayesian shrinkage; stabilizes sparse cells | ROR / PRR | Prefer when PT-level sparse cells dominate; report IC025 |
| **EBGM (MGPS)** | Bayesian shrinkage, FDA-style | IC | Use when the audience expects FDA/Empirica conventions; report EB05 |
| **Case de-duplication by latest version** | Reduce duplicate-report inflation | Naive case counting | Strongly preferred whenever raw exports may contain multiple versions (see `faers-data-prep.md`) |
| **Suspect-drug prioritization (PS only)** | Tighten exposure definition | All-role inclusion | Prefer when specificity matters more than breadth |

**Multi-metric rule** — when a signal is sparse or controversial, report at least two metrics (one frequentist + one Bayesian). Divergence between ROR and IC025/EB05 is itself an informative robustness finding.

---

## 2. Comparator and scope methods

| Method | Primary use | Main alternative | Decision rule |
|---|---|---|---|
| **Active-comparator restriction** | Reduce denominator mismatch / confounding by indication | Whole-database background | Use when the question is comparative within a therapeutic space |
| **Same-class head-to-head** | Detect subclass or pharmacologic contrast | Class vs non-class | Use when the story is *within* a class |
| **Fixed single-SOC analysis** | Keep one coherent clinical safety theme | Whole-profile scan | Prefer for a reviewer-friendly, single-question paper |
| **Curated PT panel** | Focus on clinically meaningful events | Broad SOC scan | Use when the AE family is known and specific |

**Comparator validity check** — before accepting an active comparator, confirm indication overlap. Weak overlap must be flagged in Limitations; it does not invalidate the design but caps the claim at Tier 2.

---

## 3. Characterization methods

| Method | Primary use | Main alternative | Decision rule |
|---|---|---|---|
| Age / sex stratified signal summary | Demographic characterization | Unstratified result only | Use when a subgroup angle is requested or clinically motivated |
| Seriousness outcome tabulation | Adds clinical context (hospitalization, death) | Signal-only report | Use when outcome severity matters to the question |
| Time-to-onset summary | Temporal characterization | No temporal layer | Only if date fields are adequately populated |
| Label-context comparison (openFDA `drug/label.json`) | Frame known vs under-discussed signals | Pure signal table | Use when translational or regulatory framing is part of the goal; ct-safety supports this via `--with-fda-label` |

---

## 4. Robustness methods

| Method | Primary use | Main alternative | Decision rule |
|---|---|---|---|
| Alternate exposure filter | Test stability under stricter inclusion | Single extraction rule | Standard+ when overreporting risk is high |
| Alternate denominator / comparator restriction | Test comparative stability | One comparator frame | Standard+ for reviewer-facing comparative papers |
| Multi-metric confirmation | Reduce one-metric overinterpretation | Single primary metric | Standard+ when sparse or controversial signals dominate |
| Conservative PT thresholding | Control multiple weak noisy signals | Rank everything equally | Prefer whenever the scan is broad |
| Role-code sensitivity (PS vs PS+SS) | Test exposure-definition sensitivity | PS only | Standard+ |
| Reporter-type restriction (HCP only) | Reduce consumer-report noise | All reporters | Advanced+ |

---

## 5. Evidence ceiling reminder

No method combination in this family supports:

- incidence estimation
- absolute risk quantification
- definitive causal attribution
- prescribing or regulatory recommendations

All outputs stay within pharmacovigilance **signal and characterization** boundaries. See `evidence-hierarchy.md` for the tier labels that must accompany every result.
