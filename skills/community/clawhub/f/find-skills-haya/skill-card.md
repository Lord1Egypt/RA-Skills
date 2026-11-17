## Description:

Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hayasam](https://clawhub.ai/user/hayasam)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to discover relevant installable skills, compare basic quality signals, and install selected skills when they want to extend an agent's capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to run unpinned external tooling and install third-party skills globally.

Mitigation: Require explicit user approval before installation, avoid global installs unless needed, and pin or verify the CLI and target skill source.

Risk: Skipped confirmations during skill installation can allow future agent sessions to inherit unreviewed behavior.

Mitigation: Avoid automatic confirmation flags and inspect each skill before allowing it to affect future sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hayasam/skills/find-skills-haya)
- [Skills directory](https://skills.sh/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with inline shell commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recommended skill names, install commands, quality considerations, and next-step guidance.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
