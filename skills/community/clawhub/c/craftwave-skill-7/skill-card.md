## Description: <br>
专为追求奢华的旅行者推荐高端邮轮体验，提供顶级设施与服务。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[309441738](https://clawhub.ai/user/309441738) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External travel-planning agents and users use this MCP skill to discover luxury cruise options and filter cruise products by brand, departure city, price range, destination, trip duration, ship, and date. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cruise search inputs are sent through CruiseSkillBridge/olavacations infrastructure and counted in gateway statistics. <br>
Mitigation: Avoid sensitive personal, financial, or identity information; review third-party privacy, retention, and access-control terms before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/309441738/skills/craftwave-skill-7) <br>
- [MCP Server 接入](references/mcp.md) <br>
- [CruiseSkillBridge](https://cruiseskillbridge.com) <br>
- [Remote MCP gateway](https://cruise-mcp.olavacations.com/api/gw/mcp/7b49d758-2bec-48a6-be3d-19b11f954c07) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [MCP tool responses with JSON request and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a remote streamable HTTP MCP gateway; gateway calls are counted in CruiseSkillBridge statistics.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence; artifact metadata reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
