## Description:

Credential Manager helps OpenClaw users scan scattered credential files, consolidate secrets into a protected ~/.openclaw/.env file, create backups, validate permissions and format, and clean up old credential files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[callmedas69](https://clawhub.ai/user/callmedas69)

### License/Terms of Use:


## Use Case:

Developers and operators of OpenClaw deployments use this skill to migrate scattered API keys and secrets into a single local .env store, validate basic protections, and enforce a consistent credential-loading standard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly reads and reorganizes sensitive credentials across the user account.

Mitigation: Install only when credential migration is intended, review scan results before consolidation, and prefer interactive confirmation over --yes for sensitive migrations.

Risk: Backups and the consolidated .env can contain high-value secrets, including wallet or seed material.

Mitigation: Keep ~/.openclaw/.env restricted to mode 600, protect or encrypt backups, and avoid storing irreplaceable private keys or seed phrases unless the risk is fully accepted.

Risk: Cleanup can delete original credential files after migration.

Mitigation: Verify applications work with the new credential store and confirm backups before running cleanup with deletion flags.

## Reference(s):

- [Credential Manager on ClawHub](https://clawhub.ai/callmedas69/skills/credential-manager)
- [Core Principle](CORE-PRINCIPLE.md)
- [Credential Consolidation Rule](CONSOLIDATION-RULE.md)
- [Security Best Practices](references/security.md)
- [Supported Services](references/supported-services.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands and generated local configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May scan credential locations and write, chmod, back up, or delete local credential files when scripts are run.]

## Skill Version(s):

1.3.0 (source: server release metadata and artifact CHANGELOG, released 2026-02-07)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
