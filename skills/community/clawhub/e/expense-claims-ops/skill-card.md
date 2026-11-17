## Description:

Process personal/work expenses and reimbursement claims in a structured, low-friction workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[austineyapp](https://clawhub.ai/user/austineyapp)

### License/Terms of Use:


## Use Case:

Employees and operations staff use this skill to turn receipts and expense details into claim-ready summaries, blocked-item fixes, totals, and follow-up drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated claim summaries may include personal or business-sensitive expense details or receipt information.

Mitigation: Review summaries before submission and handle receipts according to the organization's expense and data-handling policies.

Risk: Claim readiness can be wrong when policy rules are not provided or source receipts are incomplete.

Mitigation: Mark policy checks as "policy not provided" and verify blocked items, totals, and exceptions before submitting.

## Reference(s):

- [Claim Templates](references/claim-templates.md)
- [Expense Item Schema](references/expense-schema.md)
- [Ops Cadence](references/ops-cadence.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Concise Markdown sections with totals, blocked-item reasons, checklists, and follow-up draft text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maximum of three sections: Ready, Blocked, Next action; includes totals and missing-document count.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
