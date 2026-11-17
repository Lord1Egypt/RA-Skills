## Description:

Installs a macOS or Linux service that probes the OpenClaw gateway every 2 minutes and auto-recovers it on failure, sending Telegram alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[judas-oc](https://clawhub.ai/user/judas-oc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators managing OpenClaw deployments use this skill to install a lightweight macOS LaunchAgent or Linux systemd user service that monitors the gateway and attempts automatic recovery when health checks fail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installers can turn unvalidated setup values into persistent user-level shell or service execution risks.

Mitigation: Review or patch installers before installing; validate OC_PORT as a numeric port, restrict TELEGRAM_ID to the expected format, and avoid unusual or attacker-controlled workspace paths and environment variables.

Risk: The skill installs a persistent user-level watchdog that automatically restarts the gateway and can send Telegram alerts when configured.

Mitigation: Install only when that persistent recovery behavior is acceptable, and verify the generated LaunchAgent or systemd user service before enabling it.

Risk: State and logs are written under shared /tmp paths.

Mitigation: Move state and log files out of shared /tmp when using the skill in environments where local users or cleanup policies could affect those files.

Risk: The Linux watchdog includes a pkill fallback if the expected systemd service is not active.

Mitigation: Remove the fallback unless the target gateway process can be identified exactly.

## Reference(s):

- [Gateway Watchdog Lite on ClawHub](https://clawhub.ai/judas-oc/skills/gateway-watchdog-lite)
- [Gateway Recovery Gotchas](references/gotchas.md)
- [ConfusedUser.com](https://confuseduser.com)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces installation, verification, logging, manual recovery, and uninstall guidance for macOS and Linux OpenClaw gateway watchdog setup.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
