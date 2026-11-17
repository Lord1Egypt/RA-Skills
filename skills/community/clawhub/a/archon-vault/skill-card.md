## Description:

Encrypted distributed storage using Archon DID vaults. Manage vaults, backup and restore workspace/config/memory with multi-party access control. Use for creating/managing DID vaults, backing up files, restoring from vault, disaster recovery, or managing vault contents and membership.

This skill is ready for commercial/non-commercial use.

## Publisher:

[macterra](https://clawhub.ai/user/macterra)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to manage Archon DID vaults, back up workspace and configuration data, restore backups, verify backup integrity, and manage multi-party vault access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles wallet recovery secrets and broad workspace/configuration backups.

Mitigation: Review and harden the scripts before real use, avoid passing mnemonics on the command line, and run only in an account or environment scoped to the exact vault and files intended for protection.

Risk: Backup exclusions, temporary files, and restore extraction can expose or overwrite sensitive data if used carelessly.

Mitigation: Use private temporary directories with cleanup, fail closed on backup exclusions, validate ZIP contents before extraction, and review restore targets before moving recovered files into active locations.

Risk: The scripts invoke @didcid/keymaster through npx at runtime.

Mitigation: Pin or vendor @didcid/keymaster before using the skill with production identities or backups.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/macterra/skills/archon-vault)
- [Publisher Profile](https://clawhub.ai/user/macterra)
- [Archon Technology](https://archon.technology)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands depend on Archon identity environment variables and local backup/vault state.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
