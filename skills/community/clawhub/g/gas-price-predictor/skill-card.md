## Description:

Predict optimal gas prices for Base L2 transactions using historical block analysis and moving-average trends. Use when an agent needs to minimize gas costs, time transactions efficiently, or automate gas price selection for DeFi operations on Base L2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manteclaw](https://clawhub.ai/user/manteclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DeFi operators use this skill to review recent Base L2 gas fees and get advisory gas-price and transaction-timing recommendations before submitting transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound HTTPS JSON-RPC requests to the configured Base endpoint; a keyed provider may include a credential in the endpoint URL.

Mitigation: Use an RPC provider you trust, keep any keyed endpoint private, and avoid sharing it in logs or command history.

Risk: Gas prices and estimated costs are advisory and may not reflect current network conditions or the cost of a particular transaction.

Mitigation: Check current fees and transaction details before choosing a max fee or deciding when to submit.

Risk: The security scan had partial coverage, so its benign verdict does not cover every artifact path.

Mitigation: Review the skill files and configured RPC endpoint before installing or running the skill.

## Reference(s):

- [Base gas market model](artifact/references/base-gas-model.md)
- [Base documentation](https://docs.base.org)
- [EIP-1559 specification](https://eips.ethereum.org/EIPS/eip-1559)
- [ClawHub skill page](https://clawhub.ai/manteclaw/skills/gas-price-predictor)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, JSON, Text]

**Output Format:** [Structured JSON or human-readable text with gas price estimates, congestion status, and timing recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory estimates based on up to 200 recent blocks; monitor mode prints threshold alerts.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
