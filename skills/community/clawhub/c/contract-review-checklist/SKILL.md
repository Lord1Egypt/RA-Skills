---
name: contract-review-checklist
description: "Contract risk review checklists — clause-by-clause red-flag scanning by contract type, risk grading with rewrite suggestions, missing-clause detection, and a negotiation-ready review report. Not ”AI lawyer”: structured triage before counsel review."
version: 1.0.0
author: RAY
license: CC-BY-4.0
tags: [legal, contracts, risk-review, msa, negotiation]
pricing:
  free: Free — 2 contract risk summaries/month
  pro: $29/month — full 12-checklist library + clause rewrite bank
  annual: $290/year
  pay_per_use: $19 one-time (single contract review)
  enterprise: $199/month (company template mapping + compliance link)
tiers:
  - id: free
    name: Free
    price: Free
    quota: Free — 2 contract risk summaries/month
  - id: pro
    name: Pro Monthly
    price: $29/month — full 12-checklist library + clause rewrite bank
    quota: unlimited
  - id: annual
    name: Pro Annual
    price: $290/year
    quota: unlimited
  - id: enterprise
    name: Enterprise
    price: $199/month (company template mapping + compliance link)
    quota: team unlimited
monetization:
  model: freemium_subscription
  currency: USD
  paywall_trigger: free quota exhausted
  trial_days: 7
  free_trial: true
  upgrade_path: Pro Monthly -> Pro Annual -> Enterprise

---# Contract Review Checklist Pack

## What problem it solves

This is not an "AI lawyer" — it standardizes the **checking motions** of legal review: run a contract through the checklist, get a first-pass triage in 30 minutes, output an issue list your lawyer can verify instead of bill you to discover.

## Review framework (five layers)

### 1. Counterparty screening
Independent legal entity? Signing authority? Authorized signatory vs. seal consistency? Industry-specific licenses. Check: business-scope vs. contract subject-matter alignment.

### 2. Red-flag clause scan (differentiated by contract type)

**Sales/service agreements — 12-item core checklist**:
| # | Clause | Red flag |
|---|---|---|
| 1 | Payment | Payable only after acceptance + vague acceptance standard = infinite deferral |
| 2 | Liquidated damages | Binds us only; no reciprocal liability |
| 3 | Delivery | Open-ended "per actual needs" clauses |
| 4 | IP | Deliverable IP defaults to counterparty |
| 5 | Confidentiality | Unlimited term / one-way NDA |
| 6 | Termination | Counterparty's unilateral convenience termination |
| 7 | Liability cap | Their cap is low, ours is unlimited |
| 8 | Disputes | Venue at their home turf |
| 9 | Acceptance | Deemed-acceptance clause (silence = accepted) |
| 10 | Amendments | Oral amendments valid |
| 11 | Assignment | Counterparty freely subcontractors |
| 12 | Notices | Address clause makes service on us impractical |

### 3. Missing-clause check
Should exist but absent: liability, dispute resolution, force majeure, notice/service, termination triggers.

### 4. Consistency check
Amounts (words vs. figures), dates, entity names across the document; annex vs. body precedence.

### 5. Output
Risk grading (HIGH = don't sign unamended / MEDIUM = negotiate / LOW = acknowledge) + rewrite suggestion per finding + review report you can send to the counterparty as negotiation basis.

## Boundaries

Output is **assisted screening, not legal advice**; high-stakes contracts (large value / cross-border / guarantees) must be verified by a licensed attorney.
