## Description:

专为追求奢华的旅行者推荐高端邮轮体验，提供顶级设施与服务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[309441738](https://clawhub.ai/user/309441738)

### License/Terms of Use:

MIT

## Use Case:

Travelers and travel advisors can use this MCP skill to request filtered luxury cruise product recommendations by brand, departure city, destination, price, trip duration, ship, and date.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill includes unclear instructions to send generic user input to an unrelated external testing endpoint.

Mitigation: Review the publisher's intended endpoint and data handling before installation or use.

Risk: The security guidance warns against sending personal travel details, budgets, dates, or other sensitive information until the endpoint behavior is clarified.

Mitigation: Avoid submitting sensitive travel or budget information through the skill unless the publisher clarifies the remote endpoint and data handling.

## Reference(s):

- [MCP Server 接入](references/mcp.md)
- [ClawHub skill page](https://clawhub.ai/309441738/skills/craftwave-skill-7)
- [CruiseSkillBridge](https://cruiseskillbridge.com)
- [Model Context Protocol server schema](https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json)

## Skill Output:

**Output Type(s):** [text, configuration, API calls, guidance]

**Output Format:** [Markdown setup guidance with JSON request examples and MCP remote tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a remote streamable HTTP MCP endpoint; tool behavior depends on the publisher-operated gateway.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and server.json list 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
