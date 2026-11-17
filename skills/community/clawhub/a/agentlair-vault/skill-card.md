## Description:

Store and fetch credentials securely at runtime via AgentLair Vault REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hawkaa](https://clawhub.ai/user/hawkaa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to store, fetch, rotate, list, and revoke runtime credentials through AgentLair Vault instead of placing third-party API keys in local agent configuration or environment files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores high-impact API keys with a hosted credential custodian and evidence reports under-disclosed plaintext handling.

Mitigation: Install only when the user accepts AgentLair as custodian; store least-privileged, revocable credentials and avoid live financial or administrator tokens unless necessary.

Risk: Rotate and delete actions can change or remove credentials used by agents and downstream services.

Mitigation: Require explicit user confirmation before rotating, revoking, or deleting secrets, and use descriptive key names and metadata that do not contain secret values.

Risk: The optional AES-CBC shell example should not be treated as sufficient zero-knowledge storage guidance.

Mitigation: Use a reviewed client-side encryption library or security-reviewed encryption workflow when zero-knowledge storage is required, and keep local passphrases out of the vault.

## Reference(s):

- [AgentLair homepage](https://agentlair.dev)
- [AgentLair security documentation](https://agentlair.dev/security)
- [AgentLair trust model blog](https://agentlair.dev/blog)
- [agentlair-vault-crypto](https://github.com/piiiico/agentlair-vault-crypto)
- [ClawHub AgentLair Vault skill page](https://clawhub.ai/hawkaa/skills/agentlair-vault)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENTLAIR_API_KEY and curl.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
