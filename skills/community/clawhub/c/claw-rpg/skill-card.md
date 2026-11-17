## Description:

Claw RPG adds a D&D-style progression layer for OpenClaw agents by generating character sheets, tracking XP and levels, producing RPG-flavored conversation text, and providing a character dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ramboxie](https://clawhub.ai/user/ramboxie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to give an agent persistent RPG character state, XP progression, level tracking, optional conversation flavor, daily reports, arena interactions, and a local dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent after-reply hooks can decorate unrelated future responses and change RPG state outside intentional RPG workflows.

Mitigation: Enable the AGENTS.md after-reply hook only when persistent RPG behavior is desired, and remove or disable it for neutral agent sessions.

Risk: The cron setup can use an OpenClaw gateway token to create a recurring main-session event.

Mitigation: Run setup-cron.mjs only after reviewing the scheduled event and token use, or configure XP synchronization manually.

Risk: The dashboard can expose character and activity data on the local network.

Mitigation: Run the dashboard only on trusted networks, preferably with localhost-only access or host firewall restrictions.

Risk: Telegram reporting can send character and activity data outside the local workspace.

Mitigation: Configure Telegram notifications only after reviewing the data included in reports and event messages.

## Reference(s):

- [Claw RPG on ClawHub](https://clawhub.ai/ramboxie/skills/claw-rpg)
- [Classes reference](references/classes.md)
- [Abilities reference](references/abilities.md)
- [Prestige reference](references/prestige.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and terminal text with inline shell commands and JSON-backed agent state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can update persistent character data, emit optional RPG flavor text, send reports, and serve a local web dashboard.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
