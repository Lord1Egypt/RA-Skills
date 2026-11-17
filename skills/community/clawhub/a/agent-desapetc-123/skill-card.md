## Description:

Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[desapetc](https://clawhub.ai/user/desapetc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create and manage decentralized agent identities, link an agent DID to a human owner, sign authentication challenges, and verify DID ownership proofs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles long-lived private keys and authentication proofs with weak defaults.

Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating identities and restrict permissions on $HOME/.openclaw/billions.

Risk: Importing a valuable or funded Ethereum private key through --key could expose sensitive key material.

Mitigation: Use a dedicated, unfunded identity key for this skill instead of importing a valuable wallet key.

Risk: The verification flow is not suitable for high-assurance authentication until challenge replay and dependency issues are fixed.

Mitigation: Use this flow only where its assurance level is acceptable and perform additional review before relying on it for identity-sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/desapetc/skills/agent-desapetc-123)
- [Billions Network](https://billions.network/)
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and script outputs as text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and can read or write local identity data under $HOME/.openclaw/billions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
