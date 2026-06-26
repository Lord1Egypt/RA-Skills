## Description: <br>
BTC and ETH market monitor with public API data, six bottom-fishing signals, and optional Discord delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Liammme](https://clawhub.ai/user/Liammme) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and market-monitoring users can run this skill to generate scheduled or on-demand BTC/ETH oversold-signal summaries from public market APIs. It is suited for lightweight informational reporting and optional Discord delivery, not trade execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market summaries and coarse recommendations may be mistaken for trading advice. <br>
Mitigation: Treat the report as informational only, review the underlying signals, and note that the artifact does not place trades. <br>
Risk: Discord delivery can post generated reports to an unintended channel if credentials or channel settings are misconfigured. <br>
Mitigation: Enable Discord only for the intended channel and use a least-privilege bot token stored in the configured environment variable. <br>
Risk: Recurring cron scheduling can run background monitoring more often or longer than intended. <br>
Mitigation: Review config.json schedule before running setup_cron.sh and remove the marked crontab entry when recurring monitoring is no longer wanted. <br>
Risk: Public market APIs may fail, rate-limit, or return incomplete data. <br>
Mitigation: Monitor runtime errors, reduce scheduler frequency when needed, and treat missing indicators as a data availability issue rather than a signal. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Liammme/btc-monitor-talentversex) <br>
- [Skill runtime documentation](docs/README.md) <br>
- [Troubleshooting guide](docs/TROUBLESHOOTING.md) <br>
- [Binance Klines API](https://api.binance.com/api/v3/klines) <br>
- [Bybit Kline API](https://api.bybit.com/v5/market/kline) <br>
- [CoinGecko API](https://api.coingecko.com/api/v3/coins) <br>
- [Alternative.me Fear & Greed API](https://api.alternative.me/fng/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain-text market report with optional Discord messages and shell setup commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are informational, include heuristic signal counts and recommendations, and do not place trades.] <br>

## Skill Version(s): <br>
4.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
