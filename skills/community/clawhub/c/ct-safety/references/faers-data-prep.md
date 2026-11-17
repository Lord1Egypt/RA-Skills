# FAERS Data Preparation: Drug Normalization, Role-Code Filtering, De-duplication

> 中文摘要：FAERS 原始数据清洗三件套——药物名标准化（正则 + RxNorm/ATC/OHDSI 映射）、角色码过滤（仅保留 PS 主要怀疑药）、重复病例去重（patient + event + date）。这是所有 disproportionality 计算之前的强制前置步骤。
>
> **Adapted from**: `faers-multi-drug-soc-planner` + `active-comparator-single-soc-faers-safety-comparison` — AIPOCH, MIT License
> **Source**: https://github.com/aipoch/medical-research-skills
> **Migrated**: 2026-08-04 (into ct-safety)

---

## Why this matters

openFDA returns `patient.drug[].medicinalproduct` as free text submitted by the reporter. Without preparation you will:

- **undercount** exposure (brand names, misspellings, salt forms counted as different drugs);
- **overcount** signals (concomitant drugs treated as if they were the suspect drug);
- **inflate** cell counts (multiple versions of the same case counted repeatedly).

All three inflate or deflate the 2×2 table that PRR / ROR / IC / EBGM are computed from. Run this pipeline **before** any disproportionality step.

---

## Step 1 — Drug name normalization

### 1.1 Regex layer (cheap, first pass)

Normalize the raw `medicinalproduct` string:

| Operation | Example |
|---|---|
| Uppercase + trim + collapse whitespace | `" propranolol  hcl "` → `PROPRANOLOL HCL` |
| Strip dosage / strength / form | `METOPROLOL SUCCINATE ER 50 MG TAB` → `METOPROLOL SUCCINATE` |
| Strip salt / ester suffixes | `HCL`, `HYDROCHLORIDE`, `SUCCINATE`, `TARTRATE`, `MALEATE`, `SODIUM`, `MESYLATE` |
| Strip packaging noise | `(TABLET)`, `/ORAL`, `UNKNOWN`, `NOS` |
| Split combination products | `LISINOPRIL/HCTZ` → two exposure records, flag as combination |
| Map common misspellings | maintain an explicit alias table, never fuzzy-match silently |

> `ct-safety` already ships `references/drug_name_map.json` — extend that file rather than creating a parallel mapping.

### 1.2 Vocabulary layer (authoritative)

Map the cleaned string to a generic ingredient using, in order of preference:

1. **RxNorm** (`RxNav` REST API, free, no key) → `ingredient` / `IN` term
2. **ATC** code (WHO ATC index) → enables class-level grouping (needed for class-vs-class designs)
3. **OHDSI / ATHENA** concept ID → for cross-vocabulary work

**Rules**

- Always record both the raw string and the mapped ingredient — never discard the original (auditability).
- Report the mapping hit rate. If < 80% of cases map, the exposure definition is unreliable; report it as a limitation.
- Brand → generic mapping must be one-directional and logged.
- Class membership (for "beta-blockers", "sartans", …) must come from ATC, not from a name suffix. A suffix heuristic (`*olol`, `*sartan`) may be used as a *recall* aid but must be verified against ATC.

**Output**: a clean drug-indexed case file with case counts per normalized ingredient and per class.

---

## Step 2 — Role-code filtering

FAERS assigns each drug in a report a role:

| Code | Meaning | Default handling |
|---|---|---|
| `PS` | Primary suspect | **Retain** |
| `SS` | Secondary suspect | Exclude from primary analysis; re-include as sensitivity |
| `C` | Concomitant | Exclude |
| `I` | Interacting | Exclude from primary; consider separately for DDI questions |

**Rules**

1. The primary analysis retains `PS` only — this tightens the exposure definition and reduces confounding by co-medication.
2. Always state the exclusion explicitly in Methods, with the case count lost at this step.
3. Run a **role-code sensitivity analysis** (`PS` + `SS`) at Standard tier and above; report directional stability.
4. If retaining `PS` only drops an arm below n = 30, do not silently relax the rule — report the underpowered arm and offer widening the time window instead.

---

## Step 3 — Duplicate case removal

Spontaneous-report databases contain both *report versions* (follow-ups of the same case) and *true duplicates* (same event reported through multiple channels).

### 3.1 Version de-duplication (mandatory for raw FAERS)

Group by `caseid` and keep the record with the **latest** `caseversion` / `receiptdate`. openFDA's `safetyreportid` already collapses most versions, but raw quarterly files do not.

### 3.2 Probabilistic de-duplication (patient + event + date)

Within the remaining records, treat as duplicates records matching on the composite key:

```
key = (age_bucket, sex, country, reporter_type, event_pt_set, event_onset_date ± 7d, suspect_ingredient)
```

Practical guidance:

- Bucket age (e.g. 5-year bins) — exact age is often missing or inconsistent.
- Use the **set** of PTs, not the ordered list.
- Allow a ±7-day window on onset/receipt date.
- When a candidate duplicate pair disagrees on outcome seriousness, keep the more serious record.

### 3.3 Reporting requirement

Always produce a case-selection flowchart (CONSORT-style) with counts at every stage:

```
Raw records retrieved                    N = ...
  − non-PS role codes                    − ...
  − version duplicates (caseid)          − ...
  − probabilistic duplicates             − ...
  − missing key fields                   − ...
= Analysis set                           N = ...
```

---

## Step 4 — Post-preparation quality gate

| Gate | Threshold | If failed |
|---|---|---|
| Cases per exposure arm | n ≥ 30 | Flag underpowered; widen window or broaden regex |
| Normalization hit rate | ≥ 80% | Report as limitation; do not compare classes |
| Indication completeness | ≥ 20% | Complete-case sensitivity, or class-indication proxy |
| Duplicate removal rate | typically 5–20% | > 40% suggests a broken key — re-inspect before proceeding |

---

## Integration with ct-safety

| ct-safety component | Relation |
|---|---|
| `references/drug_name_map.json` | Extend with new aliases discovered during Step 1.1 |
| `scripts/faers_fetch.py` | Apply Steps 1–3 after fetch, before building the 2×2 table |
| Disproportionality step | Consumes the cleaned analysis set only |
| Report template | Must include the case-selection flowchart and the quality-gate table |

**Never** report PRR / ROR / IC / EBGM computed on unprepared raw counts.
