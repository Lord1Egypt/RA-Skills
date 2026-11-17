## Description:

Provides web search and real-time information retrieval through DingTalk's Xiaosu AI search, with keyword search, freshness filters, configurable result counts, and optional JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[breath57](https://clawhub.ai/user/breath57)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agent operators use this skill to run current web searches, retrieve recent technical or news information, and collect formatted text or JSON search results from a configured DingTalk MCP endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A saved search-server URL may route future searches to an unexpected service.

Mitigation: Install only from a trusted MCP configuration source, review the endpoint before saving it, and prefer the documented DingTalk HTTPS gateway.

Risk: Search queries are sent to the saved endpoint.

Mitigation: Avoid sending sensitive or confidential queries unless the configured endpoint and its data handling are acceptable for the intended use.

Risk: The security guidance recommends a version that validates requested result counts and warns before endpoint replacement.

Mitigation: Review count values and configuration changes before use, and prefer releases that add explicit validation and replacement warnings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/breath57/skills/dingtalk-ai-web-search)
- [DingTalk MCP configuration page](https://mcp.dingtalk.com/#/detail?detailType=instanceMcpDetail&instanceId=78440)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and optional JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search result count defaults to 5 and can be requested up to 50; freshness filters include noLimit, oneDay, oneWeek, oneMonth, and oneYear.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
