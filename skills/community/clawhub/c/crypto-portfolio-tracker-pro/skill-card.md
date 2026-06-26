## Description: <br>
Real-time cryptocurrency portfolio tracking and analysis for monitoring holdings, portfolio value, performance metrics, and price alerts across crypto sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dagangtj](https://clawhub.ai/user/dagangtj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to track cryptocurrency holdings, calculate portfolio value and short-term performance, configure alerts, and review portfolio allocation across exchanges and wallets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crypto exchange, wallet, and alert integrations can expose sensitive financial data or credentials if configured too broadly. <br>
Mitigation: Review integrations before use, prefer read-only exchange keys, never provide seed phrases or withdrawal-enabled credentials, and confirm what data is sent, stored, and retained. <br>
Risk: Portfolio values and price alerts rely on external market data that may be delayed, incomplete, or unavailable. <br>
Mitigation: Verify important balances and prices against authoritative exchange or wallet sources before making financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dagangtj/crypto-portfolio-tracker-pro) <br>
- [Configuration reference](references/config.json) <br>
- [CoinGecko API](https://api.coingecko.com/api/v3) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal text with shell command examples and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch live market data from third-party cryptocurrency APIs and may write local alert configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
