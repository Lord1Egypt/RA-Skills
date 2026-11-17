## Description:

Generates Word (.docx) reports and Excel (.xlsx) workbooks as downloadable files for SMSF, accounting, compliance, and business document workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mysmsf](https://clawhub.ai/user/mysmsf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business practitioners use this skill to create draft SMSF reports, trustee summaries, checklists, budget workbooks, invoice layouts, and simple spreadsheet exports as real Word or Excel files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spreadsheet text from untrusted JSON may be interpreted as an active formula by spreadsheet software.

Mitigation: Use trusted JSON data for spreadsheets and review cells that begin with formula characters before sharing workbooks.

Risk: Python dependencies are version-ranged rather than pinned.

Mitigation: Install in a virtual environment and pin dependency versions for repeatable deployments.

Risk: Generated SMSF, accounting, and compliance documents may be mistaken for final professional advice or compliant filings.

Mitigation: Treat generated documents as drafts and require review by a qualified accountant, auditor, or adviser before client or regulator use.

Risk: The skill writes user-requested files to disk.

Mitigation: Write only to user-approved locations and overwrite existing files only when explicitly authorized.

## Reference(s):


## Skill Output:

**Output Type(s):** [files, shell commands, configuration, guidance]

**Output Format:** [DOCX and XLSX files generated from command-line arguments or JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates draft .docx and .xlsx files; refuses to overwrite existing outputs unless --force is used.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
