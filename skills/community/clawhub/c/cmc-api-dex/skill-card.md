## Description: <br>
API reference for CoinMarketCap DEX endpoints, including token lookup, pools, transactions, trending lists, and security analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bryan-cmc](https://clawhub.ai/user/bryan-cmc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to answer CoinMarketCap DEX API questions and draft REST calls for on-chain token data, pricing, liquidity pools, transactions, trending tokens, and token security checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated curl commands can send requests with a real CoinMarketCap API key. <br>
Mitigation: Review commands before execution, provide the key only for intended requests, and avoid pasting or logging secrets. <br>
Risk: The package metadata marks this skill as outdated. <br>
Mitigation: Prefer the newer onchain-data skill linked in the release changelog when current endpoint guidance is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bryan-cmc/cmc-api-dex) <br>
- [Latest onchain data skill](https://clawhub.ai/bryan-cmc/cmc-api-onchain-data) <br>
- [CoinMarketCap Pro login](https://pro.coinmarketcap.com/login) <br>
- [Skill overview](artifact/SKILL.md) <br>
- [Use cases](artifact/references/use-cases.md) <br>
- [Token endpoints](artifact/references/tokens.md) <br>
- [Pair endpoints](artifact/references/pairs.md) <br>
- [Platform endpoints](artifact/references/platforms.md) <br>
- [Discovery endpoints](artifact/references/discovery.md) <br>
- [Security endpoint](artifact/references/security.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with REST endpoint summaries and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a CoinMarketCap Pro API key for real API requests; the release is marked outdated and points users to a newer onchain-data skill.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
