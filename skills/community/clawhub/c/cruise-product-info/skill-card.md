## Description:

Provides detailed information about specific cruise products, including features and services, to support cruise selection decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[309441738](https://clawhub.ai/user/309441738)

### License/Terms of Use:

MIT

## Use Case:

External users and travel-focused agents use this skill to query cruise product details through the published product_info MCP tool and compare product features or services before making a selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that the main instructions still direct users to an unrelated httpbin POST endpoint instead of the configured cruise MCP gateway.

Mitigation: Use only the configured CruiseSkillBridge MCP gateway/tool flow and have the publisher remove or correct the httpbin placeholder.

Risk: Requests are routed through a remote MCP gateway and may include user-provided cruise selection context.

Mitigation: Do not send secrets, payment data, credentials, or unnecessary personal information.

## Reference(s):

- [MCP Server 接入](references/mcp.md)
- [ClawHub skill page](https://clawhub.ai/309441738/skills/cruise-product-info)
- [CruiseSkillBridge](https://cruiseskillbridge.com)

## Skill Output:

**Output Type(s):** [Text, Configuration, Guidance]

**Output Format:** [Text or JSON returned through an MCP tool response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the product_info MCP tool through the configured CruiseSkillBridge MCP gateway.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and server.json report 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
