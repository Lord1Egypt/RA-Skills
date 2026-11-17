## Description:

A local file-writing skill for enterprise security policy environments that writes authorized text, code, configuration, DOCX, and XLSX files with encoding-aware handling; it does not provide encryption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[endcy](https://clawhub.ai/user/endcy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and employees use this skill to write or append content to local files they are already authorized to access, especially when encoding-safe output or simple DOCX/XLSX creation is needed. It should not be used for encryption or to bypass file access controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may assume the skill encrypts files because the release is named Encrypted File Writer.

Mitigation: Treat it as a local file writer only; use operating-system encryption or dedicated encryption tools when encryption is required.

Risk: Overwrite and append modes can change or destroy existing local file contents.

Mitigation: Back up important files and review target paths before using overwrite or append.

Risk: Spreadsheet append mode can destroy existing workbook data.

Mitigation: Avoid XLSX append on existing workbooks unless the workbook can be regenerated or restored.

Risk: Appending to untrusted DOCX files can preserve unsafe or unexpected document content.

Mitigation: Do not append to untrusted DOCX files; create a new document from trusted content when possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/endcy/skills/encrypted-file-writer)
- [Skill Definition](artifact/SKILL.md)
- [README](artifact/README.md)
- [Verification Report](artifact/VERIFICATION_REPORT.md)
- [Fix Report v1.2.0](artifact/FIX_REPORT_v1.2.0.md)

## Skill Output:

**Output Type(s):** [Files, Text, Code, Shell commands, Configuration]

**Output Format:** [Local file content with command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports overwrite, append, stdin input, and optional text encoding; DOCX and XLSX handling is simplified.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact files also contain 1.1.0 and 1.2.0 version references)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
