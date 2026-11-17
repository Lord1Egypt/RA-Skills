## Description:

使用 Microsoft MarkItDown 将各种文档格式（PDF/DOCX/PPTX/XLSX/图片/音频等）转换为 Markdown，专为 AGENT 和 LLM 工作流优化

This skill is ready for commercial/non-commercial use.

## Publisher:

[xsm0826](https://clawhub.ai/user/xsm0826)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to convert PDFs, Office files, HTML, EPUB, images, audio, and YouTube sources into structured Markdown for LLM, RAG, and document-analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the skill adds MarkItDown and optional dependencies for broad document and media conversion.

Mitigation: Use a virtual environment and pin reviewed package versions where possible.

Risk: Processing confidential documents, recordings, or URLs can expose sensitive content to installed converters or configured processing services.

Mitigation: Avoid processing confidential inputs unless the converter behavior and dependency chain have been reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xsm0826/skills/everything2markdown-cn)
- [MarkItDown GitHub](https://github.com/microsoft/markitdown)
- [MarkItDown PyPI](https://pypi.org/project/markitdown/)
- [MarkItDown MCP Server](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp)
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/guide/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, Python examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended to help agents produce structured Markdown and supporting document-processing workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
