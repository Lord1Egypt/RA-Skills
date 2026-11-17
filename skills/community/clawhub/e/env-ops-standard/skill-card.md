## Description:

Safe .env key-first operations (CRUD) with secret-safe defaults.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pioneer-weirdo](https://clawhub.ai/user/pioneer-weirdo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect, add, update, remove, lint, and health-check .env entries while avoiding accidental disclosure of secret values.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill manages .env secrets, and documented command examples could expose real values if a user places secrets directly in command text or shell history.

Mitigation: Prefer stdin or a protected secret-entry mechanism for values, avoid echoing real secrets in chat or logs, and use value-in-argv only for exceptional cases.

Risk: Backups and audit logs created during env-file operations may contain sensitive operational details and can become an exposure point if stored loosely.

Mitigation: Keep backup and audit-log locations permission-restricted, apply retention settings, and review storage paths before using the skill with production secrets.

Risk: Deleting or force-changing protected keys can break authentication or configuration-dependent workflows.

Mitigation: Confirm destructive intent, use policy-controlled protected keys, run lint or doctor after writes, and prefer dry-run previews before risky changes.

## Reference(s):

- [ENV Key Naming & Comment Standard](references/env-key-standard.md)
- [Example envsafe Policy](references/policy.example.json)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Secret values are omitted by default; key listing and status output use non-secret text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
