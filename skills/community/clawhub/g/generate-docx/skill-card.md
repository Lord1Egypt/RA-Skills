## Description:

Generate DOCX creates Word (.docx) documents from agent-generated or edited content and can reformat existing .docx files using Chinese national and industry document formatting templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ftois](https://clawhub.ai/user/ftois)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-producing agents use this skill to create or reformat Chinese Word documents for government, business, academic, technical, medical, legal, financial, engineering, marketing, and general document workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency setup instructions may encourage privileged package installation or system-wide Python changes.

Mitigation: Install dependencies in a virtual environment or have an administrator provision Pandoc and fonts; do not let an agent run sudo or --break-system-packages automatically.

Risk: Generated documents and temporary Markdown files could be written to shared or unintended locations.

Mitigation: Use explicit output paths in a private output directory and avoid shared writable directories.

Risk: Untrusted Markdown or raw OpenXML can alter document content or formatting in ways that are hard to inspect.

Mitigation: Do not pass untrusted content into raw_markdown, and review generated documents before distribution.

Risk: Legal, medical, financial, or official documents may be formatted convincingly even when source content is inaccurate.

Mitigation: Require qualified human review before relying on generated legal, medical, financial, or official documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ftois/skills/generate-docx)
- [Pandoc documentation](https://pandoc.org)

## Skill Output:

**Output Type(s):** [files, markdown, code, shell commands, configuration, guidance]

**Output Format:** [DOCX files generated from Markdown, with optional Markdown previews and Python API or command-line snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python, python-docx, Pandoc, generated reference templates, and explicit output paths.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists internal version 4.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
