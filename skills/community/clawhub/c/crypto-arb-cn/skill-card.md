## Description: <br>
Crypto Arbitrage CN monitors Binance, OKX, Gate.io, and Huobi prices for cryptocurrency arbitrage opportunities, calculates estimated profit, and can send optional Telegram alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guohongbin-git](https://clawhub.ai/user/guohongbin-git) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and crypto traders use this skill to run one-time or continuous monitoring of public exchange prices and review estimated cross-exchange arbitrage opportunities before making manual trading decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Displayed arbitrage opportunities may disappear quickly or differ from executable prices because crypto markets are volatile. <br>
Mitigation: Verify each opportunity directly on the exchanges before trading and treat the monitor output as informational only. <br>
Risk: Continuous monitoring repeatedly calls exchange APIs and may send Telegram notifications when credentials are configured. <br>
Mitigation: Use --once for single checks, start continuous mode only intentionally, and use a dedicated Telegram bot token for alerts. <br>
Risk: Profit estimates can be affected by fees, withdrawal delays, transfer availability, and slippage. <br>
Mitigation: Review fees, withdrawal status, deposit support, transfer time, and order size on the relevant exchanges before acting. <br>


## Reference(s): <br>
- [Exchange API Reference](references/exchanges.md) <br>
- [ClawHub skill listing](https://clawhub.ai/guohongbin-git/crypto-arb-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands plus terminal text and optional JSON opportunity output from the monitor.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single-check and continuous monitoring modes; Telegram alerts are optional and require user-provided bot configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
