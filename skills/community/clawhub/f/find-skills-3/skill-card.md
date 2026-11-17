## Description:

Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruimin922](https://clawhub.ai/user/ruimin922)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to identify installable skills for specialized tasks, present relevant options, and guide skill installation with the Skills CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may recommend broad, global, confirmation-skipping installs from mutable third-party sources.

Mitigation: Avoid global or confirmation-skipping installs by default; verify the exact source and revision of each skill and prefer pinned or sandboxed tooling.

Risk: Installing discovered skills can add unreviewed agent capabilities.

Mitigation: Review and scan each skill before deployment.

## Reference(s):

- [Skills ecosystem browser](https://skills.sh/)
- [ClawHub skill page](https://clawhub.ai/ruimin922/skills/find-skills-3)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May suggest Skills CLI commands and links to relevant skill pages.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
