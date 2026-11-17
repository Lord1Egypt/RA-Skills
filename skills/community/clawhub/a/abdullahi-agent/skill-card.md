## Description:

Billions decentralized identity for agents that links agents to human identities using Billions ERC-8004 and Attestation Registries and supports authentication proof generation and verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abdallah349193](https://clawhub.ai/user/abdallah349193)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create and manage decentralized identities, link an agent DID to a human owner, sign identity challenges, and verify signed proofs of DID control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles long-lived identity private keys and signed challenges that can prove control of an identity.

Mitigation: Review before installing, treat verification outputs as sensitive, and restrict access to $HOME/.openclaw/billions.

Risk: Private keys may be stored without at-rest encryption if BILLIONS_NETWORK_MASTER_KMS_KEY is not set.

Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating or importing identities and store the master key securely.

Risk: Passing real private keys on the command line can expose them through shell history or process inspection.

Mitigation: Avoid passing real private keys on the command line; prefer generated identities or a controlled secret-handling path.

Risk: The skill depends on network endpoints and npm dependencies for identity, resolver, and attestation flows.

Mitigation: Review configured endpoints and update or audit dependencies before using the skill in a high-trust environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abdallah349193/skills/abdullahi-agent)
- [Billions Network](https://billions.network/)
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment)
- [DID resolver endpoint](https://resolver.privado.id/1.0/identifiers/)
- [Billions wallet](https://wallet.billions.network)
- [Billions identity dashboard](https://identity-dashboard.billions.network)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON output from Node.js helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts may read and write identity, key, challenge, credential, and profile files under $HOME/.openclaw/billions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
