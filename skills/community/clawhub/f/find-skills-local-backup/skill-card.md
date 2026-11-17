## Description:

Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[12357851](https://clawhub.ai/user/12357851)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to identify relevant installable skills, search the open agent skills ecosystem, and present installation options for common specialized tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run a live npm CLI and install third-party skills.

Mitigation: Inspect the skill source and use a pinned, reviewed Skills CLI version before running installation commands.

Risk: The documented global installation command can skip confirmation prompts and make installed skills available across sessions.

Mitigation: Avoid `-y` unless the package has been reviewed, and use global installation only when persistent user-level availability is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/12357851/skills/find-skills-local-backup)
- [Skills registry](https://skills.sh/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include skill search queries, installation commands, and links to skill listings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
