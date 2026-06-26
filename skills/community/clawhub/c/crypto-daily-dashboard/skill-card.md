## Description: <br>
Crypto Daily Dashboard is a terminal dashboard that shows Binance portfolio balances, BTC/ETH/SOL prices, Fear & Greed sentiment, funding rates, and optional economic tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dagangtj](https://clawhub.ai/user/dagangtj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to run a Node.js terminal dashboard for monitoring cryptocurrency portfolio balances, market prices, sentiment, funding rates, and optional local economic status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional ECONOMIC_TRACKER_PATH can run a shell command from an environment variable. <br>
Mitigation: Set ECONOMIC_TRACKER_PATH only to a fully trusted local script path; prefer a future implementation that uses validated execFile or spawn arguments instead of a shell string. <br>
Risk: The dashboard can access Binance account data when API credentials are configured. <br>
Mitigation: Use Binance keys with read-only permissions, no withdrawal or trading rights, and IP restrictions where possible. <br>
Risk: The dashboard is a networked finance tool that calls third-party market data services. <br>
Mitigation: Review configured data sources and avoid treating dashboard output as financial advice or an authority for trading decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dagangtj/crypto-daily-dashboard) <br>
- [Publisher profile](https://clawhub.ai/user/dagangtj) <br>
- [Binance API endpoint](https://api.binance.com) <br>
- [Binance Futures API endpoint](https://fapi.binance.com) <br>
- [CoinGecko API endpoint](https://api.coingecko.com) <br>
- [Alternative.me Fear & Greed API endpoint](https://api.alternative.me) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Terminal text dashboard] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js; optionally uses Binance API credentials and ECONOMIC_TRACKER_PATH environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
