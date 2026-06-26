# Clinical Trial Protocol Synopsis

**Platforms:** Claude · Openclaw · Codex
**Domain:** Clinical Research — Protocol Development

## Purpose

A protocol-synopsis drafting partner for sponsor and academic clinical-research teams. Turns an investigator concept, sponsor target product profile, or feasibility note into a structured DRAFT clinical-trial protocol synopsis aligned with ICH E6(R3) Good Clinical Practice, the ICH M11 Clinical electronic Structured Harmonised Protocol (CeSHaRP) template, ICH E9(R1) estimands, and CONSORT design discipline.

## When to Use

- Preparing a synopsis for a Phase 1 / 2 / 3 / 4 interventional study or a device pivotal / post-market study before the full protocol is drafted
- Aligning a study team on PICOT, primary and secondary endpoints, and ICH E9(R1) estimands
- Producing a draft synopsis for sponsor medical, biostatistics, regulatory, pharmacovigilance, and IRB / IEC review
- Standardizing the synopsis format across studies in a sponsor portfolio
- Preparing an academic-PI synopsis for grant submission or IRB feasibility review

## What It Does

**Phase 1: Intake**
1. Captures sponsor, role, target template (ICH M11 CeSHaRP, TransCelerate CPT, sponsor SOP, institution), target regions, regulatory pathway, and phase
2. Captures indication, mechanism of action, scientific rationale, prior clinical data, and nonclinical-data highlights
3. Captures intervention, comparator, background and prohibited concomitant therapy, rescue therapy
4. Captures PICOT, key inclusion / exclusion criteria, and special-population handling
5. Captures objectives, endpoints, and ICH E9(R1) estimand attributes
6. Captures design, randomization, blinding, stopping rules, interim analyses, DMC / DSMB intent
7. Captures sample-size assumptions, analysis populations, primary analysis method, missing-data handling, multiplicity-control strategy
8. Captures schedule of assessments outline, safety reporting plan, and regulatory / ethics considerations
9. Restates every fact with Confirmed / Assumed / Unknown tags and shows draft PICOT, Estimand Table, and sample size before drafting

**Phase 2: Drafting**
10. Drafts a 4–8 page synopsis with all sections in the Output Format
11. Builds the Estimand Table with all five ICH E9(R1) attributes per primary objective
12. Produces a Schedule of Assessments Outline, a Statistical Considerations block, and a Safety Reporting Plan
13. Flags first-in-human, pediatric-first, adaptive-design, biomarker-stratification, cross-border, and external-control concerns

**Phase 3: Review scaffolding**
14. Produces an Evidence Matrix, an Open-Questions list, a Regulatory / Ethics Flags block, and a sign-off block for sponsor medical, biostatistics, regulatory, pharmacovigilance, and IRB submission leads

## Output

A DRAFT synopsis with:

- Background and rationale with cited prior data
- PICOT statement
- Primary, secondary, and exploratory objectives and endpoints
- Estimand Table per primary objective
- Study design with design schematic
- Key inclusion / exclusion criteria and special-population handling
- Intervention, comparator, background / prohibited therapy, and rescue therapy
- Safety reporting plan (AE / SAE / SUSAR / AESI)
- Schedule of Assessments Outline
- Statistical considerations including sample size, analysis populations, primary analysis, missing-data handling, multiplicity control, and sensitivity analyses
- Ethics, consent, vulnerable-population, data-privacy, and trial-registration items
- Evidence Matrix and Unresolved-Questions list
- Regulatory / Ethics Flags block
- Sign-off block for sponsor reviewers

## Safety

This skill drafts a synopsis, **not** a final protocol. Every output is labeled **DRAFT — SPONSOR MEDICAL / BIOSTATISTICS / REGULATORY / IRB REVIEW REQUIRED**. The skill never finalizes a protocol, never makes a regulatory submission, never communicates with a regulator or IRB / IEC, never invents incidence rates or effect sizes, and never copies confidential investigator-brochure or TPP text verbatim. First-in-human, pediatric-first, vulnerable-population, adaptive-design, biomarker-stratification, cross-border, and external-control studies each trigger a dedicated flag. All sponsor, patient, and biomarker data are treated as confidential and are never pasted to external services.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
