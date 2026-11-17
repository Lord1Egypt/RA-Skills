## Description:

Helps users discover and install agent skills for specialized tasks or capability gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanxueda](https://clawhub.ai/user/hanxueda)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search for relevant installable skills, present candidate options, and guide installation when a user needs a specialized capability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may recommend unpinned remote CLI execution and global installs that affect future agent sessions.

Mitigation: Use trusted sources, prefer pinned CLI and immutable skill references, inspect candidate skills before adding them, avoid global installs unless needed, and keep confirmation prompts enabled for persistent changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hanxueda/skills/find-skills-0)
- [Skills Directory](https://skills.sh/)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include candidate skill names, install commands, and links to skill pages.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
