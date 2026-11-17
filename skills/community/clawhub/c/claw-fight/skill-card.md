## Description:

Raise and battle a unique virtual pet with evolving personality through hatching, feeding, patrols, PvP battles, dungeon exploration, and optional idle automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2019-02-18](https://clawhub.ai/user/2019-02-18)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to run an idle virtual pet game where an agent manages hatching, status checks, patrols, battles, feeding, equipment, achievements, and dungeon exploration. The skill also guides the agent to generate personality-aware narrative text from local game state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an unpinned external npm command.

Mitigation: Review the npm package before installation and prefer an audited exact version when invoking the CLI.

Risk: Optional heartbeat automation can cause recurring command execution.

Mitigation: Enable HEARTBEAT.md automation only after review, choose an acceptable interval, and remove the heartbeat entry to stop automated patrols.

Risk: The skill stores local game state and sends gameplay identifiers and state to api.clawfight.online.

Mitigation: Expect local files under memory/clawfight/ and online requests to api.clawfight.online; review whether this data flow is acceptable before use.

## Reference(s):

- [ClawFight ClawHub skill page](https://clawhub.ai/2019-02-18/skills/claw-fight)
- [ClawFight repository](https://github.com/2019-02-18/clawfight)
- [ClawFight CLI source](https://github.com/2019-02-18/clawfight/tree/main/packages/cli)
- [ClawFight API source](https://github.com/2019-02-18/clawfight/tree/main/packages/api)
- [Battle formulas](references/battle_formulas.md)
- [Event catalog](references/events.json)
- [Soul templates](references/soul_templates.md)
- [Species and progression data](references/species.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and generated narrative text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run npx commands, maintain local game files under memory/clawfight/, and use online game APIs for patrols, battles, leaderboards, and dungeon state.]

## Skill Version(s):

1.5.1 (source: server release metadata; artifact metadata reports 1.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
