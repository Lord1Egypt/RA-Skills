## Description:

Manage wallet-backed on-chain agent identity with Devtopia ID for Base-chain registration, identity status checks, challenge proofs, wallet management, and verified agent interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[npmrunspirit](https://clawhub.ai/user/npmrunspirit)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to register and manage wallet-backed Devtopia identities on Base, generate challenge-response proofs, and coordinate verified agent interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private-key handling could expose wallet credentials if PEM keys are pasted into command lines or handled outside encrypted keystore workflows.

Mitigation: Prefer encrypted keystore-file workflows, avoid command-line PEM private keys, and review wallet import/export steps before using the skill for real identities.

Risk: Challenge-proof examples may produce insecure identity checks if verifiers do not enforce replay protections and request context.

Mitigation: Require fresh single-use challenges, expiration, audience and action binding, and clear token issuance before accepting proofs.

Risk: On-chain registration may be permanent and depends on external Devtopia CLI and Base-chain behavior.

Mitigation: Confirm the Devtopia CLI, chain target, and registration consequences before minting or publishing an identity.

## Reference(s):

- [Challenge-Response Proofs](references/challenge-proofs.md)
- [Devtopia Docs](https://devtopia.net/docs)
- [Base Chain Docs](https://docs.base.org)
- [ECDSA P-256](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm)
- [AES-256-GCM](https://en.wikipedia.org/wiki/Galois/Counter_Mode)
- [Challenge-Response Authentication](https://en.wikipedia.org/wiki/Challenge%E2%80%93response_authentication)
- [ClawHub Skill Page](https://clawhub.ai/npmrunspirit/skills/devtopia-identity)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline bash, JSON, JavaScript, and Solidity code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet identity workflows, challenge-proof examples, and security handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
