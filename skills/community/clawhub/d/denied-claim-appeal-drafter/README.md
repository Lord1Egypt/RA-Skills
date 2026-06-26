# Denied Claim Appeal Drafter

**Platforms:** Claude · Openclaw · Codex
**Domain:** Medical Billing — Denials & Appeals

## Purpose

An appeal-letter drafting partner for medical billers, denials specialists, coders, revenue-cycle analysts, and the clinicians who sign their appeals. Turns a payer remittance (EOB / 835 ERA), denial reason codes (CARC / RARC), and chart excerpts into a DRAFT appeal letter that is matched to the actual denial reason, anchored in chart evidence, addressed to the correct appeal level, and filed within the payer's window.

## When to Use

- Appealing a medical-necessity denial (CARC 50, 55, 96 with medical-necessity RARC)
- Appealing a prior-authorization denial (CARC 197 / 198)
- Appealing a timely-filing denial (CARC 29) where you have proof of original submission
- Appealing a coding / bundling / NCCI denial (CARC 4, 16, 97, 226, 234)
- Appealing a level-of-care or DRG downgrade (inpatient vs. observation, sepsis-2 vs. sepsis-3)
- Appealing a non-covered-service or experimental denial (CARC 96 with experimental RARC) where peer-reviewed evidence supports the service
- Building a clean, payer-specific letter that meets first-level, second-level, external-review (state IRO), or Medicare redetermination / reconsideration / ALJ requirements

## What It Does

**Phase 1: Intake and triage**
1. Captures payer, plan type (commercial / Medicare FFS / Medicare Advantage / Medicaid managed care / TRICARE / workers' comp), provider taxonomy, and clearinghouse / 835 trail
2. Captures patient (PHI minimized — uses internal identifiers), DOS, claim #, ICD-10-CM, CPT/HCPCS with modifiers, billed and allowed amounts
3. Captures denial as posted: CARC, RARC, group code (CO / PR / OA / PI), remark text
4. Routes the denial to the correct appeal *type* (clinical / administrative / coding) and the correct appeal *level*
5. Pulls the payer's filing window and prior-deadline events

**Phase 2: Argument construction**
6. Maps each CARC / RARC to the argument it actually requires (medical necessity, prior-auth-on-file, timely-filing proof, coding correction, level-of-care upgrade, place-of-service correction, duplicate-rebuttal, etc.)
7. Collects supporting chart evidence with page / section anchors (H&P, progress notes, op note, imaging report, lab, prior-auth fax confirmation, medical-policy citation)
8. Flags evidence gaps and refuses to draft a fabricated clinical fact

**Phase 3: Drafting**
9. Drafts a payer-addressed letter with header block, claim identifiers, single-issue framing, denial-reason quote, point-by-point rebuttal, evidence cite list, requested remedy (overturn / reprocess / pay at correct level), signature block for the credentialed signer, and an enclosures list
10. Generates a filing-deadline tracker, certified-delivery checklist, and an internal escalation calendar (next-level deadline if denied again)

## Output

A DRAFT appeal packet with:

- Cover appeal letter (single-issue, denial-reason-matched, evidence-cited)
- Denial-reason mapping table (CARC → RARC → argument used → evidence anchor)
- Enclosures index (numbered, redaction-noted)
- Filing-deadline tracker (this level + next-level if denied)
- Certified-delivery / portal-submission checklist
- Internal escalation calendar
- Unresolved-information list

## Safety

This skill drafts an appeal, **not** a guarantee of payment. Every output is labeled **DRAFT — BILLER / CODER / CLINICIAN MUST REVIEW BEFORE SUBMISSION**. The skill never fabricates clinical facts, never asserts medical necessity beyond what the chart supports, never quotes PHI in examples, and never bypasses payer / state / federal appeal-process rules. Medicare appeals flow through the five statutory levels; ERISA plans flow through 29 C.F.R. § 2560.503-1; state external review follows the state's IRO regulation. The skill flags any deadline within 7 calendar days as critical and recommends certified mail or payer-portal submission with confirmation.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
