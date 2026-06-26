---
name: failure-analysis-report
description: >
  Use this skill when a licensed forensic engineer (PE/SE/ME/EE), expert witness, or
  engineering consultant needs to draft a failure analysis report for an insurance claim,
  litigation matter, or safety investigation. Covers scene documentation, physical evidence
  inventory, applicable standards at time of construction, failure mode hypothesis screening,
  root cause determination, and expert opinion. Produces a DRAFT for licensed PE review
  before delivery to any attorney, insurer, or regulatory body.
---

# Failure Analysis Report

Structures an engineering failure investigation into a defensible, court-ready failure analysis report. Covers every element from investigation scope and scene methodology through root cause determination and expert opinion, producing a DRAFT for licensed PE stamp and signature before delivery.

---

## Before You Start

This skill produces **DRAFT documentation only**. All content requires review, signature, and professional engineer stamp by a licensed PE before delivery to any attorney, insurer, court, or regulatory body.

**Critical rule — applicable standards:** The skill always uses standards, codes, and editions that were **in effect at the time of construction, manufacture, or installation** — not current editions. This is a hard requirement. Flag any case where the applicable edition is unknown as **[STANDARDS DATE UNKNOWN — PE TO CONFIRM]**.

**Data integrity rule:** Never fabricate measurement values, test results, laboratory data, or failure observations. All quantitative findings are entered by the engineer. If a value is unavailable, mark it **[DATA NOT AVAILABLE — PE TO PROVIDE]**.

---

## Flow

### Phase 1 — Investigation Identification and Scope

Ask one question at a time. Collect:
1. Case or file number (no personally identifying information for claimants)
2. Investigation date(s) and report preparation date
3. Client name and retention type (insurer / plaintiff counsel / defense counsel / regulatory body / owner)
4. Incident date, location (city/state/type of facility — no street addresses in the body unless the PE specifically provides them)
5. Failure type — select one primary type to set routing in Phase 2:
   - **A. Structural** (building, foundation, retaining wall, floor/ceiling system, roof)
   - **B. Mechanical** (machinery, equipment, piping, vehicle or transportation)
   - **C. Fire Origin and Cause** (building fire, vehicle fire, equipment fire)
   - **D. Electrical** (wiring, panels, transformers, electrical equipment)
   - **E. Product / Consumer or Industrial Product** (manufacturing defect, design defect, failure in service)
6. Brief incident description (as reported by client — label **[AS REPORTED — NOT VERIFIED]**)
7. Scope limitations (areas not accessed, evidence not available, testing not performed)

---

### Phase 2 — Scene Documentation Methodology

Collect the documentation approach used during the investigation:

- **Site access:** Date(s) of site visit, who accompanied the engineer, any access restrictions
- **Documentation method:** Photography (still / video / 3D laser scan / drone), sketches, measurements
- **Evidence preservation protocol:** Any evidence tagged, sampled, or collected for laboratory analysis
- **Chain-of-custody status:** Evidence retained by PE / returned to owner / transferred to lab — flag any gaps as **[CHAIN OF CUSTODY GAP — DOCUMENT]**
- **Destructive testing notice:** If any destructive examination was performed, document that all parties were notified or waived notice

---

### Phase 3 — Physical Evidence Inventory

For each piece of physical evidence or observed condition, collect:

| Item # | Description | Location (as found) | Condition | Disposition (retained / photographed / released) |
|--------|-------------|---------------------|-----------|---------------------------------------------------|
| | | | | |

Flag any evidence that was altered, missing, or unavailable as **[EVIDENCE CONDITION FLAG — DOCUMENT IN LIMITATIONS]**.

---

### Phase 4 — Applicable Standards and Codes

Collect or confirm the standards in effect **at the time of construction, manufacture, or installation**:

| Standard / Code | Applicable Edition (at time of construction) | Source |
|-----------------|---------------------------------------------|--------|
| (e.g., IBC, ASCE 7, NFPA 70, ASTM, UL, ISO) | (e.g., IBC 2012, not IBC 2024) | (construction permit / date of manufacture / product listing) |

**Rule:** If the applicable edition cannot be confirmed, mark it **[STANDARDS DATE UNKNOWN — PE TO CONFIRM]**. Never substitute a current edition for an unknown historical edition without explicit PE direction.

Add a note if current standards are referenced for comparison only: **[CURRENT EDITION — FOR COMPARISON ONLY; NOT THE APPLICABLE STANDARD]**.

---

### Phase 5 — Failure Mode Hypothesis Screening

Generate 2–5 failure mode hypotheses based on the investigation findings. For each hypothesis:

| # | Failure Mode Hypothesis | Supporting Evidence | Contradicting Evidence | Status |
|---|------------------------|---------------------|----------------------|--------|
| 1 | | | | Consistent / Inconsistent / Indeterminate |
| 2 | | | | |
| … | | | | |

Route by failure type for domain-specific hypothesis framing:

**A. Structural:** Consider overload, material defect, design deficiency, construction defect, maintenance neglect, environmental deterioration, improper modification.

**B. Mechanical:** Consider fatigue fracture, overload, corrosion/erosion, improper assembly, maintenance neglect, material defect, design deficiency, misuse or abuse.

**C. Fire:** Apply NFPA 921 scientific method. Consider accidental (electrical, mechanical, chemical, open flame, smoking) vs. incendiary vs. natural (lightning). Each hypothesis must be evaluated by physical evidence — never assume incendiary without positive evidence.

**D. Electrical:** Consider overcurrent, insulation breakdown, arcing (series / parallel), connection failure, overvoltage, ground fault, equipment malfunction, improper installation.

**E. Product:** Consider manufacturing defect, design defect, failure to warn, misuse, post-sale modification, end-of-service-life failure.

---

### Phase 6 — Root Cause Determination

Based on Phase 5 screening, state the most probable cause:

**Most probable root cause:** [State clearly and specifically]

**Basis:** [List the evidence that supports this determination]

**Exclusions:** [List hypotheses eliminated and why]

**Degree of certainty:** Definitive / More probable than not / Indeterminate — explain basis for each.

If certainty is indeterminate, document what additional investigation, testing, or evidence would be needed to reach a conclusion. Label the section **[ROOT CAUSE — INDETERMINATE — SEE ADDITIONAL INVESTIGATION NEEDED]**.

---

### Phase 7 — Expert Opinion

Collect the expert opinion from the PE. Draft using the following structure:

> "Based on my investigation, analysis of the physical evidence, review of applicable standards in effect at the time of [construction/manufacture], and my professional training and experience as a licensed [discipline] engineer, it is my professional opinion that [most probable root cause statement]. This opinion is stated to a [reasonable degree of engineering certainty / more probable than not] standard."

Label the entire opinion section: **[DRAFT EXPERT OPINION — PE TO REVIEW, REVISE, AND ADOPT AS THEIR OWN]**

The PE must adopt this language in their own words. This draft is a structural aid, not a ready-to-sign opinion.

---

### Phase 8 — Limitations Statement

Include a standard limitations statement:

- Investigation was limited to the areas, evidence, and time described in this report
- Opinions are based on information available at the time of this report
- Additional evidence or testing may modify the conclusions
- This report was prepared in anticipation of litigation and may be subject to work-product protection (if applicable — PE to confirm with retaining counsel)

Add any case-specific limitations identified during the investigation.

---

### Phase 9 — DRAFT Report Assembly

Compile all phases into the following structured report:

```
FAILURE ANALYSIS REPORT — DRAFT
Case / File No.: [From Phase 1]
Report Date: [Phase 1]
Incident Date: [Phase 1]
Prepared for: [Client name and retention type]
Prepared by: [PE name, discipline, license no. — PE TO COMPLETE]

1. EXECUTIVE SUMMARY
   [2–4 sentences: incident description, investigation scope, most probable root cause]
   DRAFT — FOR PE REVIEW ONLY

2. BACKGROUND AND SCOPE
   [Incident description — AS REPORTED — NOT VERIFIED]
   [Scope and limitations from Phase 1]

3. SCENE DOCUMENTATION METHODOLOGY
   [From Phase 2]

4. PHYSICAL EVIDENCE INVENTORY
   [Table from Phase 3]
   [Chain-of-custody flags]

5. APPLICABLE STANDARDS AND CODES
   [Table from Phase 4]
   [Standards-at-time-of-construction notation]

6. FAILURE MODE HYPOTHESIS SCREENING
   [Table from Phase 5 with routing-specific hypotheses]

7. ROOT CAUSE DETERMINATION
   [From Phase 6]
   [Basis and exclusions]

8. EXPERT OPINION
   [DRAFT text from Phase 7]
   DRAFT EXPERT OPINION — PE TO REVIEW, REVISE, AND ADOPT AS THEIR OWN

9. LIMITATIONS
   [From Phase 8]

APPENDICES
   Appendix A: Photographs (referenced by item number)
   Appendix B: Physical evidence inventory (expanded)
   Appendix C: Documents and records reviewed
   Appendix D: Curriculum vitae of PE

─────────────────────────────────────────
DRAFT — FOR LICENSED PE REVIEW ONLY
This document is not finalized and must not be delivered to any attorney, insurer,
court, or regulatory body until reviewed, revised, and stamped by a licensed
Professional Engineer (PE).

Reviewing PE: _________________________ License No.: _______________ State: ____
Discipline: ___________________________ Stamp: ______________________________
Signature: ____________________________ Date: ________________________________
─────────────────────────────────────────
```

Present the complete DRAFT and list any open items or flags for PE attention.

---

## Key Rules

- **Standards at time of construction is a hard rule.** Never apply a current code edition to a historical project without explicit PE direction. Always confirm the applicable edition.
- **No fabricated data.** All measurements, test results, and observations come from the engineer. If a value is missing, flag it.
- **Fire origin investigations must follow NFPA 921.** Never state incendiary cause without positive physical evidence. Incendiary is a conclusion of last resort after all accidental hypotheses are eliminated.
- **Expert opinion is always DRAFT.** The PE must adopt, revise, and sign the opinion in their own professional capacity.
- **Chain of custody:** Any gap in chain of custody must be documented in the limitations section — it may affect admissibility.
- **Work-product privilege:** Remind the PE to confirm with retaining counsel whether the report is privileged before it is transmitted.

---

## Output Format

The final output is a single structured DRAFT report (as defined in Phase 9) plus:
- A numbered open-items list of any flags, data gaps, or indeterminate conclusions requiring PE attention
- A note confirming the report is DRAFT and must not be delivered until PE review and stamp

---

## Feedback

If the user expresses an unmet need, a workflow gap, or dissatisfaction with the skill, surface the contribution link:
[Open an issue on GitHub](https://github.com/archlab-space/Open-Skill-Hub/issues)
