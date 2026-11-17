## Description:

Dreaming lets an agent use quiet heartbeat periods for freeform exploratory thinking, returning topics and capturing later-reviewable notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[briancolinger](https://clawhub.ai/user/briancolinger)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to turn low-activity heartbeat windows into reflective topic generation and Markdown notes for later human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Modified local state can abuse dreamChance handling to execute arbitrary Python code.

Mitigation: Constrain dreamChance to a numeric value before use and keep data/dream-state.json writable only by trusted components.

Risk: Dream notes may capture sensitive private, client, or workspace information.

Mitigation: Avoid storing sensitive information in dream files and review generated notes before sharing or committing them.

## Reference(s):

- [Dreaming on ClawHub](https://clawhub.ai/briancolinger/skills/dreaming)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Topic string output, Markdown note guidance, shell command snippets, and JSON state/configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local dream state under data/ and expects dream notes under memory/dreams/.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
