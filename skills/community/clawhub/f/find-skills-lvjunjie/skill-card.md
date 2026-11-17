## Description:

Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to discover installable skills for specialized domains, evaluate search results, and optionally install selected skills with the Skills CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may steer an agent toward unpinned third-party skill installs, including global installs that skip confirmation.

Mitigation: Review the target skill and install source before use, avoid global installs unless needed, remove `-y` from install commands, and prefer pinned trusted sources.

## Reference(s):

- [Find Skills Pro on ClawHub](https://clawhub.ai/lvjunjie-byte/skills/find-skills-lvjunjie)
- [Skills Directory](https://skills.sh/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown with inline shell commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose third-party skill install commands for user review.]

## Skill Version(s):

1.0.0 (source: server release evidence, released 2026-03-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
