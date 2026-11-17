## Description:

Auto Backup Pro helps an agent configure scheduled local or cloud backups with incremental backup, compression and encryption options, verification reports, and retry behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linbo405](https://clawhub.ai/user/linbo405)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to set up recurring backups, inspect backup status, and recover recent work products from local or cloud backup targets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Overbroad source directory settings can copy unnecessary files or sensitive data.

Mitigation: Configure the narrowest practical source directories and avoid backing up secrets unless they are intentionally required.

Risk: Backups to cloud or shared storage can expose confidential data if encryption is disabled.

Mitigation: Enable encryption for cloud or shared backup targets and review retention settings.

Risk: Restore operations can overwrite existing files when target paths are misconfigured.

Mitigation: Confirm restore targets before recovery and test restores in a noncritical location when possible.

## Reference(s):

- [Auto Backup Pro ClawHub Page](https://clawhub.ai/linbo405/skills/auto-backup-pro)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and JSON configuration examples with backup status, storage usage, and backup history information]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include backup source directories, target locations, schedules, compression, encryption, and retention settings.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
