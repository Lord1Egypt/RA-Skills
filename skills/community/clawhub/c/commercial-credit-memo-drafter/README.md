# Commercial Credit Memo Drafter

**Platforms:** Claude · Openclaw · Codex
**Domain:** Banking — Commercial Credit

## Purpose

A credit-memo drafting partner for commercial loan officers, credit analysts, and underwriters. Turns borrower financials, a loan request, collateral, and guarantor information into a structured DRAFT Credit Analysis Memorandum (CAM) organized around the 5 Cs of credit, with computed ratios, a risk-rating recommendation, a covenant package, and exception flags.

## When to Use

- Drafting a CAM for a working-capital line, term loan, equipment loan, owner-occupied or investor CRE, construction, acquisition, refinance, or M&A facility
- Standardizing the 5Cs analysis across borrowers and facilities
- Producing the headline ratios, sensitivity rows, and covenant package for credit-committee review
- Flagging policy exceptions and proposing mitigants
- Preparing renewal / annual-review memos when historical and projected figures are available

## What It Does

**Phase 1: Intake**
1. Captures institution, policy framework (bank, SBA 7(a)/504, USDA B&I, CDFI), and risk-rating scale
2. Captures loan request: purpose, structure, use of proceeds, repayment sources, sponsor equity
3. Captures borrower: ownership, business model, customer concentration, management depth, 3Y + interim financials, projected financials, existing debt schedule, add-backs
4. Captures collateral, guaranties, insurance, and conditions / market context
5. Restates every fact with Confirmed / Assumed / Unknown tags and shows headline ratios before drafting

**Phase 2: Drafting**
6. Drafts a 5Cs-structured memo (Character, Capacity, Capital, Collateral, Conditions)
7. Computes Global DSCR, fixed-charge coverage, senior and total leverage, LTV, LTC, current and quick ratios, working-capital coverage, Debt/TNW, liquidity-to-debt-service
8. Runs sensitivity rows (revenue −10%, gross margin −200bps, rate +200bps)

**Phase 3: Risk and recommendation**
9. Recommends a risk rating with named drivers
10. Proposes a covenant package tied to the headline ratios
11. Flags policy exceptions with rationale and mitigant
12. Recommends Approve as proposed / Approve with conditions / Counter-structure / Decline

## Output

A DRAFT memo with:

- Executive summary
- Loan request and borrower overview
- 5Cs sections with figures and source tags
- Headline-ratios table with policy thresholds and pass/watch/fail flags
- Sensitivity rows
- Risk-rating recommendation with drivers
- Proposed covenant package
- Policy-exceptions table with mitigants
- Evidence matrix
- Unresolved-questions list

## Safety

This skill drafts a recommendation, **not** a decision. Every output is labeled **DRAFT — CREDIT OFFICER MUST REVIEW**. Cash flow is treated as the primary repayment source; collateral-only repayment is flagged. The skill never invents financial figures, projects more than 12 months past user-supplied data, or pastes bureau / KYC / OFAC / BSA-AML data verbatim. All borrower data is treated as confidential and is never written to external services.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
