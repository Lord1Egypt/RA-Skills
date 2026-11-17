## Description:

Consolidates scattered OpenClaw credentials into a centralized ~/.openclaw/.env file with scanning, backup, permission validation, cleanup, and enforcement helpers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cxz9909](https://clawhub.ai/user/cxz9909)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to locate scattered credential files, migrate values into the OpenClaw root .env file, validate file permissions and git-ignore protection, and remove old credential files after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Centralizing credentials can concentrate impact if the generated .env file or its backups are exposed.

Mitigation: Inspect migrated values, keep permissions at 600, ensure .env is git-ignored, and secure or encrypt backups before relying on the consolidated store.

Risk: Cleanup modes can delete old credential files after migration.

Mitigation: Run scan and backup-only or dry-run modes first, verify backups, test applications against the new credential store, and avoid force or auto-confirm cleanup until migration is confirmed.

Risk: Shell sourcing of .env files can expose secrets through shell behavior or unsafe file contents.

Mitigation: Prefer controlled loaders, avoid sourcing the generated .env in an interactive shell, and review file contents before any shell-based loading.

Risk: Wallet seed phrases and private keys are difficult or impossible to recover if exposed.

Mitigation: Do not centralize irreplaceable wallet seed phrases or private keys unless that storage model is explicitly accepted and protected with stronger operational controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cxz9909/skills/cxz9909-credential-manager)
- [Credential security best practices](references/security.md)
- [Supported credential service patterns](references/supported-services.md)
- [Core centralized credential management principle](CORE-PRINCIPLE.md)
- [Credential consolidation rule](CONSOLIDATION-RULE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and Python helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update credential files, backups, .env.example, and .gitignore when the bundled scripts are run by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact documentation reports 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
