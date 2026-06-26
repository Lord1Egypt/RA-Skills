## Description: <br>
Binance Pro Cn helps an agent provide Binance spot and futures trading guidance, including balance checks, price queries, order placement, leverage changes, staking-related context, and Binance API command examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guohongbin-git](https://clawhub.ai/user/guohongbin-git) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for Binance account, spot trading, futures trading, leverage, order management, and market data workflows. It is intended for Binance API command guidance and should be used with explicit human review before any trading action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to place real Binance spot or futures trades, cancel orders, and change leverage. <br>
Mitigation: Require explicit human confirmation for every order, cancellation, leverage change, symbol, side, quantity, and price before execution. <br>
Risk: Use of broad or high-privilege Binance API keys could expose funds or allow unintended trading activity. <br>
Mitigation: Use a dedicated Binance API key with withdrawals disabled, minimum required trading permissions, and IP restrictions where possible. <br>
Risk: Leveraged futures actions can amplify losses if parameters or account state are misunderstood. <br>
Mitigation: Prefer testnet or very small amounts first, verify the current position before closing or changing leverage, and use stop-loss controls for leveraged trades. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guohongbin-git/binance-pro-cn) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/guohongbin-git) <br>
- [ClawHub](https://clawhub.ai) <br>
- [Binance API Documentation](https://binance-docs.github.io/apidocs/) <br>
- [Binance Testnet](https://testnet.binance.vision/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Binance API credential setup examples and curl-based command patterns for account, order, futures, and market data operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
