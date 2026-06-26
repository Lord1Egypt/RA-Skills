## Description: <br>
FBoxMCP helps agents manage FBox industrial IoT devices through MCP, including device status, PLC monitoring points, alarms, historical trends, and VNC monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwbgo](https://clawhub.ai/user/wwbgo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams with authorized FBox access use this skill to inspect device state, read and write PLC monitoring data, review alarms, query historical data, and open remote monitoring sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unauthorized or overbroad use could expose or alter industrial IoT device state. <br>
Mitigation: Install only for users authorized to manage the relevant FBox devices and scope access to the required device fleet. <br>
Risk: API keys or bearer tokens could be leaked through logs, repositories, or shared transcripts. <br>
Mitigation: Use least-privilege FBOXMCP_API_KEY credentials and keep them out of source control, logs, and pasted conversation context. <br>
Risk: PLC writes, alarm acknowledgements, VNC sessions, and precise location lookups can affect production equipment or sensitive operational data. <br>
Mitigation: Require human review and explicit confirmation before executing writes, alarm confirmations, VNC access, or precise location queries on production devices. <br>
Risk: Stale or assumed device readings could mislead operational decisions. <br>
Mitigation: Use live FBox MCP tool results for device status, monitoring values, alarms, and historical data rather than prior conversation state or assumptions. <br>


## Reference(s): <br>
- [FBoxMCP on ClawHub](https://clawhub.ai/wwbgo/fboxmcp) <br>
- [FBox Homepage](https://fbox360.com) <br>
- [FBox MCP Endpoint](https://fboxmcp.fbox360.com) <br>
- [Installation Guide](INSTALL.md) <br>
- [User Access Guide](references/user-guide.md) <br>
- [Device Management Reference](references/device-management.md) <br>
- [Monitoring Point Reference](references/monitoring.md) <br>
- [Alarm Management Reference](references/alarm-management.md) <br>
- [Historical Data Reference](references/historical-data.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown responses with tables, live MCP tool results, and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FBOXMCP_API_KEY and network access to the FBox MCP Server; state-changing operations require explicit user confirmation.] <br>

## Skill Version(s): <br>
0.1.3 (source: evidence release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
