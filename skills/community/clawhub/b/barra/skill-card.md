## Description: <br>
Barra helps an agent buy BTC spot on Binance using market or limit orders, including account checks, order-parameter handling, and execution-result reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[violetsakura-7](https://clawhub.ai/user/violetsakura-7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill when they intentionally want an agent to prepare and execute Binance BTC spot buy orders from natural-language instructions. It is intended for controlled trading workflows where the user reviews the symbol, amount, order type, price, fees, and slippage before any live order. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend real funds by placing live Binance BTC spot buy orders, and the security evidence says it lacks clear mandatory confirmation before spending. <br>
Mitigation: Require explicit manual review and approval of the symbol, amount, order type, limit price when applicable, fees, and slippage before every live trade. <br>
Risk: The skill requires Binance API credentials with account-read and spot-trading permissions. <br>
Mitigation: Use a dedicated low-balance API key, disable withdrawals and unrelated permissions, enable IP allowlisting, and rotate keys if they may have been exposed. <br>
Risk: Market and limit orders can execute at unfavorable prices or with unintended quantities if parameters are parsed incorrectly. <br>
Mitigation: Confirm the parsed order parameters and estimated cost before execution, and prefer conservative limits or dry-run review where available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/violetsakura-7/barra) <br>
- [Publisher profile](https://clawhub.ai/user/violetsakura-7) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, api calls, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with Binance API key setup guidance, trading-parameter summaries, and order-result details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate live Binance spot buy orders and report filled price, quantity, order ID, and related execution details.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata; artifact frontmatter states 1.0.0 and artifact _meta.json states 0.1.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
