## Description:

Email Ledger parses .eml mail files from ZIP archives or directories, extracts reporting fields, generates an Excel ledger, and can append new records to an existing ledger with duplicate detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operations teams use this skill to convert batches of reporting emails into a structured Excel ledger. It is intended for workflows where users provide .eml files or ZIP archives and may optionally provide an existing workbook for append-and-deduplicate processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill parses potentially sensitive email attachments and writes extracted summaries, names, and addresses into an XLSX ledger.

Mitigation: Use it only with authorized email data and handle generated workbooks according to the same access controls and retention rules as the source messages.

Risk: The workflow uploads the generated ledger through a separate uploader.

Mitigation: Require explicit user confirmation before upload and share the resulting download link only with intended recipients.

Risk: The security summary flags unsafe ZIP and Excel handling.

Mitigation: Use trusted, reasonably sized ZIP archives, add cleanup and size limits before broad use, and open generated spreadsheets with appropriate spreadsheet protections.

## Reference(s):

- [Parsing Rules Reference](artifact/references/parsing_rules.md)
- [ClawHub Skill Listing](https://clawhub.ai/smallkeyboy/skills/email-ledger)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Excel workbook plus Markdown status summary with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an .xlsx ledger containing extracted email metadata, classification fields, summaries, deduplicated rows, highlighted fields needing manual completion, and optional upload guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
