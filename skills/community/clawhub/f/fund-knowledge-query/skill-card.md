## Description:

一个基于Model Context Protocol (MCP)的基金知识库服务器，提供基金相关知识的查询和检索功能，支持多种部署模式和协议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to query fund knowledge and search stock information through a Xiaobenyang API-backed MCP service. It is intended for users who need fund-related lookup results summarized from the service response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the user-provided XBY API key in a local plaintext .env file.

Mitigation: Only provide a key when the publisher is trusted, avoid shared directories, and rotate the key if it may have been exposed.

Risk: The security evidence reports mismatched, broken tool definitions.

Mitigation: Verify the tool implementation and API endpoint before relying on lookup results.

Risk: The security verdict is suspicious.

Mitigation: Review the skill before installation and deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/fund-knowledge-query)
- [Publisher profile](https://clawhub.ai/user/cainingnk)
- [Xiaobenyang](https://xiaobenyang.com)
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Markdown summary of API results, with raw JSON available from tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided XBY API key before API-backed lookups can run.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
