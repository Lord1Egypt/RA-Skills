# Claims FNOL Triage

**Platforms:** Claude · Openclaw · Codex
**Domain:** Insurance

## Purpose

Turns a raw First Notice of Loss (FNOL) — call notes, online form, agent email, telematics or IoT alert — into a structured triage record that a desk adjuster can pick up and run. Captures incident facts, coverage hooks to verify against policy, severity tier, fraud red-flag checklist, recommended next actions, and an insured-facing acknowledgement draft. Designed for auto, property (personal and commercial), general liability, and workers' compensation lines.

## When to Use

- Claim intake teams turning a call/portal/IoT FNOL into a structured first record
- Inside-adjusters triaging an overnight queue of new claims for assignment
- MGAs and carriers routing claims to Express / Standard / Complex / Catastrophe tracks
- Special investigations units pre-screening for fraud red flags before assigning to a SIU adjuster
- Pre-fill of a claims-management system record (Guidewire, Duck Creek, Origami) before adjuster handoff

## What It Does

**Phase 1: PII Gate and Intake**
1. Refuses raw PHI/PII (full SSN, full credit card, full bank account, full medical record) and asks for masked equivalents before any drafting
2. Collects loss date/time, reported date, line of business, policy number (last 4), insured name (initials only in draft), loss location (city/state/ZIP), reporter-to-insured relationship, contact channel, and a free-text loss narrative
3. Tags every field as Confirmed / Reported (claimant-stated, unverified) / Unknown; requires user approval of the assumption summary before drafting

**Phase 2: Coverage Hooks, Severity, and Fraud Screen**
4. Generates line-of-business-specific **coverage questions for the adjuster to verify** against the policy (e.g., for auto: was the listed driver behind the wheel? was the vehicle on the declarations page? is the use consistent with rated use? UM/UIM applicable?). The skill never opines on coverage itself.
5. Assigns a severity tier — **Express / Standard / Complex / Catastrophe** — using a transparent rubric (injury reported, fatality, third-party bodily injury, total loss, large-loss threshold, multi-claimant, CAT-event flag, regulatory/litigation indicator)
6. Runs a fraud red-flag checklist by line of business (late reporting beyond a defined threshold, prior-claim density, witness-claimant relationship, staged-loss indicators, post-loss policy changes) and scores Low / Elevated / High SIU referral

**Phase 3: Triage Record and Acknowledgement**
7. Drafts a structured triage record with assignment recommendation (Express auto-pay path, desk adjuster, field adjuster, SIU, large-loss unit, CAT team)
8. Produces a next-action playbook for the receiving adjuster (24-hour, 72-hour, 7-day items)
9. Drafts an insured-facing acknowledgement that confirms receipt, gives the claim number placeholder, names the assigned point of contact placeholder, and avoids any coverage commitment, fault statement, or settlement language
10. Runs a self-check gate: no coverage decision, no fault attribution, no reserve number, no medical advice, no settlement offer, PII masked, DRAFT label present

## Output

A four-block deliverable: (1) FNOL triage record, (2) adjuster coverage-verification question set, (3) fraud red-flag scorecard with SIU referral recommendation, and (4) insured acknowledgement draft. Every block is labelled **DRAFT — for licensed-adjuster review** and explicitly disclaims coverage, fault, and settlement determinations.

## Notes

This skill never determines whether a loss is covered, who is at fault, what the reserve should be, or what the carrier will pay — those are licensed-adjuster decisions made against the actual policy. It hardens against prompt-injection from claimant narratives by treating all reported facts as unverified until the adjuster confirms them, and refuses to ingest unmasked PHI/PII. All claimant content shared in session is excluded from tool calls, web searches, or examples.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.