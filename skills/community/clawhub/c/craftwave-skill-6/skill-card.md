## Description: <br>
为公司团体或组织提供邮轮旅行方案，适合团队出行的需求，制定专属的邮轮产品。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[309441738](https://clawhub.ai/user/309441738) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External travel planners, company administrators, and agents use this MCP skill to request group cruise travel options and filter cruise products for corporate or organizational trips. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests are sent to an external MCP gateway. <br>
Mitigation: Use the skill only when the publisher and remote service are trusted, and avoid sending confidential traveler, employee, or payment data. <br>
Risk: Documentation is thin and contains template-style placeholder content. <br>
Mitigation: Review the MCP tool behavior and remote configuration before deployment, especially for workflows that affect travel purchasing or employee data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/309441738/skills/craftwave-skill-6) <br>
- [Publisher profile](https://clawhub.ai/user/309441738) <br>
- [MCP Server 接入](references/mcp.md) <br>
- [CruiseSkillBridge](https://cruiseskillbridge.com) <br>
- [MCP gateway remote](https://cruise-mcp.olavacations.com/api/gw/mcp/c3c56c15-63d5-472c-907b-cddb5d809871) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JSON request examples and MCP remote configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an external streamable HTTP MCP gateway for cruise product filtering.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter and server.json state 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
