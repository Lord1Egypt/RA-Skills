## Description:

Discover, install, update, or create the right skill when a workflow gap appears.

This skill is ready for commercial/non-commercial use.

## Publisher:

[505768069-rgb](https://clawhub.ai/user/505768069-rgb)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to decide whether a recurring workflow gap should reuse an existing skill, install a ClawHub skill, or create or update a concise local skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to install, create, update, or delete skills, including in shared skill directories.

Mitigation: Require explicit confirmation before installing, creating, updating, or deleting skills, and use shared paths only when persistent cross-role changes are intended.

Risk: Broad implicit invocation may cause skill-management steps to be considered for tasks that do not need them.

Mitigation: Use the skill for recurring workflow gaps and skip it for one-off trivial tasks or generic reasoning.

## Reference(s):

- [Adaptive Skill Factory on ClawHub](https://clawhub.ai/505768069-rgb/skills/adaptive-skill-factory)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline commands, paths, and skill file snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed skill files or install, update, or delete commands when explicitly confirmed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
