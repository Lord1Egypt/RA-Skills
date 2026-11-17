## Description:

将纯文本或现有 Word 文档按党政机关公文格式规范生成或重排为 .docx，支持常见公文文种、红头、密级、附件、版记、页码和格式校验。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wing-art](https://clawhub.ai/user/wing-art)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and document-preparation agents use this skill to generate or reformat Chinese Party/government official Word documents. It helps preserve source content in format-only workflows while applying document layout, font, heading, recipient, attachment, pagination, and validation conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The python-docx dependency is specified with an open lower-bound version, which can allow supply-chain or compatibility drift.

Mitigation: Install dependencies in a virtual environment and pin or lockfile-verify python-docx before use in sensitive environments.

Risk: Generated documents may include user-provided confidential markings or sensitive document content and are written to the selected output path.

Mitigation: Review the output path and handle generated DOCX files according to the source document's confidentiality requirements.

Risk: Format-only conversion does not preserve images, comments, tracked changes, text boxes, or complex headers.

Mitigation: Keep the original document and manually review the generated DOCX when those elements matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wing-art/skills/format-official-docx)
- [README](README.md)
- [公文文种选择速查](references/document-types.md)
- [党政机关公文格式规则](references/format-rules.md)

## Skill Output:

**Output Type(s):** [Files, Text, Shell commands, Guidance]

**Output Format:** [DOCX files with optional plain-text or JSON validation output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated documents to the selected output path; installed fonts can affect final Word rendering.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
