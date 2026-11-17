## Description:

context-game turns an agent into a Chinese-language open-world dialogue game engine with structured world simulation, relationship tension, dice-based adjudication, and persistent saves across fourteen genres.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlesresearch001](https://clawhub.ai/user/charlesresearch001)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users and players use this skill to run a structured Chinese-language narrative game where the agent acts as world simulator, narrator, and referee. It supports new or resumed games, genre selection, custom worlds, risk checks, dice rolls, state updates, and retirement summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Save-slot handling may write outside the intended save folder when the agent has broad filesystem write access.

Mitigation: Review the skill before installation, restrict the agent filesystem scope where possible, and require save-slot validation that rejects '.', '..', and symlinked paths.

Risk: The skill creates and updates local persistent game files during normal play.

Mitigation: Install it only in workspaces where local save files are expected, and keep game saves inside the skill's saves directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlesresearch001/skills/context-game)
- [Publisher profile](https://clawhub.ai/user/charlesresearch001)
- [Skill README](artifact/README.md)
- [World library overview](artifact/world/README.md)
- [Core game rules](artifact/rules/rules.md)
- [Suspicion event module](artifact/rules/suspicion.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese-language narrative text with Markdown status summaries, JSON-backed save files, and shell commands for save operations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local persistent save files; gameplay relies on Python script commands for rolls, validation, archiving, world initialization, and state updates.]

## Skill Version(s):

0.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
