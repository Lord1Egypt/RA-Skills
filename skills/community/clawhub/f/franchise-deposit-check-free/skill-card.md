## Description:

加盟保证金与费项结算核对（免费版） helps users locally recompute franchise deposit balances, fee amounts, totals, duplicate fee lines, over-deductions, missing cells, and negative amounts from headered settlement table text, with each finding tied to the source line and franchisee.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and settlement staff at franchise headquarters or regional operators use this skill to check franchisee deposit and fee settlement tables before monthly reconciliation, billing, payment, or deposit refund workflows. It is limited to arithmetic and table tie-out checks, not contract, compliance, tax, or bank-ledger verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat arithmetic table checks as legal, compliance, contract, tax, or bank-ledger verification.

Mitigation: Use the output only as a local settlement-table reconciliation aid; confirm contract terms, compliance questions, tax treatment, and payment status against authoritative contracts, policies, invoices, receipts, and bank records.

Risk: Incomplete headers, blank key cells, placeholder values, or malformed pasted table text can prevent reliable conclusions.

Mitigation: Provide a complete headered settlement table, use 0 only when no activity is confirmed, and treat insufficient-input output as no conclusion rather than as a clean result.

Risk: The free version omits cross-franchise, cross-period, and deeper attribution analyses that may still matter before final settlement action.

Mitigation: Review the checks-not-run list and perform the omitted analyses separately when settlement decisions depend on cross-period balances, fee-rate attribution, basis attribution, or deduction justification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/franchise-deposit-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable console text or JSON containing scope, findings, summary, checks executed, checks withheld, notes, and disclaimers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers and franchisee or fee context; insufficient input returns missing-field guidance without a pass/fail conclusion.]

## Skill Version(s):

1.0.6 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
