## Description:

Helps users discover and install agent skills when they ask for specialized capabilities or ways to extend an agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylinjackson](https://clawhub.ai/user/kylinjackson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search for installable skills, present relevant options, and optionally run Skills CLI installation commands after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can encourage unpinned external CLI execution and persistent global skill installation with skipped confirmations.

Mitigation: Use a pinned, trusted Skills CLI version, inspect target skill source before installation, avoid global installation unless needed, and avoid skipped confirmations unless the exact install has already been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kylinjackson/skills/find-skill-heqi1111)
- [Skills directory](https://skills.sh/)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include search summaries, install commands, and links to discovered skills.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
