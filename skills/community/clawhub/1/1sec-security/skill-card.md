## Description:

Install, configure, and manage 1-SEC, an open-source all-in-one cybersecurity platform for Linux servers and VPS-hosted AI agent hosts, including setup, enforcement presets, module configuration, alert management, and ongoing operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cutmob](https://clawhub.ai/user/cutmob)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and operators use this skill to secure Linux servers and AI agent hosts with 1-SEC monitoring, intrusion detection, enforcement tuning, alert workflows, and operational runbooks. It is most relevant when installing endpoint defense, hardening a VPS, or managing response presets for an unattended agent host.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a powerful downloaded security binary that can run with root enforcement privileges.

Mitigation: Review the upstream project and release provenance, use the manual GitHub Releases download path, and independently verify checksums before installing.

Risk: Live enforcement presets can block IPs, drop connections, kill processes, quarantine files, or otherwise disrupt important systems.

Mitigation: Keep dry-run enabled until tested, monitor alerts and enforcement history, and avoid the vps-agent live preset on important systems without active monitoring.

Risk: Self-update behavior may change the installed binary after deployment.

Mitigation: Disable self-update checks in hardened environments or require a controlled update process with checksum verification.

Risk: Full enforcement requires elevated permissions.

Mitigation: Run unprivileged when only log-only monitoring is needed, and grant root or sudo access only for explicitly approved enforcement actions.

## Reference(s):

- [1-SEC source repository](https://github.com/1sec-security/1sec)
- [1-SEC security policy](https://github.com/1sec-security/1sec/blob/main/SECURITY.md)
- [Security Policy](SECURITY.md)
- [Configuration Reference](references/config-reference.md)
- [Operations Runbook](references/operations-runbook.md)
- [VPS Agent Deployment Guide](references/vps-agent-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose privileged installation, enforcement, and monitoring commands for Linux hosts; operators should review commands before execution.]

## Skill Version(s):

0.4.15 (source: server release metadata; skill metadata lists 0.4.11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
