## Description:

Scan crypto funding rates and find arbitrage opportunities. No API key needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dagangtj](https://clawhub.ai/user/dagangtj)

### License/Terms of Use:

MIT

## Use Case:

Developers and crypto market analysts use this skill to run Binance Futures funding-rate scans, monitor selected coins, and inspect recent funding-rate history. Its output should be treated as market-data screening support, not investment advice or validated arbitrage analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Funding-rate screens and annualized return estimates may be mistaken for validated arbitrage analysis or investment advice.

Mitigation: Treat results as market-data screening only, verify risks independently, and do not trade solely from the skill output.

Risk: Funding rates can change quickly, and high leverage can amplify losses.

Mitigation: Confirm current market conditions before acting and use appropriate risk controls such as position sizing and stop-losses.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dagangtj/skills/funding-rate-scanner)
- [Binance Futures Premium Index API](https://fapi.binance.com/fapi/v1/premiumIndex)
- [Binance Futures Funding Rate API](https://fapi.binance.com/fapi/v1/fundingRate)
- [Binance Futures 24hr Ticker API](https://fapi.binance.com/fapi/v1/ticker/24hr)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and CLI output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches public Binance Futures market data without API keys; output is informational and requires independent verification before trading.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
