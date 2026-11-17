## Description:

Creates cryptographic proof-of-existence receipts for selected digital artifacts by submitting their SHA-256 hashes to AOTrust and supports receipt verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitserge-crypto](https://clawhub.ai/user/gitserge-crypto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create and verify a timestamped proof that a specific artifact hash existed, with optional paid evidence bundles or signed time attestations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The submitted artifact hash can become a permanent public link to a receipt, signatures, or payment activity.

Mitigation: Submit only when explicitly requested; explain that the artifact itself is not uploaded but its hash is public, and retain the receipt.

Risk: Paid notarization and optional paid products involve irreversible USDC payments.

Mitigation: Require user approval for each payment, review the amount, network, and recipient in the wallet, and keep private keys outside the agent.

## Reference(s):

- [AOTrust PDR Verification API](https://api.aotrust.link/v1/pdr/verify)
- [AOTrust Transparency Documentation](https://docs.aotrust.link/transparency.html)
- [PDR Specification](https://github.com/GitSerge-crypto/aotrust-skills/blob/main/pdr-spec.md)
- [Offline PDR Parser](https://github.com/GitSerge-crypto/aotrust-skills/blob/main/pdr_parser.py)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON proof receipts and verification results with concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Receipts identify the artifact by its hash; paid requests require user approval and payments are irreversible.]

## Skill Version(s):

3.10.1 (source: server-resolved release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
