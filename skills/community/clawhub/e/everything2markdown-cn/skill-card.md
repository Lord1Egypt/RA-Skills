## Description: <br>
使用 Microsoft MarkItDown 将各种文档格式（PDF/DOCX/PPTX/XLSX/图片/音频等）转换为 Markdown，专为 AGENT 和 LLM 工作流优化。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xsm0826](https://clawhub.ai/user/xsm0826) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert PDFs, Office documents, HTML, EPUB, images, audio, and YouTube subtitles into clean Markdown for LLM, automation, analysis, and RAG workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Converted files, media, URLs, transcripts, subtitles, and metadata may become visible to the agent and downstream LLM or RAG systems. <br>
Mitigation: Only convert content suitable for that workflow, and review generated Markdown and metadata before using it downstream. <br>
Risk: Installing MarkItDown with all optional dependencies broadens the local Python environment. <br>
Mitigation: Install in an isolated Python environment when possible and review the MarkItDown package and version before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xsm0826/everything2markdown-cn) <br>
- [MarkItDown GitHub](https://github.com/microsoft/markitdown) <br>
- [MarkItDown PyPI](https://pypi.org/project/markitdown/) <br>
- [MarkItDown MCP server](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Converted outputs may include extracted document text, subtitles, transcripts, links, and metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
