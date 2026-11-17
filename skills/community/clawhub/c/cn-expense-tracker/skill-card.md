## Description:

Chinese personal expense tracking assistant for recording expenses, reviewing monthly statistics, setting budgets, comparing spending trends, and exporting CSV data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking users and agents use this skill for local personal bookkeeping: adding expense records, listing and deleting records, generating monthly reports, setting budgets, comparing monthly trends, and exporting expense data for spreadsheet analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal expense data is stored as local JSON files under ~/.qclaw/workspace.

Mitigation: Use the skill only on trusted machines and include the workspace in normal local backup and access-control practices.

Risk: Deleted expense records are treated as permanent.

Mitigation: Review record IDs before running delete commands and keep backups when records need to be recoverable.

Risk: Exported CSV files can carry spreadsheet formula risks if record text starts with =, +, -, or @.

Mitigation: Inspect or sanitize exported CSV values before opening them in spreadsheet software.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-expense-tracker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and plain-text CLI output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, update, delete, and export local expense files under ~/.qclaw/workspace when the generated commands are executed.]

## Skill Version(s):

1.2.6 (source: server release metadata, released 2026-06-07)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
