# DPIA Drafter

**Platforms:** Claude · Openclaw · Codex
**Domain:** Privacy / Data Protection

## Purpose

Drafts a GDPR Article 35 Data Protection Impact Assessment (DPIA) for a single processing activity that is likely to result in a high risk to natural persons. Aligns the draft to the European Data Protection Board (EDPB) harmonised DPIA template V1.0 (adopted 10 March 2026, public consultation 14 April 2026) — Section 0 identification, Section 1 systematic description, Section 2 necessity / proportionality / compliance tables, Section 3 risk register and mitigation plan, Section 4 stakeholder views and DPO opinion — and produces a DRAFT DPIA with an open-questions list and an Article 36 prior-consultation recommendation. The output supports — never replaces — the DPO's Article 35(2) opinion and the controller's sign-off.

## When to Use

- A new product, feature, vendor, or data flow that processes personal data in a way likely to be high-risk
- A material change to an existing processing activity already documented in the Records of Processing Activities (RoPA)
- A periodic DPIA review (typical cadence: annual or on material change)
- Onboarding a new sub-processor in a sensitive context
- Roll-out of profiling, automated decision-making, biometrics, large-scale monitoring, generative-AI features, or processing involving children, employees, patients, or asylum seekers
- Preparation for a supervisory-authority audit, prior consultation under Article 36, or breach-readiness review
- A privacy-by-design checkpoint before architecture freeze

## What It Does

**Phase 1: Threshold and Scoping**
1. Walks the WP29 / EDPB nine-criteria test and any Article 35(4) supervisory-authority blacklist to confirm a DPIA is required, and documents the decision either way
2. Captures lead supervisory authority, controller(s), joint controllers, processor(s), sub-processor(s), DPO contact, DPIA owner, DPIA team, processing internal name, and trigger

**Phase 2: Section 1 — Systematic Description**
3. Walks each distinct purpose with Article 6(1) lawful basis, Article 9(2) condition where applicable, and a legitimate-interest-assessment reference where applicable
4. Builds a data inventory by element with source, subject category, volume, retention, and mandatory / optional status
5. Maps the data lifecycle (collection → use → storage → sharing → transfer → deletion) with location, encryption, and access roles
6. Captures recipients, international transfers, Article 28 contract references, and Article 44–49 transfer mechanism with transfer-impact-assessment references
7. Captures supporting assets and technical architecture

**Phase 3: Section 2 — Necessity, Proportionality, Compliance**
8. Marks each purpose Pass / Concern / Fail on adequacy, minimisation, retention, and proportionality
9. Walks five compliance tables — Article 5 principles, Articles 12–22 data-subject rights, Article 28 processor relationships, Article 25 privacy by design / by default, Article 32 security of processing — with implementation summary and evidence per row

**Phase 4: Section 3 — Risk Assessment**
10. Frames risks as harms to natural persons across nine risk families (illegitimate access, unwanted modification, data loss, unlawful disclosure, loss of control, discrimination, re-identification, physical / psychological harm, material harm)
11. Scores each risk on a 1–4 likelihood × 1–4 severity scale with rationale, producing an inherent rating (Low / Medium / High / Very High)
12. Builds a mitigation plan with owner, due date, and evidence reference, then re-scores residual likelihood × severity
13. Maps the highest residual risk to an Article 36 prior-consultation determination

**Phase 5: Section 4 — Stakeholder Views, DPO Opinion, Sign-off**
14. Captures Article 35(9) data-subject views and works-council consultation where applicable
15. Records the DPO opinion under Article 35(2) — including any disagreement and controller justification
16. Prepares an unsigned sign-off block for DPO and controller signature

**Phase 6: Draft Output**
17. Produces the DRAFT DPIA in the EDPB section structure with explicit Pass / Concern / Fail / Open verdicts, a visible Appendix A open-questions list, an evidence index, and the mandatory review banner

## Output

A DRAFT DPIA aligned to the EDPB harmonised template, with a complete risk register (inherent rating, mitigation, residual rating), a prior-consultation determination under Article 36, an open-questions appendix, an evidence index, and a verbatim review banner labelling the document DRAFT — FOR DPO REVIEW.

## Notes

This skill **drafts** a DPIA to support — never replace — the DPO's Article 35(2) opinion and the controller's sign-off. The skill does not opine on whether a specific processing operation is lawful, does not opine on supervisory-authority approval outcomes, does not opine on fine exposure or litigation outcomes, does not request data-subject identifiers, and does not echo raw personal data into the draft. The skill applies the EDPB harmonised template by default and substitutes a binding national template (e.g. CNIL PIA, ICO DPIA, Garante) when the user specifies one — naming the substitution in the output. The skill refuses to lower a residual-risk score to avoid Article 36 prior consultation: if the user pushes to reduce a score, the skill holds the rating and re-states the mitigation gap. The skill never signs the DPIA.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
