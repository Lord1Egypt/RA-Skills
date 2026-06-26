## Description: <br>
A Stock Paper Trade helps an agent manage a local simulated A-share paper-trading portfolio, including market quotes, buy and sell orders, holdings, profit and loss, and rankings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luaqnyin](https://clawhub.ai/user/luaqnyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to practice A-share trading workflows with virtual funds, inspect market data, and review simulated holdings and transaction history without connecting to a brokerage account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading commands change local paper-trading history and simulated balances. <br>
Mitigation: Confirm before asking the agent to initialize, reset, buy, or sell, and review the simulated portfolio state after changes. <br>
Risk: Market data and paper-trading outputs can be mistaken for financial advice or real brokerage execution. <br>
Mitigation: Treat outputs as simulated information only and do not rely on them as financial advice or as evidence of real trades. <br>
Risk: The skill depends on Python packages and external market-data sources. <br>
Mitigation: Install dependencies from trusted sources and expect quote accuracy to vary outside A-share trading hours. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luaqnyin/a-stock-paper-trade) <br>
- [Sina Finance market data endpoint](http://hq.sinajs.cn/list={sc}) <br>
- [Sina Finance](https://finance.sina.com.cn) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, guidance] <br>
**Output Format:** [JSON responses from local Python commands, with occasional plain-text quote summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may read live market data and may modify the local simulated portfolio file under the user's home directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
