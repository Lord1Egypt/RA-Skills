## Description:

PDF文档工具（专业版） helps agents extract text and tables from PDFs, create, merge, split, watermark, encrypt, OCR, and batch-process PDF documents with structured outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and enterprise teams use this skill to automate PDF text and table extraction, file creation, merge and split workflows, watermarking, encryption, OCR, and audit-style exports. It is not intended for cracking encrypted files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad read, write, and command execution authority for document workflows.

Mitigation: Run it in a constrained workspace, require explicit input and output file paths, and confirm merge, split, watermark, encryption, OCR, audit export, or shell-command actions before execution.

Risk: PDF content, generated audit reports, callbacks, or webhooks could expose sensitive document content or metadata.

Mitigation: Use only documents the user is comfortable letting an agent read and rewrite, review audit fields before export, and enable callbacks only to approved HTTPS endpoints.

Risk: The security evidence marks the release suspicious because write scope, callback behavior, and audit data handling are not clearly limited.

Mitigation: Review the skill before installation, keep generated outputs isolated until inspected, and apply organization policy for document retention and data handling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/document-pdf-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with code snippets and structured JSON or file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write extracted text, tables, merged or watermarked PDFs, audit reports, and export files when explicit paths are provided.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
