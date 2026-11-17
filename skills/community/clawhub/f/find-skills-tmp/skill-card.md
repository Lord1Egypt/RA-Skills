## Description:

Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhichengsong](https://clawhub.ai/user/zhichengsong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to find installable skills for specialized tasks, compare relevant options, and install a chosen skill through the Skills CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned remote CLI execution may run changing third-party code in sensitive environments.

Mitigation: Review the skill and CLI source before use, and prefer pinned CLI versions when executing install or search commands.

Risk: Global non-interactive installation can make third-party skills available across sessions without an explicit per-install review.

Mitigation: Use non-global installs by default and require source review before approving global installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhichengsong/skills/find-skills-tmp)
- [Skills Directory](https://skills.sh/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include skill names, install commands, and links to skill listings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
