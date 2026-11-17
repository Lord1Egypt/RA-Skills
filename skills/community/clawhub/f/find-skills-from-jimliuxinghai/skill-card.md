## Description:

Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baotangyin](https://clawhub.ai/user/baotangyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search for installable skills, compare relevant options, and install skills that extend an agent for a requested task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to search for and install external skills, including global installs that persistently change the user's agent environment.

Mitigation: Use it only when the user explicitly wants skill discovery or installation, inspect target skills before installation, and avoid global unattended installs unless persistent environment changes are intended.

Risk: Recommended installation commands may be unpinned or not source-verified.

Mitigation: Prefer pinned package references and source-verified commands before running installation steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baotangyin/skills/find-skills-from-jimliuxinghai)
- [Skills directory](https://skills.sh/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include suggested skill names, installation commands, and links to skill listings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
