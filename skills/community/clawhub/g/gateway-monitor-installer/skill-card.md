## Description:

Install, update, run, and remove OpenClaw Gateway Monitor + Gateway Watchdog on macOS via LaunchAgent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yes999zc](https://clawhub.ai/user/yes999zc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and macOS OpenClaw operators use this skill to install, update, check, and remove a local Gateway Monitor UI server and watchdog LaunchAgent for gateway self-healing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a persistent local monitor service that can read OpenClaw logs and session data and use a MiniMax credential from the local auth profile.

Mitigation: Review the skill before installing, document credential use, and limit installation to environments where the local operator trusts the service.

Risk: The monitor exposes unauthenticated HTTP APIs on the network and includes an endpoint that can restore OpenClaw configuration.

Mitigation: Prefer a version that binds only to localhost, requires API authentication, and removes or gates configuration restore behind explicit local approval.

Risk: The installer expects LaunchAgent templates that are not present in the submitted artifact.

Mitigation: Verify the required plist templates are included and reviewed before running the installer.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yes999zc/skills/gateway-monitor-installer)
- [Local Gateway Monitor UI](http://127.0.0.1:18990)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target macOS LaunchAgent installation, status checks, and removal.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
