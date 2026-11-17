## Description:

Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kinetosgr](https://clawhub.ai/user/kinetosgr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create and manage Billions Network decentralized identities, sign identity challenges, link an agent DID to a human owner, and verify DID ownership.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, store, import, and use signing keys for decentralized identity operations.

Mitigation: Install only when the agent is expected to manage a Billions DID, configure BILLIONS_NETWORK_MASTER_KMS_KEY before creating identities, and protect the local identity directory.

Risk: Challenge signing and human-agent linking can bind identity claims or prove DID ownership.

Mitigation: Require explicit user confirmation before any signing or human-agent linking action and stop if any identity script fails.

Risk: Supplying private keys through command-line arguments can expose sensitive identity material.

Mitigation: Avoid importing private keys through command-line arguments; prefer generated identities protected by the configured KMS key.

## Reference(s):

- [Verified Agent Identity on ClawHub](https://clawhub.ai/kinetosgr/skills/agent156)
- [Billions Network](https://billions.network/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON or text script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js. BILLIONS_NETWORK_MASTER_KMS_KEY is optional but recommended before identity creation.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
