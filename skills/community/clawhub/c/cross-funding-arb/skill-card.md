## Description: <br>
Runs a cross-exchange funding-rate arbitrage strategy that opens delta-neutral perpetual futures positions across Hyperliquid and Binance, with opportunity scanning, stability checks, atomic execution, health checks, and auto-switching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[synththoughts](https://clawhub.ai/user/synththoughts) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and operators use this skill to configure and run an automated Hyperliquid and Binance funding-rate arbitrage bot that scans opportunities, validates risk controls, executes paired futures trades, monitors position health, and reports status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trade live crypto futures accounts unattended and uses sensitive exchange credentials. <br>
Mitigation: Use testnet first, create restricted trading-only API keys with withdrawals disabled, set explicit small budgets instead of relying on full balances, and protect the .env file before enabling cron. <br>
Risk: Financial notifications may reuse local Discord or Telegram credentials. <br>
Mitigation: Review or disable Discord and Telegram credential fallback behavior before enabling scheduled execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/synththoughts/cross-funding-arb) <br>
- [Funding arbitrage algorithm](references/funding-arb-algorithm.md) <br>
- [Runtime configuration](references/config.json) <br>
- [Python trading script](references/cross_funding.py) <br>
- [Python requirements](references/requirements.txt) <br>
- [VarFunding API endpoint](https://varfunding.xyz/api/funding?exchanges=hyperliquid,binance) <br>
- [Binance signed endpoint security](https://developers.binance.com/docs/binance-spot-api-docs/rest-api/public-api-definitions#signed-trade-and-user_data-endpoint-security) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands, configuration guidance, and text status or report output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 plus Hyperliquid and Binance futures credentials; intended commands include tick, status, and report.] <br>

## Skill Version(s): <br>
2.8.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
