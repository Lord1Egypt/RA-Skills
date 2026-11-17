## Description:

一个基于Python和MCP协议的域名注册状态检查服务器，支持批量检查和双重验证。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to check whether one or more domain names are registered through the Xiaobenyang service. It is intended for domain availability checks that return structured registration-status results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the Xiaobenyang API key in a plaintext .env file in the working directory.

Mitigation: Use a disposable or tightly scoped API key and avoid running the skill in shared repositories or shared directories.

Risk: The API key can be sent to a configurable endpoint.

Mitigation: Install only after trusting the Xiaobenyang service and reviewing environment variables that could override the API endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/fastdomaincheck)
- [Xiaobenyang API key site](https://xiaobenyang.com)
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API Calls, JSON, guidance, configuration]

**Output Format:** [Markdown summary with structured JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY value before API calls can be made.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
