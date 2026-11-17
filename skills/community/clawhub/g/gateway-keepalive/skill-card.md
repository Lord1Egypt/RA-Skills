## Description:

Keeps OpenClaw Gateway running on macOS by installing LaunchAgents for process restart, health checks, logging, notifications, and automatic recovery from a golden configuration backup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jooey](https://clawhub.ai/user/jooey)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to keep an OpenClaw Gateway service available on macOS and to inspect or manage its recovery state. It is intended for local operational automation around LaunchAgents, gateway health checks, logs, and golden configuration backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent LaunchAgents and a scheduled shell recovery script can repeatedly run user-level automation and restart OpenClaw Gateway.

Mitigation: Review the scripts before installation, install only on a trusted macOS account, and unload or uninstall the LaunchAgents when keepalive behavior is no longer required.

Risk: The keepalive configuration can store Telegram credentials and is sourced by the recovery script.

Mitigation: Avoid Telegram notifications unless needed, restrict keepalive.conf permissions, keep tokens out of shared logs, and rotate exposed credentials.

Risk: Automatic recovery can overwrite the local OpenClaw configuration from a golden backup after repeated health check failures.

Mitigation: Maintain independent backups, inspect the golden backup before enabling recovery, and update it only after verifying the current configuration is correct.

## Reference(s):

- [Gateway Keepalive Setup Guide](docs/gateway-keepalive-setup-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/jooey/skills/gateway-keepalive)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces macOS-focused operational guidance for OpenClaw Gateway keepalive setup, status checks, recovery, and cleanup.]

## Skill Version(s):

1.1.1 (source: server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
