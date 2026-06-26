## Description: <br>
Helps agents use the Alpaca Python CLI to set up credentials, inspect account and market data, manage portfolios, and place stock or crypto orders through Alpaca Markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zijunl](https://clawhub.ai/user/zijunl) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent developers use this skill to connect an agent to Alpaca Markets for market status checks, quotes, account and portfolio review, and guarded stock or crypto order workflows. It is best started with paper-trading keys before any live brokerage use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill gives an agent access to brokerage workflows, including account setup, credential handling, and trading actions. <br>
Mitigation: Use paper-trading keys first and require explicit confirmation before every order, including symbol, side, quantity, order type, and paper or live mode. <br>
Risk: Alpaca API keys may be stored in shell startup files and become available to processes in that shell environment. <br>
Mitigation: Create and enter API keys yourself when possible, avoid live credentials in shell startup files, and use the least-privileged keys available. <br>
Risk: Broad setup and trading authority can create financial loss if live trading is enabled without adequate review. <br>
Mitigation: Keep live trading disabled until the workflow has been tested in paper mode and monitor Alpaca account activity after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zijunl/alpaca-py-cli) <br>
- [Alpaca Markets](https://alpaca.markets) <br>
- [Alpaca Python SDK documentation](https://alpaca.markets/docs/python-sdk/) <br>
- [Alpaca Trading API documentation](https://docs.alpaca.markets/docs/trading-api) <br>
- [Alpaca Market Data API documentation](https://docs.alpaca.markets/docs/market-data) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, alpaca-py, pytz, and Alpaca API environment variables.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
