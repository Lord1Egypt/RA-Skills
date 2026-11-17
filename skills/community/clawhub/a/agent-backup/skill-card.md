## Description:

Openclaw Backup helps agents create encrypted, verifiable OpenClaw backups, restore from staged archives with rollback, schedule daily backups, and optionally push operational archives to GitHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zurbrick](https://clawhub.ai/user/zurbrick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to back up operational state, optionally encrypt secrets for local recovery, verify backup integrity, rehearse restores, and recover an OpenClaw installation after data loss or configuration failure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Operational archives can contain broad workspace data and may be sensitive even when secrets are excluded.

Mitigation: Inspect archive contents before upload and store operational backups only in private, access-controlled locations.

Risk: Encrypted secrets archives may be uploaded if the operator passes them explicitly.

Mitigation: Upload secrets only by deliberate exception, confirm the file is .age encrypted, and use strong age keys or passphrases.

Risk: Restoring an archive from an untrusted source can replace local OpenClaw state.

Mitigation: Restore only trusted archives, verify manifests and checksums, run dry-run first, and keep the pre-restore rollback copy.

## Reference(s):

- [Restore Guide](references/restore-guide.md)
- [What to Back Up](references/what-to-backup.md)
- [Retention Policy](references/retention-policy.md)
- [ClawHub skill page](https://clawhub.ai/zurbrick/skills/agent-backup)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline bash commands; scripts create tar.gz archives, optional .age secrets archives, manifest.json files, and verification status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local command-line tools such as python3, tar, age for secrets workflows, gh for GitHub push, and the OpenClaw CLI for scheduling.]

## Skill Version(s):

1.1.0 (source: release metadata and changelog, released 2026-03-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
