## Description:

Set up and run complete, encrypted, off-site backups of an OpenClaw install to Cloudflare R2 via restic, plus portable restore.

This skill is ready for commercial/non-commercial use.

## Publisher:

[servicosmkt](https://clawhub.ai/user/servicosmkt)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to configure encrypted off-site backups, test restores, and migrate or recover OpenClaw configuration, credentials, agents, workspace, and cron state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenClaw credentials and auth profiles are backed up to a third-party Cloudflare R2 bucket.

Mitigation: Use a private bucket, scope the S3 token to that bucket, and protect backups with a strong restic password.

Risk: Anyone with both the R2 credentials and .restic-pass can decrypt backed-up secrets.

Mitigation: Keep .env and .restic-pass private, store the password separately, and avoid sharing the portable restore folder.

Risk: The real restore replaces the live .openclaw directory and can lose changes made after the latest backup.

Mitigation: Run the non-destructive restore test first and proceed with the live restore only after explicitly accepting replacement of the active install.

Risk: Restore test and portable restore folders can contain decrypted secrets after inspection.

Mitigation: Manually delete restore-test and OpenClaw-restore folders after review.

## Reference(s):

- [OpenClaw](https://openclaw.ai)
- [restic](https://restic.net)
- [restic installation](https://restic.net/#installation)
- [Cloudflare R2](https://developers.cloudflare.com/r2/)
- [ClawHub skill page](https://clawhub.ai/servicosmkt/skills/backup-to-r2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with PowerShell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers Windows PowerShell backup, non-destructive restore testing, destructive portable restore, and scheduled backup setup.]

## Skill Version(s):

1.1.1 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
