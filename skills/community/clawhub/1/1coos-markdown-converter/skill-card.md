## Description:

Converts supported documents, data files, media, archives, and URLs into formatted Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1coos](https://clawhub.ai/user/1coos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and knowledge workers use this skill to convert PDFs, Office files, spreadsheets, web and data files, images, audio, ZIP archives, EPUBs, and YouTube URLs into Markdown. It can optionally reformat output for GitHub, CommonMark, clean Markdown, or Obsidian workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security review flags unpinned runtime code and unsafe installer guidance.

Mitigation: Review before installation, install uv through trusted or official channels, and pin or sandbox markitdown where possible.

Risk: Document conversion may expose sensitive file contents to the conversion toolchain or optional external processing services.

Mitigation: Use only documents approved for the target environment, and avoid optional external processing for sensitive files unless separately authorized.

## Reference(s):

- [Supported Formats](references/supported-formats.md)
- [uv Installation Documentation](https://docs.astral.sh/uv/getting-started/installation/)
- [ClawHub Skill Page](https://clawhub.ai/1coos/skills/1coos-markdown-converter)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files plus concise execution and status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports configurable output directory, conversion-only mode, charset and timeout settings, and formatting styles for GitHub, CommonMark, clean Markdown, and Obsidian.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
