## Description: <br>
Multi-chain blockchain analytics for wallet balances, transaction history, and address validation across EVM chains, Bitcoin, and Solana. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solidgea](https://clawhub.ai/user/solidgea) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation authors use this skill to inspect public blockchain wallets and transactions, validate addresses, check gas prices, and retrieve token balances for supported chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses and transaction hashes are sent to Etherscan, Blockchair, or public Solana RPC providers during lookups. <br>
Mitigation: Use the skill only for identifiers you are comfortable sharing with those public API providers. <br>
Risk: Short-lived local cache files may contain queried addresses, transaction hashes, and returned public blockchain data. <br>
Mitigation: Rely on the five-minute cache expiry for routine use and manually delete the local cache when queries should not remain on disk. <br>
Risk: A workspace .env file may expose an Etherscan API key to other workspace processes or collaborators. <br>
Mitigation: Prefer a narrow ETHERSCAN_API_KEY environment variable and avoid placing broad secrets in shared workspace .env files. <br>


## Reference(s): <br>
- [API Reference Index](references/api_index.md) <br>
- [Supported Blockchain Networks](references/chains.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/solidgea/crypto-analytics) <br>
- [ClawHub Listing](https://clawhub.com/skills/crypto-analytics) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text, guidance] <br>
**Output Format:** [JSON with optional human-readable text formatting] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet balances, transaction history, transaction details, gas prices, token balances, address validation results, and supported-chain lists.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
