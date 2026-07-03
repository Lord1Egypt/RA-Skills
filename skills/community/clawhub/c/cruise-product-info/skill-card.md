## Description: <br>
Provides detailed information about specific cruise products, including features and services, to support cruise selection decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[309441738](https://clawhub.ai/user/309441738) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and travel-focused agents use this skill to look up cruise product details by product identifier and compare product features or services before making cruise selection decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cruise product lookup requests are sent to the listed CruiseSkillBridge/olavacations remote MCP endpoint. <br>
Mitigation: Install only if this remote routing is acceptable, and avoid sending secrets, account credentials, or unrelated personal data unless the publisher provides clear privacy and retention terms. <br>


## Reference(s): <br>
- [MCP Server 接入](references/mcp.md) <br>
- [ClawHub skill page](https://clawhub.ai/309441738/skills/cruise-product-info) <br>
- [CruiseSkillBridge](https://cruiseskillbridge.com) <br>
- [CruiseSkillBridge remote MCP endpoint](https://cruise-mcp.olavacations.com/api/gw/mcp/478d82fd-8ff7-46e2-9cda-7576fb74ed83) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown or text responses backed by remote MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the product_info MCP tool to retrieve cruise product details.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter and server.json report 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
