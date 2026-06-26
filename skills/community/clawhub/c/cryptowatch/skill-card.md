## Description: <br>
CryptoWatch monitors cryptocurrency prices, market rankings, and local price alerts using public CoinGecko market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gztanht](https://clawhub.ai/user/gztanht) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to check cryptocurrency prices, compare 24-hour gainers and losers, and configure local threshold alerts. It is informational only and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool sends selected coin symbols and currency choices to CoinGecko when fetching market data. <br>
Mitigation: Use it only when sharing those query choices with CoinGecko is acceptable. <br>
Risk: Alert thresholds are stored locally, and sponsorship payment claims are not enforced by the reviewed code. <br>
Mitigation: Review local alert files before sharing the workspace and independently verify any sponsorship unlock before sending payment. <br>
Risk: Cryptocurrency market output can be mistaken for investment advice. <br>
Mitigation: Treat generated price, ranking, and alert output as informational market data, not a recommendation to trade. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gztanht/cryptowatch) <br>
- [CoinGecko API](https://www.coingecko.com/en/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public market data from CoinGecko and stores alert thresholds locally.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
