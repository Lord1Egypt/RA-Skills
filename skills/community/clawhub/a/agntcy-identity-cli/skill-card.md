## Description:

AGNTCY Identity Issuer CLI and Node Backend for managing verifiable agent identities, metadata, and badges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jadiaconu](https://clawhub.ai/user/jadiaconu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install and run the AGNTCY identity issuer CLI and node backend for creating agent identities, issuing and publishing badges, and verifying verifiable credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install or run mutable upstream code.

Mitigation: Review and pin the upstream repository or Go module before installing or running commands.

Risk: The skill may handle high-value OAuth client secrets and signing-key vault material.

Mitigation: Use only test OAuth clients and test signing-key vaults in a restricted test environment until the code path and secret-handling behavior are verified.

## Reference(s):

- [AGNTCY Identity repository](https://github.com/agntcy/identity)
- [AGNTCY Identity CLI on ClawHub](https://clawhub.ai/jadiaconu/skills/agntcy-identity-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the identity CLI, issuer URL configuration, OAuth client values for IdP-backed flows, and a local vault path.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
