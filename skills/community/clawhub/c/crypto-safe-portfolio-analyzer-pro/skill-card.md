## Description: <br>
Tracks cryptocurrency portfolios, calculates P&L with custom cost basis, fetches live prices from CoinGecko, and generates text or JSON reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iamcooper2026](https://clawhub.ai/user/iamcooper2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and crypto portfolio operators use this skill to analyze holdings, monitor allocation and P&L, and generate reports for manual review or automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes under-disclosed trading-signal and aggressive strategy behavior. <br>
Mitigation: Review the trading-signal script and configuration before installation, and disable or avoid automation that you do not intend to use. <br>
Risk: Holdings, cost basis, wallet addresses, generated reports, and Discord outputs can expose sensitive financial information. <br>
Mitigation: Keep portfolio files and generated reports private, limit where Discord or automation outputs are posted, and avoid sharing wallet details unnecessarily. <br>
Risk: Market-data calls send watchlist data to third-party services. <br>
Mitigation: Run the skill only when you accept the third-party API calls needed for live pricing, market overview, sentiment, and scanner outputs. <br>


## Reference(s): <br>
- [Usage Examples](references/usage-examples.md) <br>
- [Example Configuration](references/config-example.json) <br>
- [CoinGecko Simple Price API](https://api.coingecko.com/api/v3/simple/price) <br>
- [CoinGecko Markets API](https://api.coingecko.com/api/v3/coins/markets) <br>
- [Alternative.me Fear and Greed API](https://api.alternative.me/fng/) <br>
- [Coinbase Spot Price API](https://api.coinbase.com/v2/prices/BTC-USD/spot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Text or Markdown reports with optional JSON output and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public market-data APIs and local JSON holdings or configuration files.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
