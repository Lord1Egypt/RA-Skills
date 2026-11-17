## Description:

Bootstrap and automate OBS scenes for local or remote instances via agentic-obs + mcporter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ironystock](https://clawhub.ai/user/ironystock)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and stream operators use this skill to bootstrap reusable OBS scene packs, host browser overlays, switch OBS targets, apply transition and audio defaults, and run recording or streaming smoke tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can alter OBS scenes and recording or streaming state.

Mitigation: Run it first against a test OBS profile, back up scenes, and only run the streaming dry-run when you intend to go live.

Risk: The target-switch workflow can write an external agentic-obs configuration database.

Mitigation: Back up the agentic-obs database and require an explicit database path plus acknowledgement flag before running the target switch.

Risk: Overlay HTTP and OBS WebSocket ports can expose control or files if placed on public networks.

Mitigation: Keep OBS WebSocket and overlay HTTP ports on trusted LAN or VPN networks and avoid placing private files under the skill folder.

## Reference(s):

- [ClawCast homepage](https://github.com/ironystock/clawcast)
- [ClawHub skill page](https://clawhub.ai/ironystock/skills/claw-cast)
- [Scene Map](references/scene-map.md)
- [Networking Notes](references/networking.md)
- [Troubleshooting](references/troubleshooting.md)
- [v0.2.0 Feature Notes](references/v0.2-features.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline bash commands and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local shell scripts that control OBS, write an agentic-obs configuration database, serve overlay files over HTTP, and start recording or streaming workflows.]

## Skill Version(s):

0.2.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
