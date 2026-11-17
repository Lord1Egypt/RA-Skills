## Description:

COC Soul Immortality helps agents manage COC on-chain identity, encrypted IPFS-backed state backups, guardian recovery, and carrier-based recovery or migration across hosts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ngplateform](https://clawhub.ai/user/ngplateform)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent operators use this skill to configure and run COC Soul workflows: register agent DIDs, create encrypted backups, restore agent state on another host, set up guardian recovery, and operate carrier nodes. It is intended for agents that need persistent identity and recoverable state across device loss or migration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups can publish broad private agent data off-host, and weak defaults may expose sensitive state.

Mitigation: Before backup, disable autoBackup and backupOnSessionEnd unless intentionally needed, enable encryption, narrow backup categories, and treat recovery files and signing keys as secrets.

Risk: The release evidence reports a documented package version mismatch.

Mitigation: Review the exact @chainofclaw/soul package version that will run before installing or executing the skill.

Risk: A documented force-install repair command can bypass normal installation safeguards.

Mitigation: Avoid the unsafe force-install command unless the package has been independently verified and a broken install must be repaired.

Risk: Cross-host restore can overwrite host-local policy or production state if used without inspection.

Mitigation: Restore to a temporary directory first, verify integrity, preserve target-host authentication and policy settings, and promote to production only after explicit operator confirmation.

## Reference(s):

- [Backup and restore reference](artifact/references/backup.md)
- [Carrier operations reference](artifact/references/carrier.md)
- [Configuration schema reference](artifact/references/config.md)
- [DID identity management reference](artifact/references/did.md)
- [Guardian and social recovery reference](artifact/references/guardian-recovery.md)
- [@chainofclaw/soul npm package](https://www.npmjs.com/package/@chainofclaw/soul)
- [claw-mem2db related skill](https://clawhub.ai/ngplateform/claw-mem2db)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recovery commands, configuration snippets, status checks, and operator safety guidance.]

## Skill Version(s):

1.2.10 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
