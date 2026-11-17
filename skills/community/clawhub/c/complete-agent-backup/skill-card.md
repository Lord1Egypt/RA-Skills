## Description:

Complete Agent Backup supports multi-platform backup and restore workflows for Hermes Agent and OpenClaw, including configuration, credentials, sessions, skills, workspace state, optional encryption, cloud upload, retention, integrity checks, and restore guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geoffguides](https://clawhub.ai/user/geoffguides)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent operators use this skill to create, configure, verify, and restore backups for Hermes Agent and OpenClaw installations. It is intended for preserving or migrating agent state that may include secrets, conversations, skills, and workspace files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backup archives can contain passwords, tokens, conversations, and executable agent components.

Mitigation: Treat every archive as sensitive data, keep restrictive file permissions, encrypt intentionally with --encrypt when needed, and avoid sharing archives broadly.

Risk: Restoring an archive can overwrite active agent state or introduce executable components.

Mitigation: Restore only archives from fully trusted sources, run a dry run first, and review the target paths before applying changes.

Risk: Configured encryption may not protect an archive unless encryption is explicitly requested for that backup run.

Mitigation: Require --encrypt for sensitive backups and verify the resulting archive is encrypted before transfer or cloud upload.

Risk: Cloud upload can expose sensitive archives if the uploader or destination is not audited.

Mitigation: Audit the uploader and destination before enabling cloud upload, and avoid cloud upload for high-sensitivity backups unless storage controls are verified.

## Reference(s):

- [Complete Agent Backup ClawHub Page](https://clawhub.ai/geoffguides/skills/complete-agent-backup)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)
- [Backup Script](artifact/scripts/backup.sh)
- [Restore Script](artifact/scripts/restore.sh)
- [Configuration Script](artifact/scripts/config.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe file creation, restore, cloud upload, retention, and verification workflows for local agent backup archives.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
