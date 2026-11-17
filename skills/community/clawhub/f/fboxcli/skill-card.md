## Description:

FBoxCLI helps agents manage industrial IoT devices through the FBox CLI, including device lookup, PLC monitoring point reads and writes, alarm and contact management, historical data queries, device groups, and unified write groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flexemdev](https://clawhub.ai/user/flexemdev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, automation engineers, and industrial operations teams use this skill to ask an agent for FBox CLI commands and workflows for inspecting, querying, and safely changing FBox industrial IoT resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide writes, deletes, alarm confirmations, contact changes, location exports, and batch control operations for industrial IoT resources.

Mitigation: Require explicit operator review before any high-impact command and use least-privilege FBox accounts.

Risk: The CLI install path may use an unpinned global package or external binary distribution.

Mitigation: Use a pinned and verified fboxcli version from a trusted FlexEM distribution source.

Risk: Credential examples may encourage secrets in shell command arguments.

Mitigation: Avoid putting passwords or client secrets directly in shell commands; prefer interactive login or approved secret handling.

Risk: Incorrect device, monitoring point, group, alarm, or contact IDs could target the wrong resource.

Mitigation: Retrieve IDs from fboxcli JSON responses and do not guess or fabricate identifiers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flexemdev/skills/fboxcli)
- [FBox website](https://fbox360.com)
- [FBox OpenAPI endpoint](https://openapi.fbox360.com)
- [fboxcli releases](https://github.com/flexem/fboxcli/releases)
- [Installation guide](INSTALL.md)
- [Skill instructions](SKILL.md)
- [Device management command reference](references/device-management.md)
- [Monitoring point command reference](references/monitoring.md)
- [Alarm and contact command reference](references/alarm-management.md)
- [Historical data command reference](references/historical-data.md)
- [Unified write group command reference](references/control.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured JSON-output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers fboxcli --json for machine-readable command output; table output is used only when requested.]

## Skill Version(s):

0.1.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
