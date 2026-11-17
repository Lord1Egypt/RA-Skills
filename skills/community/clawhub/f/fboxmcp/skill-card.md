## Description:

FBoxMCP helps agents manage FBox industrial IoT devices through an MCP server, including device status, PLC monitoring data, alarms, historical data, and VNC remote monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwbgo](https://clawhub.ai/user/wwbgo)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, operators, and maintenance engineers use this skill with an authorized FBox account to inspect industrial IoT device status, read and write PLC monitor points, manage alarms, review historical data, and open remote monitoring sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthorized use or credential exposure could reveal or control sensitive industrial IoT equipment.

Mitigation: Install only for an FBox account the user is authorized to operate, keep FBOXMCP_API_KEY secret, use HTTPS, apply least privilege, and rotate keys periodically.

Risk: PLC monitor writes and alarm acknowledgments can affect equipment state or operational response.

Mitigation: Verify the exact device, site, current value or alarm state, and maintenance context, then require explicit user confirmation before executing writes or acknowledgments.

Risk: Device network settings, locations, PLC data, alarm history, and VNC sessions expose sensitive operational information.

Mitigation: Show only data returned by authorized tool calls, avoid reusing stale values, and open remote monitoring sessions only after confirming the target device and authorization.

Risk: UTC server timestamps can be misread during operational review.

Mitigation: Use the server time tool for current time and clearly convert displayed operational timestamps to Beijing time unless the user expects another timezone.

## Reference(s):

- [FBoxMCP ClawHub listing](https://clawhub.ai/wwbgo/skills/fboxmcp)
- [FBox homepage](https://fbox360.com)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Installation Guide](INSTALL.md)
- [Device Management Reference](references/device-management.md)
- [Monitoring Reference](references/monitoring.md)
- [Alarm Management Reference](references/alarm-management.md)
- [Historical Data Reference](references/historical-data.md)
- [User Guide](references/user-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, tables, and MCP tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should use fresh tool data, present alarms and historical data as tables, convert server UTC timestamps to Beijing time when displayed, and require explicit user confirmation before writes or alarm acknowledgments.]

## Skill Version(s):

0.1.3 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
