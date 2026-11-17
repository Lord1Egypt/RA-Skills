## Description:

Scans public perpetual futures funding rates across Hyperliquid, Binance, and Bybit, ranks high-yield delta-neutral carry opportunities, detects cross-exchange spreads, and writes results to a local JSON file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mibayy](https://clawhub.ai/user/mibayy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this automaton to monitor public crypto funding-rate data and produce a local shortlist of potential delta-neutral carry and cross-exchange spread opportunities for further review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automaton makes recurring outbound requests to public exchange APIs every 15 minutes.

Mitigation: Run it only in environments where those network calls are expected and acceptable.

Risk: Results are written to a shared /tmp path, which may be inappropriate on multi-user systems.

Mitigation: Run under an unprivileged account and change the output path to a private application directory when needed.

Risk: Funding-rate opportunities can be misleading or stale and do not remove market, liquidity, exchange, or execution risk.

Mitigation: Treat the output as market-data screening for review, not as automated trading or financial advice.

## Reference(s):

- [Hyperliquid info API](https://api.hyperliquid.xyz/info)
- [Binance USD-M futures premium index API](https://fapi.binance.com/fapi/v1/premiumIndex)
- [Bybit market tickers API](https://api.bybit.com/v5/market/tickers)

## Skill Output:

**Output Type(s):** [Files, JSON, Text]

**Output Format:** [JSON file with log text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes /tmp/funding_opportunities.json; optional environment variables tune funding-rate threshold, spread threshold, and request timeout.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, clawhub.json, server release evidence, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
