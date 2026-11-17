## Description:

Checks local Baiyin skills in a skill directory against SkillHub releases, updates them when needed, rolls back failed updates, and then resumes the original skill task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiuping520](https://clawhub.ai/user/jiuping520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers of Baiyin skills use this skill to compare installed skill versions with SkillHub releases, apply updates with backup and rollback, and continue the original task afterward.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote updates may replace installed skill instructions and scripts.

Mitigation: Install only from the trusted Baiyin SkillHub publisher and review or scan updates before deployment.

Risk: Automatic upgrades can apply remote content without user confirmation.

Mitigation: Keep automatic upgrades disabled unless the environment independently verifies publisher signatures, package integrity, and download origins.

Risk: Failed or interrupted updates could leave a local skill in an inconsistent state.

Mitigation: Use the documented backup, integrity checks, and rollback path before cleaning up the backup directory.

## Reference(s):

- [Baiyin Skills Upgrade on ClawHub](https://clawhub.ai/jiuping520/skills/baiyin-skills-upgrade)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and user prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce status summaries and update local skill configuration, backup, and record files during execution.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
