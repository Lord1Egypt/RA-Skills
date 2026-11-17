## Description:

AI-powered financial tracking for solopreneurs that helps log income and expenses, monitor revenue goals, generate profit-and-loss snapshots, flag cash-flow risks, and maintain a running financial picture without spreadsheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdssen](https://clawhub.ai/user/clawdssen)

### License/Terms of Use:

CC-BY-NC-4.0

## Use Case:

External solopreneurs and small-business operators use this skill to configure an agent as a lightweight finance tracker for local income logs, expense logs, revenue targets, monthly summaries, cash-flow flags, and rough tax reserve estimates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advanced automation can send recurring financial summaries externally when the cron example is configured with announcement and destination options.

Mitigation: Review the advanced automation before use; do not run the cron example with announcement or destination options unless recurring external summaries are intentional and the scheduled task can be removed.

Risk: Financial, tax, legal, and investment outputs are rough organizational estimates, not professional advice.

Mitigation: Treat summaries and tax reserves as tracking aids only, and consult qualified professionals for financial, tax, legal, or investment decisions.

Risk: Local finance files may contain sensitive business information.

Mitigation: Keep finance files local, avoid storing account numbers, full card numbers, or banking credentials, and record only the amounts and vendors needed for business tracking.

## Reference(s):

- [Financial Tracker Advanced Patterns](references/advanced-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/clawdssen/skills/agentledger-financial-tracker)
- [The Agent Ledger](https://www.theagentledger.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file templates, JSON state examples, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local finance logs, summaries, dashboards, and reminders; optional cron examples may send summaries externally when configured.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
