# FAERS Comparative Study Design (Multi-Drug, Single-SOC)

> 中文摘要：多药物 / 单 SOC 的 FAERS 对比药物警戒研究设计方法论——四档工作量配置（Lite / Standard / Advanced / Publication+）、七类研究样式、分步工作流、图表计划与发表升级路径。补齐 ct-safety 原本只做"单药信号检测"的缺口。
>
> **Adapted from**: `faers-multi-drug-soc-planner` — AIPOCH, MIT License
> **Source**: https://github.com/aipoch/medical-research-skills
> **Migrated**: 2026-08-04 (into ct-safety)

---

## 1. Scope and Trigger

Use this reference when the user asks for a **comparison** rather than a single-drug scan:

- "compare drug X vs drug Y adverse events"
- "FAERS safety comparison across a drug class"
- "within-class head-to-head pharmacovigilance"
- "active-comparator restricted disproportionality"
- "publishable FAERS comparative paper"

`ct-safety`'s default pipeline (`scripts/faers_fetch.py` → disproportionality → report) computes PRR / ROR / IC / EBGM for **one drug against the whole database background**. That is a *signal-detection* design. Everything below concerns *comparative* designs, where the denominator is a deliberately chosen **active comparator** instead of the full FAERS background.

---

## 2. Study Styles

| Style | Design | Typical question |
|---|---|---|
| A | Drug class vs active comparator class | Beta-blockers vs ACE inhibitors for psychiatric disorders |
| B | Within-class head-to-head | Propranolol vs atenolol vs metoprolol |
| C | Single SOC + multi-PT deepening | SOC-level signal, then 5–12 clinically meaningful PTs |
| D | Active-comparator restricted disproportionality | Indication-restricted confounding control |
| E | Pharmacologic-property heterogeneity | Lipophilic vs hydrophilic, selective vs non-selective |
| F | Sensitivity-strengthened design | Post hoc indication adjustment, comparator robustness |
| G | Integrated publication design | Full pipeline: subgroup + PT + sensitivity |

**Selection rules**

1. Pick the simplest style that answers the core question.
2. Do not stack advanced layers unless the chosen configuration (§3) explicitly supports them.
3. If a style depends on a data field not declared available (indication, onset date, reporter type), drop it.
4. A minimal executable plan should normally use **one** primary style.
5. When a second style is added, label it explicitly **necessary / recommended / optional**.

---

## 3. Four Workload Configurations

Always present all four, then recommend one.

| Config | Goal | Timeline | Core content | Target |
|---|---|---|---|---|
| **Lite** | Crude + adjusted ROR, one SOC, one comparator | 2–4 wk | One extraction, one exposure definition, one signal route, ≤1 characterization branch; internal consistency check only; 4–5 figures | Pilot / feasibility |
| **Standard** | Conventional publishable FAERS paper | 5–8 wk (1–2 mo) | Lite + stronger restriction logic, PT deepening, one subgroup/onset/seriousness/label-context branch, sensitivity framing; alternate-filter robustness; 7–8 figures | Mid-tier journal |
| **Advanced** | Competitive journal, deeper defensibility | 8–13 wk (2–3 mo) | Standard + pharmacologic subgroup, multi-metric / multi-restriction robustness, tighter claim-boundary handling; 8–10 figures | Mid-to-high tier PV journal |
| **Publication+** | Maximum reviewer defensibility | 12–18 wk (3–6 mo) | Advanced + alternate comparator robustness, endpoint compression, richer evidence labeling, integrated evidence schematic; 10–12 figures | High-ambition PV journal |

**Decision tree**

```
Results needed in < 1 month, FAERS only?        → Lite (Standard if output quality is critical)
Conventional FAERS safety paper?                → Standard (Advanced if timeline allows)
Wants richer robustness / reviewer-proofing?    → Advanced
Wants subgroup architecture / high-impact?      → Publication+
Unspecified?                                    → Standard primary, Lite minimum, Advanced upgrade path
```

For each configuration state: goal, required data, major modules, workload, figure set, strengths, weaknesses.

---

## 4. Dependency Consistency Rules (hard constraints)

**Core principle** — a downstream step may appear **only if its prerequisite data source, evidence layer, and method family are already explicitly included in the same configuration.**

1. Comparator-dependent analyses require a configuration that explicitly declares a comparator restriction or class comparison.
2. A FAERS-only signal-detection configuration is limited to: exposure definition, signal detection, signal ranking/compression, declared subgroup/onset/seriousness description, limited robustness checks. It must **not** introduce incidence estimation, causal claims, clinical/regulatory recommendations, or unsupported mechanistic interpretation.
3. The **Minimal Executable Version** inherits only Lite modules, unless explicitly stated to be an upgraded variant.
4. Every module added in the **Publication Upgrade** path must be labeled: newly introduced / why added / what new evidence tier it enables.

**Self-check before output**

- Does any step require a comparator, subgroup field, or onset variable never declared earlier?
- Does any signal-selection step assume evidence absent from the configuration?
- Does the minimal version contain Advanced/Publication+-only methods?
- Are all endpoint formulas valid given the declared inputs?

Any "yes" → revise before output.

**Intersection formula** — every endpoint-selection step must declare its exact set logic and never switch silently:

```
suspect-drug cases
suspect-drug cases ∩ fixed SOC/PT family
suspect-drug cases ∩ fixed SOC/PT family ∩ active-comparator restriction
suspect-drug cases ∩ signal-positive PTs ∩ robustness-stable PTs
```

---

## 5. Analytical Modules

### 5.1 Data access
- openFDA API (`drug/event.json`) or FAERS quarterly ASCII downloads.
- Declare the time window (e.g. 2013–present).
- Justify openFDA vs raw FAERS by preprocessing needs (openFDA de-duplicates only partially).

### 5.2 Data quality gate (apply **before** analysis)
| Check | Threshold | Action if failed |
|---|---|---|
| Minimum cases per drug arm | n ≥ 30 | Flag underpowered; widen time window or broaden the drug-name regex |
| API availability | openFDA reachable | Fall back to FAERS quarterly ASCII (`https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html`) |
| Indication completeness | ≥ 20% of cases | Note in limitations; report complete cases only as sensitivity, or use class indication as proxy. Sparse indication is **not** grounds for abandoning comparator restriction |
| Zero-case PT | any arm = 0 | Unanalyzable for that PT; drop from primary table, keep in supplementary |

### 5.3 Comparator definition
- Active comparator requires a **shared therapeutic indication**; justify by indication overlap.
- Exclude classes with obvious confounding concern; flag weak overlap explicitly.
- Output a comparator-group definition table with justification.

### 5.4 Outcome definition
- One primary MedDRA SOC (optionally one adjacent SOC).
- 5–12 clinically meaningful PTs within the SOC; broad SOC signal first, PT deepening second.
- Output an SOC/PT table with MedDRA codes.

### 5.5 Effect estimation
| Step | Method | Notes |
|---|---|---|
| Crude | 2×2 per drug per outcome; ROR = (a/b)/(c/d); 95% CI by Woolf | Primary signal rule: lower CI > 1.0; always report the CI |
| Adjusted | Logistic regression `outcome ~ drug_group + covariates` | Covariates: age, sex, weight, indication-relevant comorbidities; reference = active comparator. Report aROR + 95% CI and compare with crude |
| Sparse cells | Firth penalized logistic | Or explicitly note instability |
| Within-class head-to-head | Pairwise logistic, one drug as reference | For ≥ 4 pairwise comparisons apply Bonferroni or FDR; report uncorrected and corrected side by side |
| Pharmacologic subgroup (Advanced+) | Compare aROR distributions across property subgroups | Hypothesis-supporting only, never causal proof |

### 5.6 Sensitivity analysis (Standard+)
- Post hoc adjustment for non-primary indications.
- Alternate comparator swap → directional stability.
- Role-code sensitivity: re-include `SS` cases and compare.
- Reporter-type restriction (HCP-only).

---

## 6. Figure and Table Plan

| Item | Content |
|---|---|
| Fig 1 | Study design schematic |
| Fig 2 | Case selection flowchart (CONSORT-style) |
| Fig 3 | SOC-level forest plot (aROR per drug vs comparator) |
| Fig 4 | PT-level forest plot |
| Fig 5 | Within-class head-to-head figure |
| Fig 6 | Time-to-onset distribution per drug group (violin / box) |
| Fig 7 | Sensitivity comparison (primary vs sensitivity aROR) |
| Table 1 | Drug normalization + comparator definition |
| Table 2 | Descriptive case characteristics |
| Table 3 | Crude + adjusted ROR summary (SOC + PT) |
| Table 4 | Sensitivity analysis summary |

---

## 7. Risk Review (always output)

- **Strongest component**: active-comparator restriction + logistic adjustment.
- **Most assumption-dependent**: completeness of FAERS indication fields.
- **Most likely false-positive source**: multiple PT comparisons without multiplicity correction.
- **Easiest to overinterpret**: ROR read as "risk" rather than "reporting proportion difference".
- **Expected reviewer criticisms**: underreporting bias, notoriety bias, residual confounding by indication, drug-name misclassification, absence of population-based validation.
- **Revision path if findings fail**: switch to PT-level primary outcome, restrict to HCP reports, expand covariates.

---

## 8. Minimal Executable Version (2–3 weeks)

openFDA only · one drug class + one active comparator · one SOC · primary-suspect restriction · drug normalization · crude + adjusted ROR · 3–5 key PTs · one summary table + one forest plot.

## 9. Publication Upgrade Path

| Addition | Gain | Effort |
|---|---|---|
| Second active comparator | High (comparator robustness) | Low |
| Within-class head-to-head | High (heterogeneity story) | Low–Medium |
| Time-to-onset summary | Medium | Low |
| Pharmacologic subgroup comparison | Medium (mechanistic framing) | Medium |
| Post hoc sensitivity analysis | High (reviewer defense) | Low |
| Expand PT architecture to 10–12 | Medium | Low |
| HCP-only reporter sensitivity | Medium | Low |

---

## 10. Hard Rules

1. Never output a single generic plan — always present all four configurations, then recommend one with justification.
2. Always separate **necessary** from **optional** modules.
3. Always distinguish disproportionality evidence, adjusted-signal support, heterogeneity evidence, and sensitivity support (see `evidence-hierarchy.md`).
4. Never present FAERS signals as incidence estimates.
5. Never claim causality from disproportionality alone.
6. Do not force an all-SOC sweep when the user wants one SOC.
7. Always flag weak comparator indication overlap.
8. Always include the drug-normalization step (see `faers-data-prep.md`).
9. If the user gives limited detail, infer a reasonable default design and state the assumptions explicitly.
