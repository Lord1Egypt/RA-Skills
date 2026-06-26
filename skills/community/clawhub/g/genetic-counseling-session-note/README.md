# Genetic Counseling Session Note Drafter

**Platforms:** Claude · Openclaw · Codex
**Domain:** Genetic Counseling
**Skill:** `genetic-counseling-session-note`

## Purpose

A clinical documentation assistant for board-certified genetic counselors (CGC, MS), CGC candidates, and supervising clinical geneticists. Converts session intake data into a structured, NSGC-aligned counseling note covering pre-test and post-test sessions — ready for licensed CGC review before entry into the medical record.

## When to Use

- When drafting a pre-test genetic counseling session note (test rationale, informed consent, risk assessment)
- When drafting a post-test session note (result disclosure, variant documentation, family cascade testing)
- When you need a structured pedigree narrative, risk quantification summary, or psychosocial assessment
- When documenting patient understanding and plan from a genetic counseling encounter
- When preparing a NSGC-aligned session note for EMR entry, billing, or supervisory review

## What It Does

**Phase 1: Intake**
1. Collects session identification (type, patient initials + case number, indication, date)
2. Gathers three-generation pedigree summary and relevant personal and family history; flags pedigree data gaps

**Phase 2: Risk Assessment**
3. Quantifies personal and reproductive risk using published estimates or empiric recurrence figures; labels all estimates PRELIMINARY

**Phase 3: Testing/Disclosure (Routing)**
- *Pre-test:* Documents test rationale, alternatives, and informed consent elements including GINA/insurance implications
- *Post-test:* Documents result type and HGVS notation, ClinGen/ACMG classification, and result disclosure narrative; applies VUS rule (never reclassifies VUS)

**Phase 4: Psychosocial and Educational Assessment**
5. Assesses emotional state, support system, and referrals; documents teach-back or stated patient understanding

**Phase 5: Plan and Assembly**
6. Documents follow-up plan, family testing recommendations, and outstanding items
7. Assembles a complete DRAFT session note with CGC Review Block

## Safety Boundaries

- Never uses full patient names, dates of birth, or MRNs — initials + case number only
- All risk estimates are labeled PRELIMINARY and require licensed CGC verification
- Never classifies or reclassifies VUS results — documents lab classification and flags for CGC review
- Informed consent must be confirmed before testing; missing consent is flagged with CONSENT FLAG
- No family member names — relatives described by relationship only
- All output is a DRAFT requiring licensed CGC review before EMR entry or patient release
- Includes HIPAA reminder for AI tool usage in clinical environments

## Notes

This skill is intended for genetic counseling professionals working within a licensed clinical framework. It does not replace clinical judgment, licensed CGC supervision, or institutional compliance review. All risk figures and diagnostic interpretations must be verified by a licensed CGC or supervising clinical geneticist before any clinical use.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
