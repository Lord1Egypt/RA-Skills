## Description:

ExpenseLog lets agents record conversational expense entries, categorize spending, track budgets, produce monthly reports, and export CSV data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

External users and personal finance assistants use this skill to log expenses from natural-language statements, review monthly category totals, monitor budgets, and export records for tax preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal expense details are stored in a local JSON file and may be sensitive.

Mitigation: Use an intentional local storage location, restrict file access, review logged entries for mistakes, and keep independent backups.

Risk: CSV exports can carry formula-like values that may execute when opened in spreadsheet software.

Mitigation: Sanitize formula-leading characters before opening exported CSV files in spreadsheet tools.

## Reference(s):

- [OpenClaw](https://github.com/openclaw/openclaw)
- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/expense-log)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, CSV]

**Output Format:** [Conversational text, markdown-style reports, JSON-like expense records, and CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores expense records locally and can summarize monthly totals by category.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
