## Description:

一个支持多AI人格召唤与协作的MCP协议服务器，可用于代码分析、产品设计等多场景智能协作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to call a remote XiaoBenYang persona MCP service, summon named AI personas, list available personas, check service version information, and request interactive persona collaboration for tasks such as code analysis and product design.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a XiaoBenYang API key and sends that key to the remote MCP service.

Mitigation: Install only when the remote service is trusted, provide the key through a trusted secret manager or environment channel, and avoid exposing the key in chat transcripts.

Risk: The artifact persists XBY_APIKEY in a local plaintext .env file.

Mitigation: Keep the .env file private, exclude it from git and backups, restrict filesystem access, and rotate the key if it may have been exposed.

Risk: Changing the API base URL would redirect credentialed requests to a different destination.

Mitigation: Do not override the default API base URL unless the destination is fully trusted and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/ai-persona)
- [Publisher profile](https://clawhub.ai/user/cainingnk)
- [XiaoBenYang API key site](https://xiaobenyang.com)
- [XiaoBenYang MCP service endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration guidance]

**Output Format:** [Markdown or text summaries of JSON responses returned by the remote persona service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key before remote persona tools can return results.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
