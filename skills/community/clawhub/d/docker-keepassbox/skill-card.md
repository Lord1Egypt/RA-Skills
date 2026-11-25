## Description:

Manage KeePass vaults, entries and TOTP through a configured KeePassBox instance. Use when a user asks to manage an authorized KDBX vault.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Vault owners and operators use this skill to create or unlock KeePass vaults, manage entries and groups, generate passwords, and configure or retrieve TOTP for an authorized KeePassBox instance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bearer token can manage vaults and may reveal passwords or generate TOTP codes.

Mitigation: Connect only to the trusted instance over HTTPS, use restricted-scope tokens where possible, and keep tokens, passwords, recovery codes, and OTP seeds out of replies and logs.

Risk: Vault changes outside the user's authorization or based on a stale revision could affect stored credentials.

Mitigation: Limit changes to vaults the user is authorized to manage and fetch the current vault revision before security changes or rekeying.

## Reference(s):

- [Connect to KeePassBox](references/setup.md)
- [KeePassBox API access scopes](https://psyb0t.github.io/docker-keepassbox/api/#access)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance]

**Output Format:** [Text responses and KeePassBox API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can include sensitive vault data or current TOTP codes; keep passwords, recovery codes, and OTP seeds out of replies and logs.]

## Skill Version(s):

0.2.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
