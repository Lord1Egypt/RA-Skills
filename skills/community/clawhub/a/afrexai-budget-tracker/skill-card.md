## Description:

Budget & Expense Tracker helps an AI agent log personal income and expenses, enforce category budgets, track recurring transactions and savings goals, and produce financial summaries from local workspace files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1kalin](https://clawhub.ai/user/1kalin)

### License/Terms of Use:


## Use Case:

Individuals use this skill with an AI agent to maintain a local personal finance ledger, monitor spending against budgets, manage savings goals, and request weekly, monthly, or year-to-date reports. It is intended for conversational personal budgeting rather than regulated financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores detailed financial records in local workspace JSON files.

Mitigation: Keep budget files out of shared folders and repositories, and review file permissions before recording sensitive transactions.

Risk: Natural language requests can log, export, change, or undo financial records.

Mitigation: Require explicit confirmation before logging transactions, exporting data, changing budgets, or undoing records.

Risk: Backup guidance can expose financial history if ledger files are committed to git.

Mitigation: Avoid committing budget files unless repository remotes and history retention are understood and approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1kalin/skills/afrexai-budget-tracker)
- [Artifact README](artifact/README.md)
- [Artifact skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, JSON files, CSV]

**Output Format:** [Conversational text and Markdown with local JSON ledger/profile files and optional CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores financial profile, ledger, savings goal, and recurring transaction data locally in workspace files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
