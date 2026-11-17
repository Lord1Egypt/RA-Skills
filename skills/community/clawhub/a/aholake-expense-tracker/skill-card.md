## Description:

Track daily expenses in structured markdown files organized by month. Use when the user wants to log spending, view expense summaries, analyze spending patterns, or manage personal finance tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aholake](https://clawhub.ai/user/aholake)

### License/Terms of Use:


## Use Case:

Employees, external users, and personal finance users use this skill to log spending, maintain month-organized markdown expense records, and review category-level summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores spending history in local markdown files, which may contain sensitive personal finance details.

Mitigation: Avoid sensitive descriptions or tags, keep the workspace private, and review stored expense files before sharing or backing them up.

Risk: Conversation-derived expenses may be ambiguous or incorrectly categorized before they are persisted.

Mitigation: Confirm amount, category, date, and description with the user before logging expenses.

Risk: The helper script may read or write markdown files outside the intended expenses folder if workspace or date/month inputs are misused.

Mitigation: Use trusted input, prefer an explicit trusted workspace path, and harden date and month validation before shared or automated use.

## Reference(s):

- [Expense Categories](references/categories.md)
- [ClawHub Skill Page](https://clawhub.ai/aholake/skills/aholake-expense-tracker)
- [Publisher Profile](https://clawhub.ai/user/aholake)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; expense data is stored as markdown tables and summaries can be emitted as text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local monthly expense files under an expenses directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
