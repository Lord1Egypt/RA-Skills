## Description:

Agent-first service to register and manage Human Bitcoin Addresses (BIP-353) on clank.money with L402 bitcoin payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matbalez](https://clawhub.ai/user/matbalez)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to register a clank.money Human Bitcoin Address, pay the L402 Lightning invoice, securely save the returned management token, and update the registered Bitcoin payment URI later.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The management token controls future Bitcoin address updates and may be exposed by copy-paste shell workflows, shared machines, logs, shell tracing, or predictable temporary files.

Mitigation: Treat the management token like a password or API key, avoid shared machines and shell tracing, avoid logging token values, and prefer a private temp directory or secret store for real use.

Risk: Losing the management token prevents authenticated updates to the registered address.

Mitigation: Save the token immediately after successful registration in a secure location with restrictive permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/matbalez/skills/get-hba)
- [clank.money registrations API](https://clank.money/api/v1/registrations)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API request examples and local management-token storage guidance.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
