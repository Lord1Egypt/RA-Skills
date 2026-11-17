## Description:

Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[williamwang-wh](https://clawhub.ai/user/williamwang-wh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to identify relevant installable skills, present discovery results, and guide skill installation when a requested capability may already exist in the skill ecosystem.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to run unpinned remote CLI commands for skill discovery or installation.

Mitigation: Use trusted and pinned CLI versions where possible, and verify the exact skill source and revision before installation.

Risk: The skill includes an unattended global install pattern for third-party skills.

Mitigation: Avoid unattended global installs unless the user explicitly approves the specific package after reviewing its contents and provenance.

Risk: Third-party skills discovered through marketplace search may have limited or unavailable provenance.

Mitigation: Review the candidate skill files and server-resolved provenance before installing or using the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/williamwang-wh/skills/claw-find-skills)
- [Skills marketplace](https://skills.sh/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include skill names, install commands, marketplace links, fallback guidance, and installation offers.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
