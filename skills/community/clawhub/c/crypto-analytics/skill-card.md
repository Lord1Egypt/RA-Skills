## Description:

Multi-chain blockchain analytics for wallet balances, transaction history, and address validation. Supports 60+ EVM chains via Etherscan V2, plus Bitcoin and Solana. Use to check wallet balances, view transactions, get transaction details, validate addresses, or list supported chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solidgea](https://clawhub.ai/user/solidgea)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to inspect public blockchain wallet balances, transaction histories, token balances, gas prices, and address validity across supported EVM, Bitcoin, and Solana networks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read a workspace .env file, which may expose unrelated secrets to the skill process.

Mitigation: Provide only ETHERSCAN_API_KEY explicitly when needed and keep unrelated credentials out of the workspace .env file.

Risk: Queried wallet addresses and transaction hashes are sent to external blockchain API providers and may be cached locally for a short time.

Mitigation: Query only public blockchain data you are comfortable sending to Etherscan, Blockchair, or public Solana RPC endpoints, and clear the local cache when needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/solidgea/skills/crypto-analytics)
- [ClawHub Listing](https://clawhub.com/skills/crypto-analytics)
- [API Reference Index](references/api_index.md)
- [Supported Blockchain Networks](references/chains.md)
- [Etherscan API Key Setup](https://etherscan.io/apis)
- [Etherscan V2 API](https://api.etherscan.io/v2)
- [Blockchair API](https://blockchair.com/api)
- [Solana Mainnet RPC](https://api.mainnet-beta.solana.com)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON with optional human-readable text formatting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live API responses may be cached locally for 5 minutes; command limits vary by API provider and command.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
