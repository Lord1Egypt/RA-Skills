## Description:

Verify a submitted same-chain ERC-20 payment against its intended token, payer, recipient and raw amount.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and payment operations staff use it to compare a submitted same-chain ERC-20 receipt with an independently supplied payment instruction, then report matching transfer details and block finality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial, and a referenced script was only partly inspected; the skill also has a file-reading capability.

Mitigation: Before installing, review the referenced script and consider whether the file-reading capability is needed and acceptable.

## Reference(s):

- [Collect a receipt](references/reads.md)
- [ERC-20](https://eips.ethereum.org/EIPS/eip-20)
- [Ethereum Execution APIs](https://github.com/ethereum/execution-apis)
- [Base transaction finality](https://docs.base.org/base-chain/network-information/transaction-finality)
- [ClawHub release page](https://clawhub.ai/galleonlabs/skills/galleon-erc20-payment-receipt)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, JSON]

**Output Format:** [Markdown summary or classified JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports transaction and transfer evidence, exact amounts and finality; unresolved or conflicting observations remain explicitly unresolved.]

## Skill Version(s):

0.3.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
