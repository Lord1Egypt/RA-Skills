## Description: <br>
Capture receipt details, categorize spending, and generate monthly reports from a local SQLite ledger. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mehulupase01](https://clawhub.ai/user/mehulupase01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers can use this skill to record receipt or spending details, keep categories consistent, review monthly totals against budgets, and export expense records for reimbursement or spreadsheet workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Receipt records, notes, and CSV exports may contain sensitive spending or account details stored on the local filesystem. <br>
Mitigation: Use a trusted local runtime and export folder, avoid entering secrets or full account numbers, and restrict access to generated SQLite and CSV files. <br>
Risk: Receipt OCR or transcription may be incomplete or ambiguous, leading to incorrect merchant, amount, currency, category, or line-item data. <br>
Mitigation: Mark ambiguous fields as inferred, keep totals and currencies aligned with the source receipt, and avoid fabricating unreadable line items. <br>
Risk: CSV export paths are user supplied and can write expense records to an unintended location. <br>
Mitigation: Review the output path before exporting and choose a trusted folder for generated CSV files. <br>


## Reference(s): <br>
- [Category Rules](references/category-rules.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/mehulupase01/expense-snap) <br>
- [Project Homepage](https://github.com/Mehulupase01/openclaw-skill-suite/tree/main/skills/expense-snap) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; helper script emits JSON responses and CSV exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores receipt data locally in SQLite under the skill runtime directory and can write month-filtered CSV exports.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
