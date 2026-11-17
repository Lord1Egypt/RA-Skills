## Description:

Backs up or restores a complete OpenClaw installation, including configuration, agents, flows, skills, credentials, memory, workspace, and Telegram bots, as a portable archive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brunovu20](https://clawhub.ai/user/brunovu20)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create portable backups, migrate OpenClaw installations, list backups, verify archives, and restore configurations on another machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups can contain credentials, secrets, identity files, and other sensitive OpenClaw state.

Mitigation: Store backups in secure locations, use encrypted backups for transfer or shared storage, and avoid plaintext backups in cloud-synced or multi-user locations.

Risk: Restore behavior can write files outside the intended OpenClaw directory if archive path validation is insufficient.

Mitigation: Only restore archives you created or fully trust, verify archives before restore, and review archive paths until restore path validation is fixed.

Risk: Backing up or restoring while OpenClaw is running can capture or apply inconsistent runtime state.

Mitigation: Stop OpenClaw before backup or restore, especially when SQLite databases or other mutable state may be active.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brunovu20/skills/claw-home-dir-backup-restore)
- [OpenClaw Backup Path Policy](references/paths.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands and archive file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create, list, verify, or restore .tar.gz and .tar.gz.gpg backup archives through bundled shell scripts.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
