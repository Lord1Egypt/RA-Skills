## Description:

Backup Claw helps agents back up and restore OpenClaw configuration files, excluding workspace data, using date-stamped backups with change detection and changelog logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyingtimes](https://clawhub.ai/user/flyingtimes)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to maintain local OpenClaw configuration backups, change the configured backup directory, detect configuration changes, and restore a dated backup after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The restore source may be pointed outside the selected backup folder and copy arbitrary local files into OpenClaw configuration after confirmation.

Mitigation: Use only private, trusted backup directories; provide only real YYYY-MM-DD backup dates; and fix restore validation to require the canonical restore source to be an immediate child of the backup root before use.

Risk: Backup and restore operations copy or overwrite local OpenClaw configuration data.

Mitigation: Review the backup path and restore date before execution, keep backups private, and confirm restore only when replacing the current OpenClaw configuration is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flyingtimes/skills/backupclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Backups target ~/.openclaw/, exclude workspace/, and use dated backup directories.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
