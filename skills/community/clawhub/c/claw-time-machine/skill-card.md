## Description:

Backup, restore, and migrate OpenClaw installations while preserving workspace memories, credentials, custom skills, scheduled tasks, and core configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tacitlab](https://clawhub.ai/user/tacitlab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create, inspect, restore, and migrate backups of important OpenClaw state during upgrades, server moves, or recovery work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups can contain credentials and other sensitive OpenClaw state.

Mitigation: Treat each archive as a secrets bundle, store it privately, and do not share or restore archives from untrusted sources.

Risk: Restore and migration flows overwrite preserved OpenClaw state paths.

Mitigation: Inspect the backup list first, keep the safety backup path shown by the script, and use --force only when non-interactive automation is intentional.

Risk: Remote migration depends on SSH restore commands and a caller-provided remote directory.

Mitigation: Use trusted target hosts and remote directories, and review remote-script quoting, archive validation, and file-permission controls before production use.

## Reference(s):

- [Claw Time Machine Usage Notes](references/usage.md)
- [Claw Time Machine on ClawHub](https://clawhub.ai/tacitlab/skills/claw-time-machine)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include destructive restore or migration commands that should be reviewed before execution.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
