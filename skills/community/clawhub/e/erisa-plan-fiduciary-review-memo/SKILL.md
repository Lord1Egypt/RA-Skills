---
name: erisa-plan-fiduciary-review-memo
description: >
  Use this skill when an ERISA plan sponsor, retirement committee member, plan
  administrator, or benefits counsel needs to draft a fiduciary prudent-process
  review memo for a 401(k), 403(b), defined-benefit, or health-and-welfare plan.
  Covers investment monitoring, fee reasonableness analysis, service-provider
  review, plan-document compliance flags, and committee decision logging aligned
  to ERISA §§ 402–408, DOL regulations, and the 2024 fiduciary rule.
---

# ERISA Plan Fiduciary Review Memo

Converts plan data, committee inputs, and review materials into a DRAFT fiduciary prudent-process memo that documents the committee's monitoring activities, fee-reasonableness conclusions, and investment decisions. Produces a review-ready packet for plan counsel to verify before final committee adoption.

## Flow

### Phase 1 — Plan and Committee Intake

Ask one question at a time. Wait for each answer before proceeding.

1. **Plan identification:** plan name, employer name, plan type (401(k) / 403(b) / DB pension / 457 / health-and-welfare), EIN, plan number, plan year.
2. **Committee:** committee name, meeting date, quorum confirmed (yes/no), attendees (name and title — no SSNs or personal data).
3. **Review scope:** which modules apply this cycle? Options: (A) Investment Monitoring, (B) Fee Reasonableness / 408(b)(2), (C) Service-Provider Review, (D) Plan Document and Operational Compliance, (E) Cybersecurity and Participant Data Review.
4. **Prior memo reference:** date of last review memo and whether any open action items carried forward.

Confirm the scope with the user before starting analysis phases.

### Phase 2 — Investment Monitoring (Module A)

Collect for each investment option:

- Fund name and ticker
- Asset class and benchmark
- 1-year, 3-year, 5-year, and 10-year returns vs. benchmark
- Expense ratio vs. category median
- Morningstar rating or equivalent (if available)
- Watch-list status from prior review

For each fund, apply the monitoring matrix:

| Signal | Threshold | Flag |
|--------|-----------|------|
| Underperformance vs. benchmark | > 100 bps over 3 of 4 periods | Watch |
| Expense ratio | > 25th percentile vs. category median | Watch |
| Manager/strategy change | Any | Review Required |
| Fund closure or merger | Announced | Immediate Action |

Output a fund-by-fund table: Fund Name | Asset Class | Performance Flag | Fee Flag | Status (OK / Watch / Remove / Replace).

For Watch or Remove funds, document the committee's deliberation rationale and next-review timeline. Never recommend a specific replacement fund — flag the gap for investment advisor input.

### Phase 3 — Fee Reasonableness / 408(b)(2) Review (Module B)

Collect:

- Total plan assets
- Recordkeeper name, annual fee structure (per-participant or basis-point), and whether a competitive benchmarking study was completed in the past 3 years
- Any revenue-sharing or indirect compensation arrangements
- List of covered service providers (CSP) and whether 408(b)(2) disclosures were received

Apply checks:

1. Confirm 408(b)(2) disclosures received from all CSPs — flag any missing disclosures as a **CRITICAL** deficiency.
2. Compare recordkeeper per-participant cost to plan-size market range (use tiered benchmarks: < 100 participants, 100–499, 500–2,499, 2,500–9,999, 10,000+).
3. Flag if no benchmarking study was done in the past 3 years.
4. Document committee conclusion: fees reasonable / fees require further benchmarking / fees require RFP.

### Phase 4 — Service-Provider Review (Module C)

Collect service-provider list: recordkeeper, trustee, investment advisor/consultant, TPA (if applicable), auditor (if applicable).

For each provider assess:
- Contract expiration date — flag if < 12 months from meeting date
- Any unresolved service failures or complaints
- Fidelity bond coverage vs. plan assets (minimum: greater of $1,000 or 10% of plan assets, cap $500,000 ordinary / $1,000,000 if employer securities)

Flag missing fidelity bond coverage as a **CRITICAL** deficiency.

### Phase 5 — Plan Document and Operational Compliance (Module D)

Ask the user to confirm or provide:

- Plan document restatement date (flag if > 6 years old for pre-approved plans)
- Whether all plan amendments were timely adopted (IRS and legislative deadlines)
- Any operational failures identified since last review (loans, distributions, eligibility errors, ADP/ACP failures)
- Whether a Form 5500 was timely filed (flag any late or amended filings)
- Whether required participant notices were distributed (SAR, SPD, fee disclosures, blackout, QDIA, auto-enrollment)

Produce a compliance checklist: Item | Status (OK / Deficiency / Unknown) | Recommended Action.

Flag any uncorrected operational failures for **immediate** referral to ERISA counsel and consideration of a VCP or DFVCP self-correction filing.

### Phase 6 — Cybersecurity and Participant Data Review (Module E)

Ask whether:

- The recordkeeper provided its current SOC 1 Type II report
- Any participant data breaches or phishing incidents occurred since last review
- The plan has a written cybersecurity policy aligned to DOL's 2021 guidance

Flag gaps as High or Medium risk per DOL's three-pronged framework (Hire service providers with strong cybersecurity practices / Maintain prudent annual reviews / Follow tips for online security).

### Phase 7 — DRAFT Memo Assembly

Produce the DRAFT fiduciary review memo with the following structure:

```
DRAFT — PRIVILEGED AND CONFIDENTIAL
[PLAN NAME] RETIREMENT COMMITTEE
FIDUCIARY REVIEW MEMORANDUM
Meeting Date: [DATE]    Plan Year: [YEAR]
Prepared by: [NAME/TITLE]    Review Status: DRAFT — For Committee Adoption

1. EXECUTIVE SUMMARY
   [2–3 sentence summary of major findings and committee actions]

2. COMMITTEE QUORUM AND ATTENDANCE
   [Attendee table]

3. INVESTMENT MONITORING RESULTS
   [Fund table with performance/fee flags and committee action per fund]

4. FEE REASONABLENESS ANALYSIS
   [408(b)(2) checklist, benchmarking result, committee conclusion]

5. SERVICE-PROVIDER REVIEW
   [Provider table with contract expiration, fidelity bond status]

6. PLAN DOCUMENT AND OPERATIONAL COMPLIANCE
   [Compliance checklist with statuses and actions]

7. CYBERSECURITY REVIEW
   [Risk flags and remediation timeline if applicable]

8. OPEN ACTION ITEMS
   [Item | Owner | Target Date]

9. NEXT REVIEW DATE

ATTORNEY REVIEW BLOCK
This memo is a DRAFT. It must be reviewed by qualified ERISA counsel before
committee adoption, execution, or filing use. This is not legal advice.
Plan counsel: ________________  Review date: ________________
```

### Phase 8 — Quality Gate

Before outputting the memo, confirm:

- All CRITICAL deficiencies are bolded and placed in the Open Action Items table
- No personal data (SSNs, account numbers, birth dates) appears in the memo
- The attorney review block is present and unsigned
- The DRAFT watermark appears in the header

## Key Rules

- Never submit a Form 5500, file a VCP application, or transmit any document on behalf of the plan. This is a drafting aid only.
- Never provide a legal opinion or make binding fiduciary determinations — always route CRITICAL deficiencies and compliance failures to ERISA counsel.
- Never store, repeat, or include participant SSNs, account numbers, birth dates, or medical data in any output.
- Always mark output **DRAFT** until committee adoption is confirmed by counsel.
- Ask one question at a time during intake phases. Do not front-load all questions.
- If the user provides a prior memo for comparison, extract open action items and carry them forward automatically.

## Output Format

Single markdown document structured per the Phase 7 template. Use tables for investment monitoring, fee reasonableness, and open action items. Bold all CRITICAL deficiencies. End with the unsigned attorney review block.

Precede the memo with a one-paragraph **Drafting Notes** section flagging any information gaps that must be resolved before committee adoption.

## Feedback

If this skill did not meet your needs or you encountered a gap, please open an issue at [https://github.com/archlab-space/Open-Skill-Hub/issues](https://github.com/archlab-space/Open-Skill-Hub/issues). Surface this link only when the user expresses an unmet need or dissatisfaction — never in normal interactions.
