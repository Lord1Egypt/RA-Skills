## Description:

Local-first document-to-Markdown converter supporting HTML, DOCX, PDF, XLSX, CSV, JSON, XML, and PPTX inputs with Markdown output flavours for GitHub, CommonMark, Slack, Discord, Reddit, Confluence, R Markdown, and custom formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[britrik](https://clawhub.ai/user/britrik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent workflows use this skill to convert local documents, pasted content, or selected web content into platform-specific Markdown through the FormatFerry CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow installs and runs an unpinned global npm executable against potentially sensitive documents.

Mitigation: Use only a trusted and reviewed FormatFerry package version, prefer a pinned install where possible, and avoid broad global installs in shared environments.

Risk: URL extraction sends content to server-side processing.

Mitigation: Do not use --url for sensitive, internal, or confidential content unless server-side processing is acceptable; use local file or stdin conversion instead.

Risk: License validation may make a network request when a license key is stored.

Mitigation: Use --offline for private local conversion when network calls are not acceptable.

## Reference(s):

- [FormatFerry CLI Reference](references/cli-reference.md)
- [FormatFerry homepage](https://github.com/britrik/FormatFerry)
- [ClawHub skill page](https://clawhub.ai/britrik/skills/formatferry-markdown)

## Skill Output:

**Output Type(s):** [markdown, shell commands, files, configuration, guidance]

**Output Format:** [Markdown, Markdown file output, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports local file, stdin, URL, and batch conversion modes; optional credentials are only needed for URL extraction and premium batch mode.]

## Skill Version(s):

1.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
