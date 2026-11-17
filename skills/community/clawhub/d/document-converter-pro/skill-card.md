## Description:

Document format converter for Word, PDF, Markdown, HTML, and related local document conversion workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and document authors use this skill to generate conversion scripts and guidance for local document transformations between DOCX, PDF, Markdown, HTML, and text formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The HTML-to-PDF path can enable unrestricted local-file access when rendering HTML with wkhtmltopdf.

Mitigation: Use the skill only with trusted documents, disable local-file access by default, run conversions in a sandbox or allow-listed asset directory, and pin dependencies before production use.

## Reference(s):

- [Conversion Matrix](references/conversion-matrix.md)
- [ClawHub Skill Page](https://clawhub.ai/tobewin/skills/document-converter-pro)
- [ClawHub Publisher Profile](https://clawhub.ai/user/tobewin)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Python and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local conversion guidance and script snippets; generated files depend on the user's execution environment and installed dependencies.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
