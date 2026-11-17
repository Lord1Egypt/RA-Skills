## Description:

Expense tracker - log expenses, categorize by type, track against budget, flag overspending. Monthly cron or on-demand.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ceobotson-bot](https://clawhub.ai/user/ceobotson-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Business owners and finance operators use this skill to log expenses, categorize spending, compare monthly totals against budgets, and generate reports for review or tax preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may handle sensitive financial records, receipts, reports, and tax-related exports.

Mitigation: Use private storage, restrict access to expense logs and receipt folders, and set retention rules for reports and exports.

Risk: Optional bank, card, Google Sheets, and chat delivery integrations can expose financial data through connected services.

Mitigation: Review each connector's access scope before installation and use private delivery channels for alerts and reports.

Risk: Automatically logged or categorized expenses may be inaccurate.

Mitigation: Confirm each expense before saving and review monthly reports before using them for budget or tax decisions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ceobotson-bot/skills/doctorclaw-expense-tracker)
- [DoctorClaw website](https://www.doctorclaw.ceo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured text with optional CSV export guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce monthly expense reports, budget alerts, categorized expense entries, and export instructions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
