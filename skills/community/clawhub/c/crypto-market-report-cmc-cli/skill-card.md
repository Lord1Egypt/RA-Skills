## Description:

Daily coin market report and crypto snapshot via CoinMarketCap CLI covering BTC and ETH prices, top gainers and losers, trending tokens, and current crypto news.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coinmarketcap-official](https://clawhub.ai/user/coinmarketcap-official)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operators use this skill to generate concise crypto market briefs from the configured CoinMarketCap CLI. It is suited for daily market snapshots, crypto morning briefs, and requests about current BTC, ETH, momentum, and news flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a CoinMarketCap API key through the configured cmc CLI, so report generation may make external API calls.

Mitigation: Install only where the cmc CLI and CMC_API_KEY are approved, and review ambiguous market-report requests before execution.

Risk: Malformed metadata may affect reliable installation or dependency discovery.

Mitigation: Clean package metadata and verify the cmc binary and CMC_API_KEY prerequisites before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coinmarketcap-official/skills/crypto-market-report-cmc-cli)
- [CoinMarketCap CLI installation reference](https://github.com/openCMC/CoinMarketCap-CLI)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown market report with ordered sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the cmc CLI and CMC_API_KEY; report content depends on current CoinMarketCap data available at execution time.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
