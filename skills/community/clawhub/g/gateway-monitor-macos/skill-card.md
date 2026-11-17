## Description:

Install and operate a local OpenClaw Gateway Monitor stack on macOS with LaunchAgent and watchdog support for setup, repair, validation, and one-command status or uninstall workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yes999zc](https://clawhub.ai/user/yes999zc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install, monitor, repair, and remove a local macOS OpenClaw Gateway Monitor service stack. It is intended for LaunchAgent-based gateway health checks, watchdog restarts, service status inspection, and local monitor operation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installed monitor is a persistent local service that exposes unauthenticated network APIs.

Mitigation: Bind the service to 127.0.0.1, add authentication, and avoid installing it on shared or untrusted networks until access controls are in place.

Risk: Administrative actions can restart the gateway or restore OpenClaw configuration through GET-based API calls.

Mitigation: Remove GET-based administrative actions or require authenticated, explicit operator approval before enabling restart or restore endpoints.

Risk: The service reads provider credentials without clear disclosure.

Mitigation: Disable automatic MiniMax credential reading unless the operator explicitly opts in and understands which credential file will be read.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yes999zc/skills/gateway-monitor-macos)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text]

**Output Format:** [Markdown with inline bash code blocks and local service status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces macOS launchctl commands and installs local LaunchAgent configuration for OpenClaw gateway monitoring.]

## Skill Version(s):

1.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
