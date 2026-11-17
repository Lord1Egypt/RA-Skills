## Description:

Coin research and crypto token analysis with CoinMarketCap (CMC) CLI for deep dives into price, market cap, volume, on-chain stats, historical OHLCV, trading pairs, news sentiment, and bull/bear assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coinmarketcap-official](https://clawhub.ai/user/coinmarketcap-official)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research a specific cryptocurrency and produce a structured, evidence-based Markdown report covering market data, fundamentals, price action, sentiment, and bull/bear assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a local CoinMarketCap CLI installation.

Mitigation: Install only a trusted CoinMarketCap CLI source before using the workflow.

Risk: The workflow requires a CMC_API_KEY for market-data lookups.

Mitigation: Provide a CMC API key only when that account is appropriate for the requested research session.

Risk: The generated cryptocurrency report may be mistaken for financial advice.

Mitigation: Treat the report as informational research output and apply independent due diligence before making financial decisions.

## Reference(s):

- [CoinMarketCap CLI](https://github.com/openCMC/CoinMarketCap-CLI)
- [ClawHub Skill Page](https://clawhub.ai/coinmarketcap-official/skills/coin-crypto-research-cmc-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Structured Markdown research report with tables, concise analysis sections, and bull, bear, and verdict sections.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the cmc CLI and CMC_API_KEY; generated reports are informational and not financial advice.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
