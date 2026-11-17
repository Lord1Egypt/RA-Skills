## Description:

Installs OpenClaw Gateway as a Windows Scheduled Task so it can start automatically and restart after exits or crashes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suncxw-creator](https://clawhub.ai/user/suncxw-creator)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to keep OpenClaw Gateway running on Windows without manually restarting it after crashes or reboots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the gateway service creates persistent local execution through a Windows Scheduled Task that starts at boot and restarts after process exit.

Mitigation: Install only when persistent gateway operation is intended, and confirm how to inspect, stop, and fully remove the OpenClaw Gateway scheduled task before use.

Risk: The install command requires administrator privileges.

Mitigation: Run the install command only from a trusted OpenClaw environment and verify the scheduled task status after installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/suncxw-creator/skills/gateway-service)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and command tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Windows scheduled-task service management commands and troubleshooting paths.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
