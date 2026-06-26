## Description: <br>
基于 MarkItDown 将 PDF、Word、PowerPoint、Excel、图片和音频等文档批量转换为 Markdown，用于文档数字化、知识库构建和内容提取。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byteuser1977](https://clawhub.ai/user/byteuser1977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge-base maintainers, and documentation teams use this skill to convert source documents and media-derived text into Markdown files for search, archival, and downstream content workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Converted documents may contain sensitive content or metadata from source files, images, or media. <br>
Mitigation: Use narrow input and output folders, avoid sensitive files when possible, and review generated Markdown before sharing. <br>
Risk: Optional URL, media, OCR, and transcription features may introduce network behavior or additional local tooling. <br>
Mitigation: Install the skill in a virtual environment and enable optional dependencies only when their behavior is acceptable for the target workflow. <br>


## Reference(s): <br>
- [MarkItDown API Reference](references/API_REFERENCE.md) <br>
- [Supported Formats](references/FORMATS.md) <br>
- [PDF Configuration Guide](references/PDF_CONFIG.md) <br>
- [MarkItDown PyPI](https://pypi.org/project/markitdown/) <br>
- [MarkItDown GitHub Repository](https://github.com/microsoft/markitdown) <br>
- [ClawHub Skill Page](https://clawhub.ai/byteuser1977/convert-markdown) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown files and CLI status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are written as UTF-8 Markdown and may preserve directory structure during batch conversion.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
