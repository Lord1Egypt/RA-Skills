## Description:

Document Tools helps agents work with Word documents, PDFs, OCR, Markdown conversion, document splitting and merging, signatures, encryption, and watermarking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cooperiano](https://clawhub.ai/user/cooperiano)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-heavy teams use this skill to ask an agent for document editing, PDF and OCR workflows, broad Markdown conversion, and setup guidance for related document tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package installation commands, including privileged system package installation, can change the host environment.

Mitigation: Review pip and system packages before installation, prefer a virtual environment, and run sudo apt only when the OS package sources are trusted.

Risk: OCR, conversion, signing, watermarking, encryption, and document editing workflows may process sensitive files or alter originals.

Mitigation: Treat documents as sensitive, keep backups before modifying originals, and review outputs before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cooperiano/skills/document-tools)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include package installation commands and document workflow guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
