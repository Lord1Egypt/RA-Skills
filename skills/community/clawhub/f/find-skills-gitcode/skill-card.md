## Description:

Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jherculesqz](https://clawhub.ai/user/jherculesqz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to discover installable skills for a requested task, compare candidate quality, and receive relevant install commands or links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages broad activation and can lead agents toward installing additional skills.

Mitigation: Install only after confirming the user wants help discovering and installing other skills, and inspect target skills before adding them.

Risk: The skill suggests remote CLI execution through npx, which can run changing package code when unpinned.

Mitigation: Pin or verify the Skills CLI version before use, and prefer an isolated environment for testing.

Risk: The documented global non-interactive install flags can create persistent user-level changes without a confirmation prompt.

Mitigation: Avoid `-g -y` unless a persistent global install is explicitly intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jherculesqz/skills/find-skills-gitcode)
- [Skills directory](https://skills.sh/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include install commands and quality checks for third-party skills.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
