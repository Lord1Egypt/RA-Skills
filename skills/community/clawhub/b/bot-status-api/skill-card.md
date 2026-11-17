## Description:

Deploy a lightweight Node.js status API that exposes an OpenClaw bot's runtime health, service connectivity, cron jobs, skills, and system metrics for dashboards, health endpoints, or status pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suspect80](https://clawhub.ai/user/suspect80)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to deploy and configure a status API for monitoring an OpenClaw agent's runtime health, configured services, cron jobs, skills, containers, email counts, and host metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Detailed status output can reveal services, ports, cron timing, email metadata, skill inventory, and host details.

Mitigation: Run only in a trusted private environment, add authentication, and bind detailed status routes to localhost or a protected interface.

Risk: The service runs shell-command collectors and disables TLS verification.

Mitigation: Remove the global TLS bypass and replace raw command collectors with fixed allowlisted commands or safer APIs before deployment.

## Reference(s):

- [Bot Status API ClawHub Skill Page](https://clawhub.ai/suspect80/skills/bot-status-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, shell command, configuration, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deployment and configuration guidance for a Node.js status API that serves JSON status responses.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact package.json reports 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
