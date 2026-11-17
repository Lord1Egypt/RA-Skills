## Description:

Self-hosted infrastructure monitoring with local checks for HTTP and HTTPS endpoints, TCP ports, Docker containers, system resources, SSL expiry, DNS, Proxmox VMs and CTs, and alerts via WhatsApp, Telegram, or Discord.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariusfit](https://clawhub.ai/user/mariusfit)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to configure and run local infrastructure health checks for self-hosted services, containers, system resources, certificates, DNS, and Proxmox resources. It is suited for homelab, API uptime, SSL expiry, and resource alerting workflows where monitoring data should remain local.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports broad monitoring-related capabilities that may be more permissive than some deployments need.

Mitigation: Review the manifest before installation, use the skill only in trusted workspaces, and prefer a version with narrower permissions and explicit user control for alerts or scheduled checks.

Risk: The security review reports unsafe HTTPS and SSL-expiry checks that may produce false health results.

Mitigation: Do not rely on the skill's HTTPS or SSL-expiry results until certificate validation and expiry parsing are fixed; verify TLS status with an independent trusted check.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local monitor setup guidance, command invocations, status summaries, dashboards, and alert configuration details.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
