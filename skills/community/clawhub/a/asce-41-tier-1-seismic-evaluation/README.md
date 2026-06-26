# ASCE 41 Tier 1 Seismic Evaluation

**Platforms:** Claude · Openclaw · Codex
**Domain:** Structural Engineering / Existing-Building Seismic Evaluation

## Purpose

A conversational guide for licensed structural engineers and reviewing engineers preparing a Tier 1 deficiency-based seismic evaluation under **ASCE/SEI 41-23** ("Seismic Evaluation and Retrofit of Existing Buildings"). Walks scope and Performance Objective intake, FEMA Common Building Type selection, BSE-1E / BSE-2E seismicity look-up, and execution of the Basic / Structural / Nonstructural / Foundation-Geologic checklists in Chapter 17 and Appendix C, then produces a peer-reviewable Tier 1 evaluation memo with a clear recommendation either to stop, to proceed to Tier 2, or to proceed directly to Tier 3.

## When to Use

- Pre-purchase / pre-lease seismic evaluation of an existing building (PML / SEL reports often start with Tier 1 screening, even though PML/SEL itself is governed by ASTM E2026/E2557)
- Mandatory municipal evaluation programs (e.g., soft-story ordinances, URM ordinances) that accept ASCE 41 Tier 1 as the screening basis
- Voluntary retrofit project scoping where the engineer needs a deficiency list to size Tier 2 / Tier 3 effort
- ASCE 7-22 / IBC 2024 change-of-occupancy or substantial-alteration triggers that require seismic evaluation of the existing structure
- Insurance, lender, or owner due diligence requiring a defensible deficiency list before committing capital

## What It Does

1. Captures project scope: building address, owner / client, evaluating engineer (PE / SE), reviewing engineer, evaluation date, drawings and documents available, site visit posture
2. Confirms the **Performance Objective** — Basic Performance Objective for Existing Buildings (BPOE), Basic Performance Objective Equivalent to New Building Standards (BPON), or a project-specific objective — and the associated Structural Performance Level (Life Safety / Immediate Occupancy / Collapse Prevention) and Hazard Levels (BSE-1E, BSE-2E)
3. Looks up site seismicity (mapped acceleration parameters, Site Class, BSE-1E and BSE-2E S<sub>XS</sub> and S<sub>X1</sub>) and confirms whether the building is in a Level of Seismicity that **permits** Tier 1 use
4. Selects the FEMA Common Building Type from the 17-row table (W1, W1a, W2, S1, S2, S3, S4, S5, C1, C2, C3, PC1, PC2, RM1, RM2, URM, URMA), records building height in stories, and flags any building that exceeds Tier 1 height limits for its type
5. Walks the **Basic Configuration Checklist**, the **Structural Checklist** for the selected building type, the **Nonstructural Checklist** at the appropriate Nonstructural Performance Level, and the **Foundation and Geologic Site Hazards Checklist**
6. For every statement, records **C** (Compliant), **NC** (Non-Compliant), **U** (Unknown), or **N/A** (Not Applicable), with a one-line justification and a reference to the controlling section of ASCE 41-23
7. Aggregates non-compliant and unknown statements into a deficiency list, ranks them by potential life-safety impact, and recommends Tier 2 deficiency-based evaluation, Tier 3 systematic evaluation, or no further evaluation, with reasoning
8. Emits a signed-PE memo with cover page, scope, basis of evaluation, completed checklists, deficiency list, recommendation, and a "What This Memo Is Not" disclaimer

## Note

This skill drafts the Tier 1 evaluation memo. It does **not** replace engineering judgment, a site visit, or the responsible PE / SE's signed and sealed determination, and it does not perform Tier 2 quick-check calculations or Tier 3 nonlinear analyses. Buildings outside the height and seismicity bounds for Tier 1 must be evaluated under Tier 2 or Tier 3 — the skill flags this and stops. URM and pre-Northridge steel-moment-frame buildings carry known hazards that may warrant going directly to Tier 3. The skill assumes the engineer has lawful access to the building and to drawings; never paste owner contact PII, security-sensitive floor plans, or confidential lease terms into examples.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
