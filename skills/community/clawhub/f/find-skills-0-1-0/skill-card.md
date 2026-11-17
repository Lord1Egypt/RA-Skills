## Description:

Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leochan14](https://clawhub.ai/user/leochan14)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to discover relevant installable skills for requested tasks, compare search results, and receive installation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may encourage broad, global installation of third-party skills using unpinned package-manager commands.

Mitigation: Review the specific skill source and publisher before installation, prefer explicit local installs, avoid `-g -y`, and pin or verify the CLI and skill version before running commands.

## Reference(s):

- [Skill page](https://clawhub.ai/leochan14/skills/find-skills-0-1-0)
- [Skills CLI catalog](https://skills.sh/)
- [Example skill result](https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include skill search suggestions, install commands, and links to inspect skill sources.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
