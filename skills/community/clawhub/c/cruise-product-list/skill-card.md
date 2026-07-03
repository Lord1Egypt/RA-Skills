## Description: <br>
Filters cruise product lists by criteria such as brand, departure city, price range, destination, trip duration, cruise ship, and travel date. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[309441738](https://clawhub.ai/user/309441738) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and travel-commerce agents use this MCP skill to quickly find cruise products that match user-selected filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests are sent to an external MCP/API service through a gateway. <br>
Mitigation: Avoid sending secrets, private business data, or personal information unless the service is trusted and its retention and logging practices are understood. <br>
Risk: The skill depends on a remote service for cruise product filtering. <br>
Mitigation: Confirm the remote endpoint is available and appropriate for the deployment environment before relying on it in production workflows. <br>


## Reference(s): <br>
- [MCP Server 接入](references/mcp.md) <br>
- [CruiseSkillBridge](https://cruiseskillbridge.com) <br>
- [ClawHub skill page](https://clawhub.ai/309441738/skills/cruise-product-list) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, API calls] <br>
**Output Format:** [MCP tool responses and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a remote streamable HTTP MCP endpoint through a CruiseSkillBridge gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact MCP version 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
