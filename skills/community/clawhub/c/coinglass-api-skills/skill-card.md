## Description: <br>
CoinGlass API skill. Routes to the appropriate sub-skill based on user intent. Covers futures, ETF, options, spots, on-chain, indicators, account, and other market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coinglass-official](https://clawhub.ai/user/coinglass-official) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to route CoinGlass market-data questions to the relevant API documentation and produce user-directed CoinGlass API requests for crypto futures, ETFs, options, spot markets, on-chain data, indicators, account details, news, and financial calendar data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CoinGlass API keys may be exposed through prompts, logs, shared transcripts, or command history. <br>
Mitigation: Use environment variables or a secret store for CG-API-KEY, redact secrets before sharing outputs, and avoid placing raw keys directly in prompts. <br>
Risk: Wallet and address lookup requests can reveal sensitive or user-specific blockchain activity. <br>
Mitigation: Run wallet or address lookups only for legitimate, user-approved purposes and avoid sharing returned data beyond the intended audience. <br>
Risk: Subscription tiers, rate limits, and historical data availability can affect request success and completeness. <br>
Mitigation: Check response headers and plan-specific documentation before relying on large or frequent CoinGlass API queries. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/coinglass-official/coinglass-api-skills) <br>
- [CoinGlass API Skills Homepage](https://github.com/coinglass-official/coinglass-api-skills) <br>
- [CoinGlass API Error Codes](account/references/errors-codes.md) <br>
- [CoinGlass API Plans, Intervals, and History Length](account/references/plans-interval-history-length.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Text] <br>
**Output Format:** [Markdown guidance with inline curl commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and a user-provided CoinGlass API key for authenticated requests.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
