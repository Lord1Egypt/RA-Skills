## Description:

Routes physical performance requests across workout coaching, fitness tracking, nutrition, meal logging, macro planning, recipes, and Hevy-backed training data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cylqqqcyl](https://clawhub.ai/user/cylqqqcyl)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to route body-related requests to training, nutrition, and Hevy integration workflows. It can summarize workouts, track progress, log meals, estimate macros, save recipes, generate meal plans, and prepare grocery lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Hevy integration installs an unverified third-party CLI executable.

Mitigation: Review before installing and prefer a pinned, verified hevycli release.

Risk: The skill handles a Hevy API key and may store it in a local configuration file.

Mitigation: Avoid passing API keys on the command line, never commit credentials, and set restrictive permissions on ~/.hevycli/config.yaml.

Risk: The skill can make persistent local changes to vault, character, fitness, calendar, meal, recipe, meal-plan, and grocery-list files.

Mitigation: Confirm write operations before execution and review or back up affected files before deployment.

Risk: Fitness and nutrition outputs may be inappropriate for injuries, medical conditions, or extreme diet requests.

Mitigation: Keep recommendations performance- and recovery-oriented, avoid medical advice, and direct injury or pain concerns to a qualified professional.

## Reference(s):

- [Hevy CLI API Commands Reference](artifact/hevy/references/api_commands.md)
- [Hevy Data Structures and JSON Examples](artifact/hevy/references/data_structures.md)
- [Hevy API Docs](https://api.hevyapp.com/docs/)
- [Hevy App](https://www.hevyapp.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, structured fitness and nutrition summaries, and local file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update Obsidian vault notes for workouts, meals, recipes, meal plans, grocery lists, body metrics, and character XP when the agent has write access.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
