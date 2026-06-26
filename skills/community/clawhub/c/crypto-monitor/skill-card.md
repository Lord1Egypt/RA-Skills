## Description: <br>
Crypto Monitor helps agents monitor cryptocurrency prices, on-chain activity, whale transactions, trending tokens, and airdrop opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawto](https://clawhub.ai/user/clawto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and crypto-focused agents use this skill to fetch market prices, trending tokens, whale activity, and airdrop leads from public crypto APIs. It supports market monitoring and research workflows, not custody of funds or execution of trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes external public crypto API requests, so responses can be unavailable, delayed, rate limited, or inaccurate. <br>
Mitigation: Confirm time-sensitive market or on-chain information with authoritative sources before acting on it. <br>
Risk: The skill can attempt to install jq automatically if it is missing. <br>
Mitigation: Review or remove the automatic jq installation behavior before running in locked-down or production environments. <br>
Risk: Crypto workflows may invite requests for seed phrases, private keys, wallet credentials, or exchange credentials. <br>
Mitigation: Do not provide wallet seed phrases, private keys, or exchange credentials to this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawto/crypto-monitor) <br>
- [CoinGecko API](https://api.coingecko.com/api/v3) <br>
- [DeFiLlama airdrops API](https://api.llama.fi/airdrops) <br>
- [Whale Alert API](https://api.whale-alert.io/v1/transactions) <br>
- [Etherscan API](https://api.etherscan.io/api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, CSV, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and script outputs in text, JSON, or CSV.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include live market data from public crypto APIs and may depend on third-party rate limits or availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
