# Chain-of-Custody Log Drafter

**Platforms:** Claude · Openclaw · Codex
**Domain:** Digital Forensics — Evidence Handling

## Purpose

A drafting partner for qualified digital-forensic examiners, DFIR responders, e-discovery custodians, internal-investigation leads, and counsel. Turns case facts, evidence-item details, acquisition data, and transfer events into a DRAFT court-admissible chain-of-custody record, acquisition worksheet, and examiner-action log aligned to NIST SP 800-86 and ISO/IEC 27037, with hash-verification gates at acquisition, duplication, transfer, and return.

## When to Use

- Recording a chain of custody for digital evidence in a criminal investigation, civil litigation under FRCP, regulatory inquiry, employee-misconduct investigation, or incident-response engagement
- Producing a discoverable acquisition worksheet that captures tool name **and** version, write-blocker, source / image / verification hashes, and acquisition result
- Maintaining an examiner-action log against working copies only, with one tool per row and contemporaneous timestamps
- Onboarding a new evidence item under an existing case ID and preserving the unbroken-sequence requirement
- Preparing a hand-off pack for transfer to counsel, opposing counsel, an outside lab, or a regulator

## What It Does

**Phase 1: Intake**
1. Captures engagement type, case ID, evidence-handling framework, search authority, and legal hold / preservation notice
2. Captures evidence-item characterization, seizure context, and physical condition
3. Captures acquisition method, tool + version, write-blocker, source / image / verification hashes, and acquisition result
4. Captures transfer events with from-role / to-role / method / seal status / hash-check / notes

**Phase 2: Working-copy discipline**
5. Confirms original-vs-working-copy separation, working-copy hashes, encryption at rest, and retention schedule
6. Captures examiner-action log against working copies only, one tool + version per row

**Phase 3: Assumption summary and drafting**
7. Restates every fact as Confirmed / Assumed / Reconstructed / Unknown
8. Drafts the DRAFT CoC record, acquisition worksheet, examiner-action log, and working-copy register
9. Runs the self-check rubric

## Output

A DRAFT CoC package with:

- Evidence-item register
- Acquisition worksheet with source / image / verification hashes
- Chain-of-custody transfer log with unsigned signature column
- Examiner-action log against working copies
- Working-copy register with encryption and retention
- Original-evidence handling block
- Evidence-integrity verification table
- Evidence matrix (Confirmed / Assumed / Reconstructed / Unknown)
- Unresolved-questions list

## Safety

This skill drafts CoC documentation, **not** signed or authenticated records. Every output is labeled **DRAFT — EXAMINER OF RECORD MUST REVIEW AND SIGN**. Hashes, timestamps, serial numbers, tool versions, and custodian names are never invented; missing fields render as `Unknown — required for admissibility`. Reconstructed entries are explicitly labelled and never appear as original entries. The skill never recommends destruction, sanitization, wiping, factory reset, decryption-key disclosure, or any chain-breaking action; it surfaces the legal-hold / preservation obligation instead. It never opines on admissibility, weight, sufficiency, or the merits of the investigation. All case data is treated as confidential and is never written to external services.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
