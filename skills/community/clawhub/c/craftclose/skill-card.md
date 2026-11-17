## Description:

AI-powered Minecraft server monitoring with crash detection, auto-restart, and smart alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ginhooser-cyber](https://clawhub.ai/user/ginhooser-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Minecraft server operators use CraftClose to monitor Java/Paper Minecraft servers, diagnose crashes and performance issues, configure alerts, and manage Pterodactyl-backed server operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install an unpinned global CLI that can use SSH/API credentials, restart servers, run console commands, and send logs to external services.

Mitigation: Review before installing, prefer a pinned and audited craftclose version, and run it under a restricted service account.

Risk: Minecraft host, Pterodactyl, Gemini, Telegram, and Discord credentials or logs may be exposed through broad configuration or external data-sharing paths.

Mitigation: Use dedicated least-privilege SSH/API credentials, avoid broad admin keys, and treat AI and alert integrations as external data-sharing destinations.

Risk: Auto-restart and console actions can affect live server availability or state.

Mitigation: Enable restart and console operations only after reviewing rate limits, confirmation gates, and operational impact.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ginhooser-cyber/skills/craftclose)
- [CraftClose npm Package](https://www.npmjs.com/package/craftclose)
- [CraftClose GitHub Project](https://github.com/LaunchDay-Studio-Inc/craftclose)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational guidance for SSH, RCON, Pterodactyl, Telegram, Discord, and Gemini configuration.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
