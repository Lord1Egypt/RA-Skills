## Description: <br>
Crypto Market helps agents fetch cryptocurrency market data and monitor price or volatility alerts across CCXT-supported exchanges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manifoldor](https://clawhub.ai/user/manifoldor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to check ticker, OHLCV, and order book data, compare exchanges, and manage local price alerts for crypto pairs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented default exchange differs from the script default, which can send market-data requests to an unintended exchange. <br>
Mitigation: Specify --exchange when exchange choice matters and verify the selected venue before relying on the data. <br>
Risk: Advanced CCXT examples mention API keys, which could expose credentials if adapted carelessly. <br>
Mitigation: Do not add exchange API keys for simple price monitoring; keep any credentials outside the skill files and never commit them. <br>
Risk: Local alert rules persist in ~/.config/crypto/alerts.json after use. <br>
Mitigation: Review or delete the alerts file when monitoring is no longer wanted. <br>


## Reference(s): <br>
- [CCXT Documentation](https://docs.ccxt.com/) <br>
- [CCXT GitHub](https://github.com/ccxt/ccxt) <br>
- [Supported Exchanges List](references/exchanges.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CCXT exchange requests and stores alert rules in ~/.config/crypto/alerts.json.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
