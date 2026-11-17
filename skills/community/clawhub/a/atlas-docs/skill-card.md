## Description:

Atlas Docs MCP服务器为AI助手提供库和框架的技术文档，将官方文档处理为适合LLM使用的Markdown版本，适用于Cursor、Cline、Windsurf等MCP兼容的LLM客户端。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users of MCP-compatible AI clients use this skill to discover available documentation sets, search documentation, retrieve page indexes, and fetch page-level or consolidated Markdown documentation for libraries and frameworks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for a XiaoBenYang API key and stores it persistently in .env.

Mitigation: Use a low-privilege key, restrict workspace access, verify file permissions, and remove the key when it is no longer needed.

Risk: Security evidence flags confusing service identity mismatches between Atlas Docs, XiaoBenYang, and Gaokao labels.

Mitigation: Confirm the publisher, service endpoint, and intended API before sharing sensitive inputs or credentials.

Risk: The skill depends on responses from an external documentation service.

Mitigation: Review returned documentation before acting on it, especially for version-specific or security-sensitive work.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cainingnk/skills/atlas-docs)
- [XiaoBenYang API Key Service](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration guidance]

**Output Format:** [Markdown summaries with raw JSON API results where relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key and uses an external documentation API.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
