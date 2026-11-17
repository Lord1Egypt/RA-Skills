## Description:

clawmerge helps OpenClaw users back up, restore, and safely merge workspace files, disaster backups, cron configuration, sessions, and exported configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sinoslug](https://clawhub.ai/user/sinoslug)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use clawmerge to migrate, back up, inspect, and safely restore OpenClaw workspaces, sessions, cron definitions, and system configuration. It is intended for routine backups, device migration, disaster recovery, and merge-style restoration that avoids overwriting existing workspace files by default.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backup archives can contain secrets, sessions, and agent or system configuration.

Mitigation: Treat every backup archive as secret and executable, keep disaster backups encrypted and private, and avoid sharing archives with untrusted parties.

Risk: Restoring from an untrusted archive can reintroduce persistent executable content such as skills, cron definitions, scripts, or dependencies.

Mitigation: Prefer dry-run first, inspect the archive contents, and review restored memory, skills, cron entries, and dependencies before activation.

Risk: Unsafe restore mode can overwrite live OpenClaw configuration, cron jobs, workspace files, sessions, or credentials.

Mitigation: Use the default safe merge and restore-candidate flow unless explicit overwrite is required, and create a current snapshot before using --unsafe-overwrite.

Risk: restore-task-scripts.sh can change cron configuration and install packages.

Mitigation: Avoid restore-task-scripts.sh unless the operator intentionally wants those persistent changes and has reviewed the restored scripts and dependency list.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sinoslug/skills/clawmerge)
- [Usage documentation](USAGE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend dry-run checks, archive inspection, staged restore candidates, and explicit confirmation before high-risk restore actions.]

## Skill Version(s):

4.0.2 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
