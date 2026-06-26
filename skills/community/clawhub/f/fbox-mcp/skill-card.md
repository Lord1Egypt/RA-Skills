## Description: <br>
FBoxMCP guides agents to manage FBox industrial IoT devices by checking device status, reading and writing PLC monitoring data, handling alarms, querying historical data, and opening VNC monitoring sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flexemdev](https://clawhub.ai/user/flexemdev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Industrial operators, maintenance teams, and automation engineers use this skill to inspect FBox device fleets, review alarms and historical telemetry, and carry out confirmed operational actions through the FBox MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unauthorized or overprivileged access could expose sensitive industrial device data or enable operational actions. <br>
Mitigation: Install only for authorized FBox operators, use least-privilege API keys, keep FBOXMCP_API_KEY out of code and shared shells, rotate it regularly, and verify the endpoint and publisher. <br>
Risk: Write operations and alarm confirmations can affect operational workflows. <br>
Mitigation: Require explicit user confirmation before confirmed writes or alarm acknowledgements, and read the current value first so the user can compare the planned change. <br>
Risk: Device configuration, network details, location, alarms, historical readings, PLC values, and VNC screens may contain sensitive operational information. <br>
Mitigation: Treat returned data and generated tables as sensitive, limit sharing and logging, and follow the operator's data handling requirements. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/flexemdev/fbox-mcp) <br>
- [FBox Product Site](https://fbox360.com) <br>
- [Installation Guide](INSTALL.md) <br>
- [Skill Instructions](SKILL.md) <br>
- [Device Management Reference](references/device-management.md) <br>
- [Monitoring Reference](references/monitoring.md) <br>
- [Alarm Management Reference](references/alarm-management.md) <br>
- [Historical Data Reference](references/historical-data.md) <br>
- [User Guide](references/user-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with tables, inline commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to the FBox MCP service and an FBOXMCP_API_KEY environment variable.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
