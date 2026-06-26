## Description: <br>
Scans public perpetual futures funding rates across Hyperliquid, Binance, and Bybit to identify delta-neutral carry trade opportunities and save ranked results as JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mibayy](https://clawhub.ai/user/Mibayy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and trading analysts can use this skill to monitor public funding-rate data and review potential delta-neutral carry opportunities before making any trading decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs as a scheduled background task that polls public exchange APIs every 15 minutes and writes to /tmp/funding_opportunities.json. <br>
Mitigation: Install it only in environments where this polling cadence and shared temporary output path are acceptable. <br>
Risk: Funding-rate opportunities can change quickly and may not account for fees, liquidity, liquidation, exchange risk, or execution constraints. <br>
Mitigation: Independently evaluate trading risks and current market conditions before acting on any reported opportunity. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mibayy/crypto-funding-harvester) <br>
- [Hyperliquid info endpoint](https://api.hyperliquid.xyz/info) <br>
- [Binance futures premium index endpoint](https://fapi.binance.com/fapi/v1/premiumIndex) <br>
- [Bybit market tickers endpoint](https://api.bybit.com/v5/market/tickers) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Analysis] <br>
**Output Format:** [JSON file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes /tmp/funding_opportunities.json on each scheduled run with ranked opportunities, cross-exchange spreads, and summary data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
