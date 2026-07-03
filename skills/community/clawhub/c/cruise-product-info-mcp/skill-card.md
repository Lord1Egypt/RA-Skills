## Description: <br>
This MCP server provides information about specific cruise products, including features and services, to support decision-making. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[309441738](https://clawhub.ai/user/309441738) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this MCP skill to retrieve cruise product details and compare features or services before making travel-related decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cruise product details returned by the remote MCP service may be incomplete, outdated, or unsuitable as the sole basis for booking or purchase decisions. <br>
Mitigation: Verify important itinerary, pricing, availability, policy, and service details against official cruise or travel-provider sources before acting. <br>
Risk: Queries are sent to a remote MCP endpoint controlled by the third-party publisher. <br>
Mitigation: Avoid sending sensitive personal, payment, authentication, or confidential business information unless the endpoint is approved for that use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/309441738/skills/cruise-product-info-mcp) <br>
- [Remote MCP endpoint](https://cruise-mcp.olavacations.com/api/gw/mcp/478d82fd-8ff7-46e2-9cda-7576fb74ed83) <br>
- [MCP server schema](https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Guidance] <br>
**Output Format:** [MCP tool responses from a remote streamable HTTP server] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No local credential environment variables are declared in the evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
