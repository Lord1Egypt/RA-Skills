## Description:

Capture receipt details, categorize spending, and generate monthly reports from a local SQLite ledger.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mehulupase01](https://clawhub.ai/user/mehulupase01)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers can use this skill to convert receipt text or image transcriptions into structured expense records, review monthly spending, compare category budgets, and export reimbursement-ready CSV data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Receipt and spending details are stored in a local SQLite database inside the skill runtime directory.

Mitigation: Install only when local storage of expense details is acceptable, and protect the runtime directory as sensitive financial data.

Risk: CSV exports can contain sensitive receipt fields and may overwrite a user-selected output path.

Mitigation: Export only to intended locations, avoid overwriting important files, and treat generated CSV files as sensitive.

Risk: Receipt fields from untrusted text or OCR can produce unsafe or misleading spreadsheet content when exported.

Mitigation: Review receipt fields before export and be cautious when opening CSV files in spreadsheet applications.

## Reference(s):

- [Category Rules](references/category-rules.md)
- [ClawHub skill page](https://clawhub.ai/mehulupase01/skills/expense-snap)
- [Project homepage](https://github.com/Mehulupase01/openclaw-skill-suite/tree/main/skills/expense-snap)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python shell commands and JSON or CSV results from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores receipt records in a local SQLite database and can export monthly records to CSV.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
