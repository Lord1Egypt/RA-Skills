## Description:

Context7 MCP 是一款为开发者提供最新代码文档和示例的服务，通过集成到开发环境中，确保LLM生成的代码基于最新的库文档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to resolve library identifiers and fetch current library documentation or examples through a Context7-compatible workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the XiaoBenYang API key in a local plaintext .env file.

Mitigation: Use it only in a private workspace, avoid committing or backing up the .env file, and prefer environment-based secret handling if the workspace is shared or indexed.

Risk: The security summary notes mixed Context7 branding with XiaoBenYang and gaokao leftovers.

Mitigation: Confirm the publisher intended this XiaoBenYang-hosted Context7 wrapper and review the tool behavior before relying on returned documentation.

Risk: The skill depends on an external XiaoBenYang-hosted API for documentation retrieval.

Mitigation: Treat upstream API responses as external content and review generated guidance or examples before applying them to production code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/code-document-update)
- [XiaoBenYang API key portal](https://xiaobenyang.com)
- [XiaoBenYang MCP endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown summaries of API-returned JSON, with code examples when returned by the upstream documentation service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key before API-backed documentation retrieval can run.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
