## Description:

Creates hash-chained workspace backups with restore checks, an external ledger, and optional member curation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darkd](https://clawhub.ai/user/darkd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this skill to snapshot important project files, check backup integrity, and restore selected members after a reset or rollback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backup archives may contain secrets and expose them through shared storage.

Mitigation: Keep archive and stow destinations private, and review which files are included.

Risk: Configured destinations and optional command hooks can act beyond the local backup workflow.

Mitigation: Review .vault/config.json and explicitly approve --allow-cmd-ledger, --allow-external-ledger, or --stow-cmd only for trusted destinations and commands.

## Reference(s):

- [Backup protocol](references/PROTOCOL.md)
- [Security guidance](references/SECURITY.md)
- [Residual risks](references/RESIDUAL_RISK.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration guidance, Text]

**Output Format:** [Markdown with CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Running the commands can create tarball archives, SHA-256 receipts, and ledger entries.]

## Skill Version(s):

1.3.2 (source: ClawHub release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
