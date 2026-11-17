## Description:

Endpoint AIops helps agents review managed endpoint fleets, analyze health, sessions, and configuration drift, and perform profile assignments or endpoint reboots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and endpoint administrators can use the skill to inspect managed endpoint inventory and fleet health, investigate login and boot issues, and identify patch or configuration drift. It also supports changing an endpoint profile or rebooting an endpoint, so write actions need careful authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Profile changes and endpoint reboots can affect devices, and CLI confirmation safeguards do not protect MCP calls.

Mitigation: Start with a server-enforced read-only account and require explicit MCP-client approval for the specific device and action before enabling writes.

Risk: An endpoint reboot cannot be undone.

Mitigation: Confirm the target device and action before rebooting, and ensure recovery can be handled outside the skill if the endpoint does not return.

## Reference(s):

- [Capabilities reference](references/capabilities.md)
- [CLI reference](references/cli-reference.md)
- [Setup and security guide](references/setup-guide.md)
- [Agent guardrails](references/agent-guardrails.md)
- [Project homepage](https://github.com/AIops-tools/Endpoint-AIops)

## Skill Output:

**Output Type(s):** [Analysis, API calls, Shell commands, Guidance]

**Output Format:** [Structured endpoint data and concise fleet analysis, with CLI commands where relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include endpoint health, login and boot, patch, and configuration drift findings; write actions can assign profiles or reboot endpoints.]

## Skill Version(s):

0.13.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
