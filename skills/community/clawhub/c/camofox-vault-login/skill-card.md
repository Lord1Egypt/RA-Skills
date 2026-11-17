## Description:

Fill observed website login fields from an explicitly configured Bitwarden vault through a supported local Camofox runtime, without exposing credentials to the agent. Use for vault discovery, dry-run validation, password or fresh TOTP handoff; never universal automated authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aounakram](https://clawhub.ai/user/aounakram)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to find Bitwarden entries authorized for an observed HTTPS origin, validate target fields with a dry run, and hand off a password or fresh TOTP through a supported Camofox runtime. It does not submit forms or establish that a login succeeded.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vault data and filled credentials are sensitive, and the destination website receives credentials entered into its fields.

Mitigation: Use trusted, explicitly configured Bitwarden and Camofox components with the intended vault identity; review browser tracing and logging, and confirm the exact HTTPS origin and fields before filling.

Risk: An uncertain timeout or partial fill may lead to repeated credential entry.

Mitigation: Review a dry run first, never automatically retry uncertain fills, and verify the result using nonsecret indicators before any separately authorized submission.

## Reference(s):

- [Setup guide](references/setup.md)
- [Security contract](references/security.md)
- [Camofox Vault Login release](https://clawhub.ai/aounakram/skills/camofox-vault-login)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON status results and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper results omit credential values; filling does not submit forms.]

## Skill Version(s):

0.1.0 (source: release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
