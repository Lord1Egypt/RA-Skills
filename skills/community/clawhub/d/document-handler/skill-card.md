## Description:

Read, extract text and metadata, and convert documents in formats like PDF, DOCX, XLSX, PPTX, EPUB, RTF, and OpenDocument.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neckr0ik](https://clawhub.ai/user/neckr0ik)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to inspect document files they explicitly provide, extract text and metadata, and convert PDFs to images for OCR or visual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document text and metadata can contain sensitive information.

Mitigation: Only provide files the agent is authorized to read, and review extracted content before sharing it outside the intended context.

Risk: Scanned, encrypted, or complex documents may produce incomplete or lossy extraction results.

Mitigation: Use OCR or the required password when needed, and validate extracted text or images before relying on them.

## Reference(s):

- [Document Handler ClawHub Skill Page](https://clawhub.ai/neckr0ik/skills/document-handler)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce extracted document text, metadata, or PNG images derived from user-provided files.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
