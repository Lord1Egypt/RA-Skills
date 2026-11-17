## Description:

Guides coding agents to handle local API keys, environment variables, passwords, SSH access, remote servers, and authentication without exposing secret values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sirsws](https://clawhub.ai/user/sirsws)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent users use this skill to constrain how agents read local credentials, load task-specific environment variables, and connect over SSH. It is intended to reduce accidental credential exposure in agent-assisted coding workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext credentials in ~/.localcfg/base.env can be exposed through local file access, backups, or repository mistakes.

Mitigation: Use least-privilege tokens, restrict file permissions, and keep the credential file out of backups and repositories.

Risk: The credential-bridge pattern can copy secrets into another .env file.

Mitigation: Use it only after approving the destination and confirming that the target .env is private, temporary, and gitignored.

Risk: A referenced remote PowerShell installer one-liner may execute unverified remote code.

Mitigation: Do not run the installer one-liner without independent verification.

## Reference(s):

- [Coding Agent Landscape](artifact/references/coding-agent-landscape.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces operating constraints and setup patterns for credential and SSH handling; it should not produce or display secret values.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
