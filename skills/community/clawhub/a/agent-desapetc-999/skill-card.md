## Description:

Billions decentralized identity for agents: create and manage DIDs, link agents to human identities through Billions ERC-8004 and Attestation Registries, and verify authentication proofs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[desapetc](https://clawhub.ai/user/desapetc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create agent DIDs, sign identity challenges, link an agent identity to a human owner, and verify DID ownership proofs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-lived agent signing keys may be stored in plaintext when BILLIONS_NETWORK_MASTER_KMS_KEY is not set.

Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating identities and restrict filesystem access to $HOME/.openclaw/billions.

Risk: Authentication challenges and signed tokens may be reusable secrets.

Mitigation: Use fresh challenges, avoid sharing generated tokens beyond the intended verifier, and treat tokens as sensitive until challenge handling is fixed.

Risk: Passing wallet private keys on the command line can expose them through shell history or process inspection.

Mitigation: Prefer generated identities or secure secret handling, and avoid command-line private key arguments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/desapetc/skills/agent-desapetc-999)
- [desapetc publisher profile](https://clawhub.ai/user/desapetc)
- [Billions Network](https://billions.network/)
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON or string command outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local DID, key, credential, and challenge files under $HOME/.openclaw/billions.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
