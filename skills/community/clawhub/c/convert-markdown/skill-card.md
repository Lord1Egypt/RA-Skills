## Description:

文档处理与转换技能，基于 MarkItDown 工具，支持将 PDF、Word、PowerPoint、Excel、图片、音频等多种格式文件批量转换为 Markdown。

This skill is ready for commercial/non-commercial use.

## Publisher:

[byteuser1977](https://clawhub.ai/user/byteuser1977)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, knowledge-base maintainers, and documentation teams use this skill to convert source documents and media into Markdown for indexing, extraction, and downstream editing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document conversion reads user-selected files and may process sensitive PDFs, spreadsheets, images, audio, or OCR output.

Mitigation: Run conversions in a limited input folder and review generated Markdown or index files before sharing them.

Risk: Broad dependency installation and unpinned packages can introduce supply-chain variability.

Mitigation: Install in a virtual environment and prefer exact pinned package versions or a lockfile.

Risk: Overwrite options can replace existing output files.

Mitigation: Confirm output paths before enabling overwrite behavior.

## Reference(s):

- [MarkItDown API 参考](references/API_REFERENCE.md)
- [支持的格式详细说明](references/FORMATS.md)
- [PDF 处理配置指南](references/PDF_CONFIG.md)
- [MarkItDown PyPI](https://pypi.org/project/markitdown/)
- [Microsoft MarkItDown GitHub Repository](https://github.com/microsoft/markitdown)
- [MarkItDown MCP Server Documentation](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp)
- [ClawHub Skill Page](https://clawhub.ai/byteuser1977/skills/convert-markdown)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, command examples, Python snippets, and generated Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-file and recursive directory conversion, optional overwrite behavior, OCR-dependent PDF and image extraction, and optional audio transcription dependencies.]

## Skill Version(s):

1.0.3 (source: server evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
