## Description:

Budget helps users manually set budgets, log expenses, monitor category status, and receive local-only budget alerts without bank connections or external financial services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agistack](https://clawhub.ai/user/agistack)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use Budget to maintain local personal budget records, manually log income and expenses, check spending against category limits, and plan budget reallocations without connecting to financial accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store sensitive budget, income, and expense records locally.

Mitigation: Review the skill before installing with real financial data, keep appropriate backups, and manage retention or deletion of local records deliberately.

Risk: Budget records can be changed through write operations such as setting budgets, logging expenses, and reallocating category limits.

Mitigation: Preview and confirm changes where supported, especially reallocations, and avoid delete or bulk-delete workflows unless the user can inspect the affected records first.

Risk: Malformed numeric inputs such as negative values, NaN, or infinity could create misleading budget records until stronger validation is added.

Mitigation: Validate amount, date, and category values before running scripts or accepting generated commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agistack/skills/budget-pro)
- [Budget Setup](references/budget-setup.md)
- [Expense Tracking](references/expense-tracking.md)
- [Budget Alerts and Thresholds](references/alerts.md)
- [Reports and Analysis](references/reports.md)
- [Overage Recovery](references/overage-recovery.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance and command output with local JSON-backed budget records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses manual user-entered budget and expense data; does not require bank credentials or external financial service access.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
