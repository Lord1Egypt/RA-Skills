---
name: contract-red-flag-scanner
description: "Use when signing or reviewing any contract you haven't fully read — apartment lease, employment offer, Terms of Service, gym/phone subscription, freelancer agreement — and before paying a lawyer for a first pass: scans plain-text contract text for 20+ high-risk clause patterns (auto-renewal traps, arbitration and class-action waivers, one-sided termination penalties, liability caps, unilateral amendment rights, non-competes, fee schedules), infers the contract type, produces a risk-ranked findings report with plain-language explanations and the exact questions to ask the other side, plus a missing-clause checklist of protections that SHOULD be present but aren't."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [contracts, legal, lease-review, red-flags, consumer-protection, negotiation]
---

# Contract Red Flag Scanner

## Overview

Almost nobody reads the contracts they sign. Studies of ToS agreements estimate that actually reading all the agreements an average person clicks through would take 76 work-days a year — so people sign apartment leases with auto-renewal traps, employment offers with hidden non-competes, and subscriptions with one-sided cancellation penalties. The consequences are real money: eviction for breaking a lease early, fees that compound monthly, rights silently signed away to arbitration.

This skill is a **first-pass triage layer between you and the fine print**. It does not replace a lawyer — it tells you *whether you need one, and exactly what to ask*. It scans plain contract text (paste, OCR output, or a `.txt` export) for a curated library of high-risk clause patterns, infers the contract type (lease / employment / ToS / service subscription), and outputs:

1. **Risk-ranked findings** — HIGH / MEDIUM / LOW, each with the matched contract language, a plain-English explanation of what it means, and the concrete question to ask before signing.
2. **A scrutiny score** (0–100) summarizing how adversarial the document is.
3. **A missing-clause checklist** — protections that a fair contract of this type should contain (e.g., a lease without a habitability/repair clause, a subscription without a cancellation mechanism).
4. **A printable question list** for the landlord / HR / vendor conversation.

Everything runs offline on pure stdlib Python — no contract text ever leaves the machine.

## When to Use

- **Apartment / house lease before signing** — the #1 use case: early-termination penalties, deposit terms, auto-renewal, entry rights.
- **Job offer or employment agreement** — non-compete, non-solicit, IP assignment scope, at-will vs cause termination.
- **Any subscription with a term commitment** — gyms, phone plans, SaaS, solar leases: auto-renewal windows and cancellation fees.
- **Freelance / contractor agreements** — indemnification, kill fees, payment terms, work-for-hire scope.
- **Terms of Service diffs that matter** (platforms you depend on for income) — unilateral amendment, liability caps.
- **Before paying a lawyer** — arrive with a targeted question list instead of a blank page; lawyers bill by the hour you save.
- Don't use for: criminal matters, immigration, anything already in litigation — get a real attorney. Don't treat the absence of flags as legal clearance; the scanner is pattern-based, not a legal opinion.

## How It Works

1. **Extract text** — copy-paste the contract, or OCR a scanned PDF (`pymupdf`, `marker`). Save as `.txt`.
2. **Detect contract type** — keyword scoring (landlord/tenant/premises → lease; employee/employer → employment; user agreement/terms → ToS; membership/monthly → subscription).
3. **Scan clause patterns** — 20+ detectors, each a set of regexes with a base severity, an explanation, and a follow-up question. Detectors normalize whitespace and match case-insensitively.
4. **Rank and score** — findings sort by severity; the scrutiny score weights HIGH=10, MEDIUM=4, LOW=1, capped at 100.
5. **Check for missing protections** — per contract type, a list of clauses a balanced contract should contain; report any that are absent.
6. **Review the question list** — every finding maps to one concrete question to ask before signing.

## Commands

```bash
# Scan a lease (paste or export the text first)
python3 scripts/contract_scanner.py scan references/sample-lease.txt

# JSON output for programmatic use / agent pipelines
python3 scripts/contract_scanner.py scan contract.txt --json

# Force a contract type when detection is wrong
python3 scripts/contract_scanner.py scan offer.txt --type employment

# List all detectors and what they look for
python3 scripts/contract_scanner.py list-detectors

# Exit codes: 0 = clean-ish, 2 = HIGH findings present (usable in CI/hooks)
```

## Example Session

```
$ python3 scripts/contract_scanner.py scan references/sample-lease.txt

CONTRACT TYPE: lease (confidence 0.86)
SCRUTINY SCORE: 47/100 — 2 HIGH, 3 MEDIUM, 1 LOW findings

[HIGH] AUTO-RENEWAL WITH STRICT NOTICE WINDOW
  Matched: "shall automatically renew for successive twelve (12) month
  terms unless Tenant provides written notice not less than sixty (60)
  days prior to the end of the term"
  Plain language: If you forget to send written notice exactly 60 days
  out, you are locked in for another FULL year — not month-to-month.
  Ask: "Can we make this renew month-to-month after the first term,
  or reduce the notice window to 30 days?"

[HIGH] EARLY TERMINATION PENALTY — ALL REMAINING RENT
  ...

[MEDIUM] LATE FEE — FLAT PLUS DAILY ACCRETION
  ...

MISSING-CLAUSE CHECKLIST (lease):
  [ ] Habitability / landlord repair obligation — NOT FOUND
  [ ] Security deposit return deadline — NOT FOUND
  [ ] Entry notice requirement — NOT FOUND

QUESTION LIST FOR THE OTHER SIDE:
  1. Can renewal go month-to-month, or notice drop to 30 days?
  ...
```

## Detector Library (abridged)

| Category | Detectors | Typical severity |
|---|---|---|
| Renewal & exit traps | auto-renewal notice windows, early-termination rent acceleration, cancellation fees, non-refundable prepayment | HIGH / MEDIUM |
| Rights waivers | binding arbitration, class-action waiver, jury trial waiver, severability of those waivers | HIGH |
| One-sided economics | late fees + daily accretion, unilateral price change, one-sided attorney fees, indemnification of the other party | MEDIUM |
| Scope creep | non-compete, non-solicit, broad IP assignment, unilateral amendment ("we may change these terms") | HIGH / MEDIUM |
| Operational | entry without notice, as-is condition, governing law far from you, assignment of the agreement without your consent | LOW / MEDIUM |

Full list: `python3 scripts/contract_scanner.py list-detectors`, documented in `references/clause-guide.md`.

## Workflow for an Agent

1. Get the contract text (paste, email attachment, OCR of scanned PDF).
2. Save to a file, run `scan <file>`. If type detection looks wrong, re-run with `--type`.
3. Present findings to the user **ranked, with the matched language quoted** — never paraphrase away the actual contract wording; that wording is the evidence.
4. Present the missing-clause checklist — absence of protection is often worse than a present-but-bad clause.
5. Produce the question list as a copy-paste block for the user's email/conversation.
6. If HIGH findings ≥ 2 or scrutiny score ≥ 60, recommend a lawyer review for those specific clauses (cheaper than full review).

## Common Pitfalls

1. **Treating scanner output as legal advice.** It is triage. A clean scan is not clearance; some traps are phrased in unmatchable legalese.
2. **Scanning a partial document.** Schedules, exhibits, and "attachment A" fee tables often hold the worst terms. Extract the ENTIRE document.
3. **OCR garbage in, garbage out.** Broken text causes false negatives (missed clauses), which are worse than false positives. Check the `.txt` for completeness first.
4. **Ignoring the missing-clause checklist.** Users fixate on what's flagged; what's ABSENT (no repair obligation, no deposit deadline) is where landlords win disputes.
5. **Signing anyway because "everything has these clauses."** Arbitration clauses, 60-day notice windows, and rent acceleration are all negotiable before signature. After, never.
6. **Wrong contract type inference on short documents.** A 1-paragraph addendum may misclassify; use `--type`.

## Verification Checklist

- [ ] Contract text extracted completely (all pages, schedules, exhibits)
- [ ] `scan` ran without errors and detected the right contract type
- [ ] Findings presented with quoted matched language, not just labels
- [ ] Missing-clause checklist shown alongside findings
- [ ] Question list delivered as a copy-paste block
- [ ] If HIGH ≥ 2 or score ≥ 60: lawyer-review recommendation stated explicitly
