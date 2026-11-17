## Description:

Production-grade bash watchdog for the OpenClaw gateway that runs via launchd every 5 minutes and uses boot grace, progressive retry with backoff, port checks, stale PID detection, and restart cooldowns to keep the gateway available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bryantegomoh](https://clawhub.ai/user/bryantegomoh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install or run a macOS watchdog that monitors a local OpenClaw gateway and restarts the launchd service after conservative health checks fail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a user-level background job that checks the OpenClaw gateway every 5 minutes and may restart it automatically.

Mitigation: Install it only when persistent monitoring and automatic restarts are desired, verify the LaunchAgent script path, and know how to unload the LaunchAgent before loading it.

Risk: The cooldown state uses a shared /tmp path, which evidence flags as an unsafe temporary-file pattern.

Mitigation: Move the cooldown file to a private directory such as ~/.openclaw/run before deployment and protect that directory with user-only permissions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown setup guidance with XML and bash code blocks, plus a bash watchdog script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Designed for macOS launchd; writes operational logs to ~/.openclaw/logs/watchdog.log.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
