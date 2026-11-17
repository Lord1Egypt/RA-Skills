## Description:

一个通过模型上下文协议（MCP）提供DBLP计算机科学文献数据库访问的服务，支持学术文献检索、引用生成及格式化功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and developers use this skill to search DBLP publications, inspect author or venue data, calculate publication statistics, collect BibTeX entries, and export citation files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a XiaoBenYang API key and stores it in a plaintext .env file in the working directory.

Mitigation: Use a scoped key where possible, keep the workspace private, rotate the key after use, and prefer a revised release that uses secure secret storage.

Risk: Searches, citation selections, statistics inputs, and export paths may be sent to the XiaoBenYang MCP service.

Mitigation: Avoid submitting sensitive unpublished research details or local-only paths, and review the upstream service before deployment.

Risk: The security evidence marks the release suspicious because credential storage and third-party data handling are under-disclosed.

Mitigation: Install only after reviewing the security summary, publisher identity, and upstream service behavior for the intended environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/dblp)
- [XiaoBenYang API key site](https://xiaobenyang.com)
- [XiaoBenYang MCP service](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or text summaries, JSON-like API results, and BibTeX content or files for citation export.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key; BibTeX export writes to a user-selected .bib path.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
