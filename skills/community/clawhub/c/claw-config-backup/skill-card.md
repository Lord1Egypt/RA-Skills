## Description:

Backup OpenClaw configuration files with JSON5 validation, hash-based change detection, and timestamped backup copies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to validate an OpenClaw JSON5 configuration file and create a timestamped backup, while skipping backup creation when the latest copy already matches the source file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copied OpenClaw configuration files may contain sensitive settings.

Mitigation: Use an explicit OpenClaw config path and a backup directory you control; protect or delete backup copies according to local data-handling requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goog/skills/claw-config-backup)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Files]

**Output Format:** [Markdown with inline shell commands and local file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates timestamped JSON backup files in a user-selected directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
