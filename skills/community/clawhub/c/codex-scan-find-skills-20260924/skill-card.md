## Description:

Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[techflowauto](https://clawhub.ai/user/techflowauto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to discover suitable installable skills, assess basic quality signals, and optionally install skills through the Skills CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent toward fetching, globally installing, or updating external skills with mutable commands and skipped confirmations.

Mitigation: Review each recommended skill's source before installation, avoid blind -y installs in sensitive environments, and prefer pinned or locally vetted tooling.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/techflowauto/skills/codex-scan-find-skills-20260924)
- [Skills directory and leaderboard](https://skills.sh/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend external skills and install or update commands for user review before execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
