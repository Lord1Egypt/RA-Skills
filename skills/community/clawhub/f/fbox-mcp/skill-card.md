## Description:

FBoxMCP helps agents manage FBox industrial IoT devices through an MCP server, including device status checks, PLC monitoring point reads and writes, alarm handling, history queries, and VNC monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flexemdev](https://clawhub.ai/user/flexemdev)

### License/Terms of Use:

MIT-0

## Use Case:

External operators and developers who administer FBox industrial IoT deployments use this skill to query device status, monitor PLC data, handle alarms, retrieve historical trends, and launch VNC sessions through the FBox MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: FBox API keys can expose sensitive industrial IoT device-control access.

Mitigation: Use a least-privilege API key, keep it out of source control and logs, and rotate it periodically.

Risk: PLC writes, alarm acknowledgments, and VNC sessions can affect production equipment operations.

Mitigation: Require explicit human review before these actions and show current device values or alarm details before execution.

Risk: Device state and telemetry may be stale, unavailable, or missing if the MCP server returns an error.

Mitigation: Use fresh tool responses for each request, surface tool errors directly, and avoid filling gaps with inferred device data.

## Reference(s):

- [FBoxMCP ClawHub Skill Page](https://clawhub.ai/flexemdev/skills/fbox-mcp)
- [FBox Homepage](https://fbox360.com)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Installation Guide](artifact/INSTALL.md)
- [FBox MCP Server User Guide](artifact/references/user-guide.md)
- [Device Management Tool Reference](artifact/references/device-management.md)
- [Monitoring Point Tool Reference](artifact/references/monitoring.md)
- [Alarm Management Tool Reference](artifact/references/alarm-management.md)
- [Historical Data Tool Reference](artifact/references/historical-data.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with tables, inline shell commands, and MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live FBox MCP tool responses and requires FBOXMCP_API_KEY for authenticated server access.]

## Skill Version(s):

0.1.4 (source: evidence release.version and SKILL.md metadata.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
