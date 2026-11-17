## Description:

Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanfa247](https://clawhub.ai/user/yuanfa247)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search for installable skills, present relevant options, and provide Skills CLI commands for finding, adding, checking, or updating skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends mutable remote npm tooling and global, confirmation-skipping installs for third-party skills.

Mitigation: Require explicit user approval, pin CLI versions where practical, prefer local or isolated installs, and avoid confirmation-skipping flags unless the user has approved the exact package.

Risk: Search results and installed skills may come from third-party publishers with instructions the current agent has not reviewed.

Mitigation: Review publisher identity, skill source, security findings, and immutable skill references before installation or use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanfa247/skills/find-skills-yuanfa)
- [Skills directory](https://skills.sh/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown responses with inline shell commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands for searching, installing, checking, and updating third-party skills.]

## Skill Version(s):

0.1.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
