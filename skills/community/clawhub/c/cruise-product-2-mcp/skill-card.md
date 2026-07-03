## Description: <br>
A remote MCP server for discovering cruise products and filtering options to find cruises that match travel needs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[309441738](https://clawhub.ai/user/309441738) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this MCP connector to search cruise products through a remote service and narrow options with multi-dimensional filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cruise-search requests and travel preferences are sent to an external remote service. <br>
Mitigation: Avoid entering sensitive personal, payment, or account information unless the provider's privacy and retention practices are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/309441738/skills/cruise-product-2-mcp) <br>
- [Remote MCP endpoint](https://cruise-mcp.olavacations.com/api/gw/mcp/3ae0fa3d-2c56-4d01-be01-14ee8463cf04) <br>
- [Model Context Protocol server schema](https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Configuration] <br>
**Output Format:** [MCP server responses over streamable HTTP, typically structured text or JSON from the remote service.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote streamable HTTP MCP endpoint; no local code or persistence in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata; server.json advertises 0.1.0 for the remote MCP server) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
