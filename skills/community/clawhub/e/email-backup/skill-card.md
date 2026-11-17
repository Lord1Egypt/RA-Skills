## Description:

Email Backup packages selected directories into tar.gz archives and sends them through QQ Mail SMTP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragonhuge](https://clawhub.ai/user/dragonhuge)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to create compressed backups of selected local directories and optionally email them to a configured recipient through QQ Mail SMTP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad directory backups can email private files or workspace data to an unintended recipient.

Mitigation: Use only narrow, known-safe directories, configure explicit exclude patterns, and run with --no-send until the archive contents have been inspected.

Risk: Sensitive-data cleaning may miss secrets and can continue even after cleaning fails.

Mitigation: Do not rely on --clean as the only control; inspect archives before sending and keep secrets outside backup paths where possible.

Risk: QQ Mail SMTP credentials are required to send attachments.

Mitigation: Store credentials in environment variables, do not commit authorization codes, and rotate the mail authorization code if exposure is suspected.

Risk: Installation guidance includes local tarball and placeholder download flows that may be unverified.

Mitigation: Install from the ClawHub release or another verified source, avoid sudo, and review the scripts before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dragonhuge/skills/email-backup)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown with inline shell commands and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create tar.gz archives and send them as email attachments when the user runs the provided scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact changelog v1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
