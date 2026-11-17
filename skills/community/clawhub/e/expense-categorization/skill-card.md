## Description:

Receipt OCR, GL code mapping, policy compliance checking, and anomaly detection for business expenses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, finance teams, and developers use this skill to extract receipt data, map expenses to GL codes, check policy compliance, flag anomalies, and prepare expense batches for review or accounting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Expense documents can contain sensitive personal, payment, tax, vendor, or travel details.

Mitigation: Install only where the agent is permitted to process those documents and maintain appropriate audit logs or sampling for reviewed and auto-approved expenses.

Risk: Incorrect categorization, policy evaluation, QuickBooks posting, or reimbursement approval could affect accounting records or payments.

Mitigation: Configure thresholds to the company's policy and require the intended human review step before QBO posting or reimbursement payment.

Risk: Low-confidence OCR or anomaly decisions may be unreliable for handwritten, incomplete, unusual, duplicate, or out-of-policy receipts.

Mitigation: Route low-confidence, anomalous, missing-receipt, duplicate, and out-of-policy cases to human review before approval.

## Reference(s):

- [GL Code Mapping Reference](references/gl-mapping.md)
- [Standard Expense Policy Rules](references/policy-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON records, CSV batch summaries, bash examples, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes low-confidence, anomalous, out-of-policy, posting, and reimbursement decisions to human review.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
