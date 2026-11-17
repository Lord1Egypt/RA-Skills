## Description:

通过 HTTPS API 或零依赖 CLI 下载任意网站的可用 favicon，支持尺寸偏好、图片重定向、JSON 元数据和 Windows/Linux/macOS。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sweesama](https://clawhub.ai/user/sweesama)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use FaviconDL to retrieve website favicon images or JSON favicon metadata through a documented HTTPS API, a zero-dependency Bash CLI, or an optional local stdio MCP adapter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions include raw GitHub commands that can fetch changed executable code from a mutable branch.

Mitigation: Prefer the REST API or bundled reviewed Bash script; when downloading scripts, use pinned commits, checksums, or manual review before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sweesama/skills/favicondl)
- [FaviconDL API Endpoint](https://favicondl.com/api/extract)
- [OpenAPI Specification](https://favicondl.com/openapi.yaml)
- [LLM Usage Notes](https://favicondl.com/llms.txt)
- [Human API Documentation](https://favicondl.com/documentation.html)
- [Canonical Agent API Documentation](https://github.com/sweesama/favicondl.com/blob/main/SKILL.md)
- [Local MCP Adapter Documentation](https://github.com/sweesama/favicondl.com/blob/main/mcp/README.md)
- [OpenClaw Marketplace Asset](https://openclawmp.cc/asset/s-5a9fb4e7ff343062)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, URLs, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to download image files with target-controlled formats or request JSON metadata from the FaviconDL API.]

## Skill Version(s):

2.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
