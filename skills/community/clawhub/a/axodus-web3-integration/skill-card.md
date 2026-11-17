## Description:

Integrate apps with blockchain providers, wallets, and contract calls safely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzfshark](https://clawhub.ai/user/mzfshark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate frontend or backend applications with blockchain providers, wallets, and smart contract calls while validating chain, contract, ABI, signer, and error-handling behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect chain IDs, contract addresses, ABI files, or signer flows can cause failed calls or unintended blockchain transactions.

Mitigation: Verify chain IDs, contract addresses, ABI sources, and signer flows before applying generated code or commands.

Risk: Private keys or signer credentials could be exposed during Web3 setup.

Mitigation: Do not provide private keys in chat; use environment variables or a proper secrets manager.

Risk: Malformed trigger metadata may make automatic skill activation unreliable.

Mitigation: Replace malformed trigger metadata with narrow, explicit triggers before relying on automatic activation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mzfshark/skills/axodus-web3-integration)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with code paths, configuration details, and validation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wrapper module paths, environment variable requirements, and test or build commands.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
