## Description:

Set up a systemd-based watchdog that keeps long-running Node.js services alive across shell exits, SSH disconnects, agent-runtime restarts, and server reboots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dyagil](https://clawhub.ai/user/dyagil)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure a user-systemd watchdog that checks long-running Node.js services and restarts them when they stop. It is most relevant for Telegram bots, dashboards, or similar services that need to survive shell exits, SSH disconnects, runtime restarts, and reboots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The watchdog enables persistent background execution through user-systemd timers and login lingering.

Mitigation: Review the timer and lingering behavior before enabling it, and add explicit stop, disable, and uninstall steps for the deployed service.

Risk: The script sends service status to a hard-coded Telegram chat using a bot token read from a project .env file.

Mitigation: Remove the Telegram notification code or make the chat ID and token source configurable, then confirm the recipient and credential handling are intentional.

Risk: The artifact references systemd unit files that are not present in the provided artifact.

Mitigation: Verify or create the referenced unit and timer files before installing or enabling the watchdog.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dyagil/skills/dyagil-services-watchdog)
- [ClawHub publisher profile](https://clawhub.ai/user/dyagil)
- [Artifact skill definition](artifact/SKILL.md)
- [Watchdog shell script](artifact/scripts/services-watchdog.sh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash commands and shell script configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational setup guidance and service-specific script edits; users should review paths, service names, credentials, and systemd units before installation.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
