## Description:

Bank Reconciler Pro helps agents reconcile bank statements against orders or invoices by parsing CSV, Excel, PDF, JSON, or text inputs and returning matched transactions, differences, unclaimed payments, unmatched orders, summaries, and optional exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yk-global-01](https://clawhub.ai/user/yk-global-01)

### License/Terms of Use:

MIT-0

## Use Case:

Finance operators, developers, and agents use this skill to compare bank, payment-platform, marketplace, order, and invoice records and identify matched payments, amount differences, unclaimed funds, and unpaid orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive financial files and can produce reports containing transaction, counterparty, order, and invoice data.

Mitigation: Use it only with data the operator is authorized to process, review results before business action, and keep generated exports in approved storage.

Risk: The skill can prepare Feishu messages or cards that share reconciliation summaries outside the local workflow.

Mitigation: Send Feishu reports only to approved chats after confirming the destination and data-sharing policy.

Risk: PDF parsing invokes an external command-line parser.

Mitigation: Run PDF parsing in a constrained environment and treat input PDFs and generated spreadsheets as untrusted until reviewed.

## Reference(s):

- [Supported formats](references/supported-formats.md)
- [ClawHub skill page](https://clawhub.ai/yk-global-01/skills/bank-reconciler-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with Python examples plus structured reconciliation results, JSON-style Feishu cards, and optional Excel or CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include sensitive financial reconciliation data and generated spreadsheet paths.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
