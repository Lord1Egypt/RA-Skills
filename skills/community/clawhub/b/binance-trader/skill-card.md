## Description: <br>
Provides Binance spot and futures trading guidance for account balances, prices, orders, positions, order history, and market data retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenry07](https://clawhub.ai/user/shenry07) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading operators use this skill to have an agent draft Binance API setup, configuration, and Python examples for spot and futures trading workflows. It is appropriate only where the user intends the agent to assist with Binance trading tasks and reviews any live order action manually. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes ready-to-run examples for live Binance spot and futures orders that could move real money. <br>
Mitigation: Start with Binance testnet or read-only API keys, require manual approval before any live order, and use small limits for any trading-enabled account. <br>
Risk: Trading API credentials could expose account funds if over-permissioned or reused broadly. <br>
Mitigation: Never enable withdrawals, restrict API keys by IP, and prefer a dedicated subaccount with only the required permissions. <br>


## Reference(s): <br>
- [Binance Trader release page](https://clawhub.ai/shenry07/binance-trader) <br>
- [Publisher profile](https://clawhub.ai/user/shenry07) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes examples that may call live Binance trading APIs if copied and executed with trading-enabled credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
