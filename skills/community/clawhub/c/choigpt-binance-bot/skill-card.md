## Description: <br>
Automates Binance futures trading with Sweepzone V1 market scanning, dynamic risk management, backtesting, dashboard monitoring, and Telegram notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexchoi21](https://clawhub.ai/user/alexchoi21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading operators use this skill to run or evaluate a Binance futures trading bot that scans markets, backtests a strategy, places automated trades, and sends Telegram status and profit updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated live trading can place leveraged Binance futures orders and may cause financial loss. <br>
Mitigation: Audit the bot before use, start with testnet or dry-run mode, use restricted no-withdrawal Binance API keys, and add explicit confirmations or hard exposure limits before live trading. <br>
Risk: Account, trade, or position context may be sent to Google Gemini or Telegram. <br>
Mitigation: Decide whether those services are acceptable for the deployment, minimize shared details, and keep all API tokens in managed secrets. <br>
Risk: Hardcoded Google key material or paths can expose credentials. <br>
Mitigation: Remove hardcoded key material and require Gemini credentials to come from environment or secret-management configuration. <br>


## Reference(s): <br>
- [ChoiGPT Binance Trading Bot on ClawHub](https://clawhub.ai/alexchoi21/choigpt-binance-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text with shell command examples and generated trading or status reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Binance Futures, Google Gemini, and Telegram APIs when configured; may create logs, charts, and local data files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
