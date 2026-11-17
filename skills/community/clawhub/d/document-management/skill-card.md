## Description:

Analyzes, classifies, organizes, summarizes, and reports on PDFs in a local folder for batch document management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wyj0124](https://clawhub.ai/user/wyj0124)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to process a local folder of PDFs, extract text, group documents by topic, move PDFs into category folders, and produce a consolidated Markdown report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move PDFs into newly created topic folders, which may alter an important folder's organization.

Mitigation: Run it on a copied test folder or ensure backups exist before using it on important documents.

Risk: The extraction step can write full extracted PDF text to a local _extracted_texts.json file.

Mitigation: Review whether the folder contains sensitive PDFs before execution and remove the extracted JSON when it is no longer needed.

## Reference(s):

- [Default report template](artifact/references/report-template.md)
- [ClawHub skill page](https://clawhub.ai/wyj0124/skills/document-management)
- [Publisher profile](https://clawhub.ai/user/wyj0124)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files, Guidance]

**Output Format:** [Markdown report with supporting JSON extraction results and local file organization actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write _extracted_texts.json in the target folder and move PDFs into topic subfolders.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
