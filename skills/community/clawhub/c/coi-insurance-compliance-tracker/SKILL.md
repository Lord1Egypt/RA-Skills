# COI & Insurance Compliance Tracker — Coverage Gate Matrix
**Framework:** Coverage Gate Matrix
**Price:** $29
**Category:** Productivity / Compliance
**Tags:** COI, insurance, compliance, vendor management, risk, certificates of insurance
**last_validated:** 2026-03-03

---

## What This Is

The Coverage Gate Matrix is a four-phase system for managing vendor certificates of insurance (COIs) from collection through remediation. It tells you exactly what to collect, how much coverage to require, when to follow up, and what to do when a vendor falls out of compliance.

**Problem it solves:** Most ops teams manage COIs reactively — they chase documents after something goes wrong, or realize a vendor's coverage expired months ago. The Coverage Gate Matrix closes that gap by turning COI management into a proactive, scored system with clear triggers and actions.

**Output:** A complete COI compliance registry with current status for every vendor, coverage scores, expiration alerts, and documented remediation actions.

---

## The Coverage Gate Matrix Framework

The system runs across four sequential phases:

```
PHASE 1: COLLECT
What to get, from whom, by when
        ↓
PHASE 2: VALIDATE
Does coverage meet minimums? Is it current?
        ↓
PHASE 3: SCORE
Compliance score 0-100 per vendor
        ↓
PHASE 4: REMEDIATE
Action based on score and gap type
        ↓
    COMPLIANT ✓ or ESCALATED ⚠️
```

---

## PHASE 1: COLLECT

### 1.1 — What to Collect (Universal Requirements)

Every vendor, regardless of category, must provide:

1. **Certificate of Insurance (ACORD 25 form)** — the standard COI document
2. **Additional insured endorsement** naming your organization (required for all vendors with physical access or service delivery liability)
3. **Primary and non-contributory endorsement** (for vendors with significant liability exposure)
4. **Waiver of subrogation** (for construction, facilities, and high-risk service vendors)

### 1.2 — Coverage Minimums by Vendor Category

#### Technology / SaaS / Software Vendors
| Coverage Type | Minimum Required |
|--------------|-----------------|
| General Liability | $1M per occurrence / $2M aggregate |
| Professional Liability / E&O | $1M per occurrence |
| Cyber Liability | $1M per occurrence (required if handling data) |
| Workers' Compensation | Statutory limits |

#### Professional Services (Consulting, Staffing, Legal, Accounting)
| Coverage Type | Minimum Required |
|--------------|-----------------|
| General Liability | $1M per occurrence / $2M aggregate |
| Professional Liability / E&O | $2M per occurrence |
| Workers' Compensation | Statutory limits |
| Umbrella / Excess Liability | $2M (for spend >$100K) |

#### Facilities / Construction / Contractors
| Coverage Type | Minimum Required |
|--------------|-----------------|
| General Liability | $2M per occurrence / $4M aggregate |
| Workers' Compensation | Statutory limits |
| Employer's Liability | $500K per accident |
| Auto Liability | $1M combined single limit |
| Umbrella / Excess Liability | $5M (for projects >$500K) |
| Builder's Risk / Installation Floater | Project value (for construction) |

#### Logistics / Shipping / Transportation
| Coverage Type | Minimum Required |
|--------------|-----------------|
| General Liability | $1M per occurrence |
| Auto Liability | $1M per occurrence |
| Cargo Insurance | $500K per shipment (adjust to actual shipment value) |
| Workers' Compensation | Statutory limits |

#### Marketing / Creative / Events
| Coverage Type | Minimum Required |
|--------------|-----------------|
| General Liability | $1M per occurrence / $2M aggregate |
| Professional Liability | $1M per occurrence |
| Media Liability | $1M (for agencies managing public content) |
| Workers' Compensation | Statutory limits (if they have employees) |

#### Low-Risk Vendors (Pure SaaS, subscriptions, no on-site work)
| Coverage Type | Minimum Required |
|--------------|-----------------|
| General Liability | $500K per occurrence |
| Professional Liability | $500K per occurrence |
| Cyber Liability | $500K (if any data processed) |

### 1.3 — Additional Insured Requirements

Your organization name on the COI must be exact. Confirm the COI reads:

> "[Your Legal Entity Name], its officers, directors, employees, and agents are included as additional insured"

If the name is wrong, request a corrected certificate before accepting.

### 1.4 — Collection Cadence

| Trigger | Action |
|---------|--------|
| New vendor onboarding | Request COI at Gate 2 (before activation) |
| Annual renewal (for active vendors) | Request 60 days before current COI expires |
| Policy renewal noticed | Request updated COI within 5 business days |
| Vendor adds new service type | Request updated COI reflecting new scope |
| After a claim or incident | Request updated COI confirming coverage remains active |

---

## PHASE 2: VALIDATE

### 2.1 — COI Validation Checklist

When a COI is received, run this 10-point validation:

**Identity Verification**
- [ ] Insured name matches vendor legal entity name exactly
- [ ] Insurer is licensed to operate in your state (check state insurance department lookup)
- [ ] Certificate holder name is correct (your organization's exact legal name)

**Coverage Verification**
- [ ] All required coverage types are listed
- [ ] Per-occurrence limits meet category minimums
- [ ] Aggregate limits meet category minimums
- [ ] Policy effective dates are current (not expired)
- [ ] Policy expiration date is at least 30 days in the future

**Endorsements**
- [ ] Additional insured endorsement attached and correct
- [ ] Waiver of subrogation included (if required for this vendor category)
- [ ] Primary and non-contributory language included (if required)

### 2.2 — Common COI Red Flags

Flag any COI that shows:

| Red Flag | Action |
|----------|--------|
| Expiration within 30 days | Request renewal immediately — activate Phase 4 |
| Limits below category minimum | Vendor must increase coverage — hold or conditional approval |
| Insurer not admitted in your state | Confirm surplus lines filing or reject |
| Additional insured not correctly named | Request corrected certificate |
| Coverage type missing | Vendor must add coverage before activation |
| Dates don't match policy period | Verify with insurer or request binder |
| Certificate holder blank or wrong | Request corrected certificate |
| "Sample" or "for information only" stamp | Reject — request actual current certificate |

### 2.3 — Verification Best Practices

For high-value vendors (>$100K annual spend) or high-risk categories:
- **Contact the insurer directly** to verify coverage is active (call the agency listed on the ACORD form)
- **Request a binder** rather than a certificate for construction or major project starts
- **Add an endorsement verification step** — request the actual endorsement pages, not just the summary certificate

---

## PHASE 3: SCORE

### 3.1 — Vendor Compliance Score (0-100)

Score each vendor across five dimensions. Update scores quarterly and whenever a new COI is received.

#### Scoring Dimensions

**Dimension 1: Coverage Completeness (25 points)**
- All required coverage types present: 25 pts
- Missing 1 coverage type: 15 pts
- Missing 2 coverage types: 5 pts
- Missing 3+ coverage types: 0 pts

**Dimension 2: Coverage Adequacy (25 points)**
- All limits meet or exceed minimums: 25 pts
- 1-2 limits below minimum (minor gap <20%): 15 pts
- 1-2 limits below minimum (major gap >20%): 5 pts
- 3+ limits below minimum: 0 pts

**Dimension 3: Policy Currency (20 points)**
- Policy active, not expiring within 90 days: 20 pts
- Policy active, expiring in 60-90 days: 15 pts
- Policy active, expiring in 30-60 days: 8 pts
- Policy active, expiring within 30 days: 2 pts
- Policy expired: 0 pts

**Dimension 4: Documentation Quality (15 points)**
- All required endorsements present and correct: 15 pts
- Missing 1 endorsement: 10 pts
- Missing 2 endorsements: 5 pts
- Missing 3+ endorsements or certificate holder wrong: 0 pts

**Dimension 5: Response Compliance (15 points)**
- Submitted on first request, within 5 days: 15 pts
- Submitted within 10 days: 10 pts
- Required 1 follow-up, submitted within 15 days: 5 pts
- Required 2+ follow-ups or more than 15 days: 0 pts

#### Score Calculation

```
Total Score = D1 + D2 + D3 + D4 + D5
Max possible: 100 points
```

### 3.2 — Compliance Tier Classification

| Score Range | Tier | Status |
|-------------|------|--------|
| 85-100 | 🟢 Green — Compliant | No action required |
| 70-84 | 🟡 Yellow — Attention | Minor gaps, monitor closely |
| 50-69 | 🟠 Orange — At Risk | Active remediation required |
| Below 50 | 🔴 Red — Non-Compliant | Work pause or hold recommended |

---

## PHASE 4: REMEDIATE

### 4.1 — Remediation Actions by Tier

**🟢 Green (85-100): No Action**
- Log score in tracker
- Set next review date (90 days or at COI expiration, whichever comes first)
- Send acknowledgment to vendor if they improved from prior review

**🟡 Yellow (70-84): Monitor & Notify**
- Log score and specific gaps
- Send Gap Notice to vendor (Template A below)
- Set 30-day follow-up reminder
- Escalate if not resolved within 30 days

**🟠 Orange (50-69): Active Remediation**
- Log score and all gaps
- Send Remediation Required notice (Template B below)
- Notify internal owner of vendor relationship
- Give vendor 15 business days to resolve
- If spend is high: consider conditional hold on new purchase orders
- Escalate to manager if not resolved

**🔴 Red (Below 50): Non-Compliant Hold**
- Immediately notify internal vendor owner and manager
- Send Non-Compliance Notice (Template C below)
- Place hold on new purchase orders until resolved
- Give vendor 10 business days to resolve or escalate
- If coverage is expired: recommend immediate work stoppage for high-risk vendor categories
- Document in vendor record for risk history

### 4.2 — Communication Templates

#### Template A — Gap Notice (Yellow Tier)
```
Subject: Action Required: Insurance Certificate Update — [Vendor Name]

Hi [Contact Name],

During our routine review of your insurance documentation, we identified the following items that require your attention:

GAPS IDENTIFIED:
[ ] [Specific gap 1 — e.g., "Professional liability limit is $500K; our minimum is $1M"]
[ ] [Specific gap 2]

Please provide updated documentation addressing these items by [DATE — 30 days].

If you've already renewed or updated your coverage, please send the new certificate to [email].

Questions? Contact [Your Name] at [email/phone].

[Your Name]
[Your Company] Operations
```

#### Template B — Remediation Required (Orange Tier)
```
Subject: IMPORTANT: Insurance Compliance Issue — [Vendor Name] — Action Required by [DATE]

Hi [Contact Name],

Our compliance review has identified significant gaps in your current insurance documentation that require immediate attention. 

ISSUES REQUIRING RESOLUTION:
1. [Issue — e.g., "General liability aggregate limit ($1M) is below our $2M minimum"]
2. [Issue]
3. [Issue]

We need updated certificates of insurance addressing all items above by [DATE — 15 business days].

IMPORTANT: Until these items are resolved, we may need to place a hold on new purchase orders. Our goal is to work through this quickly so there's no disruption to our relationship.

Please contact us immediately to discuss a resolution timeline.

[Your Name]
[Your Company] Operations | [phone]
```

#### Template C — Non-Compliance Notice (Red Tier)
```
Subject: URGENT: Insurance Non-Compliance — [Vendor Name] — Immediate Action Required

Hi [Contact Name] and [Senior Contact at Vendor],

[Vendor Name]'s insurance coverage has fallen into non-compliance with our vendor requirements. We need to resolve this immediately.

NON-COMPLIANCE ISSUES:
1. [Issue — e.g., "General liability coverage expired [DATE]"]
2. [Issue]

REQUIRED ACTIONS:
1. Confirm in writing within 24 hours whether coverage is being reinstated
2. Provide updated certificates within 10 business days

IMPACT: We have placed a hold on new purchase orders pending resolution. [For high-risk categories: We also need to pause work in [specific area] until coverage is confirmed.]

We value our relationship with [Vendor Name] and want to resolve this quickly. Please contact me directly.

[Your Name], [Title]
[Your Company] | [direct phone]
CC: [Internal vendor owner], [Finance/Legal if applicable]
```

### 4.3 — Escalation Ladder

If vendor does not respond within defined timelines:

| Day | Action |
|----|--------|
| Day 1 | Send appropriate template (A, B, or C) |
| Day 5 | If no response: send follow-up to same contact + CC vendor's senior contact |
| Day 10 | If still no response: internal escalation to your manager + legal review |
| Day 15 | If still no response: formal non-compliance notice with contract language cite |
| Day 20 | Contract review — consider cure notice or termination for cause language |

---

## COI Registry Setup

### Required Fields in Your COI Tracker

Maintain these fields for each vendor COI:

| Field | Notes |
|-------|-------|
| Vendor ID | Links to vendor master |
| Vendor Name | Legal entity |
| COI Document # | Track multiple versions |
| Date Received | |
| Policy Period Start | |
| Policy Period End | **Sort by this for expiration management** |
| Insurer Name | |
| Insurer AM Best Rating | A- or better recommended |
| GL Per Occurrence | |
| GL Aggregate | |
| Professional Liability | |
| Cyber Liability | |
| Workers Comp | Y/N + statutory |
| Auto Liability | If applicable |
| Additional Insured | Y/N + correct name confirmed |
| Waiver of Subrogation | Y/N |
| Current Compliance Score | 0-100 |
| Compliance Tier | Green/Yellow/Orange/Red |
| Last Review Date | |
| Next Review Date | 90 days out or at expiration |
| Gaps Identified | Free text |
| Remediation Status | Open/In Progress/Resolved |

### Alert Calendar Setup

Create these calendar alerts for every COI:
- **90 days before expiration:** "COI Renewal Request Due — [Vendor Name]"
- **60 days before expiration:** "COI Renewal Follow-Up — [Vendor Name]"
- **30 days before expiration:** "URGENT: COI Expiring — [Vendor Name]"
- **Day of expiration:** "COI EXPIRED — [Vendor Name] — HOLD NEW POs"

---

## Expected Outputs

After implementing Coverage Gate Matrix, you will have:
1. ✅ A complete COI registry with current status for every vendor
2. ✅ Standardized coverage minimums by vendor category
3. ✅ Compliance scores for every vendor (0-100)
4. ✅ Automated alerts for upcoming expirations
5. ✅ Documented remediation actions for any non-compliant vendors
6. ✅ A 30-day improvement plan for vendors in Orange/Red tiers
7. ✅ Audit trail for all compliance reviews and communications

**Time savings (typical):** 2-4 hours/week for a team managing 20+ vendors. Hours increase at scale — the system doesn't.

---

*Coverage Gate Matrix — Part of the Vendor & Compliance Operations Pack by Remy Claw*
*More at remyclaw.com | @Remy_Claw on X*
