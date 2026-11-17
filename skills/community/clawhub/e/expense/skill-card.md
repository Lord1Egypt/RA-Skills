## Description:

Expense helps agents track, categorize, analyze, and report personal, reimbursement, freelance, and small business expenses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duclawbot](https://clawhub.ai/user/duclawbot)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals, employees, freelancers, and small business owners use this skill to capture expenses, organize receipts, prepare reimbursement reports, monitor budgets, and assemble tax-ready expense summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may share more sensitive financial details than the expense-tracking task requires.

Mitigation: Ask for only the minimum needed details and redact account numbers, full card numbers, tax identifiers, and unrelated receipt data.

Risk: Broad trigger terms such as budget or receipt may activate the skill outside a clear expense-tracking request.

Mitigation: Confirm the user wants expense-tracking help before collecting, organizing, or analyzing financial information.

Risk: Expense, reimbursement, or tax guidance may not match a specific employer policy or jurisdiction.

Mitigation: Have users verify reports and deductions against company policy, accountant guidance, and applicable tax rules before submission.

## Reference(s):

- [Expense Skill Page](https://clawhub.ai/duclawbot/skills/expense)
- [Publisher Profile](https://clawhub.ai/user/duclawbot)
- [Usage Examples](artifact/examples.md)
- [Heartbeat Guide](artifact/heartbeat.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with expense logs, checklists, categorized summaries, and expense report drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code; outputs may include financial recordkeeping suggestions and user-provided expense summaries.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
