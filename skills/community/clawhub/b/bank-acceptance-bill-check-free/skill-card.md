## Description:

A local Chinese-language checker for bank acceptance bill ledgers that recalculates maturity dates, reconciles receivable bill balances, flags duplicate bill numbers, missing or placeholder statuses, non-positive amounts or terms, and redeemed bills still counted in balance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and treasury users use this skill to check a bank acceptance bill ledger before month-end reconciliation or maturity/payment review. It is intended to surface ledger arithmetic and completeness issues, not to verify the authenticity or legal enforceability of bills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The advertised scope is inconsistent about which financial checks are actually run.

Mitigation: Treat the report as a local ledger-assistance output and manually verify maturity-date scope, omitted checks, and any operational financial conclusions before relying on it.

Risk: The checker does not verify bill authenticity, legal enforceability, or external payment-system records.

Mitigation: Confirm bill validity and recourse status through the accepting bank, ECDS, or qualified legal and finance review before taking action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/bank-acceptance-bill-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Plain text or JSON report with findings, summary totals, executed checks, withheld checks, and missing-input guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers when issues are detected; insufficient input returns missing fields instead of a clean-result conclusion.]

## Skill Version(s):

1.0.60 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
