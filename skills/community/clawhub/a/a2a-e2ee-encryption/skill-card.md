## Description:

Implements end-to-end encryption utilities for A2A agent communication, including key generation, message encryption and decryption, signing, HMAC helpers, and key import/export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add encryption, signing, message integrity checks, and key management helpers to A2A communication workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security-sensitive cryptographic behavior may have correctness gaps.

Mitigation: Review, fix, and test the crypto edge cases before using the skill for high-value agent commands, financial actions, or irreversible workflows.

Risk: Private keys and shared secrets could be mishandled by downstream users.

Mitigation: Store private keys and shared secrets in a secure secret manager or vault and verify public key fingerprints before exchanging sensitive messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/a2a-e2ee-encryption)

## Skill Output:

**Output Type(s):** [code, configuration, guidance]

**Output Format:** [JavaScript module exports and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces cryptographic helper functions for RSA, AES-GCM, signatures, HMAC, shared secrets, and secure message envelopes.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
