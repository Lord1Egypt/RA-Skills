## Description: <br>
FBoxCLI guides agents in using the FBox CLI to manage industrial IoT devices, inspect device status, read and write PLC monitoring points, manage alarms and contacts, query history, and operate device groups and write groups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flexemdev](https://clawhub.ai/user/flexemdev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Industrial IoT operators, developers, and support engineers use this skill to prepare and review FBox CLI commands for device management, monitoring, alarms, contacts, historical data, and batch operations. The skill is intended for authenticated environments where the user can verify device IDs, credentials, and any write or delete action before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can assist with commands that change industrial device, monitoring, alarm, contact, data push, history, and write-group state. <br>
Mitigation: Require explicit user confirmation before every write or delete operation, verify the current device state first, and compare proposed target values before execution. <br>
Risk: Incorrect device IDs or target values could affect the wrong FBox device or monitoring point. <br>
Mitigation: Fetch IDs from live fboxcli list commands, do not guess identifiers, and show the selected device, monitoring point, or alarm target before acting. <br>
Risk: Credential handling guidance is incomplete for an agent-assisted industrial IoT workflow. <br>
Mitigation: Use least-privilege FBox credentials, avoid embedding passwords or secrets in generated commands or scripts, and rely on interactive login where possible. <br>


## Reference(s): <br>
- [FBox homepage](https://fbox360.com) <br>
- [Installation guide](INSTALL.md) <br>
- [Device management command reference](references/device-management.md) <br>
- [Monitoring point command reference](references/monitoring.md) <br>
- [Alarm and contact command reference](references/alarm-management.md) <br>
- [Historical data command reference](references/historical-data.md) <br>
- [Unified write group command reference](references/control.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Text, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and structured JSON-oriented command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses fboxcli --json for structured command output by default; table output is used only when explicitly requested.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
