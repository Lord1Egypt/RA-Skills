## Description:

Operate and maintain OpenClaw installations with CLI commands, configuration management, channel, agent and model setup, security auditing, troubleshooting, and gateway administration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyafeichina](https://clawhub.ai/user/liyafeichina)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw administrators use this skill to manage channels, agents, models, gateway services, configuration, diagnostics, security audits, troubleshooting, logs, cron, and maintenance tasks for OpenClaw installations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Administrative commands such as --fix, delete/remove/rm, gateway restart/stop, memory index, chmod, SSH, and token commands can affect live OpenClaw systems.

Mitigation: Confirm targets, back up important configuration, and prefer read-only status or audit commands before applying changes.

Risk: Commands involving bot tokens, model auth, SSH, credential files, or live auth probes can expose secrets through logs, terminal history, or shared terminals.

Mitigation: Protect secrets from logs and shared terminals, use credential stores or token files where available, and restrict credential file permissions.

Risk: Security remediation guidance may change gateway authentication, allowed origins, TLS settings, channel policies, or file permissions.

Mitigation: Stage and review access-control changes, restart the gateway after configuration changes, and test channels and node connectivity after remediation.

## Reference(s):

- [OpenClaw CLI Cheat Sheet](artifact/references/cli-cheatsheet.md)
- [OpenClaw Security Audit Reference](artifact/references/security-audit.md)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw CLI Documentation](https://docs.openclaw.ai/cli)
- [OpenClaw Channels CLI Documentation](https://docs.openclaw.ai/cli/channels)
- [OpenClaw Agents CLI Documentation](https://docs.openclaw.ai/cli/agents)
- [OpenClaw Models CLI Documentation](https://docs.openclaw.ai/cli/models)
- [OpenClaw Config CLI Documentation](https://docs.openclaw.ai/cli/config)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational commands that should be reviewed before execution in an OpenClaw administrator environment.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
