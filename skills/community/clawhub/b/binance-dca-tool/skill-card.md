## Description: <br>
Binance Dollar-Cost Averaging (DCA) tool for automated and manual recurring crypto purchases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fpsjago](https://clawhub.ai/user/fpsjago) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to plan Binance DCA strategies, check balances and trade history, view projections, and place manual or scheduled spot buy orders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend live Binance funds without built-in confirmation or spending limits. <br>
Mitigation: Require explicit user confirmation before live buys, use small order amounts, and avoid unattended schedules unless they are capped and monitored. <br>
Risk: Exchange API credentials are required for signed account and order actions. <br>
Mitigation: Use restricted Binance API keys with withdrawals disabled, apply IP restrictions where possible, and provide credentials only through environment variables. <br>
Risk: Live trading behavior may be difficult to reverse if the wrong symbol, amount, or endpoint is used. <br>
Mitigation: Use Binance testnet first and verify the trading pair, amount, order type, and base URL before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fpsjago/binance-dca-tool) <br>
- [Binance Spot API](https://api.binance.com) <br>
- [Binance Spot Testnet](https://testnet.binance.vision) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Binance API calls through the bundled shell script when the user supplies credentials and requests live actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
