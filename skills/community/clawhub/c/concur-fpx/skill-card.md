## Description:

Read SAP Concur expense data from a shell — your expense reports, each report's line items (vendor, type, amounts, receipts, exceptions), and available expenses not yet on a report — through the user's signed-in Concur browser tab with the fpx CLI. Use when asked about Concur expenses, expense reports, reimbursement/payment status, what's unsubmitted, or unassigned card/receipt expenses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Employees can use this skill to review their SAP Concur expense reports, line items, reimbursement or payment status, and expenses that have not yet been assigned to a report. It reads data from the user's signed-in Concur account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Expense reports and line items may contain sensitive financial or personal information.

Mitigation: Use only the intended signed-in Concur account and keep returned expense data within authorized, private workflows.

Risk: ClawScan reports a benign verdict with medium confidence and notes that some local references could not be resolved.

Mitigation: Review the unresolved references and assess whether the evidence gap matters before installing.

## Reference(s):

- [Concur recipes](references/recipes.md)
- [Concur spend-graphql operations](references/operations.md)
- [ClawHub release](https://clawhub.ai/chrischall/skills/concur-fpx)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Concur expense data as JSON, with shell and jq usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only query results; report writes and receipt image downloads are not exposed.]

## Skill Version(s):

0.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
