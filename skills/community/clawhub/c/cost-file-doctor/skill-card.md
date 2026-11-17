## Description:

Diagnoses construction-cost files for format, likely encryption, and local parseability, then recommends practical next steps and can clean repeated headers in exported spreadsheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kormendierijon681-oss](https://clawhub.ai/user/kormendierijon681-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cost-engineering professionals use this skill to identify construction-cost file formats, assess whether files may be encrypted or locally parseable, and choose a practical way to inspect them. It can also remove repeated page headers and normalize exported Excel workbooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented export search can inspect parent and sibling folders beyond the selected project folder.

Mitigation: Restrict searches to the selected project folder and approve any expansion.

Risk: The optional cloud viewer requires uploading project documents.

Mitigation: Avoid uploading sensitive documents; use local or vendor tools when confidentiality matters.

Risk: Encryption diagnoses can be provisional, especially for OLE files.

Mitigation: Treat the diagnosis as provisional and verify using the source application or a known export.

## Reference(s):

- [造价文件诊断器 on ClawHub](https://clawhub.ai/kormendierijon681-oss/skills/cost-file-doctor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files]

**Output Format:** [Markdown diagnostic guidance with shell commands; optionally a cleaned Excel workbook (.xlsx).]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Spreadsheet cleanup produces a separate workbook; diagnostic conclusions depend on the supplied file evidence.]

## Skill Version(s):

1.0.0 (source: package.json and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
