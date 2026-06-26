## Description: <br>
Fetches TongDaXin TQ strategy-interface market, stock, financial, sector, IPO, dividend, ETF, convertible-bond, subscription, cache, and file data through Python command scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sparkmao](https://clawhub.ai/user/sparkmao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market-data analysts use this skill to run TongDaXin-backed Python commands for retrieving securities market data, financial data, sector data, subscriptions, cache refreshes, and local client data files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can interact with a local TongDaXin TQ client beyond read-only lookup, including sector deletion or clearing, file sending, alert publishing, cache refreshes, subscriptions, and direct library use of an order-submission primitive. <br>
Mitigation: Install only when those client-side actions are intended, require explicit user approval for privileged actions, and avoid exposing them to broad automatic financial-data requests. <br>
Risk: The skill depends on a local TongDaXin financial terminal TQ client and Windows DLL path, so results and side effects depend on the user's local client state and configuration. <br>
Mitigation: Confirm the terminal is installed, running, and configured for TQ strategy use before execution, and review command arguments before running scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sparkmao/financial-data-fetcher) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Initialization](artifact/references/General functions/Initialization.md) <br>
- [Obtain professional financial data](artifact/references/Financial data/Obtain professional financial data.md) <br>
- [Obtain market trading data](artifact/references/Financial data/Obtain market trading data.md) <br>
- [Get snapshot data](artifact/references/Market information/Get snapshot data.md) <br>
- [Get candlestick charts](artifact/references/Market information/Get candlestick charts.md) <br>
- [Send files to the client](artifact/references/General functions/Send files to the client.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and JSON-like script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires numpy, pandas, and a running TongDaXin financial terminal TQ client with TQ strategy enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
