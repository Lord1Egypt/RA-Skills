## Description:

Control Clash Verge Rev via mihomo API to query proxy status, switch nodes, test delays, manage connections, DNS, and related proxy settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianping7](https://clawhub.ai/user/brianping7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to administer a local Clash Verge Rev or mihomo controller from an agent session, including inspecting proxy state, changing routing mode or selected nodes, testing node latency, managing active connections, querying DNS, and triggering maintenance actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change or interrupt the user's proxy service by switching routing mode or nodes, closing connections, flushing DNS, restarting the core, or updating Geo data.

Mitigation: Require explicit user confirmation before state-changing or disruptive controller commands.

Risk: Controller credentials can be sent to an arbitrary HTTP endpoint if the API URL is configured that way.

Mitigation: Keep the controller endpoint on a local Unix socket or loopback address and avoid passing secrets on the command line.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/brianping7/skills/clash-verge-skill)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration guidance]

**Output Format:** [Markdown with inline shell commands and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May issue local Unix socket or loopback HTTP API calls to the user's configured mihomo controller.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
