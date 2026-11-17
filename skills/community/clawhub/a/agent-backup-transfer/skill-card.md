## Description:

Backup and restore an OpenClaw agent workspace and configuration to preserve memory, identity, settings, or migrate to another computer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pacifier00](https://clawhub.ai/user/pacifier00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create, list, rotate, and restore backups of local OpenClaw workspace and configuration data. It also provides migration guidance for moving an agent to a new Linux or WSL2 environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups may contain sensitive agent memory, identity, configuration, and credentials.

Mitigation: Store and transfer backup archives only with strong local permissions and encryption.

Risk: Restoring an archive can overwrite trusted OpenClaw agent files.

Mitigation: Create a fresh backup before restoring and restore only archives you created and trust.

Risk: Unreviewed archives may contain unexpected or unsafe contents.

Mitigation: Inspect backup archives before extracting them.

Risk: Auto-backup hooks or crontab entries introduce recurring backup execution from the OpenClaw workspace.

Mitigation: Enable recurring backups only when that execution pattern is acceptable for the environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pacifier00/skills/agent-backup-transfer)
- [Publisher profile](https://clawhub.ai/user/pacifier00)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of local tar.gz backup archives and hook scripts when the user runs the provided shell commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
