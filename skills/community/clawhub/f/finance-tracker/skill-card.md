## Description:

Track personal expenses, recurring payments, savings goals, income, assets, currency conversion, reports, exports, and spending insights through a local finance CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[salen-project](https://clawhub.ai/user/salen-project)

### License/Terms of Use:

MIT

## Use Case:

Individuals and agents use this skill to record and review personal finance activity from the command line, including expenses, income, assets, goals, recurring payments, budgets, and exports. It is suited to single-user local tracking rather than shared or regulated financial recordkeeping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive financial records are stored in plaintext under ~/.finance-tracker.

Mitigation: Use it on a single-user machine, tighten local file permissions, and avoid storing highly sensitive records on shared systems.

Risk: Automated recurring processing can log due items without a manual review step.

Mitigation: Review due recurring items before running or scheduling finance recurring process.

Risk: Exported CSV files may carry untrusted transaction descriptions into spreadsheet software.

Mitigation: Review descriptions before opening CSV exports in spreadsheet apps, especially when entries came from chat or other untrusted text sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/salen-project/skills/finance-tracker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, CSV]

**Output Format:** [CLI text reports and command output, with optional Markdown log, JSON export, and CSV export.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores personal finance records locally under ~/.finance-tracker.]

## Skill Version(s):

2.0.0 (source: server release metadata and user changelog; artifact package.json declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
