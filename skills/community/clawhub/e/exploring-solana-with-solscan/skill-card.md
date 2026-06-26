## Description: <br>
Use this skill to query Solana blockchain data via the Solscan Pro API for wallets, tokens, NFTs, transactions, DeFi activity, account metadata, blocks, API usage, and token search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tiennv3](https://clawhub.ai/user/tiennv3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to retrieve structured Solana on-chain data from Solscan Pro for wallet review, token and NFT research, transaction inspection, DeFi activity analysis, and block or program exploration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses, transaction signatures, token or NFT identifiers, and investigation patterns queried through this skill are disclosed to the third-party Solscan Pro API. <br>
Mitigation: Use a dedicated Solscan Pro API key and avoid submitting sensitive investigative linkages unless sharing them with Solscan Pro is acceptable. <br>
Risk: The skill depends on an external API key and Solscan Pro service availability, so requests can fail because of missing credentials, rate limits, or service errors. <br>
Mitigation: Configure SOLSCAN_API_KEY before use and handle API errors or rate limits before relying on returned data in downstream decisions. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/tiennv3/exploring-solana-with-solscan) <br>
- [Solscan Pro API Docs](https://pro-api.solscan.io/pro-api-docs/v2.0) <br>
- [Solscan Pro API FAQs](https://pro-api.solscan.io/pro-api-docs/v2.0/faq.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI examples and JSON or CSV API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Solscan Pro API key configured as SOLSCAN_API_KEY; queried wallet addresses, transaction signatures, token identifiers, NFT identifiers, and investigation patterns are sent to Solscan Pro.] <br>

## Skill Version(s): <br>
1.0.8 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
