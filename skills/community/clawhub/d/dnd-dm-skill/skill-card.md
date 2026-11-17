## Description:

An AI dungeon master for D&D 5e that guides adventures, resolves combat and checks, creates characters, and manages game saves.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ackiles](https://clawhub.ai/user/ackiles)

### License/Terms of Use:

MIT-0

## Use Case:

Players and game masters use this skill to run conversational D&D adventures, apply rules and dice checks, manage characters and saves, and create or adapt adventure modules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled host-agent instructions can change memory and agent behavior outside the game.

Mitigation: Audit or remove the bundled AGENTS.md behavior before installation; do not permit writes to global memory, heartbeat, agent-policy, or skill files without explicit user approval.

Risk: Host-agent instructions may reach unrelated personal services or repositories.

Mitigation: Keep email, calendars, social notifications, and repository access disabled unless the user explicitly enables those actions.

## Reference(s):

- [ClawHub release](https://clawhub.ai/ackiles/skills/dnd-dm-skill)
- [Dungeon master rules](artifact/references/DM_RULES.md)
- [Character creation](artifact/references/CHAR_CREATION.md)
- [Module creation workflow](artifact/module-forge/references/module-forge-workflow.md)
- [Experience mapping workflow](artifact/echo-map/references/echo-map-workflow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands]

**Output Format:** [Conversational text and Markdown; structured game and module data as JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local character sheets, adventure modules, and saved game state.]

## Skill Version(s):

1.2.1 (source: ClawHub release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
