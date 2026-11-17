## Description:

Doc To Markdown helps agents convert Word documents (.doc and .docx) into clean Markdown using MinerU's document processing tooling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and content teams use this skill to convert Word files or URLs into Markdown for documentation, static sites, wikis, blogs, GitHub, Notion, Obsidian, and related Markdown-based workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a mutable third-party CLI.

Mitigation: Use a pinned and reviewed mineru-open-api version where possible, and review the CLI before use in sensitive environments.

Risk: Document contents may be processed by an external MinerU service.

Mitigation: Avoid confidential documents unless approved, and verify whether the selected mode is local-only before converting sensitive files.

Risk: The MINERU_TOKEN credential is required for some extraction modes.

Mitigation: Provide MINERU_TOKEN only to commands that need it and avoid persisting or logging the token unnecessarily.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mzlzyca/skills/doc-to-markdown)
- [MinerU homepage](https://mineru.net)
- [MinerU project](https://github.com/opendatalab/MinerU)
- [MinerU token management](https://mineru.net/apiManage/token)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell command snippets and converted document content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Converted content is written to stdout by default or saved to a directory with -o; progress and status messages are sent to stderr.]

## Skill Version(s):

0.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
