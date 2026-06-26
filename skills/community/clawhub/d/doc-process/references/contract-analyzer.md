# Contract Analyzer — Reference Guide

## Overview
Read the full contract, produce a plain-language summary, systematically identify risks/traps/obligations across 40+ risk patterns, score the contract by type, and offer clause-level negotiation guidance.

---

## Step 1 — Read the Full Document

Read all pages without skipping. For contracts >10 pages, read in page-range chunks. Pay special attention to:
- Definitions section (words defined here change meaning of every clause that uses them)
- Schedules, Annexures, Exhibits, Appendices — risks often hide here
- Boilerplate sections — jurisdiction, arbitration, liability caps are in boilerplate

---

## Step 2 — Identify Contract Type

| Contract Type | Key Signal Phrases |
|---|---|
| SaaS / Software License | "license", "subscription", "API access", "uptime SLA", "data processing" |
| Service Agreement | "statement of work", "deliverables", "professional services", "milestone" |
| Employment / Offer Letter | "employee", "at-will", "benefits", "probation", "non-compete" |
| Independent Contractor | "independent contractor", "1099", "no employment relationship", "SOW" |
| NDA / Confidentiality | "confidential information", "non-disclosure", "proprietary", "trade secret" |
| Lease (Commercial) | "landlord", "tenant", "premises", "CAM charges", "leasehold improvements" |
| Lease (Residential) | "lessor", "lessee", "security deposit", "notice to vacate", "subletting" |
| Loan / Credit Agreement | "principal", "interest rate", "default", "collateral", "amortization" |
| Partnership / JV | "profit sharing", "capital contribution", "dissolution", "voting rights" |
| Acquisition / M&A | "representations and warranties", "indemnification", "escrow", "earnout" |
| Vendor / Supply Agreement | "purchase order", "lead time", "warranty", "acceptance criteria", "FOB" |
| IP Assignment | "assigns all right, title and interest", "work made for hire", "moral rights" |
| Settlement Agreement | "release of claims", "without admission of liability", "confidentiality" |
| Terms of Service / EULA | "user", "license to use", "prohibited uses", "content ownership" |
| Franchise Agreement | "franchisee", "royalty fee", "territory", "brand standards" |

---

## Step 3 — Plain-Language Summary (TL;DR)

Write 6–10 bullets covering:

- **Contract type and parties**: who is signing, in what capacity
- **Core obligation**: what each party must do / deliver / pay
- **Duration**: start date, end date, auto-renewal mechanics
- **Compensation / Payment**: amounts, schedule, penalties, escalation
- **Termination rights**: how each party can exit, notice periods, consequences
- **Key restrictions**: non-compete, non-solicitation, exclusivity, geographic limits
- **Governing law & dispute resolution**: jurisdiction, arbitration vs. litigation
- **Special risks summary**: call out the top 2–3 risks in one sentence each

---

## Step 4 — Comprehensive Risk Scan

### RED — High Risk (potential legal or financial harm — do not sign without addressing)

| Risk Category | Specific Patterns to Find | What to Look For |
|---|---|---|
| **Unlimited liability** | "indemnify and hold harmless from any and all claims" with no cap | Check if indemnification is uncapped or unlimited |
| **Uncapped IP transfer** | "all intellectual property... is the exclusive property of [counterparty]" | Work-for-hire, IP assignment with no carve-outs for pre-existing IP |
| **Auto-renewal with short window** | "automatically renews unless cancelled X days prior" | Cancellation windows <30 days, especially with annual terms |
| **Unilateral modification** | "may modify these terms at any time", "reserves the right to change" | Vendor can change price or terms without consent |
| **Arbitration-only clause** | "disputes shall be resolved exclusively by binding arbitration" | Waives right to class action and jury trial |
| **Personal guarantee** | "guarantor personally liable", "joint and several liability" | Pierces corporate veil — owner becomes personally liable |
| **Non-compete (broad)** | Geographic scope, duration, industry scope | >1 year non-competes or covering entire industries are often unenforceable but still risky |
| **Broad data rights** | "may use your data for any purpose", "license to your content" | Data monetization, sharing with third parties |
| **Liquidated damages** | Fixed penalty clause | Amount should be reasonable estimate of actual damages |
| **Jurisdiction in distant/adverse location** | Courts of [far-away state/country] | Cost of litigation in that jurisdiction |
| **Assignment without consent** | "may assign this agreement without consent" | Contract could be sold to a competitor |
| **Force majeure favoring counterparty** | Broadly worded clause that suspends counterparty's obligations but not yours | One-sided application |
| **Penalty interest** | "interest at X% per month on overdue amounts" | Monthly rates — annualize to check if usurious |
| **Termination for convenience (one-sided)** | Only counterparty can terminate for convenience | You are locked in; they are not |
| **Non-solicitation (employees)** | "shall not solicit or hire any employee of [counterparty]" | Duration and scope — hiring from entire industry is unreasonable |

### YELLOW — Medium Risk (negotiate before signing)

| Risk Category | What to Find | What to Negotiate |
|---|---|---|
| **Limitation of liability too low** | "liability shall not exceed $X" | Should be at least 1× annual contract value |
| **Warranty disclaimer** | "AS IS", "NO WARRANTY", "NO SLA COMMITMENT" | Push for minimum uptime SLA and response-time guarantees |
| **Renewal notice >30 days** | 45, 60, 90-day cancellation notice | Negotiate to 30 days; set a calendar reminder regardless |
| **One-sided confidentiality** | Only you bound by NDA, not counterparty | Make it mutual |
| **Perpetual confidentiality** | "obligations survive indefinitely" | Push for 3–5 year time limit |
| **Vague deliverables** | "reasonable efforts", "industry-standard quality" | Demand specific, measurable acceptance criteria |
| **Ambiguous payment terms** | "net 30 from invoice receipt" vs "net 30 from delivery" | Clarify trigger date for payment clock |
| **Price escalation clause** | "CPI + 5% annually", "pricing may increase with 30 days notice" | Cap annual increases (e.g., max 3%) |
| **Termination fee** | Early exit fee, remaining contract value owed | Negotiate 30-day notice = full exit, no fee |
| **Audit rights** | Counterparty can audit your systems/books | Limit scope, frequency (once per year), and notice requirements |
| **SLA credits only, no exit right** | Downtime credits but no right to terminate for chronic failure | Add termination right if SLA breach exceeds N days/month |
| **Unilateral notice changes** | "notice to be given at counterparty's address as they may designate" | Requires both parties to agree on change of address |

### GREEN — Notable but Standard (informational, no action needed)

- Entire agreement / merger clause (standard — supersedes prior agreements)
- Severability clause (standard — invalid provisions can be severed)
- Waiver clause (one-time waiver doesn't waive future rights)
- Counterparts clause (allows signing in separate copies)
- Headings clause (headings don't affect interpretation)
- Mutual non-disparagement (balanced — fine to have)
- Balanced liability caps (1× or more annual value)
- Reasonable notice periods (30 days or more)

---

## Step 5 — Contract-Type-Specific Checks

Run additional checks based on the identified contract type:

### SaaS / Software Agreements
- **Data Processing Agreement (DPA)**: Is there one? Required if personal data is processed (GDPR, CCPA)
- **Data portability**: Can you export your data on termination? In what format? Within how many days?
- **Data deletion**: Are your data deleted after contract ends? Confirm timeline.
- **Uptime SLA**: What is the uptime guarantee? What are credits for downtime?
- **Vendor lock-in**: Proprietary data formats, migration fees, API access after termination?
- **Subprocessors**: Does the vendor use third-party subprocessors? Are they listed?
- **Security obligations**: Encryption standards, breach notification timeline (should be ≤72 hours for GDPR)
- **Source code escrow**: Is there an escrow arrangement if vendor goes bankrupt?

### Employment Agreements
- **At-will vs. fixed term**: Can either party terminate without cause?
- **Benefits vesting**: Stock option vesting schedule, cliff, acceleration on termination
- **Garden leave**: Are you paid during the non-compete period?
- **IP assignment scope**: Pre-existing IP carve-out? Moonlighting projects?
- **Background check / drug testing consent**: Check what you're consenting to
- **Reference policy**: Can former employer give negative references?

### Lease Agreements (Commercial)
- **CAM charges**: Common area maintenance — are they capped? Auditable?
- **Rent escalation**: Fixed % or CPI-linked? Negotiate cap
- **Personal guarantee**: Is the lease signed by you personally or your company?
- **Tenant improvement allowance (TIA)**: How much, paid when, what happens if you leave early?
- **Exclusivity / permitted use**: Can landlord lease adjacent space to a competitor?
- **Assignment / subletting**: Can you sublet if you downsize?
- **Force majeure / pandemic clause**: What suspends rent obligations?

### Loan / Credit Agreements
- **Effective APR**: Annualize all fees and interest to get true cost
- **Prepayment penalty**: Can you pay off early? At what cost?
- **Covenant breaches**: What financial ratios trigger default? Debt-to-equity, EBITDA
- **Cross-default clause**: Default on another loan triggers this one
- **Material Adverse Change (MAC) clause**: Lender can call the loan if your business condition changes

### NDAs
- **What is "Confidential Information"**: Overly broad definitions protect nothing
- **Residuals clause**: "Information retained in unaided memory may be used" — this is a backdoor
- **Exceptions**: Standard exceptions (public domain, independent development, prior knowledge) should all be present
- **Return / destruction of materials**: Timeline and confirmation mechanism
- **Injunctive relief**: Standard — parties agree money damages insufficient, can seek injunction

---

## Step 6 — Renewal & Fee Traps

| Trap | What to Find | Impact |
|---|---|---|
| Auto-renewal | "automatically renews for successive [periods]" | Locked in for another year if you miss the cancellation window |
| Short cancellation window | "cancel with [N] days notice before renewal date" | Calendar the date immediately |
| Annual price increase | "pricing increases by X% each renewal" | Annualize the compound cost over 3 years |
| Early termination fee (ETF) | "remaining contract value", "liquidated damages" | Calculate total ETF at signing |
| Minimum commitment | "minimum annual spend of $X", "minimum N seats" | You pay even if you stop using |
| Setup / onboarding fee | One-time fees at signing | Often negotiable to $0 |
| Overage charges | "usage in excess of included amount billed at $X/unit" | Model worst-case overage cost |
| Late payment penalty | "1.5% per month" = 18% APR | Grace period negotiation |
| Reinstatement fee | If suspended for non-payment, fee to restore service | |
| Data export fee | "data export available for $X" | Should be free — negotiate |

---

## Step 7 — Output Format

```
## Contract Analysis: [Contract Title or "Uploaded Contract"]
Contract Type: [e.g., SaaS Subscription Agreement]
Parties: [Party A] ↔ [Party B]
Pages Analyzed: N

### TL;DR Summary
- **Type**: SaaS subscription for project management software
- **Parties**: Acme Corp (vendor) ↔ XYZ Ltd (customer)
- **Duration**: 12 months from [date], auto-renews annually
- **Payment**: $2,400/year, billed monthly at $200; 5% increase on renewal
- **Termination**: Customer: 60 days notice before renewal; Vendor: 30 days for cause
- **Governing law**: Delaware, USA; arbitration-only (JAMS rules)
- **Top risks**: Uncapped indemnification (Sec 8.2), 60-day cancellation window (Sec 12.1), unilateral term changes (Sec 3.4)

---

### Risk Report

#### RED — High Risk (3 found)
| # | Clause | Location | Issue | Recommendation |
|---|---|---|---|---|
| 1 | Indemnification | Section 8.2 | Customer indemnifies vendor for "any and all claims" — unlimited liability | Negotiate a mutual cap equal to amounts paid in prior 12 months |
| 2 | Auto-renewal | Section 12.1 | 60-day cancellation notice; easy to miss | Set a calendar reminder now; negotiate to 30 days |
| 3 | Unilateral changes | Section 3.4 | Vendor can modify pricing with 30-day email notice | Negotiate: changes require 90 days notice + your written consent |

#### YELLOW — Medium Risk (4 found)
| # | Clause | Location | Issue | Recommendation |
|---|---|---|---|---|
| 1 | Liability cap | Section 10 | Capped at $500 — less than 1 month's fees | Negotiate to 12× monthly fee ($2,400) |
| 2 | Price escalation | Section 5.3 | Up to 10% annually, uncapped | Add cap: max 3% per year or CPI, whichever is lower |
| 3 | Data portability | Section 14.2 | Export available but "within 90 days of termination" | Negotiate to 30 days; confirm CSV/standard format |
| 4 | Warranty | Section 9 | "AS IS" — no uptime or performance guarantee | Request minimum 99.5% uptime SLA with credits |

#### GREEN — Standard / Acceptable (3 noted)
- Entire agreement clause (Section 16) — standard
- Mutual NDA provisions (Schedule A) — balanced
- IP ownership retained by customer for customer data (Section 7.1) — favorable

---

### Renewal & Fee Traps
| Trap | Detail | Impact |
|---|---|---|
| Auto-renewal | YES — 60-day cancellation notice required | Calendar: [renewal date minus 61 days] |
| Price escalation | Up to 10% annually (Section 5.3) | Year 2: $2,640; Year 3: $2,904 |
| Early termination fee | 3 months of remaining contract (Section 13.2) | If cancelled month 6, owes ~$600 |
| Data export fee | $0 — export included | Good |
| Minimum commitment | 5 seats minimum (Section 4.1) | Must pay for 5 seats even if using 2 |

---

### SaaS-Specific Checks
| Check | Result |
|---|---|
| Data Processing Agreement | NOT FOUND — required if personal data processed (GDPR/CCPA) |
| Data deletion on termination | 90 days post-termination (Section 14.3) — acceptable |
| Data portability format | "machine-readable format" — vague; negotiate to CSV/JSON |
| Breach notification | 72 hours (Section 11.4) — GDPR compliant |
| Subprocessors listed | Schedule B — 12 subprocessors listed |
| Uptime SLA | NOT PROVIDED — negotiate before signing |

---

### Risk Score
| Rating | Count |
|---|---|
| RED flags | 3 |
| YELLOW flags | 4 |
| SaaS-specific gaps | 2 |
| **Recommendation** | **Review and negotiate before signing** |
```

---

## Step 8 — Suggested Clause Rewrites

When asked, provide specific replacement language for RED clauses:

**Indemnification — suggested rewrite:**
> "Each party's total aggregate liability under this Agreement shall not exceed the fees paid by Customer in the twelve (12) months preceding the claim. Indemnification obligations are mutual and limited to third-party claims arising from gross negligence or willful misconduct."

**Auto-renewal — suggested rewrite:**
> "This Agreement shall renew automatically for successive one-year terms unless either party provides written notice of non-renewal at least thirty (30) days prior to the end of the then-current term."

**Unilateral changes — suggested rewrite:**
> "Any modification to pricing or material terms requires ninety (90) days written notice and Customer's written consent. Continued use after the notice period without written objection constitutes acceptance."

---

## Step 9 — Follow Up

Offer:
- "Want me to draft suggested edits for all RED clauses as tracked changes?"
- "Should I flag which clauses are unusual for this contract type vs. standard boilerplate?"
- "Want a one-page executive summary to share with your legal team or stakeholder?"
- "Should I check if this contract complies with GDPR / CCPA / local consumer protection laws?"
- "Want me to compare this against a standard industry template?"
