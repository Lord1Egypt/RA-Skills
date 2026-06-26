## Description: <br>
Binance Pro helps agents query Binance balances and market data and prepare spot and futures trading commands, including leveraged positions, stop-loss orders, take-profit orders, cancellations, and trade-history checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[totaleasy](https://clawhub.ai/user/totaleasy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill when they intentionally want an agent to assist with Binance account queries, portfolio checks, spot trades, futures positions, order management, and trading history. It is suited to workflows where every authenticated account action is reviewed and confirmed before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated commands can place spot or futures orders, cancel orders, close positions, or change leverage on a Binance account. <br>
Mitigation: Require explicit user confirmation before every order, leverage change, cancellation, or position close, and review symbol, side, quantity, leverage, and order type before execution. <br>
Risk: Binance API keys can expose account access if over-permissioned or leaked. <br>
Mitigation: Use a dedicated Binance API key with withdrawals disabled, minimum permissions, IP restrictions, and small limits; prefer read-only or testnet access unless live trading is explicitly needed. <br>
Risk: Leveraged crypto trading can amplify losses, especially when broad routing and limited safeguards are present. <br>
Mitigation: Use low or no leverage unless the user explicitly requests otherwise, set stop-loss controls for leveraged trades, and keep position sizes within predefined limits. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/totaleasy/binance-pro) <br>
- [Binance API Documentation](https://binance-docs.github.io/apidocs/) <br>
- [Binance Testnet](https://testnet.binance.vision/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; uses Binance API credentials and may generate authenticated account or trading API commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
