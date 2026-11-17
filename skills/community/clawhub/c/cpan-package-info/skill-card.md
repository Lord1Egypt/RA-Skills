## Description:

一个MCP服务器，用于获取CPAN包的README内容、元数据和搜索功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up CPAN package README content, package metadata, dependencies, and search results. It requires a XiaoBenYang API key before making credentialed requests to the configured service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a XiaoBenYang API key and sends credentialed requests to a separate configurable API service.

Mitigation: Install only when the XiaoBenYang service is trusted, use a scoped or disposable key when possible, and rotate the key if it may have been exposed.

Risk: The skill can persist the API key in a plaintext .env file.

Mitigation: Use the skill only in trusted local workspaces, restrict access to the .env file, and remove or rotate stored credentials when no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/cpan-package-info)
- [XiaoBenYang API key service](https://xiaobenyang.com)
- [XiaoBenYang MCP API origin](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration]

**Output Format:** [Markdown summaries derived from JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires package or search parameters and a configured XBY_APIKEY credential.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
