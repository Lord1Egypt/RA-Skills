## Description:

Helps users discover and install agent skills when they ask for specialized capabilities or want to extend an agent's functionality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[v585](https://clawhub.ai/user/v585)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search the open agent skills ecosystem, compare relevant skill options, and generate install commands when they need specialized workflows or tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may suggest unpinned package-manager commands for searching and installing skills.

Mitigation: Verify the Skills CLI package and selected skill source before running commands, and prefer pinned versions or immutable references.

Risk: The skill can recommend globally installing third-party skills with confirmation skipped.

Mitigation: Avoid global non-interactive installs unless intentional; inspect candidate skills before trusting them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/v585/skills/find-skills-cn)
- [Skills directory](https://skills.sh/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May suggest package-manager commands for finding or installing skills.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
