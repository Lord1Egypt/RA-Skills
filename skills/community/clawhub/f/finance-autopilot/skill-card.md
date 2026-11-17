## Description:

A proactive personal finance manager for AI agents that tracks income and expenses, monitors subscriptions and bills, detects unusual spending, builds monthly budget reports, reminds users of payment due dates, and helps explain monthly cash flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agistack](https://clawhub.ai/user/agistack)

### License/Terms of Use:


## Use Case:

External users such as individuals, families, freelancers, and self-employed people use this skill to track personal income, expenses, bills, subscriptions, budgets, unusual spending, and annual financial patterns through natural conversation and forwarded receipts or invoices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may retain sensitive financial details in agent memory.

Mitigation: Use it only in trusted agent workspaces and require clear controls for memory retention, deletion, and access.

Risk: The skill may proactively surface budget summaries, bills, receipts, or alerts in shared contexts.

Mitigation: Configure morning briefings, proactive alerts, and budget reports so they appear only in private channels.

Risk: Forwarded receipts and invoices may include sensitive personal or financial information.

Mitigation: Forward financial documents intentionally and review the workspace's data handling before installing the skill.

## Reference(s):

- [Finance Autopilot on ClawHub](https://clawhub.ai/agistack/skills/finance-autopilot)
- [AGIstack publisher profile](https://clawhub.ai/user/agistack)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or conversational text with financial summaries, reminders, audits, alerts, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may rely on agent memory and user-forwarded financial documents; it does not perform payments or transfers.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
