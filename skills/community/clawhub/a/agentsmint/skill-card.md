## Description:

Create and manage NFT collections on Base blockchain. Use when an agent wants to mint NFTs, launch a collection, list items for sale, or check their NFT portfolio. Handles contract deployment, lazy minting, and edition tracking. Platform pays deployment gas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kit-the-fox](https://clawhub.ai/user/kit-the-fox)

### License/Terms of Use:


## Use Case:

External agents and developers use this skill to browse NFT collections, create and deploy Base collections, list NFTs for sale, and prepare or confirm minting transactions through the AgentsMint API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides agents through real NFT purchases, contract deployment, listings, and ownership transfer.

Mitigation: Require manual approval for every buy, mint, listing, deployment, and ownership transfer before any on-chain action.

Risk: Incorrect transaction details can cause unintended wallet, contract, price, gas, recipient, or chain actions.

Mitigation: Confirm the wallet, Base chain, contract address, function call, recipient, price, gas cost, and transaction hash before execution.

## Reference(s):

- [AgentsMint API Base URL](https://www.agentsmint.com/api/v1)
- [AgentsMint Skill Page](https://clawhub.ai/kit-the-fox/skills/agentsmint)
- [BitBuddies Example Collection](https://agentsmint.com/bitbuddies)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with curl examples and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents through API calls and on-chain transaction details for Base NFT collection, listing, purchase, and deployment flows.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
