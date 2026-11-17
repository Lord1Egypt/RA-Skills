## Description:

Bank Statement Reconciler helps agents parse bank statements and order or invoice records, match transactions, and report matched items, differences, unclaimed funds, and unmatched orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiji0802](https://clawhub.ai/user/qiji0802)

### License/Terms of Use:

MIT-0

## Use Case:

Finance teams, operators, and agents use this skill to reconcile bank, payment platform, and ecommerce transaction files against orders or invoices. It supports exact, fuzzy, and tier-gated semantic matching, then summarizes matched records, differences, unclaimed payments, and unpaid orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive bank, customer, invoice, and order data.

Mitigation: Review and control how financial files are processed, and restrict access to reconciliation inputs and outputs.

Risk: Generated spreadsheets from untrusted inputs may create spreadsheet-export safety risk until formula neutralization is added.

Mitigation: Avoid opening generated spreadsheets from untrusted inputs, and sanitize or neutralize formulas before distribution.

Risk: Duplicate or repeated amounts can produce incorrect reconciliation matches.

Mitigation: Manually verify matches, especially repeated amounts, differences, unclaimed funds, and unmatched orders.

Risk: Sharing output to Feishu or another external service can expose sensitive reconciliation results.

Mitigation: Require explicit approval before sending reconciliation data to Feishu or any external service.

## Reference(s):

- [Supported Formats](artifact/references/supported-formats.md)
- [ClawHub Skill Page](https://clawhub.ai/qiji0802/skills/bank-statement-reconciler)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Configuration]

**Output Format:** [Structured reconciliation results with optional Excel or CSV exports, JSON dictionaries, and Feishu interactive card payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tier settings control statement limits, export formats, platform support, semantic matching, and Feishu card availability.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
