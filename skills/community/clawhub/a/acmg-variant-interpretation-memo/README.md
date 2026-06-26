# ACMG/AMP Variant Interpretation Memo Drafter

**Platforms:** Claude · Openclaw · Codex
**Domain:** Clinical Genomics

## Purpose

Drafts a CAP / CLIA-style variant interpretation memo for a single **germline sequence variant** aligned to the **ACMG/AMP 2015** standards for the interpretation of sequence variants (Richards et al., *Genet Med* 2015) and the **ClinGen Sequence Variant Interpretation (SVI) Working Group** refinements that supersede or modify the original 2015 strengths (PVS1 decision tree, PS1 / PM5 splicing, PS3 / BS3 functional, PP1 / BS4 segregation, PP3 / BP4 computational, PP4 phenotype-specificity, PM2_Supporting). The skill walks proband and pedigree intake, HGVS nomenclature validation with a named transcript and reference assembly, gnomAD frequency look-up, computational meta-predictor tabulation, segregation and de novo evidence, functional and case-level evidence, explicit application of every triggered ACMG/AMP rule with a one-sentence justification, and the final classification — Pathogenic / Likely Pathogenic / Uncertain Significance (VUS) / Likely Benign / Benign — under the ACMG/AMP combining rules. The output is a DRAFT memo, an evidence ledger, a ClinVar-submission-ready record, recommended downstream actions, and a laboratory-director and clinical-genetic-counselor review-and-sign-out block.

## When to Use

- Variant scientist or laboratory genetic counselor drafting the variant interpretation supporting a CAP / CLIA-style clinical report (diagnostic, carrier, pre-symptomatic, prenatal, paediatric, oncology germline)
- Reanalysis of a previously reported variant when ClinGen VCEP guidance, ClinVar conflicts, gnomAD v4.x updates, SpliceAI calibration, AlphaMissense calibration, or new family data become available
- Resolution of a ClinVar conflicting-interpretation entry where the laboratory must publish its rationale
- Tumour-germline paired report where a candidate germline variant must be classified separately from the somatic call
- Pre-submission classification ahead of ClinVar submission, ELSI committee discussion, or laboratory-director review
- Training and audit of variant-classification consistency across analysts on a clinical-laboratory team

## What It Does

**Phase 1: Case and Assignment Intake**
1. Captures pseudonymised proband identifier, testing indication, HPO-coded phenotype, family history with named relatives and affected status, consanguinity status, self-reported ancestry (for frequency comparison only), ordering clinician, performing laboratory, assay type (Sanger / panel / exome / genome / RNA-seq), reference assembly (GRCh37 or GRCh38), and transcript source (MANE Select / MANE Plus Clinical / laboratory canonical)

**Phase 2: Variant Nomenclature Validation**
2. Validates the HGVS gene-coding-protein triple with the named transcript and reference assembly, captures alternate-transcript HGVS where clinically relevant, defines structural-variant breakpoints where applicable, captures mosaic fraction where called, and records the RefSeq / MANE / Ensembl cross-reference

**Phase 3: Gene and Disease Context**
3. Identifies the named MIM, mode of inheritance (AD / AR / XLD / XLR / mitochondrial / digenic / somatic / mosaic), ClinGen Gene-Disease Validity classification, penetrance class, ClinGen VCEP availability and version, and prior ClinVar interpretations (submitters and dates)

**Phase 4: Evidence Gathering**
4. Tabulates gnomAD frequency by population with the SVI PM2_Supporting refinement, computational meta-predictors (REVEL, SpliceAI, AlphaMissense, CADD) with the SVI PP3 / BP4 calibrated thresholds, functional studies under the SVI PS3 / BS3 evidence-strength rubric, splicing evidence under the SVI splicing-subgroup framework (PVS1 / PS1 / PM5 / PP3 / BP4 / BP7), segregation under SVI PP1 / BS4, case-level and de novo confirmation, and phenotype-specificity under PP4

**Phase 5: ACMG/AMP Rule Application**
5. Names every triggered rule — PVS1, PS1–PS4, PM1–PM6, PP1–PP5, BA1, BS1–BS4, BP1–BP7 — with the SVI evidence-strength modifier where applicable and a one-sentence justification per rule citing the evidence record

**Phase 6: Final Classification**
6. Applies the ACMG/AMP combining rules to assign Pathogenic / Likely Pathogenic / Uncertain Significance (VUS) / Likely Benign / Benign; reconciles against any ClinGen VCEP-applied classification; captures any criteria-conflict resolution

**Phase 7: Memo Assembly**
7. Produces a DRAFT variant-interpretation memo with classification verdict, evidence ledger, ClinVar-submission-ready record, recommended downstream actions (segregation testing, functional follow-up, RNA confirmation, parental confirmation, reanalysis interval, genetic-counseling referral), and a laboratory-director and clinical-genetic-counselor review-and-sign-out block

## Output

A DRAFT variant-interpretation package with:
- Variant-interpretation memo (case identifier, gene, HGVS triple, transcript, assembly, classification verdict, evidence ledger, rule-by-rule justification, recommended downstream actions, reanalysis interval)
- Evidence ledger (gnomAD frequency, computational predictors with calibrated thresholds, functional studies, splicing evidence, segregation, case-level data, phenotype-specificity)
- ClinVar-submission-ready record (variant nomenclature, classification, criteria applied, condition, evidence summary)
- ACMG/AMP rule trace (each triggered rule with SVI evidence-strength modifier and one-sentence justification)
- Recommended downstream actions (segregation testing, functional follow-up, RNA confirmation, parental confirmation, reanalysis interval, genetic-counseling referral, ACMG SF-list secondary-findings scope confirmation where relevant)
- Laboratory-director and clinical-genetic-counselor review-and-sign-out block
- Open-questions / unresolved-information list

## Notes

This skill **drafts** the variant-interpretation memo to support — never replace — the certifying laboratory director's review and sign-out. The skill does **not** issue a clinical report, does **not** substitute for a board-certified clinical molecular geneticist (ABMGG) / clinical molecular pathologist (ABP-MGP) / laboratory genetic counselor, does **not** perform primary variant calling or assay validation, does **not** return ACMG SF-list secondary findings without explicit scope confirmation, does **not** perform tumour somatic variant tier-classification (which uses the AMP/ASCO/CAP 2017 framework, a separate skill), and does **not** replace patient-facing genetic counseling. The skill is intended for use **only** by qualified clinical-laboratory personnel. Variant interpretations evolve as evidence accrues; the skill records a reanalysis interval and the version of every database / predictor consulted.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
