## Description: <br>
Complete Binance integration for checking balances, querying prices, managing spot and futures trades, setting stop loss and take profit orders, reviewing PnL, and performing Binance account operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xspeter](https://clawhub.ai/user/0xspeter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent prepare Binance API commands for portfolio checks, spot trading, futures position management, order cancellation, leverage changes, and trade history review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through live Binance spot and futures trades, leverage changes, cancellations, and position closes. <br>
Mitigation: Require explicit human confirmation before every live order, leverage change, cancellation, or position close. <br>
Risk: Broad Binance API credentials could expose account funds and trading authority if misused. <br>
Mitigation: Use a dedicated restricted API key, disable withdrawals, enable IP restrictions where possible, and start with read-only or testnet credentials. <br>
Risk: Leveraged futures commands can create outsized financial losses if pair, side, quantity, stop price, or leverage is wrong. <br>
Mitigation: Verify symbol, side, quantity, current position, stop loss, take profit, and leverage before execution; keep leverage conservative unless the user has explicitly approved otherwise. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xspeter/binance-pro-1-0-0) <br>
- [Publisher profile](https://clawhub.ai/user/0xspeter) <br>
- [Binance API Documentation](https://binance-docs.github.io/apidocs/) <br>
- [Binance Testnet](https://testnet.binance.vision/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Binance API command examples that may require credentials and human approval before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
