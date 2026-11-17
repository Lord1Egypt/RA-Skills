## Description:

AC-Nexus helps agents install, configure, and operate a cross-platform air-conditioner control library for Broadlink RM infrared devices and Xiaomi MIoT-compatible infrared remote controllers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oywq00008-cell](https://clawhub.ai/user/oywq00008-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to set up and control air conditioners through Broadlink IR blasters or Xiaomi MIoT-compatible infrared controllers, including weather-aware adjustment, scheduling, logging, and storm-related shutdown workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install mutable remote code and dependencies before operating connected air-conditioning devices.

Mitigation: Review the referenced repository and dependencies first, prefer a pinned commit or signed release, install in a virtual environment, and run under a non-admin account.

Risk: Configuration may persist Xiaomi tokens, API keys, device names, location data, and schedules in ~/.ac_controller/config.json.

Mitigation: Treat the configuration file as sensitive, protect it with owner-only permissions or a credential manager, and avoid sharing logs or configuration exports that may reveal device or location details.

Risk: Schedules, auto-adjustment, and storm shutdown behavior can continue autonomously after the agent task completes.

Mitigation: Require explicit user approval before enabling or modifying automation, and disable schedule_enabled and auto_adjust when autonomous control should stop.

## Reference(s):

- [AC-Nexus ClawHub Skill Page](https://clawhub.ai/oywq00008-cell/skills/acnexus)
- [AC-Nexus GitHub Repository](https://github.com/oywq00008-cell/AC-Nexus.git)
- [AC-Nexus Releases](https://github.com/oywq00008-cell/AC-Nexus/releases/latest)
- [AC-Nexus OpenWRT Plugin](https://github.com/oywq00008-cell/AC-Nexus-OpenWRT)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, Python, and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing setup and operation guidance; generated commands and configuration changes may persist credentials, schedules, and device state on the user's machine.]

## Skill Version(s):

5.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
