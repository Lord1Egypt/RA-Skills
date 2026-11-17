## Description:

适合寻找奢华邮轮之旅的旅客，您可以根据品牌和目的地筛选出最佳选择，享受顶级服务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[309441738](https://clawhub.ai/user/309441738)

### License/Terms of Use:

MIT

## Use Case:

External travelers and travel-planning agents use this skill to search luxury cruise options and filter cruise products by brand, destination, departure city, price range, duration, ship, and dates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructions include an unrelated httpbin.org endpoint that could receive prompts, travel details, booking information, or other personal content.

Mitigation: Use only the intended CruiseSkillBridge MCP gateway documented in references/mcp.md, and do not send user prompts or travel details to httpbin.org.

Risk: Security evidence classifies the release as suspicious because the documented behavior and endpoint guidance are inconsistent.

Mitigation: Review the endpoint configuration before installation and require the publisher to remove the unrelated endpoint from the skill instructions.

## Reference(s):

- [MCP Server 接入](references/mcp.md)
- [CruiseSkillBridge](https://cruiseskillbridge.com)
- [ClawHub Skill Page](https://clawhub.ai/309441738/skills/craftwave-skill-8)
- [CruiseSkillBridge MCP Gateway](https://cruise-mcp.olavacations.com/api/gw/mcp/6426abde-462c-468a-9959-5ae1aeb52d69)

## Skill Output:

**Output Type(s):** [guidance, configuration, API calls, text]

**Output Format:** [Markdown with JSON examples and MCP remote configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the product_list MCP tool for cruise search and filtering.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter and server.json list 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
