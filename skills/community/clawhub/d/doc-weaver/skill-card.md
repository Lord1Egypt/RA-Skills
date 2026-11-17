## Description:

Transform Markdown or outlines into polished Word/PDF documents with professional templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and document authors use Doc Weaver to convert Markdown drafts or outlines into formatted Word documents, PDFs, or styled Markdown previews using built-in templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF conversion can allow Markdown to trigger external or local resource loading during the pandoc and WeasyPrint workflow.

Mitigation: Avoid converting untrusted Markdown to PDF unless the conversion runs in a sandbox or network and local resource access are disabled.

Risk: Local document conversion depends on user-managed pandoc, WeasyPrint, and python-docx installations.

Mitigation: Use pinned dependency versions and run the bundled doctor and verification checks before relying on generated documents.

## Reference(s):

- [Doc Weaver Template Reference](references/templates.md)
- [Doc Weaver on ClawHub](https://clawhub.ai/harrylabsj/skills/doc-weaver)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Guidance]

**Output Format:** [DOCX/PDF files, styled Markdown previews, and Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [DOCX generation requires python-docx; PDF generation additionally requires pandoc and WeasyPrint.]

## Skill Version(s):

1.1.0 (source: frontmatter, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
