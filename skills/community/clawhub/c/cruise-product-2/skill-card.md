## Description: <br>
Explore cruise products and filter options to find trips that match travel needs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[309441738](https://clawhub.ai/user/309441738) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Travel planners and agent users use this skill to search cruise products, filter lists by brand, departure city, destination, date, trip duration, ship, and price, and retrieve product details by product ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cruise search queries and product identifiers are sent to a remote MCP gateway and may be counted for provider statistics. <br>
Mitigation: Use the skill for non-sensitive cruise discovery, and avoid personal, payment, or confidential travel details unless the publisher provides clear data-handling terms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/309441738/skills/cruise-product-2) <br>
- [Publisher profile](https://clawhub.ai/user/309441738) <br>
- [MCP server connection guide](references/mcp.md) <br>
- [CruiseSkillBridge](https://cruiseskillbridge.com) <br>
- [Model Context Protocol server schema](https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Configuration] <br>
**Output Format:** [MCP tool responses and remote server configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a remote streamable HTTP MCP gateway; security evidence found no local executable code or hidden persistence.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence; artifact frontmatter and server.json report 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
